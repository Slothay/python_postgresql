import psycopg2
import psycopg2.extras
from config import configurate

MENU = '''
Choose from the menu what would you like to do. Press the corresponding number.
0. Exit program
1. Print table values
2. Reset the database
3. Insert new record
4. Update Value(s)
5. Delete Record
'''

def reset_table():
    cur.execute('DROP TABLE IF EXISTS employee')
    create_script = """ CREATE TABLE IF NOT EXISTS employee (
                            id      int PRIMARY KEY,
                            name    varchar(40) NOT NULL,
                            salary  int,
                            dept_id varchar(30)) """
    cur.execute(create_script)

def insert_records():
    insert_script = """INSERT INTO employee (id, name, salary, dept_id) VALUES(%s,%s,%s,%s)"""
    insert_values = [(1, 'James', 12000, 'D1'), (2, 'Robin', 15000, 'D1'), (3, 'John', 20000, 'D2')]
    for record in insert_values:
        cur.execute(insert_script, record)

def update_values():
    update_script = 'UPDATE employee SET salary = salary + (salary*0.5)'
    cur.execute(update_script)

def delete_record(delete_r):
    i = 0
    cur.execute('SELECT * FROM employee')
    for record in cur.fetchall():
        if record['name'] == delete_r:
            i += 1
            delete_script = 'DELETE FROM employee WHERE name = %s'
            delete_record = (delete_r,)
            cur.execute(delete_script, delete_record)
    if i == 0:
        print("There is no such employee name in the records.")

def print_table():
    cur.execute('SELECT * FROM employee')
    for record in cur.fetchall():
        print(record['name'], record['salary'])

conn = None
menu = ["0","1","2","3","4","5"]
exit_program = False
try:
    params = configurate()
    with psycopg2.connect(
        **params
    ) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            while not exit_program:
                print(MENU)
                answer = input("What would you like to do? ")
                try:
                    if answer == "0":
                        print("Goodbye!")
                        exit_program = True
                    elif answer == "2":
                        reset_table()
                        print("Table reset.")
                    elif answer == "3":
                        insert_records()
                        print("Inserted values")
                    elif answer == "4":
                        update_values()
                        print("Data updated.")
                    elif answer == "1":
                        print_table()
                    elif answer == "5":
                        to_delete = input("Which employee record would you like to delete?:")
                        delete_record(to_delete)
                except ValueError:
                    print("Please choose valid option.")

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()