import base64
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


# ----------------------- Enumerations -----------------------

class ReportStatus(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class ConfidentialityLevel(Enum):
    PUBLIC = "PUBLIC"
    CONFIDENTIAL = "CONFIDENTIAL"
    HIGHLY_CONFIDENTIAL = "HIGHLY_CONFIDENTIAL"


# ----------------------- Utility Functions -----------------------

def hash_password(password: str) -> str:
    """Compute a SHA-256 hash for the given password."""
    return hashlib.sha256(password.encode()).hexdigest()


# ----------------------- Security Manager -----------------------

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


# ----------------------- User Classes -----------------------

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


class Teacher(User):
    def __init__(self, userID: str, name: str, email: str, passwordHash: str):
        super().__init__(userID, name, email, "Teacher", passwordHash)

    def login(self, password: str) -> bool:
        return hash_password(password) == self.passwordHash

    def reviewReport(self, report: "BullyingReport") -> None:
        print(f"[INFO] Teacher {self.name} is reviewing Report ID: {report.reportID}.")
        # For demonstration, update status if the report is new.
        if report.status == ReportStatus.NEW:
            report.status = ReportStatus.IN_PROGRESS
            print(f"[UPDATE] Report {report.reportID} status updated to IN_PROGRESS.")
        else:
            print(f"[INFO] Report {report.reportID} has already been processed.")
        # Encrypt the description if not already encrypted
        if not report.encrypted:
            report.encryptDetails()


# class Administrator(User):


# ----------------------- Report Classes -----------------------

class BullyingReport(ABC):
    def __init__(self, reportID: str, reportDate: datetime, description: str,
                 confidentialityLevel: ConfidentialityLevel, reporter: Student = None):
        self.reportID = reportID
        self.description = description
        self.status = ReportStatus.NEW
        self.encrypted = False

    @abstractmethod
    def validateReport(self) -> bool:
        pass

    @abstractmethod
    def encryptDetails(self) -> None:
        pass


class InPersonReport(BullyingReport):
    def __init__(self, reportID: str, reportDate: datetime, description: str,
                 confidentialityLevel: ConfidentialityLevel, location: str,
                 reporter: Student = None, witnesses: list = None):
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
                 reporter: Student = None, evidence: list = None):
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


# ----------------------- School -----------------------

class School:
    def __init__(self, schoolID: str, name: str, address: str):
        self.schoolID = schoolID
        self.name = name
        self.address = address
        self.users = []        # List of User objects
        self.reports = []      # List of BullyingReport objects


# ----------------------- CLI Menus -----------------------
def teacher_menu(teacher: Teacher, school: School, security_manager: SecurityManager):
    while True:
        print("\n--- Teacher Menu ---")
        print("1. Review a bullying report")
        print("2. View all reports")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            if not school.reports:
                print("[INFO] No reports available to review.")
                continue

            print("\n--- Reports List ---")
            reports_to_review = []
            for idx, report in enumerate(school.reports, start=1):
                print(f"{idx}. Report ID: {report.reportID}, Type: {type(report).__name__}, Status: {report.status.value}")
                reports_to_review.append(report)
            sel = input("Select a report number to review: ")
            try:
                sel = int(sel)
                if sel < 1 or sel > len(reports_to_review):
                    print("[ERROR] Invalid selection.")
                    continue
                selected_report = reports_to_review[sel - 1]
            except ValueError:
                print("[ERROR] Invalid input; please enter a number.")
                continue

            teacher.reviewReport(selected_report)
            view_details = input("Do you want to view the decrypted description? (y/n): ")
            if view_details.lower() == "y":
                decrypted = security_manager.decryptData(selected_report.description)
                print(f"Decrypted Description: {decrypted}")
        elif choice == "2":
            print("\n--- All Reports ---")
            for report in school.reports:
                print(f"Report ID: {report.reportID}, Type: {type(report).__name__}, Status: {report.status.value}")
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
            # if role_choice == "1" and isinstance(user, Student):
            #     if user.login(password):
            #         return user
            if role_choice == "2" and isinstance(user, Teacher):
                if user.login(password):
                    print(f"\nLogin Successful! Welcome, honorable sir {user.name}!")
                    return user
            # elif role_choice == "3" and isinstance(user, Administrator):
            #     if user.login(password):
            #         return user
    print("[ERROR] Authentication failed. Please check your credentials and role.")
    return None


# ----------------------- Main Application -----------------------

def main():
    # Instantiate the security manager.
    security_manager = SecurityManager()

    # Dummy Data Setup
    school = School(schoolID="SCH001", name="Springfield High", address="742 Evergreen Terrace")
    teacher1 = Teacher("T001", "Raffy Tulfo", "Raffy@teacher.com", passwordHash=hash_password("Raffy Tulfo in Action"))
    teacher2 = Teacher("T002", "Erwin Tulfo", "Erwin@teacher.com", passwordHash=hash_password("06-10-1963"))
    school.users.extend([teacher1, teacher2])

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
            print("Going to student menu...")
        elif role_choice == "2":
            teacher_menu(user, school, security_manager)
        elif role_choice == "3":
            print("Going to admin menu...")


if __name__ == "__main__":
    main()