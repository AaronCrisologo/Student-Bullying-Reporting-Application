from abc import ABC, abstractmethod
from Reports import BullyingReport  

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
        from DataSecurity import hash_password
        return hash_password(password) == self.passwordHash

    def fileReport(self, report: BullyingReport) -> None:
        """Allows a student to file a bullying report."""
        from School import School  

        school = School.get_instance()  # Assuming a singleton school instance
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
        from DataSecurity import hash_password
        return hash_password(password) == self.passwordHash

    def reviewReport(self, report) -> None:
        from Reports import ReportStatus
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


class Administrator(User):
    def __init__(self, userID: str, name: str, email: str, passwordHash: str):
        super().__init__(userID, name, email, "Administrator", passwordHash)

    def login(self, password: str) -> bool:
        from DataSecurity import hash_password
        return hash_password(password) == self.passwordHash

    def assignStaff(self, report, available_teachers: list[Teacher]) -> None:
        """Assign, change, or remove a teacher from the report."""
        from DataSecurity import SecurityManager  
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

    def _assignNewTeacher(self, report, available_teachers: list[Teacher]) -> None:
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
