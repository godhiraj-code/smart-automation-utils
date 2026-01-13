import unittest
from smart_automation import DataGenerator, DataProvider

class TestDataUtilities(unittest.TestCase):
    def test_random_string(self):
        s = DataGenerator.random_string(10)
        self.assertEqual(len(s), 10)
        self.assertTrue(s.isalnum())

    def test_random_email(self):
        email = DataGenerator.random_email("test.com")
        self.assertTrue(email.endswith("@test.com"))
        self.assertIn("@", email)

    def test_data_provider_json_fallback(self):
        # Test non-existent file
        data = DataProvider.load_json("non_existent.json")
        self.assertEqual(data, [])

if __name__ == "__main__":
    unittest.main()
