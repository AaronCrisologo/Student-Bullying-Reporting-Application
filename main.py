from DummyData import school
from MenuTypes import teacher_menu, login_user, admin_menu
from DataSecurity import SecurityManager

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
            print("Going to student_menu()...")
        elif role_choice == "2":
            teacher_menu(user, school, security_manager)
        elif role_choice == "3":
            admin_menu(user, school, security_manager)


if __name__ == "__main__":
    main()