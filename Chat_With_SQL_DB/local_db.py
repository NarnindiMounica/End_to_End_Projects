import sqlite3

#connecting to local db "students.db"
connection = sqlite3.connect("students.db")

#creating the cursor object
cursor = connection.cursor()

#if table already exists, delete it to create new one
cursor.execute('''drop table if exists student''')

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

#inserting records into table

cursor.execute('''insert into student values ("Mounica", 100, "Data Science", "A", 98)''')
cursor.execute('''insert into student values ("Ram", 101, "Agentic AI", "A", 78)''')
cursor.execute('''insert into student values ("Sammy", 102, "Data Science", "A", 67)''')
cursor.execute('''insert into student values ("John", 103, "Deep Learning", "A", 89)''')
cursor.execute('''insert into student values ("Amar", 104, "Agentic AI", "A", 70)''')

rows = cursor.execute('''select * from student''')

#displaying records

for row in rows:
    print(row)

print("\n") 

#drop is table already exists
cursor.execute('''drop table if exists teacher''')
#teachers table info
teacher_table_info = '''
create table teacher(
name varchar(25),
subject varchar(25),
experience int
)'''

#execution command for teacher table creation
cursor.execute(teacher_table_info)

#to insert records in teacher table
cursor.execute('''insert into teacher values("Manny", "Agentic AI", 6)''')
cursor.execute('''insert into teacher values("Tom", "Data Science", 2)''')
cursor.execute('''insert into teacher values("Mark", "Deep Learning", 4)''')
cursor.execute('''insert into teacher values("Ruby", "Data Science", 3)''')

#to display records
teacher_records=cursor.execute('''select * from teacher''')

for record in teacher_records:
    print(record)

#committing changes in your database
connection.commit()
connection.close()      