from decouple import config
import pymysql
import traceback

from src.utils.Logger import Logger

def get_connection():
    try:
        return pymysql.connect(
            host=config('HOST'),
            user=config('root'),
            password=config('PASSWORD'),
            database=config('DB')
        )
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())