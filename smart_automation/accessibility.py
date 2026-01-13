from .logger import logger

class AccessibilityChecker:
    def __init__(self, driver):
        self.driver = driver

    def check_alt_texts(self):
        """Checks if all images have alt attributes."""
        images = self.driver.find_elements("tag name", "img")
        missing_alt = []
        for img in images:
            alt = img.get_attribute("alt")
            if not alt:
                src = img.get_attribute("src")
                missing_alt.append(src)
                logger.warning(f"Accessibility: Image missing alt text: {src}")
        
        return {
            "passed": len(missing_alt) == 0,
            "missing_alt_count": len(missing_alt),
            "details": missing_alt
        }

    def check_aria_labels(self):
        """Checks if interactive elements have labels."""
        elements = self.driver.find_elements("xpath", "//*[@onclick or @role='button' or tag_name='button']")
        missing_labels = []
        for el in elements:
            label = el.get_attribute("aria-label") or el.text
            if not label:
                missing_labels.append(el.get_attribute("outerHTML")[:50])
                logger.warning(f"Accessibility: Interactive element missing label: {missing_labels[-1]}")
        
        return {
            "passed": len(missing_labels) == 0,
            "missing_label_count": len(missing_labels),
            "details": missing_labels
        }
