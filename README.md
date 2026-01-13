# Smart Automation Utils v0.2.0

An Enterprise-grade Python framework for robust web and mobile automation. `smart-automation-utils` transforms standard Selenium/Appium into a stable, fluent, and highly observable automation engine.

## 🚀 Enterprise Features

- **Fluent API**: Chain actions for readable and concise test scripts. 
- **Flakiness Elimination**: Built-in **Waitless** integration for intelligent UI stabilization.
- **Page Object Model (POM)**: Built-in `BasePage` and `SmartDriver` integration for scalable architecture.
- **Zero-Config Drivers**: Automated driver management via `webdriver-manager`.
- **Glow Reporting**: High-fidelity test diagnostics with `pytest-glow-report`.
- **Hybrid Support**: Seamlessly switch between Web (Selenium) and Mobile (Appium).
- **Proactive Debugging**: Automatic screenshots on failure + element highlighting.
- **Performance Intelligence**: Integrated memory and execution time monitoring.

## 📦 Installation

```bash
pip install smart-automation-utils
```

## 🛠 Usage

### Fluent & Professional API
```python
from smart_automation import SmartDriver
from selenium.webdriver.common.by import By

# Zero-config initialization
driver = SmartDriver(browser="chrome", headless=True)

driver.get("https://www.dhirajdas.dev") \
      .click(By.XPATH, "//a[text()='Home']") \
      .send_keys(By.NAME, "search", "Automation") \
      .quit()
```

### Page Object Model (POM)
```python
from smart_automation import SmartDriver, BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    def login(self, user, pwd):
        return self.send_keys(By.ID, "user", user) \
                   .send_keys(By.ID, "pass", pwd) \
                   .click(By.ID, "login-btn")

driver = SmartDriver()
login_page = LoginPage(driver)
login_page.open().login("admin", "secret")
```

### Performance & Data
```python
from smart_automation import monitor, DataGenerator

monitor.start_timer("API_Sync")
email = DataGenerator.random_email()
# Perform actions...
monitor.stop_timer("API_Sync")
monitor.log_memory_usage()
```

## 📊 Reporting

We use **`pytest-glow-report`** for beautiful, data-rich execution summaries.

1. **Run Tests**:
   ```bash
   pytest
   ```
2. **View Report**:
   Open `reports/report.html` in your browser for a full visual breakdown of passes, failures, and execution timings.

## ⚙️ Configuration

Configure via `config.json` or `SMART_AUTO_` environment variables.

```json
{
    "browser": "chrome",
    "timeout": 15,
    "headless": true,
    "proxy": "localhost:8080"
}
```

---
Maintained by [Dhiraj Das](https://www.dhirajdas.dev)
