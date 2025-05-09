import sys
sys.path.append('C:/Users/chise/Downloads/Student-Bullying-Reporting-Application-main') #change to your own file path

from datetime import datetime
import builtins
from unittest.mock import patch
from Reports import InPersonReport, CyberBullyingReport, ConfidentialityLevel, ReportStatus
from SchoolClass import School
from UserClasses import Administrator, Teacher
from DataSecurity import hash_password, SecurityManager

def test_tc004_assign_invalid_staff_to_report():
    """
    Test Case TC004: Administrator Attempts Invalid Staff Assignment
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
    
  # Step 3: Simulate invalid input ("99")
    original_input = builtins.input
    builtins.input = lambda _: "99"  # Mock invalid selection

    try:
        # Attempt assignment (should handle invalid input)
        admin.assignStaff(report, [teacher])
        
        # --- KEY ASSERTION CHANGE ---
        # Verify NO teacher was assigned (expected for invalid input)
        assert not hasattr(report, "assigned_teacher") or report.assigned_teacher is None, \
            "[FAIL] System incorrectly assigned a teacher for invalid input!"
    except ValueError as e:
        # Expected if system raises an error for invalid input
        assert "Invalid selection" in str(e), "[FAIL] Unexpected error message."
    finally:
        builtins.input = original_input

    print("[SUCCESS] Test Case TC004 passed: System rejected invalid selection.")

if __name__ == "__main__":
    test_tc004_assign_invalid_staff_to_report()
