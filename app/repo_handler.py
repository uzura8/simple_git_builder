import os
import sys
import subprocess
import shutil
import re
from flask import current_app
from app.common.cli import exec_cmd


class RepoHandler:

    def __init__(self):
        self.base_dir = ''
        self.options = {}
        self.options_common = {}
        self.cmds = {}
        self.cmd_exec_user = ''
        self.repo_key = ''
        self.checkout_path = ''
        self.master_path = ''
        self.branches = []
        self.packager = ''
        self.build_option = None
        self.force = 0 # 0:none / 1:force_reset
        self.debug = 0 # 0:none / 1:normal / 2:detail
        print('Start handler')


    def __del__(self):
        print('End handler')


    def init(self, repo_key, force=0, debug=0):
        self.force = int(force)
        self.debug = int(debug) or int(current_app.config['DEBUG'])
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
        self.cmd_exec_user = current_app.config['BUILD_USER']
        self.cmds = current_app.config['BUILD_CMDS']

        if not repo_key:
            raise Exception('repo_key is required')

        try:
            options = current_app.config['GIT_REPOS'][repo_key]
        except KeyError:
            raise Exception('repo_key is invalid')

        for key, val in options.items():
            try:
                self.options[key] = options[key]
            except KeyError:
                self.options[key] = val

        self.options_common = current_app.config['GIT_COMMON']

        if 'deploy_dir' in self.options:
            self.checkout_path = self.options['deploy_dir']
        else:
            self.checkout_path = self.options_common['deploy_dir']

        self.master_path = '{}/{}'.format(
                            self.options_common['master_repos_dir'], repo_key)
        self.repo_key = repo_key
        self.branches = self.get_branches()

        if 'packager' in self.options:
            self.packager = self.options['packager']

        if 'build' in self.options:
            self.build_option = self.options['build']


    def deploy(self, repo_key, force=0, debug=0):
        self.init(repo_key, force, debug)
        for br in self.branches:
            self.deploy_branch(br)


    def update(self, repo_key, branch, payload, debug=0):
        self.init(repo_key, debug=0)
        br_path = self.get_branch_path(branch)
        if os.path.exists(br_path):
            os.chdir(br_path)
            cmd = ['git', 'pull', '--rebase', 'origin', branch]
            res = exec_cmd(cmd, True)

            if self.check_npm_inatall_target(payload):
                self.npm_install(branch=branch)

            if self.check_build_target(payload):
                self.build(branch=branch)

            print('Updated ' + br_path)
        else:
            self.deploy_branch(branch)


    def create(self, repo_key, branch, debug=0):
        self.init(repo_key, debug=0)
        self.deploy_branch(branch)


    def delete(self, repo_key, branch, debug=0):
        self.init(repo_key, debug=0)
        br_path = self.get_branch_path(branch)
        if os.path.exists(br_path):
            shutil.rmtree(br_path)
            print('Deleted ' + br_path)
        else:
            print(br_path + ' is already deleted ')


    def get_branches(self):
        os.chdir(self.options_common['master_repos_dir'])

        is_clone = False
        if os.path.exists(self.repo_key):
            if self.force:
                shutil.rmtree(self.repo_key)
                is_clone = True
        else:
            is_clone = True

        if is_clone:
            cmd = ['git', 'clone', self.options['url'], self.repo_key]
            exec_cmd(cmd, True, is_debug=self.debug)
            os.chdir(self.repo_key)

            if self.packager == 'npm':
                self.npm_install(path=self.master_path)

                if len(self.options['cmds_before_build']) > 0:
                    for cmd in self.options['cmds_before_build']:
                        exec_cmd(cmd, True, is_debug=self.debug)


        if not is_clone:
            os.chdir(self.repo_key)
            cmd = ['git', 'fetch', 'origin']
            res = exec_cmd(cmd, is_debug=self.debug)

        cmd = ['git', 'branch', '-r']
        res = exec_cmd(cmd, is_debug=self.debug)
        res_lines = res[0].split('\n')
        brs = []
        for item in res_lines:
            if '->' in item:
                continue

            br = item.strip().replace('origin/', '')
            if 'ignore_branches' in self.options and br in self.options['ignore_branches']:
                continue

            brs.append(br)

        return brs


    def deploy_branch(self, br):
        os.chdir(self.checkout_path)
        cp_from = '{}/{}'.format(self.options_common['master_repos_dir'],
                                    self.repo_key)
        domain = self.get_domain(br)

        is_cp = False
        if os.path.exists(domain):
            if self.force:
                shutil.rmtree(domain)
                is_cp = True
        else:
            is_cp = True

        if is_cp:
            cmd = ['cp', '-a', cp_from, domain]
            exec_cmd(cmd, is_debug=self.debug)

        os.chdir(domain)
        if br == 'master':
            exec_cmd(['git', 'checkout', br], is_debug=self.debug)
            cmd = ['git', 'pull', '--rebase', 'origin', br]
            exec_cmd(cmd, True, is_debug=self.debug)
        else:
            exec_cmd(['git', 'checkout', '-b', br, 'origin/'+br], True, is_debug=self.debug)

        if self.packager == 'npm':
            self.npm_install(branch=br)

        if self.build_option is not None:
            self.build(branch=br)

        print('Deploy {} in {} as {}'.format(br, self.repo_key, domain))


    def get_domain(self, br):
        branch_subd = re.sub(r'[/_.@# ]', '-', br).lower()
        return '{}.{}.{}'.format(self.repo_key, branch_subd,
                                    self.options_common['domain'])

    def get_branch_path(self, br):
        return '{}/{}'.format(self.checkout_path, self.get_domain(br))


    def check_npm_inatall_target(self, payload):
        if self.packager != 'npm':
            return False

        if 'revisions' not in payload:
            return False

        for rev in payload['revisions']:
            if 'modified' not in rev:
                continue

            for file_path in rev['modified']:
                if 'package.json' in file_path:
                    return True

        return False


    def check_build_target(self, payload):
        if self.build_option is None:
            return False

        option = self.build_option

        if not payload:
            return False

        if 'revisions' not in payload:
            return False

        for rev in payload['revisions']:
            if 'modified' not in rev:
                continue

            for file_path in rev['modified']:
                if option['path'] in file_path:
                    return True

        return False


    def npm_install(self, branch='', path=''):
        if branch and not path:
            path = self.get_branch_path(branch)

        if not path:
            raise Exception('path or branch is required')

        os.chdir(path)
        cmd = 'sudo -u {} {} install'.format(self.cmd_exec_user, self.cmds['npm'])
        exec_cmd(cmd, True, is_debug=self.debug)


    def build(self, branch='', path=''):
        if self.build_option is None:
            raise Exception('build option is not set')

        option = self.build_option

        if branch and not path:
            path = self.get_branch_path(branch)

        if not path:
            raise Exception('path or branch is required')
        os.chdir(path)

        if option['tool'] == 'webpack':
            cmd = '{}/node_modules/.bin/webpack --mode=production'.format(path)
            exec_cmd(cmd, True, is_shell_option=True, is_debug=self.debug)

