from models.train import Train
from management.admin import Admin, admin_cli
from management.user import UserManagement, user_cli
#from storage.data_storage import DataStorage

#data_storage = DataStorage()

admin = Admin[Train]()
user_management = UserManagement()

#user_management.users = data_storage.load_user_data()
#admin._trains = data_storage.load_train_data()

def main():
    print("Welcome to the Railway Booking System!")

    while True:
        print("\nMain Menu")
        print("1. Admin access") 
        print("2. User access")
        print("3. Exit")

        choice_1 = input("Enter your choice: ")

        if choice_1 == "1":
            admin_cli(admin)

        elif choice_1 == "2":
            user_cli(admin, user_management)

        elif choice_1 == "3":
           # data_storage.save_train_data(admin)
           # data_storage.save_user_data(user_management)
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
