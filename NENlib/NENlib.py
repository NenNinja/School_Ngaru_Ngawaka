import mysql.connector

class Root:
    def __init__(self, host, user, password):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

    def __getattr__(self, db_name):
        return Database(self.conn, db_name)

    def get_databases(self):
        self.cursor.execute("SHOW DATABASES")
        return self.cursor.fetchall()

    def new_database(self, db_name):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.conn.commit()

    def exit(self):
        self.conn.commit() # saves changes to database
        self.cursor.close() # closes cursor
        self.conn.close() # closes connection to database (prevent memory leaks, lag, errors etc.)
        print("\nThank you for using NENlib, goodbye!")

class Database:
    def __init__(self, connection, db_name):
        self.conn = connection
        self.cursor = connection.cursor()
        self.cursor.execute(f"USE {db_name}")

    def __getattr__(self, table_name):
        return Table(self.conn, table_name)

    def get_tables(self):
        self.cursor.execute("SHOW tables")
        return self.cursor.fetchall()

class Table:
    def __init__(self, connection, table_name):
        self.conn = connection
        self.cursor = connection.cursor()
        self.name = table_name

    def insert(self, **kwargs):
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["%s"] * len(kwargs))
        values = tuple(kwargs.values())

        sql = f"INSERT INTO {self.name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def get_fields(self):
        self.cursor.execute("DESCRIBE users")
        for column in self.cursor.fetchall():
            print(column)
    
    def get_field_names(self):
        self.cursor.execute("DESCRIBE users")
        return [column[0] for column in self.cursor.fetchall()]

    def get_entries(self):
        self.cursor.execute(f"SELECT * FROM {self.name}")
        return self.cursor.fetchall()





# USE = select database
# SHOW = print to console
# Fetchall = get all the data and return

# show... tables, databases, columns, etc.


#cursor.execute("USE Ngarudb2")
#cursor.execute("show tables")
#databases = cursor.fetchall()

#prints all databases in MySQL
#for db in databases:
#    print(db[0])
# Create table

# REALLY IMPORTANT !!!!!

