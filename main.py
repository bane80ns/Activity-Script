import pymysql
from datetime import datetime

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



# print(datetime.now())


# def to check if activity is valid
def activity_type_check(activity):
    activity_type = ["login", "logout", "homework", "video_watch"]
    try:
        if activity in activity_type:
            return activity
        else:
            raise ValueError("Activity Type not recognized")
    except:
        raise ValueError("Activity type is not valid")


# add activity into db with
def add_activity(activity, user_id):
    activity_type = activity_type_check(activity)
    query_date = ("INSERT INTO activity_table (user_id, activity_name, entrance_datetime) VALUES (%s, %s, %s) ")
    sql_values = (user_id, activity, datetime.now())
    cursor.execute(query_date, sql_values)
    connection.commit()
    connection.close()



# add_activity("homework", 18)




# Check highest activity in 7 days, and list 10 highest active users descending
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

# Check current day activities, and list active users descending by activity
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








