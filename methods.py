### imports
from config import *
from datetime import datetime
from db import Db
from config import activity_types
import json

db = Db()


# def to check if activity is valid (if activity exists in config activitie_types dictionary)
def activity_type_check(activity):
    try:
        if activity in activity_types:
            return activity
        else:
            raise ValueError("Activity Type not recognized")
    except:
        raise ValueError("Activity type is not valid")


# Add activity into db (activity_table) with activity type taken from activity_type dict, also adds time when that activity happend.
def add_activity(db, activity, user_id):
    activity_type = activity_type_check(activity)
    query_date = "INSERT INTO activity_table (user_id, activity_name, entrance_datetime) VALUES (%s, %s, %s) "
    sql_values = (user_id, activity, datetime.now())

    db.execute(query_date, sql_values)


# example for call the function add_activity
# add_activity(db, "logout", 18)


# Read base (activity table) for highly active users (10 of them) in X days
# (we provide number of days into function) and as return we get dict with {[user_id, activity_count]} descending.
def daily_activities(db, number_of_days):
    query_data = f"""
        SELECT user_id, COUNT(*) AS activity_count
        FROM activity_table
        WHERE NOT activity_name LIKE '%log%'
        AND entrance_datetime >= NOW() - INTERVAL {int(number_of_days)} DAY
        GROUP BY user_id
        ORDER BY activity_count DESC
        LIMIT 10
    """

    rows = db.query(query_data)

    if rows is None:
        return {}
    else:
        return {row["user_id"]: row["activity_count"] for row in rows}


# example for function daily_activities
# print(daily_activities(db, 15))


def archive_activities():
    try:
        # Step 1: Start a transaction (ensures both copy & delete run together)
        db.execute("START TRANSACTION")
        print("Transaction started.")

        # Step 2: Copy all records older than 90 days
        query_copy_data = """
            INSERT INTO archive_activity_table (activity_id, user_id, activity_name, entrance_datetime)
            SELECT activity_id, user_id, activity_name, entrance_datetime
            FROM activity_table
            WHERE entrance_datetime < NOW() - INTERVAL 90 DAY
        """
        db.execute(query_copy_data)
        print("Data older than 90 days copied to archive_activity_table successfully.")

        # Step 3: Delete only the records that were just copied
        delete_query = """
            DELETE FROM activity_table
            WHERE entrance_datetime < NOW() - INTERVAL 90 DAY
        """
        db.execute(delete_query)
        print("Archived data successfully removed from main table.")

        # Step 4: Commit the transaction (make changes permanent)
        db.execute("COMMIT")
        print("Transaction committed. Archive process completed.")

    except Exception as e:
        # If anything fails, rollback (undo changes)
        db.execute("ROLLBACK")
        print(f"Transaction failed! Changes rolled back. Error: {e}")


# Run the function
# archive_activities()


def activity_details_for_single_user_by_day(db, user_id, number_of_days):
    query_data = f"""
        SELECT 
            u.first_name,
            u.last_name,
            u.username,
            u.email,
            DATE(a.entrance_datetime) AS activity_date, 
            TIME(a.entrance_datetime) AS activity_time, 
            a.activity_name
        FROM activity_table a
        JOIN user u ON a.user_id = u.id
        WHERE a.user_id = %s
        AND a.entrance_datetime >= NOW() - INTERVAL {int(number_of_days)} DAY
        ORDER BY activity_date DESC, activity_time ASC;
    """
    rows = db.query(query_data, (user_id,))

    if not rows:
        return {"message": "No activities found for this user"}

    user_info = {
        "first_name": rows[0]["first_name"],
        "last_name": rows[0]["last_name"],
        "username": rows[0]["username"],
        "email": rows[0]["email"],
    }

    user_data = {**user_info, "activities": {}}

    for row in rows:
        day = row["activity_date"]
        time = row["activity_time"]
        activity = row["activity_name"]

        if day not in user_data["activities"]:
            user_data["activities"][day] = []

        user_data["activities"][day].append(f"{time} - {activity}")

    return user_data


# print details for sinle user for X past days
# print(activity_details_for_single_user_by_day(db, 2, 30))


def export_to_json(user_data):


    if "message" in user_data:
        print(user_data["message"])
        return

    # Convert datetime.date to string (YYYY-MM-DD)
    if "activities" in user_data:
        new_activities = {}
        for day, activities in user_data["activities"].items():
            new_activities[str(day)] = activities
        user_data["activities"] = new_activities

    # Make filename from user first and last name
    filename = f"user_{user_data['first_name']}{user_data['last_name']}_activities.json"

    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(user_data, json_file, indent=4, ensure_ascii=False)

    print(f"Data successfully exported to {filename}")


#user_activity = activity_details_for_single_user_by_day(db, 1, 30)  # Fetch user data
#export_to_json(user_activity)