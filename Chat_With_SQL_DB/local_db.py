import sqlite3

#connecting to local db "students.db"
connection = sqlite3.Connection("students.db")

#creating the cursor
cursor = connection.cursor()
