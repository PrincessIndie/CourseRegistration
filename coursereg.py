import re  # Importing regular expressions for pattern matching


class Course:
    """Class to represent a course."""

    def __init__(usr, course_id, name, fee):
        usr.course_id = course_id  # Unique identifier for the course
        usr.name = name  # Name of the course
        usr.fee = fee  # Course fee


class Student:
    """Class to represent a student."""

    def __init__(usr, student_id, name, email):
        usr.student_id = student_id  # Unique student identifier
        usr.name = name  # Student's name
        usr.email = email  # Student's email address
        usr.courses = []  # List to store the courses the student is enrolled in
        usr.balance = 0  # Outstanding balance for the student (total fees for enrolled courses)

    def enroll(usr, course):
        """Enroll the student in a course if not already enrolled."""
        if course not in usr.courses:
            usr.courses.append(course)  # Add the course to the student's courses list
            usr.balance += course.fee  # Add the course fee to the student's balance
        else:
            print(f"Already enrolled in {course.name}.")  # Error message if student is already enrolled


class RegistrationSystem:
    """Class to manage the course registration and payment system."""

    def __init__(usr):
        # Initialize with some courses and students
        usr.courses = [
            Course("C101", "Python Programming", 500),
            Course("C102", "Data Science", 700),
        ]
        usr.students = {
            "S001": Student("S001", "Alice", "alice@gmail.com"),
            "S002": Student("S002", "Bob", "bob@gmail.com"),
        }

    # Validation for course code (must start with a letter and contain 3 digits)
    def validate_course_code(usr, course_id):
        if not re.match(r"^[A-Za-z][0-9]{3}$", course_id):
            raise ValueError(
                "Course code error: must start with a letter, contain 3 numbers, and cannot exceed 4 characters.")

    # Validation for student ID (must start with 'S' and followed by 3 digits)
    def validate_student_id(usr, student_id):
        if not re.match(r"^S[0-9]{3}$", student_id):
            raise ValueError("Student ID error: must start with 'S' followed by exactly 4 digits.")

    # Validation for payment amount (must be positive numeric value)
    def validate_payment_amount(usr, amount):
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Payment error: amount must be a positive number.")

    # Validation for course fee (must be positive numeric value)
    def validate_course_fee(usr, fee):
        if not isinstance(fee, (int, float)) or fee <= 0:
            raise ValueError("Fee error: must be a positive numeric value.")

    # Validation for student email (must contain "@" and end with ".com" or ".edu")
    def validate_email(usr, email):
        if not re.match(r"[^@]+@[^@]+\.(com|edu)$", email):
            raise ValueError("Email error: Must contain '@' and end with '.com' or '.edu'.")

    # Function to add a new course to the system
    def add_course(usr):
        while True:
            try:
                # Get and validate course ID
                course_id = input("Enter course ID (e.g., C101): ")
                usr.validate_course_code(course_id)

                # Check if the course ID already exists
                if any(course.course_id == course_id for course in usr.courses):
                    print("Course ID already exists. Try again.")
                    continue

                # Get and validate course name
                name = input("Enter course name: ").strip()
                if not name:
                    print("Course name cannot be empty. Try again.")
                    continue

                # Get and validate course fee
                try:
                    fee = float(input("Enter course fee: "))
                    usr.validate_course_fee(fee)
                except ValueError as e:
                    print(e)
                    continue

                # Add the new course to the system
                usr.courses.append(Course(course_id, name, fee))
                print(f"Course '{name}' with ID '{course_id}' added successfully!")
                break

            except ValueError as e:
                print(e)  # Catch and display any validation errors

    # Function to register a new student in the system
    def register_student(usr):
        while True:
            try:
                student_id = input("Enter student ID (e.g., S001): ")
                usr.validate_student_id(student_id)

                # Check if the student ID already exists
                if student_id in usr.students:
                    print("Student already registered. Try again.")
                    continue

                # Get student's name and email
                name = input("Enter student name: ").strip()
                if not name:
                    print("Student name cannot be empty. Try again.")
                    continue

                # Get and validate email
                email = input("Enter student email: ").strip()
                usr.validate_email(email)

                # Register the new student
                usr.students[student_id] = Student(student_id, name, email)
                print(f"Student '{name}' with ID '{student_id}' registered successfully!")
                break

            except ValueError as e:
                print(e)  # Display any validation errors

    # Function to enroll a student in a course
    def enroll_in_course(usr):
        while True:
            try:
                student_id = input("Enter student ID (e.g., S001): ")
                usr.validate_student_id(student_id)

                # Check if the student exists in the system
                student = usr.students.get(student_id)
                if not student:
                    print("Student not found. Try again.")
                    continue

                # Get and validate course ID
                course_id = input("Enter course ID (e.g., C101): ")
                usr.validate_course_code(course_id)

                # Check if the course exists in the system
                course = next((c for c in usr.courses if c.course_id == course_id), None)
                if not course:
                    print("Course not found. Try again.")
                    continue

                # Enroll the student in the course
                student.enroll(course)
                print(f"{student.name} successfully enrolled in {course.name}.")
                break

            except ValueError as e:
                print(e)  # Display any validation errors

    # Function to process a payment from a student
    def calculate_payment(usr):
        while True:
            try:
                student_id = input("Enter student ID (e.g., S001): ")
                usr.validate_student_id(student_id)

                # Check if the student exists
                student = usr.students.get(student_id)
                if not student:
                    print("Student not found. Try again.")
                    continue

                # Get and validate the payment amount
                try:
                    amount = float(input("Enter payment amount: "))
                    usr.validate_payment_amount(amount)
                except ValueError as e:
                    print(e)
                    continue

                # Ensure the payment is at least 40% of the balance
                if amount < 0.4 * student.balance:
                    print("Minimum payment is 40% of the balance. Try again.")
                    continue

                # Update the student's balance after the payment
                student.balance -= amount
                print(f"Payment of ${amount} received. Remaining balance: ${student.balance}.")
                break

            except ValueError as e:
                print(e)  # Display any validation errors

    # Function to show all available courses
    def show_courses(usr):
        print("\nAvailable Courses:")
        for course in usr.courses:
            print(f"{course.course_id}: {course.name} (${course.fee})")

    # Function to show all registered students
    def show_students(usr):
        print("\nRegistered Students:")
        for student in usr.students.values():
            print(f"{student.student_id}: {student.name} (Balance: ${student.balance})")

    # Function to show all courses a student is enrolled in
    def show_student_courses(usr):
        while True:
            try:
                student_id = input("Enter student ID (e.g., S001): ")
                usr.validate_student_id(student_id)

                # Check if the student exists
                student = usr.students.get(student_id)
                if not student:
                    print("Student not found. Try again.")
                    continue

                # Show the courses the student is enrolled in
                if not student.courses:
                    print(f"{student.name} is not enrolled in any courses.")
                else:
                    print(f"\nCourses for {student.name}:")
                    for course in student.courses:
                        print(f"{course.course_id}: {course.name} (${course.fee})")
                break

            except ValueError as e:
                print(e)  # Display any validation errors


# Menu-driven program for user interaction
def main():
    system = RegistrationSystem()

    while True:
        print("\n--- Course Registration and Payment System ---")
        print("1. Show all courses")
        print("2. Show all students")
        print("3. Add a new course")
        print("4. Register a new student")
        print("5. Enroll a student in a course")
        print("6. Process a payment")
        print("7. Show courses a student is enrolled in")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        # Menu options
        if choice == "1":
            system.show_courses()
            input("\nPress Enter to return to the menu...")

        elif choice == "2":
            system.show_students()
            input("\nPress Enter to return to the menu...")

        elif choice == "3":
            system.add_course()
            input("\nPress Enter to return to the menu...")

        elif choice == "4":
            system.register_student()
            input("\nPress Enter to return to the menu...")

        elif choice == "5":
            system.enroll_in_course()
            input("\nPress Enter to return to the menu...")

        elif choice == "6":
            system.calculate_payment()
            input("\nPress Enter to return to the menu...")

        elif choice == "7":
            system.show_student_courses()
            input("\nPress Enter to return to the menu...")

        elif choice == "8":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")
            input("\nPress Enter to return to the menu...")


# Run the program
if __name__ == "__main__":
    main()
