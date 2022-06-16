from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage


class SettingsInApp(BasePage):
    SETTINGS_BUTTON = (By.ID, "com.harman.enova.beta:id/settingsBtn")
    SETTINGS_DEVICE = (By.ID, "com.harman.enova.beta:id/settings_device")
    CURRENT_SERVER = (By.ID, "com.harman.enova.beta:id/serverName")
    SETTINGS_BACK_BUTTON = (By.ID, "com.harman.enova.beta:id/backButton")
    SETTINGS_COMMON = (By.ID, "com.harman.enova.beta:id/settings_common")
    PAUSE_DETECTION_TIMEOUT = (By.ID, "com.harman.enova.beta:id/pauseDetectionTimeoutLayout")
    TIMEOUT_FIELD = (By.ID, "com.harman.enova.beta:id/inputField")
    TIMEOUT_SAVE_BUTTON = (By.ID, "android:id/button1")
    AUDIOSTREAMING_SWITCH = (By.ID, "com.harman.enova.beta:id/audioStreamingSwitch")
    SETTINGS_LANGUAGE = (By.ID, "com.harman.enova.beta:id/settings_language")
    SWITCH_DEFAULT_LANGUAGE = (By.ID, "com.harman.enova.beta:id/switchDefaultLanguage")
    CUSTOMERS_LIST = (By.ID, "com.harman.enova.beta:id/customerName")
    LANGUAGES_LIST = (By.ID, "com.harman.enova.beta:id/languageName")

    def __init__(self, driver):
        super().__init__(driver)

    def get_server(self):
        self.do_click_by_locator(self.SETTINGS_BUTTON)
        self.do_click_by_locator(self.SETTINGS_DEVICE)
        server = self.find_element(self.CURRENT_SERVER)
        self.return_to_customer_screen()
        return server.text

    def return_to_customer_screen(self):
        self.do_click_by_locator(self.SETTINGS_BACK_BUTTON)
        self.do_click_by_locator(self.SETTINGS_BACK_BUTTON)

    def set_common_pause_timeout(self, pauseDetectionTimeoutLayout):
        self.do_click_by_locator(self.SETTINGS_BUTTON)
        self.do_click_by_locator(self.SETTINGS_COMMON)
        self.do_click_by_locator(self.PAUSE_DETECTION_TIMEOUT)
        timeout_field = self.find_element(self.TIMEOUT_FIELD)
        self.clear_element_by_element(timeout_field)
        self.do_send_keys_by_element(timeout_field, pauseDetectionTimeoutLayout)
        self.do_click_by_locator(self.TIMEOUT_SAVE_BUTTON)
        self.return_to_customer_screen()

    def set_common_audiostreaming_turnon(self):
        self.do_click_by_locator(self.SETTINGS_BUTTON)
        self.do_click_by_locator(self.SETTINGS_COMMON)
        self.do_click_by_locator(self.AUDIOSTREAMING_SWITCH)
        self.return_to_customer_screen()

    def change_language(self, customer, language):
        self.do_click_by_locator(self.SETTINGS_BUTTON)
        self.do_click_by_locator(self.SETTINGS_LANGUAGE)
        switch_default_language = self.find_element(self.SWITCH_DEFAULT_LANGUAGE)
        if self.is_element_checked_by_element(switch_default_language):
            self.do_click_by_element(switch_default_language)
        customers = self.find_elements(self.CUSTOMERS_LIST)
        for element in customers:
            if element.text == customer:
                self.do_click_by_element(element)
                break
        languages = self.find_elements(self.LANGUAGES_LIST)
        for element in languages:
            if element.text == language:
                self.do_click_by_element(element)
                break
        self.return_to_customer_screen()