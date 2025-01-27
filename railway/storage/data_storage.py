import json
from typing import Dict, Union
from management.user import UserManagement,Users
from models.train import Train

class DataStorage:
    
    def __init__(self):
        self.data: Dict[str, Dict[str, Union[Train,Users]]] = {
            "users": {},  # Stores user data
            "trains": {},  # Stores train data
        }

    def save_user_data(self, user_management: UserManagement) -> None:
        self.data["users"] = {user_id: user.__dict__ for user_id, user in user_management.users.items()}
        try:
            with open("user_data.json", "w") as f:
                json.dump(self.data["users"], f, indent=4)
            print("User data saved successfully.")
        except (IOError, OSError) as e:
            print(f"Error saving user data: {e}")


    def load_user_data(self) -> Dict[str, Users]:
        ...

    def save_train_data(self, train: Train) -> None:
        ...

    def load_train_data(self) -> Dict[str, Train]:
        ...
