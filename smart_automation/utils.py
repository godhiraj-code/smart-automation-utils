import time
from .logger import logger

def highlight_element(driver, element, duration=0.5, color="red", border=5):
    """
    Highlights (blinks) a Selenium Webdriver element.
    """
    original_style = element.get_attribute("style")
    new_style = "border: {0}px solid {1};".format(border, color)
    
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, new_style)
    
    if duration > 0:
        time.sleep(duration)
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)

def capture_screenshot(driver, filename_prefix="failure"):
    """
    Captures a screenshot and saves it to the screenshots directory.
    """
    import os
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    filepath = os.path.join("screenshots", filename)
    
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
        
    try:
        driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved to: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {e}")
        return None

def retry(tries=3, delay=1, backoff=2, exceptions=(Exception,)):
    """
    Retry decorator with exponential backoff.
    """
    def deco_retry(f):
        import functools
        @functools.wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = f"Retrying {f.__name__} in {mdelay}s due to {type(e).__name__}. {mtries-1} attempts left."
                    logger.warning(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry
    return deco_retry
