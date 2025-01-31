import os
from models.train import Train
from management.admin import Admin, admin_cli
from management.user import UserManagement, user_cli
from storage.data_storage import DataStorage

data_storage = DataStorage()

admin = Admin[Train]()
user_management = UserManagement()

try:
    user_management.users = data_storage.load_user_data()
    admin._trains = data_storage.load_train_data()
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")

def main():
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

if __name__ == "__main__":
    main()
