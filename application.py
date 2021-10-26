import MovieService
from flask import Flask, Response, request, sessions
from application_services.imdb_resource import IMDBResource
from flask_cors import CORS
# from middleware.notifications import notifications as notify
from middleware.simple_security import Security
import json

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

application = Flask(__name__)
CORS(application)
sec = Security()


def handle_error(code, path, msg):
    return


@application.before_request
def before_decorator():
    print("before_request is running!")
    print(request.path)
    a_ok = sec.check_authentication(request)
    print(a_ok)
    if a_ok[0] != 200:
        handle_error(a_ok[0], a_ok[1], a_ok[2])
    # make check_auth return some boolean, to decide whether to not to redirect to login page


@application.after_request
def after_decorator(response):
    print("after_request is running!")
    return response


@application.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@application.route('/movies')
def get_movies():
    res = IMDBResource.get_by_template(None)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


# http://0.0.0.0:5000/movies/tt0298148
@application.route('/movies/<movie_id>')
def get_movie_by_movie_id(movie_id):
    if MovieService.check_movie_id(movie_id):
        res = IMDBResource.get_by_movie_id(movie_id)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    else:
        msg = ("The Movie Recommendation Service is unable to provide any information on the movie with movie_id "
               + f"= {str(movie_id)} at this moment. This movie does not exist in our database. Please double check "
               + "your movie_id and try again."
               )
        rsp = Response(msg, status=404, content_type="application/json")
    return rsp


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000)
