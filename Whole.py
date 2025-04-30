import base64
import hashlib

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

class ReportStatus(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class ConfidentialityLevel(Enum):
    PUBLIC = "PUBLIC"
    CONFIDENTIAL = "CONFIDENTIAL"
    HIGHLY_CONFIDENTIAL = "HIGHLY_CONFIDENTIAL"


class BullyingReport(ABC):
    def __init__(self, reportID: str, reportDate: datetime, description: str,
                 confidentialityLevel: ConfidentialityLevel, reporter: 'Student' = None):
        self.reportID = reportID
        self.reportDate = reportDate
        self.description = description
        self.confidentialityLevel = confidentialityLevel  
        self.status = ReportStatus.NEW
        self.encrypted = False
        self.reporter = reporter

    @abstractmethod
    def validateReport(self) -> bool:
        pass

    @abstractmethod
    def encryptDetails(self) -> None:
        pass


class InPersonReport(BullyingReport):
    def __init__(self, reportID: str, reportDate: datetime, description: str,
                 confidentialityLevel: ConfidentialityLevel, location: str,
                 reporter: 'Student' = None, witnesses: list = None):
        super().__init__(reportID, reportDate, description, confidentialityLevel, reporter)
        self.location = location
        self.witnesses = witnesses if witnesses is not None else []

    def validateReport(self) -> bool:
        return bool(self.description and self.location)

    def encryptDetails(self) -> None:
        if not self.encrypted:
            sec_mgr = SecurityManager()
            self.description = sec_mgr.encryptData(self.description)
            self.encrypted = True
            print(f"[SECURITY] InPersonReport {self.reportID} details encrypted.")
        else:
            print(f"[SECURITY] InPersonReport {self.reportID} is already encrypted.")


class CyberBullyingReport(BullyingReport):
    def __init__(self, reportID: str, reportDate: datetime, description: str,
                 confidentialityLevel: ConfidentialityLevel, onlinePlatform: str,
                 reporter: 'Student' = None, evidence: list = None):
        super().__init__(reportID, reportDate, description, confidentialityLevel, reporter)
        self.onlinePlatform = onlinePlatform
        self.evidence = evidence if evidence is not None else []

    def validateReport(self) -> bool:
        return bool(self.description and self.onlinePlatform)

    def encryptDetails(self) -> None:
        if not self.encrypted:
            sec_mgr = SecurityManager()
            self.description = sec_mgr.encryptData(self.description)
            self.encrypted = True
            print(f"[SECURITY] CyberBullyingReport {self.reportID} details encrypted.")
        else:
            print(f"[SECURITY] CyberBullyingReport {self.reportID} is already encrypted.")

class School:
    _instance = None  

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(School, cls).__new__(cls)
            cls._instance.reports = []
            cls._instance.users = []
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance if cls._instance else cls()
        
    def __init__(self, schoolID: str, name: str, address: str):
        self.schoolID = schoolID
        self.name = name
        self.address = address
        self.users = []        # List of User objects
        self.reports = []      # List of BullyingReport objects

    def registerReport(self, report) -> None:
        self.reports.append(report)
        print(f"[REGISTER] Report {report.reportID} registered in {self.name}.")

class User(ABC):
    def __init__(self, userID: str, name: str, email: str, role: str, passwordHash: str):
        self.userID = userID
        self.name = name
        self.email = email
        self.role = role
        self.passwordHash = passwordHash

    @abstractmethod
    def login(self, password: str) -> bool:
        pass

class Student(User):
    def __init__(self, userID: str, name: str, email: str, grade: int, passwordHash: str):
        super().__init__(userID, name, email, "Student", passwordHash)
        self.grade = grade  

    def login(self, password: str) -> bool:
        return hash_password(password) == self.passwordHash

    def fileReport(self, report: 'BullyingReport') -> None:
        """Allows a student to file a bullying report."""

        school = School.get_instance() 
        if not isinstance(report, BullyingReport):
            print("[ERROR] Invalid report submission.")
            return

        report.reporter = self  # Assign the student as the reporter
        school.registerReport(report)  # Register report within the school system
        print(f"[SUCCESS] Report {report.reportID} submitted by {self.name}.")

class Teacher(User):
    def __init__(self, userID: str, name: str, email: str, passwordHash: str):
        super().__init__(userID, name, email, "Teacher", passwordHash)

    def login(self, password: str) -> bool:
        return hash_password(password) == self.passwordHash

    def reviewReport(self, report) -> None:
        print(f"\n[INFO] Teacher {self.name} is reviewing Report ID: {report.reportID}.")
        # For demonstration, update status if the report is new.
        if report.status == ReportStatus.NEW:
            report.status = ReportStatus.IN_PROGRESS
            print(f"[UPDATE] Report {report.reportID} status updated to IN_PROGRESS.")
        else:
            print(f"[INFO] Report {report.reportID} has already been processed.")
        # Encrypt the description if not already encrypted
        if not report.encrypted:
            report.encryptDetails()


class Administrator(User):
    def __init__(self, userID: str, name: str, email: str, passwordHash: str):
        super().__init__(userID, name, email, "Administrator", passwordHash)

    def login(self, password: str) -> bool:
        return hash_password(password) == self.passwordHash

    def assignStaff(self, report, available_teachers: list) -> None:
        """Assign, change, or remove a teacher from the report."""
        security_manager = SecurityManager()  

        if not security_manager.checkPermission(self, "assign_staff"):  
            print("Permission denied to assign staff.")
            return

        # Check if a staff is already assigned
        if hasattr(report, "assigned_teacher") and report.assigned_teacher:
            print(f"\n[INFO] Report {report.reportID} is already assigned to {report.assigned_teacher.name}.")
            print("1. Change Staff")
            print("2. Remove Staff")
            print("3. Back")

            choice = input("Select an option: ")

            if choice == "1":
                self._assignNewTeacher(report, available_teachers)
            elif choice == "2":
                report.assigned_teacher = None
                print(f"\n[UPDATE] Staff removed from Report {report.reportID}.")
            else:
                print("[INFO] Returning to previous menu.")
                return
        else:
            self._assignNewTeacher(report, available_teachers)

    def _assignNewTeacher(self, report, available_teachers: list) -> None:
        """Helper method to assign a new teacher to the report."""
        if not available_teachers:
            print("[ERROR] No available teachers to assign.")
            return

        print("\n--- Available Teachers ---")
        for idx, teacher in enumerate(available_teachers, start=1):
            print(f"{idx}. {teacher.name} ({teacher.email})") 

        try:
            sel = int(input("Select a teacher by number: "))
            if sel < 1 or sel > len(available_teachers):
                print("[ERROR] Invalid selection.")
                return
            selected_teacher = available_teachers[sel - 1]
        except ValueError:
            print("[ERROR] Invalid input; please enter a number.")
            return

        report.assigned_teacher = selected_teacher  
        print(f"\n[UPDATE] Administrator {self.name} assigned {selected_teacher.name} to report {report.reportID}.")

class SecurityManager:
    def checkPermission(self, user: "User", action: str) -> bool:
        permissions = {
            "file_report": ["Student"],
            "review_report": ["Teacher"],
            "assign_staff": ["Administrator"]
        }
        if action in permissions and user.role in permissions[action]:
            return True
        return False

    def encryptData(self, data: str) -> str:
        encoded_bytes = base64.b64encode(data.encode("utf-8"))
        return str(encoded_bytes, "utf-8")

    def decryptData(self, data: str) -> str:
        decoded_bytes = base64.b64decode(data.encode("utf-8"))
        return str(decoded_bytes, "utf-8")
    
def hash_password(password: str) -> str:
    """Compute a SHA-256 hash for the given password."""
    return hashlib.sha256(password.encode()).hexdigest()

from datetime import datetime

# Dummy Data Setup
school = School(schoolID="SCH001", name="BatStateU-The-NEU", address="Golden Country Homes, Brgy. Alangilan, Batangas City")
teacher1 = Teacher("T001", "Raffy Tulfo", "Raffy@teacher.com", passwordHash=hash_password("Raffy Tulfo in Action"))
teacher2 = Teacher("T002", "Erwin Tulfo", "Erwin@teacher.com", passwordHash=hash_password("Para sa mahirap"))
admin1 = Administrator("A001", "Cardo Dalisay", "Cardo@admin.com", passwordHash=hash_password("bengbeng"))
student1 = Student("S001", "Ben Gonzales", "Ben@student.com", grade=10, passwordHash=hash_password("yulo"))
student2 = Student("S002", "Jose Rizz Al", "Jose@student.com", grade=11, passwordHash=hash_password("NoliMeTangereLite"))
school.users.extend([teacher1, teacher2, admin1, student1, student2])

# Dummy Reports
inperson_report = InPersonReport(
    reportID="R001",
    reportDate=datetime.now(),
    description="A bullying incident near the school entrance.",
    confidentialityLevel=ConfidentialityLevel.CONFIDENTIAL,
    location="School Entrance",
)
cyber_report = CyberBullyingReport(
    reportID="R002",
    reportDate=datetime.now(),
    description="Online bullying on social media platform.",
    confidentialityLevel=ConfidentialityLevel.HIGHLY_CONFIDENTIAL,
    onlinePlatform="Instagram",
)
school.reports.extend([inperson_report, cyber_report])

def student_menu(student: Student, school: School):
    while True:
        print("\n--- Student Menu ---")
        print("1. File a bullying report")
        print("2. View my reports")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n--- Report Bullying ---")
            print("1. In-Person Bullying")
            print("2. Cyberbullying")
            report_type = input("Select report type: ")

            reportID = f"R{len(school.reports) + 1:03}"  # Generate a unique ID
            report_date = datetime.now()
            description = input("Enter report description: ")

            print("\nConfidentiality Levels:")
            print("1. Public")
            print("2. Confidential")
            print("3. Highly Confidential")
            conf_choice = input("Select confidentiality level: ")
            conf_level = {
                "1": ConfidentialityLevel.PUBLIC,
                "2": ConfidentialityLevel.CONFIDENTIAL,
                "3": ConfidentialityLevel.HIGHLY_CONFIDENTIAL
            }.get(conf_choice, ConfidentialityLevel.CONFIDENTIAL)

            if report_type == "1":
                location = input("Enter location of incident: ")
                report = InPersonReport(
                    reportID=reportID,
                    description=description,
                    reportDate=report_date,
                    confidentialityLevel=conf_level,
                    location=location,
                )
            elif report_type == "2":
                online_platform = input("Enter online platform (e.g., Facebook, Instagram): ")
                report = CyberBullyingReport(
                    reportID=reportID,
                    description=description,
                    reportDate=report_date,
                    confidentialityLevel=conf_level,
                    onlinePlatform=online_platform,
                )
            else:
                print("[ERROR] Invalid report type selection.")
                continue

            student.fileReport(report)  # File report through Student method
            print(f"[SUCCESS] Report {report.reportID} filed successfully.")

        elif choice == "2":
            print("\n--- My Filed Reports ---")
            student_reports = [r for r in school.reports if r.reporter == student]

            if not student_reports:
                print("[INFO] No reports filed yet.")
                continue

            for report in student_reports:
                print(f"Report ID: {report.reportID}, Type: {type(report).__name__}, Status: {report.status.value}")

        elif choice == "3":
            print("[INFO] Logging out...")
            break
        else:
            print("[WARN] Invalid choice. Please try again.")

def teacher_menu(teacher: Teacher, school: School, security_manager: SecurityManager):
    while True:
        print("\n--- Teacher Menu ---")
        print("1. Review an assigned bullying report")
        print("2. View all your assigned reports")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Filter reports assigned to this teacher
            assigned_reports = [report for report in school.reports if hasattr(report, "assigned_teacher") and report.assigned_teacher == teacher]
            if not assigned_reports:
                print("[INFO] No reports assigned to you for review.")
                continue

            print("\n--- Assigned Reports List ---")
            for idx, report in enumerate(assigned_reports, start=1):
                print(f"{idx}. Report ID: {report.reportID}, Type: {type(report).__name__}, Status: {report.status.value}")
            try:
                sel = int(input("Select a report number to review: "))
                if sel < 1 or sel > len(assigned_reports):
                    print("[ERROR] Invalid selection.")
                    continue
                selected_report = assigned_reports[sel - 1]
            except ValueError:
                print("[ERROR] Invalid input; please enter a number.")
                continue

            teacher.reviewReport(selected_report)
            view_details = input("\nDo you want to view the decrypted description? (y/n): ")
            if view_details.lower() == "y":
                decrypted = security_manager.decryptData(selected_report.description)
                print(f"Decrypted Description: {decrypted}")

        elif choice == "2":
            # Again, list only reports assigned to this teacher
            assigned_reports = [report for report in school.reports if hasattr(report, "assigned_teacher") and report.assigned_teacher == teacher]
            if not assigned_reports:
                print("[INFO] No reports assigned to you.")
                continue

            print("\n--- All Your Assigned Reports ---")
            for report in assigned_reports:
                print(f"Report ID: {report.reportID}, Type: {type(report).__name__}, Status: {report.status.value}")

        elif choice == "3":
            print("[INFO] Logging out...")
            break

        else:
            print("[WARN] Invalid choice. Please try again.")

def admin_menu(administrator: Administrator, school: School, security_manager: SecurityManager):
    available_teachers = [user for user in school.users if isinstance(user, Teacher)]  # Extract only Teachers

    while True:
        print("\n--- Administrator Menu ---")
        print("1. Assign staff")
        print("2. View all reports")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            if not school.reports:
                print("[INFO] No reports available to review.")
                continue

            reports_to_assign = [
                {
                    "Report ID": report.reportID,
                    "Type": type(report).__name__,
                    "Status": report.status.value,
                    "Assigned Teacher": getattr(report, "assigned_teacher", None).name if hasattr(report, "assigned_teacher") and report.assigned_teacher else "None"
                }
                for report in school.reports
            ]

            print("\n--- Reports List ---")
            for idx, report_info in enumerate(reports_to_assign, start=1):
                print(f"{idx}. Report ID: {report_info['Report ID']}, Type: {report_info['Type']}, Status: {report_info['Status']}, Assigned Staff: {report_info['Assigned Teacher']}")

            sel = input("Select a report number to assign a staff on the case: ")
            try:
                sel = int(sel)
                if sel < 1 or sel > len(reports_to_assign):
                    print("[ERROR] Invalid selection.")
                    continue
                selected_report = school.reports[sel - 1]  # Get the actual Report object
            except ValueError:
                print("[ERROR] Invalid input; please enter a number.")
                continue

            administrator.assignStaff(selected_report, available_teachers)

        elif choice == "2":
            reports_to_assign = [
                {
                    "Report ID": report.reportID,
                    "Type": type(report).__name__,
                    "Status": report.status.value,
                    "Assigned Teacher": getattr(report, "assigned_teacher", None).name if hasattr(report, "assigned_teacher") and report.assigned_teacher else "None"
                }
                for report in school.reports
            ]

            print("\n--- Reports List ---")
            for idx, report_info in enumerate(reports_to_assign, start=1):
                print(f"{idx}. Report ID: {report_info['Report ID']}, Type: {report_info['Type']}, Status: {report_info['Status']}, Assigned Staff: {report_info['Assigned Teacher']}")

        elif choice == "3":
            print("[INFO] Logging out...")
            break

        else:
            print("[WARN] Invalid choice. Please try again.")

    
def login_user(role_choice: str, school: School):
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    for user in school.users:
        if user.email.lower() == email.lower():
            if role_choice == "1" and isinstance(user, Student):
                if user.login(password):
                    print(f"\nLogin Successful! Welcome, {user.name}!")
                    return user
            elif role_choice == "2" and isinstance(user, Teacher):
                if user.login(password):
                    print(f"\nLogin Successful! Welcome, honorable sir {user.name}!")
                    return user
            elif role_choice == "3" and isinstance(user, Administrator):
                if user.login(password):
                    print(f"\nLogin Successful! Welcome, {user.name}!")
                    return user
    print("[ERROR] Authentication failed. Please check your credentials and role.")
    return None

def main():
    # Instantiate the security manager.
    security_manager = SecurityManager()

    # Main CLI loop.
    while True:
        print("\n=== Welcome to the School Bullying Report System ===")
        print("Select your role to log in:")
        print("1. Student")
        print("2. Teacher")
        print("3. Administrator")
        print("4. Quit")
        role_choice = input("Enter your choice: ").strip()

        if role_choice == "4":
            print("[INFO] Exiting system...")
            break

        user = login_user(role_choice, school)
        if user is None:
            continue

        if role_choice == "1":
            student_menu(user, school)
        elif role_choice == "2":
            teacher_menu(user, school, security_manager)
        elif role_choice == "3":
            admin_menu(user, school, security_manager)


if __name__ == "__main__":
    main()
