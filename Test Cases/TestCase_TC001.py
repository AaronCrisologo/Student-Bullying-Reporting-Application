import sys
sys.path.append('C:/Users/NV3/Code/Student-Bullying-Reporting-Application') #change to your own file path

from datetime import datetime
from Reports import InPersonReport, ConfidentialityLevel
from SchoolClass import School
from UserClasses import Student
from DataSecurity import hash_password

def test_tc001_file_bullying_report():
    # Setup: Initialize school and student
    school = School("SCH001", "BatStateU-The-NEU", "Golden Country Homes, Brgy. Alangilan, Batangas City")
    
    # Clear any existing reports to ensure a clean test environment
    school.reports.clear()
    
    student = Student(
        userID="S001",
        name="Ben Gonzales",
        email="Ben@student.com",
        grade=10,
        passwordHash=hash_password("yulo")  # Pre-hashed password for "hello"
    )
    school.users.append(student)

    # Step 1: Log in as the student
    assert student.login("yulo"), "[ERROR] Login failed for student."

    # Step 2: Create a new bullying report
    report_id = f"R{len(school.reports) + 1:03}"
    report_date = datetime.now()
    description = "A bullying incident near the cafeteria."
    confidentiality_level = ConfidentialityLevel.CONFIDENTIAL
    location = "Cafeteria"

    report = InPersonReport(
        reportID=report_id,
        reportDate=report_date,
        description=description,
        confidentialityLevel=confidentiality_level,
        location=location
    )

    # Step 3: File the report
    student.fileReport(report)

    # Step 4: Verify the report is registered in the school system
    registered_report = next((r for r in school.reports if r.reportID == report_id), None)
    assert registered_report is not None, "[ERROR] Report was not registered in the school system."
    assert registered_report.description == description, "[ERROR] Report description mismatch."
    assert registered_report.location == location, "[ERROR] Report location mismatch."
    assert registered_report.confidentialityLevel == confidentiality_level, "[ERROR] Confidentiality level mismatch."
    assert registered_report.reporter == student, "[ERROR] Reporter mismatch."

    print("[SUCCESS] Test Case TC001 passed.")

if __name__ == "__main__":
    test_tc001_file_bullying_report()