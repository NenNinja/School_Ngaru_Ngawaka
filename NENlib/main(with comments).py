from NENlib import * 
# imports all the classes and functions from the NENlib module, 
# which is the library we created for connecting to MySQL databases 
# and executing SQL commands in Python.

# welcome! this is a simple example of how to use NENlib, 
# a library for connecting to MySQL databases 
# and executing SQL commands in Python.
# by Ngaru Ngawaka

# the main idea behind NENlib is to make it easy to access and manipulate MySQL databases using Python
# without having to write raw SQL commands all the time.
# it provides a simple interface for connecting to a MySQL server,
# selecting databases and tables, and performing common operations like inserting data and getting entries.

#=============================================================================

# this is the more in depth version of the project and will show how each part of the code works and how to use it, 
# the other version is more concise and just shows how to use the library without the explanations
# this will also show how to use the built in functions of mysql.connector to execute raw SQL commands if needed, 
# but its generally better to use functions i've made for common operations to avoid mistakes and make your code 
# cleaner and easier to read

#=============================================================================

# BACKGROUND INFO:
# currently the database im using is called "Ngarudb2" and the table is called "users"
# the users table has 3 columns: id, name, and age
# the id column is an auto-incrementing primary key, so we dont need to specify it when inserting data

#=============================================================================

# MYSQL SETUP:
# to use NENlib you need to create a MySQL server (THIS IS NOT INCLUDED IN THE LIBRARY, YOU NEED TO SET THIS UP YOURSELF)
# I belive teacher will teach this but if not go to https://www.w3schools.com/python/python_mysql_getstarted.asp
# YOU DO NOT NEED TO SIGN INTO ORACLE TO DOWNLOAD there is a way to download MySQL without signing in, just click the "No thanks, just start my download" 
# link at the bottom of the page
# MYSQL WORKBENCH is a good program for managing your MySQL server and databases,
# but you can also use the command line if you prefer (its better for setup and basic management)

# this library serves as a way to connect to your MySQL server and execute SQL commands using Python,
# but you still need to set up the MySQL server and create databases and tables yourself

#=============================================================================

# once you have a mySQL server set up, you can connect to it using the Root class in NENlib
# the Root class takes 3 arguments: host, user, and password
# the host is usually "localhost" if you're running the MySQL server on your own computer
root = Root("localhost", "root", "Fearless2023") 
# change the password to your MySQL password 
# (the default password for MySQL is usually "root" or "" but it should have been changed during setup for security reasons)

# by using root as the starting point, we can access any database and table on the MySQL server by using dot notation
# for example, root.ngarudb2.users will give us access to the users table in the Ngarudb2 database
root.new_database("NENlibdb") # creates a new database called NENlibdb if it doesnt already exist

# you can still execute raw SQL commands using the cursor object, which is accessible through the database object
root.NENlibdb.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)") # creates a new table called users with the specified columns if it doesnt already exist
#root.{database_name}.cursor.execute("[SQL CODE HERE]")

# this will execute any SQL code you put in the string, 
# but its generally better to use the built-in functions for common operations like inserting data 
# and getting entries or make your own functions for more complex operations to avoid mistakes in future
# idk what teach will do in the future but i might add a function for executing raw SQL commands if enough people want it


# prints a list of all databases on the MySQL server example: [('information_schema',), ('mysql',), ('NENlibdb',), ('performance_schema',), ('sys',)]
print(root.get_databases()) 

# prints a list of all tables in the NENlibdb database (example: [('users',)])
print(root.NENlibdb.get_tables()) 

# the tables have 3 functions: insert, get_fields, and get_entries
# insert takes keyword arguments for each column and inserts a new row into the table
# get_fields prints the column names and types to the console
# get_entries returns all the rows in the table as a list of tuples

# this is a simple example of how to use NENlib to view the field names and entries in the users table
print(root.NENlibdb.users.get_field_names()) # prints the field names of the users table
for entry in root.NENlibdb.users.get_entries():
    print(entry) # prints each entry in the users table as a tuple (in brackets) eg. (1, "Alice", 30)
root.nenlibdb.users.insert(name="Alice", age=30) # inserts a new row into the users table with the specified name and age (id is auto-incremented so we dont need to specify it)

