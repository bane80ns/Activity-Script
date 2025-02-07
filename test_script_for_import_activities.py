# Script for importing 20 random activities into activity_db >> activity_table
# older than 90 days for testing purposes.

### imports
import pymysql
from datetime import datetime
from config import activity_types
import random




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

import pymysql
import random
from datetime import datetime, timedelta


# Generate 20 random activity records
for _ in range(20):
    user_id = random.randint(1, 20)  # Random user_id between 1-20
    activity_name = random.choice(activity_types)  # Random activity name

    # Generate a random date between 91 and 180 days ago
    random_days_ago = random.randint(91, 180)
    entrance_datetime = datetime.now() - timedelta(days=random_days_ago)
    formatted_date = entrance_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Insert into activity_table
    query = """
        INSERT INTO activity_table (user_id, activity_name, entrance_datetime)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (user_id, activity_name, formatted_date))

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

print("20 random activities added to activity_table!")
