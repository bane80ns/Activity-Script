import pymysql
from faker import Faker
import random
from datetime import datetime, timedelta


####### DB

# Database connection

db_name = "activity_db"

connection = pymysql.connect(
    host='localhost',  # localhost - Local PC, or 127.0.0.1 (This field is for DB IP address)
    user='root',  # username created for accessing DB (Database)
    password='root',  # password created for accessing DB
    database=db_name,  # DB name
    cursorclass=pymysql.cursors.DictCursor
    #   port=xxxx # Port which we use for connecting to DB (in our case not needed)
    )
cursor = connection.cursor()



activity = "logout"

def activity_type_check(activity):
    activity_type = ["login", "logout", "homework", "video_watch"]
    try:
        if activity in activity_type:
            return activity
        else:
            raise ValueError("Activity Type not recognized")
    except:
        raise ValueError("Activity type is not valid")


def add_activity(activity):
    return activity


def last_week_activity():

    query_data = ("SELECT user_id, COUNT(*) AS activity_count "
                  "FROM activity_table "
                  "WHERE NOT activity_name LIKE '%log%' "
                  "AND entrance_datetime >= NOW() - INTERVAL 7 DAY "
                  "GROUP BY user_id "
                  "ORDER BY activity_count DESC "
                  "LIMIT 10")

    cursor.execute(query_data)
    rows = cursor.fetchall()
    for row in rows:
        print(f"User id:{row["user_id"]:4}       Activity Count: {row["activity_count"]:2}")

# last_week_activity()


def current_day_activity():
    query_data = ("SELECT user_id, COUNT(*) AS activity_count "
                  "FROM activity_table "
                  "WHERE entrance_datetime >= NOW() - INTERVAL 1 DAY "
                  "GROUP BY user_id "
                  "ORDER BY activity_count DESC ")

    cursor.execute(query_data)
    rows = cursor.fetchall()
    for row in rows:
        print(f"User id:{row["user_id"]:4}       Activity Count: {row["activity_count"]:2}")

# current_day_activity()








