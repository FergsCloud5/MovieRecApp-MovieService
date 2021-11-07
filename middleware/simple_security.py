import os
import json
from flask import Flask, Response, request, sessions, redirect, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_user, logout_user)
from flask_dance.contrib.google import make_google_blueprint, google
import os


class Security:

    def __init__(self):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        wl_file = open(dir_path + "/white_list.json")
        self.white_list = json.load(wl_file)
        print(self.white_list)
        self.login_path = "/"

    def check_whitelist(self, path):
        """
        Returns True is request.path is a white list path.
        Returns False if the request.path requires login.
        """
        if path not in self.white_list.keys():
            if len(path) > 1:
                prefix = path[0:7]
                if prefix in self.white_list.keys():
                    if path[8] == "t":
                        return True
            return False
        return True

    def check_authentication(self, path):

        if self.check_whitelist(path):
            print("whitelist")
            return 200, "", ""
        else:
            print("blacklist")
            return 401, path, "UNAUTHORIZED"
