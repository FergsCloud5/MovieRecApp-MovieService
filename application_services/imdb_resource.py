from application_services.BaseApplicationResource import BaseApplicationResource
from database_services.RDBService import RDBService


class IMDBResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = RDBService.find_by_template("imdb", "imdb_ajax_metadata", template)
        return res

    @classmethod
    def get_by_movie_id(cls, movie_id):
        res = RDBService.get_by_movie_id("imdb", "imdb_ajax_metadata", "movie_id", movie_id)
        return res

    @classmethod
    def get_prev_attributes(cls, template):
        res = RDBService.get_prev_attributes(template)
        return res

    @classmethod
    def get_next_attributes(cls, template):
        res = RDBService.get_next_attributes(template)
        return res
