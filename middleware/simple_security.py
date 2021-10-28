import os
import json


class Security():

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        wl_file = open(dir_path + "/white_list.json")
        self.white_list = json.load(wl_file)
        self.login_path = "/"

    def check_whitelist(self, request):
        """
        Returns True is request.path is a white list path.
        Returns False if the request.path requires login.
        """
        if request.path not in self.white_list.keys():
            return False
        return True

        #check methods

    def check_authentication(self, request):
        if self.check_whitelist(request):
            print("it's a white list path")
            # (200, , )
            return 200, "", ""
        else:
            # fix this tbh, generalize the path with <movie_id> & actually
            # no paths to blacklist for this service.
            print("it's a BLACK list path")
            # check to see if encrypted token in session is in user db
            # (400, redirect page, msg)
            return 401, self.login_path, "UNAUTHORIZED"

# make a class
# pict of public and private paths
# private ones reroute to authentication
# def check_authentication(request):


#TODO:
    # after oath gets done do the encryption checking in user db token blah
    # JSON file also consider methods in addition to path. leave the white list in the env vars