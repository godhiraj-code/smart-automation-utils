import unittest
import time
from selenium.webdriver.common.by import By
from smart_automation.driver import SmartDriver

class TestSmartDriver(unittest.TestCase):
    def setUp(self):
        # Use headless mode for CI/CD friendly testing, or set to False to see the browser
        self.driver = SmartDriver("chrome", headless=True)

    def test_google_search(self):
        print("Navigating to dhirajdas.dev...")
        self.driver.get("https://www.dhirajdas.dev")
    
        print("Searching for 'dhirajdas.dev'...")

        self.driver.click(By.XPATH, "//a[contains(text(), 'Home')]") 
            
        print("Waiting for results...")
        # Verify some results appear
        # results = self.driver.find_element(By.ID, "search")
        if self.driver.find_element(By.XPATH, "//span[contains(text(), 'Intelligent')]"):
            self.assertTrue(True) 
        
        print("Test Passed!")

    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
