import random
import string
import csv
import json
from .logger import logger

class DataGenerator:
    @staticmethod
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def random_email(domain="example.com"):
        return f"{DataGenerator.random_string(8)}@{domain}"

    @staticmethod
    def random_number(min_val=0, max_val=1000):
        return random.randint(min_val, max_val)

class DataProvider:
    @staticmethod
    def load_csv(filepath):
        """Loads data from a CSV file."""
        data = []
        try:
            with open(filepath, mode='r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            logger.warning(f"Data: Failed to load CSV {filepath}: {e}")
            return []

    @staticmethod
    def load_json(filepath):
        """Loads data from a JSON file."""
        try:
            with open(filepath, mode='r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Data: Failed to load JSON {filepath}: {e}")
            return []
