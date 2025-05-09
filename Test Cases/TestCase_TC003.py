import sys
sys.path.append('C:/Users/chise/Downloads/Student-Bullying-Reporting-Application-main') #change to your own file path

from datetime import datetime
import builtins
from unittest.mock import patch
from Reports import InPersonReport, CyberBullyingReport, ConfidentialityLevel, ReportStatus
from SchoolClass import School
from UserClasses import Administrator, Teacher
from DataSecurity import hash_password, SecurityManager

def test_tc003_assign_staff_to_report():
    """
    Test Case TC003: Administrator assigns a teacher to a bullying report
    """
    # Setup: Initialize school, administrator, teacher, and create a report
    school = School("SCH001", "BatStateU-The-NEU", "Golden Country Homes, Brgy. Alangilan, Batangas City")
    school.reports.clear()
    school.users.clear()
    
    # Create an administrator and teacher
    admin = Administrator(
        userID="A001",
        name="Cardo Dalisay",
        email="Cardo@admin.com",
        passwordHash=hash_password("bengbeng")
    )
    
    teacher = Teacher(
        userID="T001",
        name="Raffy Tulfo",
        email="Raffy@teacher.com",
        passwordHash=hash_password("Raffy Tulfo in Action")
    )
    
    # Add users to school
    school.users.extend([admin, teacher])
    
    # Create a test report
    report = InPersonReport(
        reportID="R001",
        reportDate=datetime.now(),
        description="A bullying incident in the gymnasium",
        confidentialityLevel=ConfidentialityLevel.CONFIDENTIAL,
        location="School Gymnasium"
    )
    
    # Add report to school
    school.reports.append(report)
    
    # Step 1: Log in as administrator
    assert admin.login("bengbeng"), "[ERROR] Login failed for administrator."
    
    # Step 2: Check administrator has permission to assign staff
    security_manager = SecurityManager()
    assert security_manager.checkPermission(admin, "assign_staff"), "[ERROR] Administrator doesn't have permission to assign staff."
    
    # Step 3: Administrator assigns the teacher to the report
    # Mock the input function to automatically select the first teacher
    original_input = builtins.input
    
    # Define a mock input function that returns "1" when called
    def mock_input(prompt):
        return "1"
    
    # Replace the built-in input function with our mock version
    builtins.input = mock_input
    
    try:
        # Now when assignStaff is called, the mock input will automatically select option 1
        admin.assignStaff(report, [teacher])
    finally:
        # Restore the original input function
        builtins.input = original_input
    
    # Step 4: Verify the teacher was assigned to the report
    assert hasattr(report, "assigned_teacher"), "[ERROR] Report doesn't have assigned_teacher attribute."
    assert report.assigned_teacher == teacher, "[ERROR] Teacher wasn't correctly assigned to the report."
    
    print("[SUCCESS] Test Case TC003 passed.")

if __name__ == "__main__":
    test_tc003_assign_staff_to_report()
