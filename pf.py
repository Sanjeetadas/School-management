import mysql.connector as myc

# Connect to MySQL
mydb = myc.connect(host='localhost', user='root', password='s20120148829', charset='utf8')
mycursor = mydb.cursor()

# Create Database and Tables
mycursor.execute("CREATE DATABASE IF NOT EXISTS school_management;")
mycursor.execute("USE school_management;")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        full_roll_no CHAR(20) PRIMARY KEY,
        addmission_no VARCHAR(20) UNIQUE,
        name VARCHAR(50) NOT NULL,
        class INT,
        section CHAR(1),
        age INT,
        gender CHAR(1) CHECK (gender IN ('M', 'F'))
    );
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS fee(
        roll_no char(20),         
        fee int,
        date date,
        month char(20),
        mode_of_payment char(20),
        foreign key(roll_no) references student(full_roll_no)
        );
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        empid CHAR(20) PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        designation CHAR(20),
        subject CHAR(20),
        gender CHAR(1) CHECK (gender IN ('M', 'F')),
        DOB DATE,
        phone_no BIGINT UNIQUE
    );
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS salary(
        empid char(20),
        salary int,
        date date,
        month char(20),
        mode_of_payment char(20),
        foreign key(empid) references staff(empid)
    );
""")
mydb.commit()

# Menu-driven program
while True:
    print("\n1: Add new student" "\n2: Add new staff member" "\n3: Search student" "\n4: Search staff member" "\n5: Add fee details" "\n6: Add salary details")
    print("7: Remove student" "\n8: Remove staff member" "\n9: Search fee detail of student" "\n10: Search salary detail" "\n11: Analyse FEE and SALARY" "\n12: Exit")

    try:
        choice = int(input("Enter your choice: "))

        # Add new student
        if choice == 1:
            full_roll_no = input("Enter full roll number: ").strip()
            add_no = input("Enter admission number: ").strip()
            name = input("Enter name: ").strip()
            cl = int(input("Enter class (in numeric form): ").strip())
            sec = input("Enter section: ").strip().upper()
            gen = input("Enter gender (M/F): ").strip().upper()
            age = int(input("Enter age: ").strip())

            val = (full_roll_no, add_no, name, cl, sec, age, gen)
            sql = "INSERT INTO student (full_roll_no, addmission_no, name, class, section, age, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, val)
            mydb.commit()
            print("Student record added successfully.")

        # Add new staff member
        elif choice == 2:
            empid = input("Enter employee ID: ").strip()
            name = input("Enter name: ").strip()
            desg = input("Enter designation: ").strip()
            sub = input("Enter subject: ").strip()
            gen = input("Enter gender (M/F): ").strip().upper()
            dob = input("Enter date of birth (YYYY-MM-DD): ").strip()
            ph = int(input("Enter phone number: ").strip())

            val = (empid, name, desg, sub, gen, dob, ph)
            sql = "INSERT INTO staff (empid, name, designation, subject, gender, DOB, phone_no) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, val)
            mydb.commit()
            print("Staff record added successfully.")

        # Search student
        elif choice == 3:
            print("1. Search by name")
            print("2. Search by full roll number")
            sub_choice = int(input("Enter your choice (1/2): "))

            if sub_choice == 1:
                stu_name = input("Enter name to be searched: ").strip()
                sql = "SELECT * FROM student WHERE name LIKE %s"
                search_term = f"%{stu_name}%"
                mycursor.execute(sql, (search_term,))
            elif sub_choice == 2:
                roll_no = input("Enter full roll number to be searched: ").strip()
                sql = "SELECT * FROM student WHERE full_roll_no = %s"
                mycursor.execute(sql, (roll_no,))
            else:
                print("Invalid choice.")
                continue

            results = mycursor.fetchall()
            if results:
                for i in results:
                    print(f"ROLL NUMBER: {i[0]}, ADMISSION NUMBER: {i[1]}, NAME: {i[2]}, CLASS: {i[3]}, SECTION: {i[4]}, AGE: {i[5]}, GENDER: {i[6]}")
            else:
                print("No matching records found.")

        # Search staff member
        elif choice == 4:
            emp_id = input("Enter employee ID to be searched: ").strip()
            sql = "SELECT * FROM staff WHERE empid = %s"
            mycursor.execute(sql, (emp_id,))
            results = mycursor.fetchall()
            if results:
                for i in results:
                    print(f"EMPLOYEE ID: {i[0]}, NAME: {i[1]}, DESIGNATION: {i[2]}, SUBJECT: {i[3]}, GENDER: {i[4]}, DOB: {i[5]}, PHONE NUMBER: {i[6]}")
            else:
                print("No matching records found.")

        # Add fee details of student
        elif choice== 5:
            r_no= input("Enter roll number of student:").strip()
            fee= int(input("Enter fee to be added:").strip())
            date= input("Enter date of payment(YYYY-MM-DD):").strip()
            mon= input("Enter the month of fee):").strip()
            mode= input("Enter the mode of payment:").strip()

            val=(r_no, fee, date, mon, mode)
            sql = "INSERT INTO fee(roll_no, fee, date, month, mode_of_payment) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(sql,val)
            mydb.commit()
            print("Fee details added successfully")
        
        # Add salary details
        elif choice == 6:
            emp_id = input("Enter employee ID to be searched: ").strip()
            salary = int(input("Enter salary to be added: ").strip())
            date = input("Enter date of payment(YYYY-MM-DD): ").strip()
            month= input("Enter the month of salary:").strip()
            mode= input("Enter the mode of payment:").strip()

            val= (emp_id, salary, date, month, mode)
            sql = "INSERT INTO salary(empid, salary, date, month, mode_of_payment) VALUES(%s, %s, %s, %s, %s)"
            mydb.commit()
            print("Salary details added successfully")
            
        # Remove student
        elif choice == 7:
            name = input("Enter name of the student to be deleted: ").strip()
            sql = "DELETE FROM student WHERE name = %s"
            mycursor.execute(sql, (name,))
            mydb.commit()
            print("Student record deleted successfully.")

        # Remove staff member
        elif choice == 8:
            emp_id = input("Enter employee ID to be deleted: ").strip()
            sql = "DELETE FROM staff WHERE empid = %s"
            mycursor.execute(sql, (emp_id,))
            mydb.commit()
            print("Staff record deleted successfully.")

        # Search fee detail
        elif choice==9:
            r_no= int(input("Enter full roll number of the student:").strip())
            sql= "SELECT * from fee where roll_no like %s"
            mycursor.execute(sql, (r_no,))
            results = mycursor.fetchall()

            if results:
                for i in results:
                    print(f"ROLL NUMBER: {i[0]}, FEE: {i[1]}, DATE: {i[2]}, FEE OF MONTH: {i[3]}, MODE OF PAYEMENT: {i[4]}")
            else:
                print("No matching records found.")

        #Search salary detail
        elif choice==10:
            emp_id= int(input("Enter employee ID to be searched:").strip())
            sql= "SELECT * from salary where empid like %s"
            mycursor.execute(sql, (emp_id,))
            results = mycursor.fetchall()

            if results:
                for i in results:
                    print(f"EMPLOYEE ID: {i[0]}, SALARY: {i[1]}, DATE: {i[2]}, MONTH: {i[3]}, MODE OF PAYEMENT: {i[4]}")
            else:
                print("No matching records found.")

        #Analayse fee or salary
        elif choice==11:
            print("1. Fee Analysis\n2. Salary Analysis")
            choice2 = int(input("Enter your choice: ").strip())
            if choice2==1:
                print("1. Total Fee\n2. Average Fee\n3. Highest Fee\n4.Fee of a particular month")
                choice3 = int(input("Enter your choice: ").strip())
                if choice3==1: 
                    sql = "SELECT SUM(fee) from fee"
                    mycursor.execute(sql)
                    results= mycursor.fetchall()
                    print(f"Total Fee: {results[0][0]}")
                elif choice3==2:
                    sql = "SELECT AVG(fee) from fee"
                    mycursor.execute(sql)
                    results= mycursor.fetchall()
                    print(f"Average Fee: {results[0][0]}")
                elif choice3==3:
                    sql= "SELECT MAX(fee) from fee"
                    mycursor.execute(sql)
                    results= mycursor.fetchall()
                    print(f"Highest Fee: {results[0][0]}")
                elif choice3==4:
                    month = input("Enter the month for which you want to see the fee: ").strip()
                    sql = "SELECT SUM(fee) from fee where month like %s"
                    mycursor.execute(sql, (month,))
                    results= mycursor.fetchall()
                    print(f"Fee of {month}: {results[0][0]}")
                else:
                    print("Invalid choice")
            elif choice2==2:
                print("1. Total Salary\n2. Average Salary\n3. Highest Salary\n4.Salary of a particular month")
                choice3 = int(input("Enter your choice: ").strip())
                if choice3==1:
                    sql = "SELECT SUM(salary) from salary"
                    mycursor.execute(sql)
                    results= mycursor.fetchall()
                    print(f"Total Salary: {results[0][0]}")
                elif choice3==2:
                    sql = "SELECT AVG(salary) from salary"
                    mycursor.execute(sql)
                    results= mycursor.fetchall()
                    print(f"Average Salary: {results[0][0]}")
                elif choice3==3:
                    sql= "SELECT MAX(salary) from salary"
                    mycursor.execute(sql)
                    results= mycursor.fetchall()
                    print(f"Highest Salary: {results[0][0]}")
                elif choice3==4:
                    month = input("Enter the month for which you want to see the salary: ").strip()
                    sql = "SELECT SUM(salary) from salary where month like %s"
                    mycursor.execute(sql, (month,))
                    results= mycursor.fetchall()
                    print(f"Salary of {month}: {results[0][0]}")
                else:
                    print("Invalid choice")
        # Exit
        elif choice == 12:
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

    except ValueError:
        print("Invalid input. Please enter numeric values where required.")
    except myc.Error as err:
        print(f"Database error: {err}")

# Close connection
mycursor.close()
mydb.close() 