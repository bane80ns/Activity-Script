import pymysql
from datetime import datetime

# Database connection
db_name = "activity_db"

connection = pymysql.connect(
    host="localhost",  # localhost - Local PC, or 127.0.0.1 (This field is for DB IP address)
    user="root",  # username created for accessing DB (Database)
    password="root",  # password created for accessing DB
    database=db_name,  # DB name
    cursorclass=pymysql.cursors.DictCursor,
    #   port=xxxx # Port which we use for connecting to DB (in our case not needed)
)
cursor = connection.cursor()


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


# Add activity into db (activity_table) with activity type taken from activity_type dict, also adds time when that activity happend.
def add_activity(activity, user_id):
    activity_type = activity_type_check(activity)
    query_date = "INSERT INTO activity_table (user_id, activity_name, entrance_datetime) VALUES (%s, %s, %s) "
    sql_values = (user_id, activity, datetime.now())
    cursor.execute(query_date, sql_values)
    connection.commit()
    cursor.close()
    connection.close()

# add_activity("homework", 18)


# Read base (activity table) for highly active users (10 of them) in X days (we provide number of days into function) and as return we get dict with {[user_id, activity_count]} descending.
def daily_activities(number_of_days):
    query_data = f"""
        SELECT user_id, COUNT(*) AS activity_count
        FROM activity_table
        WHERE NOT activity_name LIKE '%log%'
        AND entrance_datetime >= NOW() - INTERVAL {int(number_of_days)} DAY
        GROUP BY user_id
        ORDER BY activity_count DESC
        LIMIT 10
    """

    cursor.execute(query_data)
    rows = cursor.fetchall()

    top_ten = {}
    for row in rows:
        top_ten[row["user_id"]] = row["activity_count"]

    cursor.close()
    connection.close()
    return top_ten


print(daily_activities(7))
