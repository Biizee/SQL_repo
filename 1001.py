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
    print("----------------------------------------\n1.Додати нового студента.\n2.Додати новий курс. \n3.Показати список студентів.\n4.Показати список курсів\n5.Записати студента на курс\n6.Показати студентів на конкретному курсі\n7.Завершення роботи.\n----------------------------------------\n")
    
    choice = int(input("Виберіть опцію (1 - 7):\n"))
    if choice == 7:
        break

    elif choice == 1:
        print("Додавання нового студента.\n")
        name = input("Ім'я нового студента:")
        age = int(input("Вік студента:"))
        major = input("Спеціальність студента:")
        query = "INSERT INTO students (name, age,major)" \
            "VALUES (?, ?, ?)"
        cursor.execute(query, (name, age, major))
        conn.commit()

    elif choice == 2:
        print("Додавання нового курса.\n")
        name = input("Ім'я нового курса:")
        instruktor = input("Ім'я викладача курса:")
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
            print(f"Спеціальність студента - {student[3]}")

    elif choice == 4:
        print("\nСписок курсів.\n")
        query = "SELECT * FROM courses"
        cursor.execute(query)
        all_courses = cursor.fetchall()
        for course in all_courses:
            print(f"Нумер курсу - {course[0]}")
            print(f"Ім'я курсу - {course[1]}")
            print(f"Ім'я викладача - {course[2]}")
    
    elif choice == 5:
        student_id = int(input("Введіть номер студента:"))
        course_id = int(input("Введіть номер курсу:"))
        query = "INSERT INTO info (student_id, course_id)" \
        "VALUES (?, ?)"
        cursor.execute(query, (student_id, course_id))
        conn.commit()

    elif choice == 6:
        print("\nПоказати студентів на конкретному курсі.\n")
        course_id = int(input("Введіть номер курсу:"))
        query = "SELECT * FROM students WHERE student_id = (" \
        "SELECT student_id FROM info WHERE couse_id = (" \
        "SELECT course_id FROM courses WHERE course_name = ?))"
        cursor.execute(query, (course_id))
        all_students = cursor.fetchall()
        for student in all_students:
            print(f"Нумер студента - {student[0]}")
            print(f"Ім'я студента - {student[1]}")
            print(f"Вік студента - {student[2]}")
            print(f"Спеціальність студента - {student[3]}")
