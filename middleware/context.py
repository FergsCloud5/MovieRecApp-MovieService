import os

# This is a bad place for this import
import pymysql

def get_db_info():
    """
    This is crappy code.
    :return: A dictionary with connect info for MySQL
    """

    # db_host = os.environ.get("DBHOST", None)
    # db_user = os.environ.get("DBUSER", None)
    # db_password = os.environ.get("DBPASSWORD", None)

    db_host: "cloudcomp.cvrnijvhtjmj.us-east-2.rds.amazonaws.com"
    db_user: "admin"
    db_password: "IZZIcho1228"

    if db_host is not None:
        db_info = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "cursorclass": pymysql.cursors.DictCursor
        }
    else:
        db_info = {
            "host": "localhost",
            "user": "dbuser",
            "password": "dbuserdbuser",
            "cursorclass": pymysql.cursors.DictCursor
        }

    return db_info
