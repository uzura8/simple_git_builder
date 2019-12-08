import os
import sys
import subprocess
import shutil
import re
from pprint import pprint
from flask import current_app
from app.common.cli import exec_cmd


class RepoHandler:

    def __init__(self):
        self.options = {}
        self.options_common = {}
        self.repo_key = ''
        self.checkout_path = ''
        self.master_path = ''
        self.force = 0 # 0:none / 1:force_reset
        self.debug = 0 # 0:none / 1:normal / 2:detail
        print('Start handler')


    def __del__(self):
        print('End handler')


    def init(self, repo_key, force=0, debug=0):
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
        self.force = int(force)
        self.debug = int(debug)


    def deploy(self, repo_key, force=0, debug=0):
        self.init(repo_key, force, debug)
        brs = self.get_branches()
        for br in brs:
            self.deploy_branch(br)


    def update(self, repo_key, branch, debug=0):
        self.init(repo_key, debug=0)
        br_path = self.get_branch_path(branch)
        if os.path.exists(br_path):
            os.chdir(br_path)
            cmd = ['git', 'pull', '--rebase', 'origin', branch]
            res = exec_cmd(cmd)
            pprint(res)
        else:
            self.deploy_branch(branch)


    def delete(self, repo_key, branch, debug=0):
        self.init(repo_key, debug=0)
        br_path = self.get_branch_path(branch)
        shutil.rmtree(br_path)
        print('Deleted ' + br_path)


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
            exec_cmd(cmd)

        os.chdir(self.repo_key)
        cmd = ['git', 'branch', '-r']
        res = exec_cmd(cmd)
        res_lines = res[0].split('\n')
        brs = []
        for item in res_lines:
            if '->' in item:
                continue
            brs.append(item.strip().replace('origin/', ''))

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
            exec_cmd(cmd)

        os.chdir(domain)
        if br == 'master':
            exec_cmd(['git', 'checkout', br])
        else:
            exec_cmd(['git', 'checkout', '-b', br, 'origin/'+br])
        print('Deploy {} in {} as {}'.format(br, self.repo_key, domain))


    def get_domain(self, br):
        branch_subd = re.sub(r'[/_.@# ]', '-', br).lower()
        return '{}-{}.{}'.format(self.repo_key, branch_subd,
                                    self.options_common['domain'])


    def get_branch_path(self, br):
        return '{}/{}'.format(self.checkout_path, self.get_domain(br))

