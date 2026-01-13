# Smart Automation Utils

A professional-grade Python framework designed for automation developers working with Selenium and Appium. `smart-automation-utils` simplifies the complexity of web and mobile automation with built-in reliability, logging, and performance monitoring.

## 🚀 Key Features

- **SmartDriver**: Enhanced Selenium wrapper with automatic waits, retry logic, and fallback mechanisms.
- **SmartMobileDriver**: Full Appium support for cross-platform mobile testing.
- **Visual Debugging**: Automatic screenshot capture on failure and element highlighting.
- **Reliability Foundation**: Structured logging, custom exceptions, and flexible YAML/JSON configuration.
- **Performance & Monitoring**: Real-time tracking of execution time and memory usage.
- **Data Utilities**: Built-in test data generators and CSV/JSON data providers.
- **Extensibility**: Plugin architecture and Event Observer pattern for customized driver behavior.
- **CI/CD Ready**: Dockerized testing support and GitHub Actions integration.

## 📦 Installation

```bash
pip install smart-automation-utils
```

## 🛠 Usage

### Basic Web Automation
```python
from smart_automation import SmartDriver
from selenium.webdriver.common.by import By

# Initialized with default_config.json or environment variables
driver = SmartDriver()

try:
    driver.get("https://www.example.com")
    driver.click(By.ID, "submit-button")
    driver.send_keys(By.NAME, "username", "admin")
finally:
    driver.quit()
```

### Mobile Automation
```python
from smart_automation import SmartMobileDriver

caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "emulator-5554",
    "app": "/path/to/app.apk"
}

driver = SmartMobileDriver(mobile_caps=caps)
# Standard Appium/Selenium commands
driver.quit()
```

### Performance Monitoring
```python
from smart_automation import monitor

monitor.start_timer("login_flow")
# ... perform login ...
monitor.stop_timer("login_flow")
monitor.log_memory_usage()
```

### Data Generation
```python
from smart_automation import DataGenerator

email = DataGenerator.random_email()
password = DataGenerator.random_string(12)
```

## ⚙️ Configuration

The framework supports `SMART_AUTO_` prefixed environment variables or a `config.json` file.

```json
{
    "browser": "chrome",
    "timeout": 15,
    "headless": true,
    "log_level": "INFO"
}
```

## 🧪 Testing

Run the comprehensive test suite with:
```bash
python -m unittest discover tests
```

---
Built with ❤️ for automation engineers.
