from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from Logs.Logs import Report


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.log = Report()

    def do_click_by_locator(self, locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).click()

    def do_click_by_element(self, element):
        element.click()

    def do_send_keys_by_locator(self, locator, text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def do_send_keys_by_element(self, element, text):
        element.send_keys(text)

    def clear_element_by_locator(self, locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).clear()

    def clear_element_by_element(self, element):
        element.clear()

    def get_element_text_by_locator(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element.text

    def get_element_text_by_element(self, element):
        return element.text

    def is_element_by_locator(self, locator):
        element = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(locator))
        return bool(element)

    def find_elements(self, locator):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(locator))
        return elements

    def find_element(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element

    def is_element_checked_by_locator(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element.get_attribute("checked")

    def is_element_checked_by_element(self, element):
        return element.get_attribute("checked")

    def swipe_left_by_element(self, element):
        x = element.location['x'] + element.size['width'] / 2
        y = element.location['y'] + element.size['height'] / 2
        self.driver.swipe(x, y, 35, y, 200)

    def swipe_right_by_element(self, element):
        x = element.location['x'] + element.size['width'] / 2
        y = element.location['y'] + element.size['height'] / 2
        self.driver.swipe(0, y, x, y, 200)

    def pause(self, seconds):
        time.sleep(seconds)

