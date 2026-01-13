import unittest
from selenium.webdriver.common.by import By
from smart_automation import SmartDriver, BasePage

class HomePage(BasePage):
    def __init__(self, driver: SmartDriver):
        super().__init__(driver)
        self.url = "https://www.dhirajdas.dev"

    def navigate_home(self):
        return self.click(By.XPATH, "//a[contains(text(), 'Home')]")

class TestPOM(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = SmartDriver(headless=True)

    def test_pom_navigation(self):
        home_page = HomePage(self.driver)
        home_page.open().navigate_home()
        
        self.assertTrue(
            self.driver.find_element(By.XPATH, "//span[contains(text(), 'Intelligent')]")
        )

    def tearDown(self) -> None:
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
