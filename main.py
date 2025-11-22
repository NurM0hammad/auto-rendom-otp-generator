from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time

def test_repeat_fill(url, attempts=100):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        time.sleep(1)
        for attempt in range(attempts):
            # generate code
            code = f"{random.randint(0, 999999):06d}"
            print(f"[{attempt+1}/{attempts}] Trying code: {code}")

            inputs = driver.find_elements(By.TAG_NAME, "input")
            filled = False
            for input_field in inputs:
                field_type = (input_field.get_attribute('type') or '').lower()
                maxlength = input_field.get_attribute('maxlength')
                if field_type in ['number', 'text'] and (maxlength == '6' or maxlength is None):
                    input_field.clear()
                    input_field.send_keys(code)
                    filled = True
                    break
            if filled:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    if "continue" in (button.text or "").lower():
                        try:
                            button.click()
                        except Exception as e:
                            print("Button click failed:", e)
                        break

            time.sleep(0.5)

    finally:
        driver.quit()

# Example usage on a local test page:
test_repeat_fill("demo_link", attempts=50)
