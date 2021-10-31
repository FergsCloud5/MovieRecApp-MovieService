import os
import json
from flask import Flask, Response, request, sessions, redirect, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_user, logout_user)
from flask_dance.contrib.google import make_google_blueprint, google
import os


class Security():

    def __init__(self):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        wl_file = open(dir_path + "/white_list.json")
        self.white_list = json.load(wl_file)
        self.login_path = "/"

    def check_whitelist(self, request):
        """
        Returns True is request.path is a white list path.
        Returns False if the request.path requires login.
        TODO: GENERALIZE THE PATH WITH <MOVIE_ID> ADD TO WHITE LIST
        TODO: WITH REGEX.
        """
        if request.path not in self.white_list.keys():
            return False
        return True

    def check_authentication(self, request):
        if self.check_whitelist(request):
            return 200, "", ""
        else:
            return 401, self.login_path, "UNAUTHORIZED"
