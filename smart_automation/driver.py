from typing import Optional, Any, Dict, List, TypeVar, Self
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from .utils import highlight_element, capture_screenshot
from .logger import logger, setup_logger
from .exceptions import DriverError, ElementError, TimeoutError
from .config import Config

T = TypeVar('T', bound='SmartDriver')

class SmartDriver:
    def __init__(self, config_path: Optional[str] = None, **kwargs: Any) -> None:
        """
        Initializes the SmartDriver with Enterprise-grade configurations.
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

        self.browser_name: str = self.config.browser.lower()
        self.timeout: int = self.config.timeout
        self.driver: webdriver.Remote = self._init_driver(self.config.headless)
        self.wait: WebDriverWait = WebDriverWait(self.driver, self.timeout)
        
        from .plugins import PluginManager
        self.plugin_manager: PluginManager = PluginManager(self)
        
        logger.info(f"Enterprise SmartDriver initialized for {self.browser_name} (headless={self.config.headless})")

    def _init_driver(self, headless: bool) -> webdriver.Remote:
        try:
            proxy = self.config.get("proxy")
            if self.browser_name == "chrome":
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument("--headless")
                    # Linux-specific flags for CI/Docker environments
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    options.add_argument("--disable-gpu")
                if proxy:
                    options.add_argument(f'--proxy-server={proxy}')
                
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
            
            elif self.browser_name == "firefox":
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                
                service = FirefoxService(GeckoDriverManager().install())
                if proxy:
                    options.set_preference("network.proxy.type", 1)
                    options.set_preference("network.proxy.http", proxy.split(':')[0])
                    options.set_preference("network.proxy.http_port", int(proxy.split(':')[1]))
                return webdriver.Firefox(service=service, options=options)
            else:
                raise DriverError(f"Unsupported browser: {self.browser_name}")
        except Exception as e:
            logger.error(f"Failed to initialize driver: {e}")
            raise DriverError(f"Driver initialization failed: {e}")

    def get(self, url: str) -> Self:
        """Navigates to a URL. Supports Fluent API chaining."""
        logger.info(f"Navigating to: {url}")
        try:
            self.driver.get(url)
            return self
        except Exception as e:
            logger.error(f"Navigation to {url} failed: {e}")
            raise DriverError(f"Navigation failed: {e}")

    def find_element(self, by: str, value: str, highlight: bool = True) -> Optional[WebElement]:
        """Finds an element with built-in retry and visual logging."""
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
            sanitized_value = "".join([c if c.isalnum() else "_" for c in value[:10]])
            capture_screenshot(self.driver, filename_prefix=f"not_found_{sanitized_value}")
            return None

    def add_cookie(self, name: str, value: str, **kwargs: Any) -> Self:
        """Add a cookie. Supports Fluent API."""
        cookie = {'name': name, 'value': value}
        cookie.update(kwargs)
        self.driver.add_cookie(cookie)
        logger.info(f"Added cookie: {name}={value}")
        return self

    def delete_all_cookies(self) -> Self:
        """Deletes all cookies. Supports Fluent API."""
        self.driver.delete_all_cookies()
        logger.info("Deleted all cookies")
        return self

    def scroll_to_element(self, element: WebElement) -> Self:
        """Scrolls to element. Supports Fluent API."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return self

    def click(self, by: str, value: str) -> Self:
        """Clicks an element with event dispatching, result tracking, and stability check."""
        from .events import dispatcher
        from .reporting import reporter
        import time
        
        if self.config.get("waitless_enabled"):
            try:
                import waitless
                waitless.stabilize(self.driver)
            except Exception as e:
                logger.warning(f"Waitless stabilization skipped: {e}")

        start_time = time.time()
        element = self.find_element(by, value)
        if element:
            try:
                self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                logger.info(f"Clicked: {by}={value}")
                dispatcher.dispatch("click", {"by": by, "value": value})
                reporter.add_result(f"Click: {by}={value}", "PASS", duration=time.time()-start_time)
                return self
            except Exception as e:
                logger.error(f"Click failed for {by}={value}: {e}")
                reporter.add_result(f"Click: {by}={value}", "FAIL", message=str(e), duration=time.time()-start_time)
                raise ElementError(f"Click failed: {e}")
        else:
             reporter.add_result(f"Click: {by}={value}", "FAIL", message="Not found", duration=time.time()-start_time)
             return self

    def send_keys(self, by: str, value: str, text: str) -> Self:
        """Sends keys with result tracking and stability check. Supports Fluent API."""
        from .events import dispatcher
        from .reporting import reporter
        import time

        if self.config.get("waitless_enabled"):
            try:
                import waitless
                waitless.stabilize(self.driver)
            except Exception as e:
                logger.warning(f"Waitless stabilization skipped: {e}")

        start_time = time.time()
        element = self.find_element(by, value)
        if element:
            try:
                element.clear()
                element.send_keys(text)
                logger.info(f"Sent keys to {by}={value}")
                dispatcher.dispatch("send_keys", {"by": by, "value": value})
                reporter.add_result(f"Send Keys: {by}={value}", "PASS", duration=time.time()-start_time)
                return self
            except Exception as e:
                logger.error(f"Send keys failed for {by}={value}: {e}")
                reporter.add_result(f"Send Keys: {by}={value}", "FAIL", message=str(e), duration=time.time()-start_time)
                raise ElementError(f"Send keys failed: {e}")
        else:
            reporter.add_result(f"Send Keys: {by}={value}", "FAIL", message="Not found", duration=time.time()-start_time)
            return self

    def stabilize(self) -> Self:
        """Manually trigger waitless stabilization."""
        try:
            import waitless
            waitless.stabilize(self.driver)
        except Exception as e:
            logger.warning(f"Fail to stabilize: {e}")
        return self

    def quit(self) -> None:
        """Quits the driver and generates final report."""
        logger.info("Terminating Enterprise SmartDriver session")
        if hasattr(self, 'plugin_manager'):
            self.plugin_manager.notify_teardown()
        from .reporting import reporter
        reporter.generate_report()
        self.driver.quit()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.driver, name)
