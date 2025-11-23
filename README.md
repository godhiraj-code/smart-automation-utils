# Smart Automation Utils

A Python package designed to help automation developers and testers working with Selenium and Appium.

## Features

- **SmartDriver**: A wrapper around Selenium WebDriver that handles automatic waits and common interactions intelligently.
- **Element Highlighting**: Visual debugging tool to highlight elements during test execution.
- **Smart Waits**: Decorators and context managers for handling dynamic content.

## Installation

```bash
pip install smart-automation-utils
```

## Usage

```python
from smart_automation.driver import SmartDriver

driver = SmartDriver("chrome")
driver.get("https://example.com")
driver.find_element_by_id("submit").click()
```
