import json
from typing import Dict, Union
from management.user import UserManagement,Users
from models.train import Train

class DataStorage:
    """
    A class for managing data persistence, including saving and loading
    user and train data to/from JSON files.
    """

    def __init__(self):
        self.data: Dict[str, Dict[str, Union[Train,Users]]] = {
            "users": {},  # Stores user data
            "trains": {},  # Stores train data
        }

    def save_user_data(self, user_management: UserManagement) -> None:
        """
        Save user data to a JSON file.

        Args:
            user_management (Any): An object containing user data in a `users` attribute.
        """
        self.data["users"] = user_management.users
        try:
            with open("user_data.json", "w") as f:
                json.dump(self.data["users"], f, indent=4)
            print("User data saved successfully.")
        except (IOError, OSError) as e:
            print(f"Error saving user data: {e}")

    def load_user_data(self) -> Dict[str, Users]:
        """
        Load user data from a JSON file.

        Returns:
            Dict[str, Any]: The loaded user data, or an empty dictionary if no data exists.
        """
        try:
            with open("user_data.json", "r") as f:
                self.data["users"] = json.load(f)
            print("User data loaded successfully.")
        except FileNotFoundError:
            print("No previous user data found. Returning an empty dictionary.")
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error loading user data: {e}")
        return self.data["users"]

    def save_train_data(self, train: Train) -> None:
        """
        Save train data to a JSON file.

        Args:
            train (Any): A Train object containing train details, including schedule and coaches.
        """
        try:
            self.data["trains"][train.train_id] = {
                "schedule": train._schedule,
                "coaches": {
                    coach_id: {
                        "total_seats": coach.total_seats,
                        "available_seats": coach.available_seats,
                        "coach_type": coach.coach_type,
                        "seat": coach._seat,
                    }
                    for coach_id, coach in train._coach.items()
                },
            }
            with open("train_data.json", "w") as f:
                json.dump(self.data["trains"], f, indent=4)
            print("Train data saved successfully.")
        except (IOError, OSError) as e:
            print(f"Error saving train data: {e}")

    def load_train_data(self) -> Dict[str, Train]:
        """
        Load train data from a JSON file.

        Returns:
            Dict[str, Any]: The loaded train data, or an empty dictionary if no data exists.
        """
        try:
            with open("train_data.json", "r") as f:
                self.data["trains"] = json.load(f)
            print("Train data loaded successfully.")
        except FileNotFoundError:
            print("No previous train data found. Returning an empty dictionary.")
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error loading train data: {e}")
        return self.data["trains"]
