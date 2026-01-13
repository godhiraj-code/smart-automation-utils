import unittest
import time
from selenium.webdriver.common.by import By
from smart_automation.driver import SmartDriver

class TestSmartDriver(unittest.TestCase):
    def setUp(self):
        # Use headless mode for CI/CD friendly testing, or set to False to see the browser
        self.driver = SmartDriver("chrome", headless=True)

    def test_google_search(self):
        print("Executing Fluent API test...")
        self.driver.get("https://www.dhirajdas.dev") \
                   .click(By.XPATH, "//a[contains(text(), 'Home')]")
            
        print("Verifying page content...")
        if self.driver.find_element(By.XPATH, "//span[contains(text(), 'Intelligent')]"):
            self.assertTrue(True) 
        
        print("Test Passed with Fluent API!")

    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
