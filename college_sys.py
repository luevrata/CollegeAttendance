import mysql.connector as mysql

#Variables 
host = "localhost"
user = "root"
password = ""

#Connecting to mysql
try:
    db  = mysql.connect(host = host, user = user, password = password, database = "college")
    command_handler =  db.cursor(buffered = True)
    print("Connected to database")
except Exception as e:
    print(e)
    print("Failed to connect")

def student_session(username):
    while 1:
        print("")
        print("Student Menu")
        print("1. View Register")
        print("2. Download Register")
        print("3. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("Displaying register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status from attendance WHERE username  =%s", username)
            records = command_handler.fetchall()
            for record in records:
                print(record)
        if user_option == "2":
            print("Downloading register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status from attendance WHERE username  =%s", username)
            records = command_handler.fetchall()
            with open("C:/Users/lu_ev/Desktop/table/study/SQL_Tutorial/register.txt", "w") as f:
                f.write(str(records)+"\n")
            f.close()
            print ("All records saved")
        elif user_option=="3":
            break
        else:
            print("No valid option selected")


def teacher_session():
    while 1:
        print("")
        print("Teacher Menu")
        print("1. Mark student register")
        print("2. View register")
        print("3. Logout")

        user_option = input(str("Option : "))
        if user_option =="1":
            print("")
            print("Mark student register")
            command_handler.execute("SELECT username from users WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = input(str("Date : DD/MM/YYYY :"))
            for record in records:
                #record is returned as tuple
                record  = str(record).replace("'", "")
                record  = str(record).replace(",", "")
                record  = str(record).replace("(", "")
                record  = str(record).replace(")", "")
                #present/absent/late
                status = input(str("Status for "+str(record) + " P/A/L : "))
                query_vals  = (str(record), date , status)
                command_handler.execute("INSERT INTO attendance (username, date, status) VALUES(%s,%s,%s)", query_vals)
                db.commit()
                print(record + " marked as "+ status)
        elif user_option == "2":
            print("")
            print("Viewing all student registers")
            command_handler.execute("SELECT username, date, status FROM attendance")
            records = command_handler.fetchall()
            print("Displaying all registers")
            for record in records:
                print(record)
        elif user_option=="3":
            break
        else:
            print("No valid option selected")



def admin_session() :
    while 1:
        print("")
        print("Admin Menu")
        print("1. Register new Student")
        print("2. Register new Teacher")
        print("3. Delete existing Student")
        print("4. Delete existing Teacher")
        print("5. Logout")

        user_option = input(str("Option : "))
        if user_option =="1":
            print("")
            print("Register new Student")
            username = input(str("Student username : "))
            password = input(str("Student password : "))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users (username, password, privilege) VALUES (%s, %s, 'student')", query_vals)
            db.commit() 
            print (username + " has been registered as a student")
        elif user_option =="2":
            print("")
            print("Register new Teacher")
            username = input(str("Teacher username : "))
            password = input(str("Teacher password : "))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users (username, password, privilege) VALUES (%s, %s, 'teacher')", query_vals)
            db.commit() 
            print (username + " has been registered as a teacher")
        elif user_option == "3":
            print("")
            print("Delete Existing Student Account")
            username = input(str("Student username :"))
            query_vals = (username, 'student')
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")
        elif user_option == "4":
            print("")
            print("Delete Existing Teacher Account")
            username = input(str("Teacher username :"))
            query_vals = (username, 'teacher')
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")
        elif user_option == "5":
            break
        else:
            print("No valid option selected")

def auth_student():
    print("")
    print("Student Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password)
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = 'student'", query_vals)
    if command_handler.rowcount <=0:
        print("Invalid login details")
    else: 
        student_session(username)

def auth_teacher():
    print("")
    print("Teacher's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password)
    command_handler.execute("SELECT* FROM users WHERE username = %s AND password = %s AND privilege  = 'teacher'",query_vals)
    if command_handler.rowcount<=0:
        print("Login is not recognized")
    else:
        teacher_session()

def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("Incorrect password!")
    else:
        print("Login details are not recognized")

def main():
    while 1:
        print("Welcome to the college system\n")
        print("1. Login as student")
        print("2. Login as teacher")
        print("3. Login as admin")
        print("4. Quit")

        user_option = input(str("Option:"))
        if user_option =="1":
            auth_student()
        elif user_option =="2":
            auth_teacher()
        elif user_option =="3":
            auth_admin()
        elif user_option =="4":
           break
        else:
            print("No valid option was selected")

main()
