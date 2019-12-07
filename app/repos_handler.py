from flask import current_app
from app.repo_handler import RepoHandler


class ReposHandler:

    def __init__(self):
        self.repos = {}
        self.force = 0 # 0:none / 1:force_reset
        self.debug = 0 # 0:none / 1:normal / 2:detail
        print('Start handler')


    def __del__(self):
        print('End handler')


    def init(self, force, debug):
        self.repos = current_app.config['GIT_REPOS']
        self.force = int(force)
        self.debug = int(debug)


    def deploy(self, force=0, debug=0):
        self.init(force, debug)
        repo_keys = list(self.repos.keys())
        for repo_key in repo_keys:
            handler = RepoHandler()
            handler.deploy(repo_key, force, debug)

