import sys
sys.path.append('C:/Users/NV3/Code/Student-Bullying-Reporting-Application') #change to your own file path

from datetime import datetime
from Reports import InPersonReport, ConfidentialityLevel
from SchoolClass import School
from UserClasses import Student
from DataSecurity import hash_password

def test_tc003_file_incomplete_report():
    # Setup: Initialize school and student
    school = School("SCH001", "BatStateU-The-NEU", "Golden Country Homes, Brgy. Alangilan, Batangas City")
    school.reports.clear()
    
    student = Student(
        userID="S001",
        name="Ben Gonzales",
        email="Ben@student.com",
        grade=10,
        passwordHash=hash_password("yulo")
    )
    school.users.append(student)

    # Step 1: Log in as the student
    assert student.login("yulo"), "[ERROR] Login failed for student."

    # Step 2: Create a new in-person bullying report with missing required fields
    report_id = f"R{len(school.reports) + 1:03}"
    report_date = datetime.now()
    description = ""    # Missing description
    confidentiality_level = ConfidentialityLevel.CONFIDENTIAL
    location = ""       # Missing location

    report = InPersonReport(
        reportID=report_id,
        reportDate=report_date,
        description=description,
        confidentialityLevel=confidentiality_level,
        location=location
    )

    # Step 3: File the report
    student.fileReport(report)

    # Step 4: Verify that the report should NOT be registered in the school system
    registered_report = next((r for r in school.reports if r.reportID == report_id), None)
    assert registered_report is None, "[ERROR] Report with missing required fields was incorrectly registered."

    print("[SUCCESS] Test Case TC003 passed.")

if __name__ == "__main__":
    test_tc003_file_incomplete_report()