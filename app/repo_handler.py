import os
import sys
import subprocess
import shutil
from pprint import pprint
from flask import current_app


class RepoHandler:

    def __init__(self):
        self.options = {}
        self.options_common = {}
        self.repo_key = ''
        self.checkout_path = ''
        self.debug = 0 # 1:normal / 2:detail
        print('Start handler')


    def __del__(self):
        print('End handler')


    def init(self, repo_key, debug):
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

        if 'path' in self.options:
            self.checkout_path = self.options['path']
        else:
            self.checkout_path = self.options_common['path']

        self.repo_key = repo_key
        self.debug = int(debug)


    def main(self, repo_key, debug=0):
        self.init(repo_key, debug)
        self.execute()


    def execute(self):
        os.chdir(self.options_common['work_dir'])
        if os.path.exists('tmp_repo'):
            shutil.rmtree('tmp_repo')
        os.system('git clone {} tmp_repo'.format(self.options['url']))
        os.chdir('tmp_repo')
        path = os.getcwd()
        print(path)
        command = ['git', 'branch', '-r']
        #res = subprocess.call(command)
        #print(res)
        res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sys.stdout.buffer.write(res.stdout)
        #os.system('git branch -r')
