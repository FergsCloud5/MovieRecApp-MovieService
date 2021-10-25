import MovieService
from flask import Flask, Response
from application_services.imdb_resource import IMDBResource
from flask_cors import CORS
# from middleware import notifications as notify
# from middleware import simple_security as sec
import json

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@app.route('/movies')
def get_movies():
    res = IMDBResource.get_by_template(None)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


# http://0.0.0.0:5000/movies/tt0298148
@app.route('/movies/<movie_id>')
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


@app.before_request
def before_decorator():
    print("before_request is running!")


@app.after_request
def after_decorator(response):
    # print(JSON.dumpsresponse)
    print("after_request is running!")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
