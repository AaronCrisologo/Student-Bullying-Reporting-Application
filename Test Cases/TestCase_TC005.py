import sys
sys.path.append('C:/Users/chise/Downloads/Student-Bullying-Reporting-Application-main')

from datetime import datetime
import builtins
from Reports import CyberBullyingReport, ConfidentialityLevel, ReportStatus
from SchoolClass import School
from UserClasses import Administrator, Teacher, Student
from DataSecurity import hash_password, SecurityManager

def test_tc005_change_assigned_teacher():
    """
    Test Case TC005: Administrator changes the teacher assigned to a report
    with simulated user input for teacher selection
    """
    try:
        # Setup
        school = School("SCH001", "BatStateU-The-NEU", "Golden Country Homes, Brgy. Alangilan, Batangas City")
        school.reports.clear()
        school.users.clear()
        
        # Create users
        admin = Administrator(
            userID="A001",
            name="Cardo Dalisay",
            email="Cardo@admin.com",
            passwordHash=hash_password("bengbeng"))
        
        teacher1 = Teacher(
            userID="T001",
            name="Raffy Tulfo",
            email="Raffy@teacher.com",
            passwordHash=hash_password("Raffy Tulfo in Action"))
        
        teacher2 = Teacher(
            userID="T002",
            name="Erwin Tulfo",
            email="Erwin@teacher.com",
            passwordHash=hash_password("Para sa mahirap"))
        
        student = Student(
            userID="S001",
            name="Ben Gonzales",
            email="Ben@student.com",
            grade=10,
            passwordHash=hash_password("yulo"))
        
        school.users.extend([admin, teacher1, teacher2, student])
        
        report = CyberBullyingReport(
            reportID="R001",
            reportDate=datetime.now(),
            description="Cyberbullying on social media",
            confidentialityLevel=ConfidentialityLevel.HIGHLY_CONFIDENTIAL,
            onlinePlatform="Facebook",
            reporter=student)
        
        school.reports.append(report)
        
        # Step 1: Login
        assert admin.login("bengbeng"), "Admin login failed"
        
        # Step 2: Verify permission
        security_manager = SecurityManager()
        assert security_manager.checkPermission(admin, "assign_staff"), \
            "Admin lacks assign_staff permission"
        
        # Step 3: Initial assignment (teacher1)
        original_input = builtins.input
        builtins.input = lambda _: "1"  # Mock selecting teacher1
        
        try:
            admin.assignStaff(report, [teacher1, teacher2])
            assert report.assigned_teacher == teacher1, \
                "Initial teacher assignment failed"
        finally:
            builtins.input = original_input
        
        # Step 4: Change assignment (teacher2)
        builtins.input = lambda _: "2"  # Mock selecting teacher2
        
        try:
            admin.assignStaff(report, [teacher1, teacher2])
            assert report.assigned_teacher == teacher2, \
                "Teacher reassignment failed"
            assert report.assigned_teacher != teacher1, \
                "Previous teacher still assigned"
        finally:
            builtins.input = original_input
        
        # Step 5: Verify status unchanged
        assert report.status == ReportStatus.NEW, \
            "Report status changed unexpectedly"
        
        # If we get here, all assertions passed
        print("\n[SUCCESS] TC005 - All test steps passed:")
        print("1. Admin login successful")
        print("2. Admin has correct permissions")
        print("3. Initial teacher assignment successful")
        print("4. Teacher reassignment successful")
        print("5. Report status maintained correctly")
        
        return True
        
    except AssertionError as e:
        print(f"\n[FAIL] TC005 - Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] TC005 - Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    test_tc005_change_assigned_teacher()
