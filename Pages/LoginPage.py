from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage


class LoginPage(BasePage):
    EMAIL = (By.ID, "com.harman.enova.beta:id/emailEditText")
    SERVER = (By.ID, "com.harman.enova.beta:id/selectHostButton")
    PROTOCOL = (By.ID, "com.harman.enova.beta:id/selectProtocolButton")
    SEND_BUTTON = (By.ID, "com.harman.enova.beta:id/submitBtn")
    SERVERS_LIST = (By.ID, "com.harman.enova.beta:id/serverName")
    SKIP_SETTINGS_BUTTON = (By.ID, "com.harman.enova.beta:id/continueButton")

    def __init__(self, driver):
        super().__init__(driver)

    def set_email(self, user_name):
        self.do_send_keys(self.EMAIL, user_name)

    def set_server(self, server_name):
        self.do_click_by_locator(self.SERVER)
        elements = self.find_elements(self.SERVERS_LIST)
        for element in elements:
            if element.text == server_name:
                self.do_click_by_element(element)
                break

    def click_send_button(self):
        self.do_click_by_locator(self.SEND_BUTTON)

    def skip_settings(self):
        continue_button = self.find_element(self.SKIP_SETTINGS_BUTTON)
        self.do_click_by_element(continue_button)
        continue_button = self.find_element(self.SKIP_SETTINGS_BUTTON)
        self.do_click_by_element(continue_button)

    def login(self, server_name, user_name):
        self.set_email(user_name)
        self.set_server(server_name)
        self.click_send_button()
        self.skip_settings()


