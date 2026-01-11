import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50),
        age INT,
        major VARCHAR(255)
        );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses(
        courses_id INTEGER PRIMARY KEY AUTOINCREMENT,
        courses_name VARCHAR(255),
        instructor VARCHAR(255)
        );
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS info(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        students_id INT,
        course_id INT,
        FOREIGN KEY (students_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (courses_id)
        );
""")


while True:
    print("""\n---------------------------------------------------------------
1.Додати нового студента.
2.Додати новий курс.
3.Показати список студентів.
4.Показати список курсів.
5.Записати студента на курс.
6.Показати студентів на конкретному курсі.
7.Завершення роботи.
---------------------------------------------------------------\n""")
    try:
        choice = int(input("Виберіть опцію (1 - 7): \n"))
    except ValueError:
        print("\nВиникла помилка, виберіть опцію ще раз!\n")
    
    else:
    

        if choice == 7:
            break


        elif choice == 1:
            print("Додавання нового студента.\n")
            while True:
                name = input("Ім'я нового студента: ")
                if not name.isalpha():
                    print("\nВиникла помилка, введіть ім'я студента правильно!\n") 
                else:
                    try:
                        age = int(input("Вік студента: "))
                    except ValueError:
                        print("\nВиникла помилка, введіть вік студента правильно.\n")
                    else:
                        major = input("Спеціальність студента: ")
                        if not major.isalpha():
                            print("\nВиникла помилка, введіть спеціальність студента правильно.\n")
                        else:
                            break
            query = "INSERT INTO students (name, age,major)" \
                "VALUES (?, ?, ?)"
            cursor.execute(query, (name, age, major))
            conn.commit()


        elif choice == 2:
            print("Додавання нового курса.\n")
            while True:
                name = input("Ім'я нового курса: ")
                if not name.isalpha():
                    print("\nВиникла помилка, введіть назву курса правильно!\n")
                else:
                    instruktor = input("Ім'я викладача курса: ")
                    if not instruktor.isalpha():
                        print("\nВиникла помилка, введіть ім'я викладача правильно.\n")
                    else:
                        break

            query = "INSERT INTO courses (courses_name, instructor)" \
                "VALUES (?, ?)"
            cursor.execute(query, (name, instruktor))
            conn.commit()


        elif choice == 3:
            print("\nСписок студентів.\n")
            query = "SELECT * FROM students"
            cursor.execute(query)
            all_students = cursor.fetchall()
            for student in all_students:
                print(f"Нумер студента - {student[0]}")
                print(f"Ім'я студента - {student[1]}")
                print(f"Вік студента - {student[2]}")
                print(f"Спеціальність студента - {student[3]}\n")


        elif choice == 4:
            print("\nСписок курсів.\n")
            query = "SELECT * FROM courses"
            cursor.execute(query)
            all_courses = cursor.fetchall()
            for course in all_courses:
                print(f"Нумер курсу - {course[0]}")
                print(f"Ім'я курсу - {course[1]}")
                print(f"Ім'я викладача - {course[2]}\n")


        elif choice == 5:
            while True:
                try:
                    student_id = int(input("Введіть номер студента: "))
                except ValueError:
                    print("\nВиникла помилка, введіть нумер студента правильно!\n")
                else:
                    query = "SELECT * FROM students WHERE id = ?"
                    cursor.execute(query,(student_id,))
                    students = cursor.fetchall()
                    if students:
                        try:
                            course_id = int(input("Введіть номер курсу: "))
                        except ValueError:
                            print("\nВиникла помилка, введіть нумер курсу правльно!\n")
                        else:
                            query = "SELECT * FROM courses WHERE courses_id = ?"
                            cursor.execute(query,(course_id,))
                            all_courses = cursor.fetchall()
                            if all_courses:
                                query = "INSERT INTO info (students_id, course_id)" \
                                "VALUES (?, ?)"
                                cursor.execute(query, (student_id, course_id,))
                                conn.commit()
                                break


        elif choice == 6:
            while True:
                try:
                    course_id = int(input("Введіть номер курсу: "))
                except ValueError:
                    print("\nВиникла помилка, введіть нумер курсу правильно!\n")
                else:
                    query = "SELECT * FROM courses WHERE courses_id = ?"
                    cursor.execute(query,(course_id,))
                    all_courses = cursor.fetchall()
                    if all_courses:
                        
                        query = """
                        SELECT * 
                        FROM students
                        INNER JOIN info ON students.id = info.students_id 
                        WHERE info.course_id = ?
                        """

                        cursor.execute(query, (course_id,))
                        all_students = cursor.fetchall()
                        print(all_students)
                        print("\n-----------------------Список студентів-----------------------\n")
                        for student in all_students:
                            print(f"Нумер студента - {student[0]}")
                            print(f"Ім'я студента - {student[1]}")
                            print(f"Вік студента - {student[2]}")
                            print(f"Спеціальність студента - {student[3]}\n")
                        print("\n--------------------------------------------------------------\n")
                        break
