from appium import webdriver as mobile_webdriver
from appium.options.common import AppiumOptions
from .logger import logger
from .exceptions import DriverError
from .config import Config

class SmartMobileDriver:
    def __init__(self, config_path=None, **kwargs):
        """
        Initializes the SmartMobileDriver for Appium.
        """
        self.config = Config(config_path)
        
        # Override with kwargs if provided
        for key, value in kwargs.items():
            if key in self.config.config:
                self.config.config[key] = value

        self.caps = self.config.get("mobile_caps", {})
        self.appium_server_url = self.config.get("appium_server_url", "http://localhost:4723/wd/hub")
        
        self.driver = self._init_driver()
        logger.info(f"SmartMobileDriver initialized targeting {self.caps.get('platformName')}")

    def _init_driver(self):
        try:
            options = AppiumOptions()
            options.load_capabilities(self.caps)
            return mobile_webdriver.Remote(self.appium_server_url, options=options)
        except Exception as e:
            logger.error(f"Failed to initialize mobile driver: {e}")
            raise DriverError(f"Mobile Driver initialization failed: {e}")

    def quit(self):
        logger.info("Quitting SmartMobileDriver")
        self.driver.quit()

    def __getattr__(self, name):
        return getattr(self.driver, name)
