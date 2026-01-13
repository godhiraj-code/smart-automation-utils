from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException
from .utils import highlight_element
from .logger import logger, setup_logger
from .exceptions import DriverError, ElementError, TimeoutError
from .config import Config

class SmartDriver:
    def __init__(self, config_path=None, **kwargs):
        """
        Initializes the SmartDriver.
        
        Args:
            config_path: Path to a JSON config file.
            **kwargs: Overrides for configuration (e.g., browser_name, timeout, headless).
                     Supports legacy positional arguments if config_path is a string like 'chrome'.
        """
        # Backwards compatibility for positional browser_name
        if config_path and not config_path.endswith('.json') and config_path in ['chrome', 'firefox', 'edge']:
            kwargs['browser'] = config_path
            config_path = None

        self.config = Config(config_path)
        
        # Override with kwargs if provided
        for key, value in kwargs.items():
            if key in self.config.config:
                self.config.config[key] = value

        # Re-setup logger based on config
        setup_logger(
            log_level=self.config.log_level,
            log_file=self.config.log_file_path if self.config.log_to_file else None
        )

        self.browser_name = self.config.browser.lower()
        self.timeout = self.config.timeout
        self.driver = self._init_driver(self.config.headless)
        self.wait = WebDriverWait(self.driver, self.timeout)
        
        from .plugins import PluginManager
        self.plugin_manager = PluginManager(self)
        
        logger.info(f"SmartDriver initialized for {self.browser_name} (headless={self.config.headless})")

    def _init_driver(self, headless):
        try:
            proxy = self.config.get("proxy")
            if self.browser_name == "chrome":
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument("--headless")
                if proxy:
                    options.add_argument(f'--proxy-server={proxy}')
                return webdriver.Chrome(options=options)
            elif self.browser_name == "firefox":
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                if proxy:
                    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
                    firefox_capabilities['proxy'] = {
                        "proxyType": "manual",
                        "httpProxy": proxy,
                        "ftpProxy": proxy,
                        "sslProxy": proxy
                    }
                    return webdriver.Firefox(options=options, desired_capabilities=firefox_capabilities)
                return webdriver.Firefox(options=options)
            else:
                raise DriverError(f"Unsupported browser: {self.browser_name}")
        except Exception as e:
            logger.error(f"Failed to initialize driver: {e}")
            raise DriverError(f"Driver initialization failed: {e}")

    def get(self, url):
        logger.info(f"Navigating to: {url}")
        try:
            self.driver.get(url)
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise DriverError(f"Navigation failed: {e}")

    def find_element(self, by, value, highlight=True):
        try:
            logger.debug(f"Searching for element: {by}={value}")
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            if highlight:
                highlight_element(self.driver, element, duration=0.5)
            return element
        except SeleniumTimeoutException:
            msg = f"Element not found within {self.timeout}s: {by}={value}"
            logger.error(msg)
            from .utils import capture_screenshot
            # Sanitize filename for Windows
            sanitized_value = "".join([c if c.isalnum() else "_" for c in value[:10]])
            capture_screenshot(self.driver, filename_prefix=f"not_found_{sanitized_value}")
            return None

    def add_cookie(self, name, value, **kwargs):
        """Add a cookie to the current session."""
        cookie = {'name': name, 'value': value}
        cookie.update(kwargs)
        self.driver.add_cookie(cookie)
        logger.info(f"Added cookie: {name}={value}")

    def get_cookies(self):
        """Returns all cookies."""
        return self.driver.get_cookies()

    def delete_all_cookies(self):
        """Deletes all cookies."""
        self.driver.delete_all_cookies()
        logger.info("Deleted all cookies")

    def scroll_to_element(self, element):
        """Scrolls to the specified element."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.debug("Scrolled to element")

    def set_page_load_timeout(self, seconds):
        """Sets the amount of time to wait for a page load to complete."""
        self.driver.set_page_load_timeout(seconds)
        logger.info(f"Page load timeout set to {seconds}s")

    def is_visible(self, by, value):
        """Checks if an element is visible."""
        try:
            return self.driver.find_element(by, value).is_displayed()
        except:
            return False

    def click(self, by, value):
        from .events import dispatcher
        from .reporting import reporter
        import time
        start_time = time.time()
        element = self.find_element(by, value)
        if element:
            try:
                self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                logger.info(f"Clicked element: {by}={value}")
                dispatcher.dispatch("click", {"by": by, "value": value})
                reporter.add_result(f"Click: {by}={value}", "PASS", duration=time.time()-start_time)
            except Exception as e:
                logger.error(f"Failed to click element {by}={value}: {e}")
                reporter.add_result(f"Click: {by}={value}", "FAIL", message=str(e), duration=time.time()-start_time)
                raise ElementError(f"Click failed: {e}")
        else:
             reporter.add_result(f"Click: {by}={value}", "FAIL", message="Element not found", duration=time.time()-start_time)

    def send_keys(self, by, value, text):
        from .events import dispatcher
        from .reporting import reporter
        import time
        start_time = time.time()
        element = self.find_element(by, value)
        if element:
            try:
                element.clear()
                element.send_keys(text)
                logger.info(f"Sent keys to {by}={value}: {text}")
                dispatcher.dispatch("send_keys", {"by": by, "value": value, "text": text})
                reporter.add_result(f"Send Keys: {by}={value}", "PASS", duration=time.time()-start_time)
            except Exception as e:
                logger.error(f"Failed to send keys to {by}={value}: {e}")
                reporter.add_result(f"Send Keys: {by}={value}", "FAIL", message=str(e), duration=time.time()-start_time)
                raise ElementError(f"Send keys failed: {e}")
        else:
            reporter.add_result(f"Send Keys: {by}={value}", "FAIL", message="Element not found", duration=time.time()-start_time)

    def inspect_element(self, by, value):
        """Highlights an element for debugging purposes."""
        logger.info(f"Inspecting element: {by}={value}")
        element = self.find_element(by, value, highlight=True)
        if element:
            logger.info("Element found and highlighted.")
        else:
            logger.warning("Element not found for inspection.")

    def quit(self):
        logger.info("Quitting SmartDriver")
        if hasattr(self, 'plugin_manager'):
            self.plugin_manager.notify_teardown()
        
        from .reporting import reporter
        reporter.generate_report()
        
        self.driver.quit()

    def __getattr__(self, name):
        return getattr(self.driver, name)
