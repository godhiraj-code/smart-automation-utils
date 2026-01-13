from typing import Any, Optional
from selenium.webdriver.common.by import By
from .driver import SmartDriver

class BasePage:
    """
    Enterprise Base Page class for Page Object Model (POM).
    """
    def __init__(self, driver: SmartDriver):
        self.driver = driver
        self.url: Optional[str] = None

    def open(self) -> 'BasePage':
        if self.url:
            self.driver.get(self.url)
        return self

    def is_loaded(self) -> bool:
        """Override this in subclasses to verify page load."""
        return True

    def find_element(self, by: str, value: str):
        return self.driver.find_element(by, value)

    def click(self, by: str, value: str) -> 'BasePage':
        self.driver.click(by, value)
        return self

    def send_keys(self, by: str, value: str, text: str) -> 'BasePage':
        self.driver.send_keys(by, value, text)
        return self
