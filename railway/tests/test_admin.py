import sys
sys.path.append("./")
import unittest
from unittest.mock import patch
from management.admin import Admin
from models.train import Train

class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.admin = Admin[Train]()

    def test_add_train(self):
        with patch('builtins.input', side_effect=["T1", "Express", "Station1", "Station2"]):
            result = self.admin.add_train()
        self.assertTrue(result)
        self.assertIn("T1", self.admin._trains)
        
    def test_add_train_with_existing_id(self):
        with patch('builtins.input', side_effect=["T1", "Express", "Station1", "Station2"]):
            first_result = self.admin.add_train()
        with patch('builtins.input', side_effect=["T1", "local", "Station3", "Station4"]):
            second_result = self.admin.add_train()
        self.assertTrue(first_result)
        self.assertFalse(second_result)

    def test_remove_train(self):
        with patch('builtins.input', side_effect=["T1", "Express", "Station1", "Station2"]):
            self.admin.add_train()
        with patch('builtins.input', side_effect=["T1"]):
            result = self.admin.remove_train()
        self.assertTrue(result)
        self.assertNotIn("T1", self.admin._trains)

    def test_remove_train_with_booked_tickets(self):
        with patch('builtins.input', side_effect=["T1", "Express", "Station1", "Station2"]):
            self.admin.add_train()

        train = self.admin._trains["T1"]
        
        with patch.object(train, 'available_tickets', return_value=90),\
            patch.object(train, 'total_tickets', return_value=100):

            with patch('builtins.input', side_effect=["T1", "n"]):
                result = self.admin.remove_train()
            self.assertFalse(result)
            self.assertIn("T1", self.admin._trains)

            with patch('builtins.input', side_effect=["T1", "y"]):
                result = self.admin.remove_train()
            self.assertTrue(result)
            self.assertNotIn("T1", self.admin._trains)

    def test_remove_nonexistent_train(self):
        with patch('builtins.input', side_effect=["T1"]):
            result = self.admin.remove_train()
        self.assertFalse(result)

    def test_list_trains(self):
        with patch('builtins.input', side_effect=["T1", "Express", "Station1", "Station2"]):
            self.admin.add_train()
        with patch('builtins.input', side_effect=["T2", "Local", "Station3", "Station4"]):
            self.admin.add_train()
        result=self.admin.list_trains()
        self.assertTrue(result)

    def test_get_train(self):
        with patch('builtins.input', side_effect=["T1", "Express", "Station1", "Station2"]):
            self.admin.add_train()
        with patch('builtins.input', side_effect=["T1"]):
            train = self.admin.get_train()
        self.assertIsNotNone(train)
        self.assertEqual(train.train_id, "T1")
        self.assertEqual(train.train_name, "Express")

    def test_get_nonexistent_train(self):
        with patch('builtins.input', side_effect=["T1"]):
            train= self.admin.get_train()
        self.assertIsNone(train)

if __name__ == '__main__':
    unittest.main()