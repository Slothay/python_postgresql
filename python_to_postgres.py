import psycopg2
import psycopg2.extras
from config import configurate

MENU = '''
Choose from the menu what would you like to do. Press the corresponding number.
0. Exit program
1. Print table values
2. Reset the database
3. Insert new record
4. Give everyone a raise
5. Delete Record
'''

def reset_table():
    cur.execute('DROP TABLE IF EXISTS employee')
    create_script = """ CREATE TABLE IF NOT EXISTS employee (
                            id      SERIAL PRIMARY KEY,
                            name    varchar(40) NOT NULL,
                            salary  int,
                            dept_id varchar(30)) """
    cur.execute(create_script)

def insert_records():
    keep_inserting_values = True
    insert_values=[]
    while keep_inserting_values:
        name = input("Please give employee name:")
        salary = input("Please give employee salary:")
        dept_id = input("Please give department ID:")
        insert_script = "INSERT INTO employee (name, salary, dept_id) VALUES(%s,%s,%s)"
        insert_values.append((name,salary,dept_id))
        continue_adding = input("Do you want to add another employee record? (Y/N):").upper()
        if not continue_adding:
            keep_inserting_values = False
    for record in insert_values:
        cur.execute(insert_script, record)

def update_values():
    raise_to_give = float(input("How big of a raise you want to give in percentages?:"))
    raise_to_give = raise_to_give*0.01
    raise_record = str(raise_to_give)
    update_script = f'UPDATE employee SET salary = salary + (salary*{raise_record})'
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
        print("There is no such employee in the records.")

def print_table():
    cur.execute('SELECT * FROM employee')
    for record in cur.fetchall():
        print(record['name'], record['salary'])

conn = None
exit_program = False
try:
    params = configurate()
    with psycopg2.connect(**params) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            while not exit_program:
                print(MENU)
                answer = input("What would you like to do? ")
                match answer:
                    case "0":
                        print("Goodbye!")
                        exit_program = True
                    case "1":
                        print_table()
                    case "2":
                        reset_table()
                        print("Table reset.")
                    case "3":
                        insert_records()
                        print("Inserted values.")
                    case "4":
                        update_values()
                        print("Everyone gained raise.")
                    case "5":
                        to_delete = input("Which employee record would you like to delete?:")
                        delete_record(to_delete)
                    case _:
                        print("Please choose a valid option.")

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()