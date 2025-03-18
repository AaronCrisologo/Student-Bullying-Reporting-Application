from datetime import datetime

from SchoolClass import School
from PassHash import hash_password
from UserClasses import Teacher
from Reports import InPersonReport, CyberBullyingReport, ConfidentialityLevel

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