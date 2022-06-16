from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from selenium.webdriver.common.by import By
from Logs.Logs import Report


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.log = Report()

    def do_click_by_locator(self, locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).click()

    def do_click_by_element(self, element):
        element.click()

    def do_send_keys(self, locator, text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_element_text(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element.text

    def is_element(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return bool(element)

    def find_elements(self, locator):
        elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(locator))
        return elements

    def find_element(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element

    def pause(self, seconds):
        time.sleep(seconds)

    def find_android_element(self, element_id=None, text=None, parent=None, class_name=None, timeout=1):
        if element_id is None and text is None and class_name is None:
            return []
        first_try = True
        if parent:
            if type(parent) is str:
                data = self.find_android_element(element_id=parent, timeout=5)
                if len(data) == 1:
                    scope = data[0]
                else:
                    scope = None
            else:
                scope = parent
        else:
            scope = self.driver
        if scope is None:
            return []
        end_time = time.time() + timeout
        if type(text) in (list, tuple):
            variants = text
        else:
            variants = [text]
        data = []
        while first_try or (time.time() < end_time):
            first_try = False
            if element_id:
                elements = scope.find_elements(by=By.ID, value=element_id)
                for element in elements:
                    if text:
                        actual = re.sub(r'\s+', ' ', element.text.strip().strip('.').lower())
                        for variant in variants:
                            if actual == variant.lower():
                                if class_name:
                                    cls = element.get_attribute('class')
                                    if cls == class_name:
                                        data.append(element)
                                        break
                                else:
                                    data.append(element)
                                    break
                    elif class_name:
                        cls = element.get_attribute('class')
                        if cls == class_name:
                            data.append(element)
                            break
                    else:
                        data.append(element)
            elif class_name:
                elements = scope.find_elements(by=By.CLASS_NAME, value=class_name)
                if text:
                    for element in elements:
                        actual = re.sub(r'\s+', ' ', element.text.strip().strip('.').lower())
                        for variant in variants:
                            if actual == variant.lower():
                                data.append(element)
                                break
                else:
                    data = elements
            elif text:
                data = scope.find_elements(by=By.LINK_TEXT, value=text)
            if data:
                break
            time.sleep(1)
        return data

    def click_android_button(self, button_id=None, button_text=None, button_name=None, class_name=None, err_msg=None):
        button = self.check_android_element(element_id=button_id,
                                            text=button_text,
                                            class_name=class_name,
                                            ui_type='Button',
                                            err_msg=err_msg)
        if button_name:
            self.log.log(f'Click [{button_name}]')
        button.click()

    def check_android_element(self, err_msg=None,
                              element_id=None,
                              text=None,
                              parent=None,
                              class_name=None,
                              ui_type=None,
                              timeout=10):
        data = self.find_android_element(element_id=element_id,
                                         text=text,
                                         parent=parent,
                                         class_name=class_name,
                                         timeout=timeout)
        if len(data) == 1:
            return data[0]
        if err_msg:
            message = err_msg
        else:
            if ui_type:
                message = ui_type
            else:
                message = 'UI element'
            if element_id:
                message += f' with Id "{element_id}"'
            if text:
                message += f' with text "{text}"'
            if class_name:
                message += f' with class "{class_name}"'
            if parent:
                message += f' with parent "{parent}"'
            if len(data) == 0:
                message += ' not found'
            else:
                message += ' is not unique'
        raise Exception(message)
