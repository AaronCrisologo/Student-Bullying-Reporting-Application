from datetime import datetime

from SchoolClass import School
from DataSecurity import hash_password
from UserClasses import Teacher, Administrator
from Reports import InPersonReport, CyberBullyingReport, ConfidentialityLevel

# Dummy Data Setup
school = School(schoolID="SCH001", name="BatStateU-The-NEU", address="Golden Country Homes, Brgy. Alangilan, Batangas City")
teacher1 = Teacher("T001", "Raffy Tulfo", "Raffy@teacher.com", passwordHash=hash_password("Raffy Tulfo in Action"))
teacher2 = Teacher("T002", "Erwin Tulfo", "Erwin@teacher.com", passwordHash=hash_password("Para sa mahirap"))
admin1 = Administrator("A001", "Cardo Dalisay", "Cardo@admin.com", passwordHash=hash_password("bengbeng"))
student1 = Student("S001", "Ben Gonzales", "benG@student.com", grade=10, passwordHash=hash_password("Bengbeng"))
student2 = Student("S002", "Jose Rizz Al", "JoseA@student.com", grade=11, passwordHash=hash_password("NoliMeTangereLite"))
school.users.extend([teacher1, teacher2, admin1])

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
