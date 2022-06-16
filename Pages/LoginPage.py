import imaplib
import re
import email

from selenium.webdriver.common.by import By

from Pages.BasePage import BasePage


class LoginPage(BasePage):
    EMAIL = (By.ID, "com.harman.enova.beta:id/emailEditText")
    SERVER = (By.ID, "com.harman.enova.beta:id/selectHostButton")
    PROTOCOL = (By.ID, "com.harman.enova.beta:id/selectProtocolButton")
    SEND_BUTTON = (By.ID, "com.harman.enova.beta:id/submitBtn")
    SERVERS_LIST = (By.ID, "com.harman.enova.beta:id/serverName")

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

    def do_login(self, server_name, user_name):
        self.set_email(user_name)
        self.set_server(server_name)
        self.click_send_button()

    def skip_settings(self):
        data = self.find_android_element(element_id='continueButton', timeout=5)
        if len(data) == 1:
            continue_btn = data[0]
            continue_btn.click()
            self.log.log('Click [Continue]')
        data = self.find_android_element(element_id='continueButton', timeout=5)
        if len(data) == 1:
            continue_btn = data[0]
            continue_btn.click()
            self.log.log('Click [Continue]')

    # def clean_pin_messages(self):
    #     pin = self.readPin()
    #     while pin:
    #         pin = self.readPin()

    def get_server(self):
        self.click_android_button(button_name='Settings', button_id='com.harman.enova.beta:id/settingsBtn')
        self.pause(2)
        self.click_android_button(button_name='Common', button_id='com.harman.enova.beta:id/settings_device')
        self.pause(2)
        self.server = self.find_android_element(element_id='com.harman.enova.beta:id/serverName')
        print(self.server)
        # return self.server

    def find_email_edit_field(self, fill=None):
        element = self.check_android_element(element_id='emailEditText',
                                        err_msg='"Mail address" text field is not present')
        if fill:
            element.send_keys(fill)
        return element

    # def readPin(self, retries=1, timeout=5):
    #     body = ''
    #     while retries:
    #         pin = None
    #         mail = imaplib.IMAP4_SSL('imap.gmail.com')
    #         mail.login(self.test_data.USER_NAME, self.test_data.PASSWORD)
    #         mail.list()
    #         mail.select("inbox")
    #         result, data = mail.search(None, "ALL")
    #         ids = data[0]
    #         id_list = ids.split()
    #         if id_list:
    #             latest_email_id = id_list[-1]
    #             result, data = mail.fetch(latest_email_id, "(RFC822)")
    #             raw_email = data[0][1]
    #             raw_email_string = raw_email.decode('utf-8')
    #             email_message = email.message_from_string(raw_email_string)
    #             if email_message.is_multipart():
    #                 for payload in email_message.get_payload():
    #                     tmp = payload.get_payload(decode=True)
    #                     if tmp:
    #                         body = tmp.decode('utf-8')
    #                     else:
    #                         body = ''
    #             else:
    #                 tmp = email_message.get_payload(decode=True)
    #                 if tmp:
    #                     body = email_message.get_payload(decode=True).decode('utf-8')
    #                 else:
    #                     body = ''
    #             tmp = re.findall(r'Your registration PIN is (\w+)', body)
    #             if tmp:
    #                 pin = tmp[0]
    #                 mail.store(latest_email_id, '+FLAGS', '\\Deleted')
    #                 mail.expunge()
    #         mail.close()
    #         if pin:
    #             return pin
    #         retries -= 1
    #         if retries:
    #             self.log.log(f'Waiting for PIN. Retry in {timeout} sec')
    #             self.pause(timeout)
    #     return None