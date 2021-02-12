import json
import mysql.connector as mysql
import sys
from os import path
from pathlib import Path

def connect_to_database():
    # connect to the database, uses relative path to config file.
    root_dir = Path((sys.modules["__main__"].__file__)).resolve().parent
    file = open(root_dir / "config" / "config.json")
    data = json.load(file)
    host = data["mysqldb"]["host"]
    username = data["mysqldb"]["username"]
    password = data["mysqldb"]["password"]
    db_name = data["mysqldb"]["db"]
    file.close()
    db = mysql.connect(host=host, user=username, password=password, database=db_name, auth_plugin='mysql_native_password')
    return db


def new_guild_table(guild_id : int, db):
    # check if table exists
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = 'bunnybot')"
                   "AND (TABLE_NAME = %s)", (guild_id, ))
    row = cursor.fetchone()
    if row is not None:
        return
    cursor.execute("CREATE TABLE %s (user_id BIGINT(20) PRIMARY KEY NOT NULL,"
                   "is_streamer TINYINT(4),"
                   "experience INT(11) DEFAULT 0,"
                   "last_message VARCHAR(45) DEFAULT 0,"
                   "currency INT(11) DEFAULT 0)", (guild_id, ))
    db.commit()

def new_user_joined(guild_id, db, member_id):
    cursor = db.cursor()


def check_if_connected(db):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT NOW()")
        return db
    except:
        return connect_to_database()

