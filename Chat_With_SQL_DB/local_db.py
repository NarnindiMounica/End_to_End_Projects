import sqlite3

#connecting to local db "students.db"
connection = sqlite3.Connection("students.db")

#creating the cursor object
cursor = connection.cursor()

#sql query to create a table

table_info="""
    create table student
    (
    student_name varchar(25),
    student_id int,
    class varchar(25),
    section varchar(25),
    marks int
    )"""

#creating a table
cursor.execute(table_info)