from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from UserClasses import Student
    from DataSecurity import SecurityManager

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
            from DataSecurity import SecurityManager
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
            from DataSecurity import SecurityManager
            sec_mgr = SecurityManager()
            self.description = sec_mgr.encryptData(self.description)
            self.encrypted = True
            print(f"[SECURITY] CyberBullyingReport {self.reportID} details encrypted.")
        else:
            print(f"[SECURITY] CyberBullyingReport {self.reportID} is already encrypted.")
