from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as DbService


class IMDBResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = DbService.find_by_template("imdb", "imdb_ajax_metadata", template, None)
        return res

    @classmethod
    def get_by_movie_id(cls, movie_id):
        res = DbService.get_by_movie_id("imdb", "imdb_ajax_metadata", "movie_id", movie_id)
        return res

