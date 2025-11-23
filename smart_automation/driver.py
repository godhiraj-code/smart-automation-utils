from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .utils import highlight_element

class SmartDriver:
    def __init__(self, browser_name="chrome", timeout=10, headless=False):
        self.browser_name = browser_name.lower()
        self.timeout = timeout
        self.driver = self._init_driver(headless)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def _init_driver(self, headless):
        if self.browser_name == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            return webdriver.Chrome(options=options)
        elif self.browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            return webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {self.browser_name}")

    def get(self, url):
        self.driver.get(url)

    def find_element(self, by, value, highlight=True):
        try:
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            if highlight:
                highlight_element(self.driver, element, duration=0.5)
            return element
        except TimeoutException:
            print(f"Element not found: {by}={value}")
            return None

    def click(self, by, value):
        element = self.find_element(by, value)
        if element:
            self.wait.until(EC.element_to_be_clickable((by, value)))
            element.click()

    def send_keys(self, by, value, text):
        element = self.find_element(by, value)
        if element:
            element.clear()
            element.send_keys(text)

    def quit(self):
        self.driver.quit()

    def __getattr__(self, name):
        # Delegate calls to the underlying driver if not found in SmartDriver
        return getattr(self.driver, name)
