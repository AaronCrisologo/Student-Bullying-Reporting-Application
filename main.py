# Main program entry point
def main():
    print("Welcome to the School Bullying Report System.\n")

    # Let the user choose a role for a session.
    while(True):
        print("Select your role:")
        print("1. Student")
        print("2. Teacher")
        print("3. Administrator")
        print("4. Exit")
        role_choice = input("Enter the number corresponding to your role: ").strip()
        if role_choice == "1":
            print(f"\nLogged in as Student\n")
        elif role_choice == "2":
            print(f"\nLogged in as Teacher\n")
        elif role_choice == "3":
            print(f"\nLogged in as Administrator\n")
        elif role_choice == "4":
            print(f"\nExiting Program\n")
            break
        else:
            print("Invalid role selection. Please try again.")

if __name__ == "__main__":
    main()