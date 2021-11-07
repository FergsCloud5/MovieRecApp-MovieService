import pymysql
import json
import logging
import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RDBService:

    def __init__(selfs):
        pass

    @classmethod
    def _get_db_connection(cls):

        db_connect_info = context.get_db_info()

        logger.info("RDBService._get_db_connection:")
        logger.info("\t HOST = " + db_connect_info['host'])

        db_info = context.get_db_info()
        db_connection = pymysql.connect(
           **db_info
        )
        return db_connection

    @classmethod
    def get_by_prefix(cls, db_schema, table_name, column_name, value_prefix):

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + \
            column_name + " like " + "'" + value_prefix + "%'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()
        return res

    @classmethod
    def get_by_movie_id(cls, db_schema, table_name, column_name, movie_id):

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + \
            column_name + "=" + "'" + movie_id + "'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()
        return res

    @classmethod
    def _get_where_clause_args(cls, template):

        terms = []
        args = []
        pagination_str = ""

        if template is None or template == {}:
            clause = ""
            args = None
        else:
            for k, v in template.items():
                if k in ["offset", "limit"]:
                    pagination_str += k + " " + v + " "
                else:
                    terms.append(k + "=%s")
                    args.append(v)

            if len(terms) == 0:
                clause = " " + pagination_str
            else:
                clause = " where " +  " AND ".join(terms) + " " + pagination_str

        return clause, args

    @classmethod
    def find_by_template(cls, db_schema, table_name, template):

        default_pagination = {"fields": "*",
                              "limit": "20",
                              "offset": "0"}

        for k in ["limit", "offset"]:
            if k not in template.keys():
                template[k] = default_pagination[k]

        any_bad = (0 > int(template["limit"]) or int(template["limit"]) > 4919
                   or 0 > int(template["offset"]) or int(template["offset"]) > 4919
                   or 0 < int(template["limit"]) + int(template["offset"]) > 4919
                   )
        if any_bad:
            template["limit"] = "20"
            template["offset"] = "0"

        fields = template.get("fields", "*")
        template.pop("fields", None)

        wc, args = RDBService._get_where_clause_args(template)

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select " + fields + " from " + db_schema + "." + table_name + " " + wc
        res = cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        limit = template["limit"]
        offset = template["offset"]

        self_href = "?limit=" + limit + "&offset=" + offset
        if 0 > int(offset) - int(limit) or int(offset) - int(limit) > 4919:
            prev_href = "?limit=" + limit + "&offset=" + offset
        else:
            prev_href = "?limit=" + limit + "&offset=" + str(int(offset) - int(limit))
        if 0 > int(offset) + int(limit) > 4919:
            next_href = "?limit=" + limit + "&offset=" + offset
        else:
            next_href = "?limit=" + limit + "&offset=" + str(int(offset) + int(limit))

        res.append({"links": [
                    {
                        "rel": "self",
                        "href": self_href,
                    },
                    {
                        "rel": "prev",
                        "href": prev_href,
                    },
                    {
                        "rel": "next",
                        "href": next_href,
                    }]}
        )
        return res

    @classmethod
    def create(cls, db_schema, table_name, create_data):

        cols = []
        vals = []
        args = []

        for k, v in create_data.items():
            cols.append(k)
            vals.append('%s')
            args.append(v)

        cols_clause = "(" + ",".join(cols) + ")"
        vals_clause = "values (" + ",".join(vals) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
                   " " + vals_clause

        res = RDBService.run_sql(sql_stmt, args)
        return res

    @classmethod
    def get_prev_attributes(cls, template):

        attributes = {}

        if template.get("offset", 0) == 0:
            attributes["offset"] = None
            attributes["limit"] = None
            return attributes
        elif int(template.get("offset", 0)) <= int(template.get("limit", 20)):
            attributes["offset"] = 0
            attributes["limit"] = int(template.get("limit", 20))
            return attributes
        else:
            attributes["offset"] = int(template.get("offset", 0)) - int(template.get("limit", 20))
            attributes["limit"] = int(template.get("limit", 20))

            return attributes

    @classmethod
    def get_next_attributes(cls, template):

        attributes = {"offset": int(template.get("offset", 0)) + int(template.get("limit", 20)),
                      "limit": int(template.get("limit", 20))
                      }

        return attributes
