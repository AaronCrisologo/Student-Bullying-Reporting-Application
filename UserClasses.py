from abc import ABC, abstractmethod
from PassHash import hash_password

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

    def reviewReport(self, report) -> None:  # Removed type annotation to avoid circular reference
        # Local import to resolve circular dependency
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


# class Administrator(User):