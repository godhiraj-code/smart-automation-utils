import time

def highlight_element(driver, element, duration=3, color="red", border=5):
    """
    Highlights (blinks) a Selenium Webdriver element.
    
    Args:
        driver: The WebDriver instance.
        element: The WebElement to highlight.
        duration: How long to keep the highlight (in seconds).
        color: Color of the border.
        border: Thickness of the border.
    """
    original_style = element.get_attribute("style")
    new_style = "border: {0}px solid {1};".format(border, color)
    
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, new_style)
    
    if duration > 0:
        time.sleep(duration)
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)
