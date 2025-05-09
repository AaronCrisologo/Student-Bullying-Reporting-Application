import sys
sys.path.append('C:/Users/louis/OneDrive/Documents/Student-Bullying-Reporting-Application-main')  # Update this to your actual path

from UserClasses import Student
from SchoolClass import School
from DataSecurity import hash_password
from datetime import datetime

def test_tc006_validate_student_creation_and_storage():
    """
    Test Case TC006: Validate Student Data Creation and Storage
    """

    # Step 0: Setup
    school = School("SCH001", "BatStateU-The-NEU", "Golden Country Homes, Brgy. Alangilan, Batangas City")
    school.users.clear()  # Clear any existing users to isolate test

    # Step 1: Create Student instances
    student1 = Student(
        userID="S001",
        name="Ben Gonzales",
        email="Ben@student.com",
        grade=10,
        passwordHash=hash_password("yulo")
    )
    student2 = Student(
        userID="S002",
        name="Jose Rizz Al",
        email="Jose@student.com",
        grade=11,
        passwordHash=hash_password("NoliMeTangereLite")
    )

    # Step 2: Add students to school user list
    school.users.extend([student1, student2])

    # Step 3: Assertions to verify correct storage
    students = [u for u in school.users if isinstance(u, Student)]
    assert len(students) == 2, "[FAIL] Expected 2 students in user list."

    # Verify student1
    assert students[0].userID == "S001", "[FAIL] Student 1 ID mismatch."
    assert students[0].name == "Ben Gonzales", "[FAIL] Student 1 name mismatch."
    assert students[0].email == "Ben@student.com", "[FAIL] Student 1 email mismatch."
    assert students[0].grade == 10, "[FAIL] Student 1 grade mismatch."
    assert students[0].passwordHash != "yulo", "[FAIL] Student 1 password should be hashed."

    # Verify student2
    assert students[1].userID == "S002", "[FAIL] Student 2 ID mismatch."
    assert students[1].name == "Jose Rizz Al", "[FAIL] Student 2 name mismatch."
    assert students[1].email == "Jose@student.com", "[FAIL] Student 2 email mismatch."
    assert students[1].grade == 11, "[FAIL] Student 2 grade mismatch."
    assert students[1].passwordHash != "NoliMeTangereLite", "[FAIL] Student 2 password should be hashed."

    print("[SUCCESS] Test Case TC006 passed: Student data correctly created, hashed, and stored.")

if __name__ == "__main__":
    test_tc006_validate_student_creation_and_storage()
