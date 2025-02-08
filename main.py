from db import Db
from methods import *


db = Db()


# add activity to db
# example: (db - database, "logout" - activity name, user_id)
# add_activity(db, "logout", 11)


# print latest activities in the past X days, sorted by most active users
# example: (db, number of days)
# print(daily_activities(db, 7))


# move activities older than 90 days to archive_activities_table
# example:
# archive_activities()


# print details for single user for X past days (db - database, 2 - user_id, 30 - number of days)
# example:
# print(activity_details_for_single_user_by_day(db, 2, 30))


# user_activity = activity_details_for_single_user_by_day(db, 3, 30)  # Fetch user data
# example:
# export_to_json(user_activity)


# user_activity = activity_details_for_single_user_by_day(db, 3, 30)  # Fetch user data
# example:
# export_to_pdf(user_activity)


db.close()
