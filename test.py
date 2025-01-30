import pymysql
import random
from datetime import datetime, timedelta

# Database connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "activity_db",
    "cursorclass": pymysql.cursors.Cursor
}

# Connect to MySQL
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# Predefined activity list
activity_list = ["login", "logout", "watch_video", "homework"]

# Fetch all user IDs from `user` table
cursor.execute("SELECT id FROM `user`")
user_ids = [row[0] for row in cursor.fetchall()]

if not user_ids:
    print("❌ No users found in the user table. Add users first.")
    connection.close()
    exit()

# Insert 100 random activities
for _ in range(100):
    user_id = random.choice(user_ids)
    activity_name = random.choice(activity_list)

    # Generate a random timestamp within the last 10 days
    random_days_ago = random.randint(0, 9)
    random_time = datetime.now() - timedelta(days=random_days_ago, hours=random.randint(0, 23),
                                             minutes=random.randint(0, 59))

    # ✅ Convert to MySQL-compatible format
    entrance_datetime = random_time.strftime('%Y-%m-%d %H:%M:%S')

    # ✅ Make sure table & column names are correct
    query = "INSERT INTO activity_table (user_id, activity_name, entrance_datetime) VALUES (%s, %s, %s)"

    try:
        cursor.execute(query, (user_id, activity_name, entrance_datetime))
    except pymysql.MySQLError as e:
        print(f"❌ MySQL Error: {e}")

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

print("✅ 100 random activities inserted into `activity_table`!")
