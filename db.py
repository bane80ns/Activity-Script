import pymysql

class Db:
    def __init__(self, host = "localhost", user = "root", password = "root", db = "activity_db"):
        try:
            self.connection = pymysql.connect(
                host='localhost',  # localhost - Local PC, or 127.0.0.1 (This field is for DB IP address)
                user='root',  # username created for accessing DB (Database)
                password='root',  # password created for accessing DB
                database=db,  # DB name
                cursorclass=pymysql.cursors.DictCursor
                #   port=xxxx # Port which we use for connecting to DB (in our case not needed)
            )
            self.cursor = self.connection.cursor()
        except pymysql.MySQLError as e:
            print(f"Connection failed: {e}")
            self.connection = None

    def query(self, sql, params=None):
        if not self.connection.open:
            print("Connection not open")
            return None
        if self.connection is None:
            print("Query failed no DB connection")
            return None
        try:
            if params:
                self.cursor.execute(sql, params)
                # Fetch all results
                result = self.cursor.fetchall()
                return result

            else:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            print(f"Query failed: {e}")


    def execute(self, sql, params=None):
        if self.connection is None:
            print("Execution failed no DB connection")
            return
        try:
            self.cursor.execute(sql, params or ())
            self.connection.commit()
        except pymysql.MySQLError as e:
            print(f"Execution failed: {e}")


    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()




