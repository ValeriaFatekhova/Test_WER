from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage


class SettingsInApp(BasePage):
    SETTINGS_BUTTON = (By.ID, "com.harman.enova.beta:id/settingsBtn")
    SETTINGS_DEVICE = (By.ID, "com.harman.enova.beta:id/settings_device")
    CURRENT_SERVER = (By.ID, "com.harman.enova.beta:id/serverName")
    SETTINGS_BACK_BUTTON = (By.ID, "com.harman.enova.beta:id/backButton")
    SETTINGS_COMMON = (By.ID, "com.harman.enova.beta:id/settings_common")

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

    def set_settings(self, settings):
        self.do_click_by_locator(self.SETTINGS_BUTTON)
        self.do_click_by_locator(self.SETTINGS_COMMON)

        self.click_android_button(button_name='Pause Detection Timeout',
                                            button_id='com.harman.enova.beta:id/pauseDetectionTimeoutLayout')
        self.pause(2)
        self.data = self.find_android_element(element_id='com.harman.enova.beta:id/inputField')
        if not self.data:
            raise Exception('"Pause detection timeout" field not found"')
        self.data[0].clear()
        self.data[0].send_keys(settings["pauseDetectionTimeoutLayout"])
        self.click_android_button(button_name='Save', button_id='android:id/button1')

        self.data = self.find_android_element(element_id='com.harman.enova.beta:id/audioStreamingSwitch')
        if not self.data:
            raise Exception('"Audio Streaming" switch not found"')
        if not self.data[0].get_attribute('checked'):
            self.data[0].click()

        self.driver.back()
        self.click_android_button(button_name='Language',
                                            button_id='com.harman.enova.beta:id/settings_language')
        self.pause(2)
        data = self.find_android_element(element_id='com.harman.enova.beta:id/switchDefaultLanguage')
        if not data:
            raise Exception('"Set language for all customers" switch not found"')
        if data[0].get_attribute('checked'):
            data[0].click()
        self.pause(2)
        self.click_android_button(button_name='Enova', button_id='com.harman.enova.beta:id/customerName',
                                            button_text='Enova')
        self.pause(2)
        self.click_android_button(button_name='Russian', button_id='com.harman.enova.beta:id/languageName',
                                            button_text='Russian')
        self.return_to_customer_screen()

