import imaplib
import re
import email
from Pages.BasePage import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def login(self, server_name, user_name):
        edit_pin = None
        data = self.find_android_element(element_id='emailEditText', timeout=15)
        if len(data) == 1:
            data[0].send_keys(user_name)
        else:
            data = self.find_android_element(element_id='parentPanel', timeout=5)
            if len(data) == 1:
                pop_up = data[0]
                message_header = ''
                data = self.find_android_element(element_id='topPanel', parent=pop_up)
                if len(data) == 1:
                    data = self.find_android_element(element_id='title_template', parent=data[0])
                    if len(data) == 1:
                        data = self.find_android_element(element_id='alertTitle', parent=data[0])
                        if len(data) == 1:
                            message_header = data[0].text
                data = self.find_android_element(element_id='contentPanel', parent=pop_up)
                if len(data) == 1:
                    data = self.find_android_element(element_id='scrollView', parent=data[0])
                    if len(data) == 1:
                        data = self.find_android_element(class_name='android.widget.LinearLayout', parent=data[0])
                        if len(data) == 1:
                            message = data[0].find_element_by_class_name('android.widget.TextView')
                            if message:
                                self.log.log(f'PopUp Message: "{message_header}: {message.text}"')
                self.driver.back()
            self.find_email_edit_field(fill=user_name)
        self.click_android_button(button_name='Host Name', button_id='selectHostButton')
        self.check_android_element(element_id='selectHostLayout', timeout=5,
                              err_msg='Server drop-down list is not available')
        self.click_android_button(button_id='serverName',
                             button_text=server_name,
                             err_msg=f'Server {server_name} not in list')
        # clean_pin_messages()
        retries = 10
        while retries:
            retries -= 1
            self.click_android_button(button_name='SUBMIT', button_id='submitBtn')
            if len(self.find_android_element(element_id='continueButton', timeout=30)) == 1:
                self.skip_settings()
                return
            data = self.find_android_element(element_id="pinInputEditText", timeout=5)
            if len(data) == 1:
                edit_pin = data[0]
                break
            else:
                edit_pin = None
            data = self.find_android_element(element_id='errorText', timeout=5)
            if len(data) == 1:
                self.log.log(f'Error Message: "{data[0].text}"')
                self.pause(15)
                continue
            data = self.find_android_element(element_id='parentPanel', timeout=5)
            if len(data) == 1:
                pop_up = data[0]
                message_header = ''
                data = self.find_android_element(element_id='topPanel', parent=pop_up)
                if len(data) == 1:
                    data = self.find_android_element(element_id='title_template', parent=data[0])
                    if len(data) == 1:
                        data = self.find_android_element(element_id='alertTitle', parent=data[0])
                        if len(data) == 1:
                            message_header = data[0].text
                data = self.find_android_element(element_id='contentPanel', parent=pop_up)
                if len(data) == 1:
                    data = self.find_android_element(element_id='scrollView', parent=data[0])
                    if len(data) == 1:
                        data = self.find_android_element(class_name='android.widget.LinearLayout', parent=data[0])
                        if len(data) == 1:
                            message = data[0].find_element_by_class_name('android.widget.TextView')
                            if message:
                                self.log.log(f'PopUp Message: "{message_header}: {message.text}"')
                self.driver.back()
                self.log.log('Click [Back]')
                self.pause(30)
                continue
            break
        self.log.log('Waiting for PIN...')
        #pin = self.readPin(retries=10, timeout=30)
        # if not pin:
        #     raise Exception('PIN was not received')
        # self.log.log('PIN received')
        # if edit_pin is None:
        #     data = self.find_android_element(element_id="pinInputEditText", timeout=5)
        #     if len(data) == 1:
        #         edit_pin = data[0]
        #     else:
        #         raise Exception('"Enter PIN" field is not present')
        # edit_pin.send_keys(pin)
        self.pause(5)
        self.skip_settings()

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
        print(self.get_element_text(self.server))
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