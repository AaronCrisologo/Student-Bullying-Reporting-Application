from UserClasses import Teacher
from SchoolClass import School
from DataSecurity import SecurityManager

# def student_menu():

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

# def admin_menu():

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