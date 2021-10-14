import database_services.RDBService as DbService


def check_movie_id(movie_id):
    res = DbService.get_by_movie_id("imdb", "imdb_ajax_metadata", "movie_id", movie_id)
    if len(res) == 0:
        return False
    else:
        return True
