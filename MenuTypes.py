from UserClasses import Teacher, Administrator, Student
from Reports import InPersonReport, CyberBullyingReport, ConfidentialityLevel
from SchoolClass import School
from DataSecurity import SecurityManager
from datetime import datetime

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
            school.reports.append(report)  # Add report to school's record
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
            view_details = input("Do you want to view the decrypted description? (y/n): ")
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
        print("2. Logout")
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
