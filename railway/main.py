import os
import sys
import fcntl
from models.train import Train
from management.admin import Admin, admin_cli
from management.user import UserManagement, user_cli
from storage.data_storage import DataStorage

LOCK_FILE = "/tmp/railway_app.lock"

def acquire_lock():
    lock_file = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("Another instance of the program is already running.")
        sys.exit(1)
    return lock_file

def release_lock(lock_file):
    fcntl.flock(lock_file, fcntl.LOCK_UN)
    lock_file.close()

def main():
    lock_file = acquire_lock()

    data_storage = DataStorage()
    admin = Admin[Train]()
    user_management = UserManagement()

    try:
        user_management.users = data_storage.load_user_data()
        admin._trains = data_storage.load_train_data()
        print("Data loaded successfully!")
    except Exception as e:
        print(f"Error loading data: {e}")

    print("Welcome to the Railway Booking System!")

    while True:
        os.system("clear")
        print("\nMain Menu")
        print("1. Admin access") 
        print("2. User access")
        print("3. Exit")

        choice_1 = input("\nEnter your choice: ").strip()

        if choice_1 == "1":
            try:
                admin_cli(admin)
            except Exception as e:
                print(f"Error in Admin Panel: {e}")

        elif choice_1 == "2":
            try:
                user_cli(admin, user_management)
            except Exception as e:
                print(f"Error in User Panel: {e}")

        elif choice_1 == "3":
            try:
                data_storage.save_train_data(admin)
                data_storage.save_user_data(user_management)
                print("Exiting the application. Goodbye!")
                break
            except Exception as e:
                print(f"Error saving data: {e}")
            break

        else:
            print("Invalid option. Please try again.")
        input("Press Enter to continue...")
    
    release_lock(lock_file)

if __name__ == "__main__":
    main()
