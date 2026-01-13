class SmartAutomationError(Exception):
    """Base exception class for smart-automation-utils."""
    pass

class DriverError(SmartAutomationError):
    """Raised when there is an issue with the WebDriver."""
    pass

class ElementError(SmartAutomationError):
    """Raised when an element cannot be found or interacted with."""
    pass

class TimeoutError(SmartAutomationError):
    """Raised when an operation times out."""
    pass

class ConfigurationError(SmartAutomationError):
    """Raised when there is an issue with the configuration."""
    pass
