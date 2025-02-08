from db import Db
from methods import *

db = Db()

# add activity to db
#add_activity(db, "logout", 11)

# print latest activities in the past X days, sorted by most active users
#print(daily_activities(db, 7))

# move activities older than 90 days to archive_activities_table
#archive_activities()

# print details for sinle user for X past days
print(activity_details_for_single_user_by_day(db, 2, 30))







db.close()

