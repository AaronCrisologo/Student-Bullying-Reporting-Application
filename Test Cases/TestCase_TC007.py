import sys
sys.path.append('C:/Users/louis/OneDrive/Documents/Student-Bullying-Reporting-Application-main')  # Adjust to your local project path

from datetime import datetime
from SchoolClass import School
from Reports import InPersonReport, CyberBullyingReport, ConfidentialityLevel

def test_tc004_validate_incident_report_creation_and_storage():
    """
    Test Case TC007: Validate Incident Report Creation and Storage
    """

    # Step 0: Setup
    school = School("SCH001", "BatStateU-The-NEU", "Golden Country Homes, Brgy. Alangilan, Batangas City")
    school.reports.clear()  # Ensure clean state

    # Step 1: Create InPersonReport
    inperson_report = InPersonReport(
        reportID="R001",
        reportDate=datetime.now(),
        description="A bullying incident near the school entrance.",
        confidentialityLevel=ConfidentialityLevel.CONFIDENTIAL,
        location="School Entrance"
    )

    # Step 2: Create CyberBullyingReport
    cyber_report = CyberBullyingReport(
        reportID="R002",
        reportDate=datetime.now(),
        description="Online bullying on social media platform.",
        confidentialityLevel=ConfidentialityLevel.HIGHLY_CONFIDENTIAL,
        onlinePlatform="Instagram"
    )

    # Step 3: Add reports to school
    school.reports.extend([inperson_report, cyber_report])

    # Step 4: Assertions to verify correct storage
    assert len(school.reports) == 2, "[FAIL] Expected 2 reports in school."

    # Verify InPersonReport
    assert isinstance(school.reports[0], InPersonReport), "[FAIL] First report is not an InPersonReport."
    assert school.reports[0].reportID == "R001", "[FAIL] InPersonReport ID mismatch."
    assert school.reports[0].description == "A bullying incident near the school entrance.", "[FAIL] InPersonReport description mismatch."
    assert school.reports[0].location == "School Entrance", "[FAIL] InPersonReport location mismatch."
    assert school.reports[0].confidentialityLevel == ConfidentialityLevel.CONFIDENTIAL, "[FAIL] InPersonReport confidentiality mismatch."

    # Verify CyberBullyingReport
    assert isinstance(school.reports[1], CyberBullyingReport), "[FAIL] Second report is not a CyberBullyingReport."
    assert school.reports[1].reportID == "R002", "[FAIL] CyberBullyingReport ID mismatch."
    assert school.reports[1].description == "Online bullying on social media platform.", "[FAIL] CyberBullyingReport description mismatch."
    assert school.reports[1].onlinePlatform == "Instagram", "[FAIL] CyberBullyingReport platform mismatch."
    assert school.reports[1].confidentialityLevel == ConfidentialityLevel.HIGHLY_CONFIDENTIAL, "[FAIL] CyberBullyingReport confidentiality mismatch."

    print("[SUCCESS] Test Case TC004 passed: Both reports created and stored with correct classification.")

if __name__ == "__main__":
    test_tc004_validate_incident_report_creation_and_storage()
