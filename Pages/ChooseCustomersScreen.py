from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage


class ChooseCustomerScreen(BasePage):
    CURRENT_CUSTOMER = (By.ID, "com.harman.enova.beta:id/titleTextView")
    CHAT_BUTTON = (By.ID, "com.harman.enova.beta:id/chatButton")
    SHOP_BUTTON = (By.ID, "com.harman.enova.beta:id/shopButton")

    def __int__(self, driver):
        super.__init__(driver)

    def check_current_customer(self):
        current_customer = self.find_element(self.CURRENT_CUSTOMER)
        return self.get_element_text_by_element(current_customer)

    def select_customer(self, customer):
        while self.check_current_customer() != customer:
            self.swipe_left_by_element(self.find_element(self.CURRENT_CUSTOMER))

    def open_chatmode_for_customer(self, customer):
        self.select_customer(customer)
        self.do_click_by_locator(self.CHAT_BUTTON)

    def selectCustomer(self, customer):
        data = self.find_android_element(element_id='chooseModeTextView', text='Выберите клиента')
        if len(data) != 1:
            self.driver.back()
            self.check_choose_customer_screen()
        self.pause(2)
        data = self.find_android_element(element_id='titleTextView', timeout=5)
        if len(data) != 1:
            raise Exception('Customer name not found')
        if data[0].text == customer:
            self.log.log(f'Current customer: {customer}')
            self.click_android_button(button_name='Chat', button_id='chatButton')
            skip = self.find_android_element(element_id='com.harman.enova.beta:id/skipButton', timeout=5)
            if len(skip) == 1:
                skip[0].click()
                self.log.log('Click [Skip]')
            return
        while self.selectNextCustomer():
            data = self.find_android_element(element_id='titleTextView', timeout=5)
            if len(data) != 1:
                raise Exception('Customer name not found')
            if data[0].text == customer:
                self.click_android_button(button_name='Chat', button_id='chatButton')
            skip = self.find_android_element(element_id='com.harman.enova.beta:id/skipButton', timeout=5)
            if len(skip) == 1:
                skip[0].click()
                self.log.log('Click [Skip]')
            return
        while self.selectPrevCustomer():
            data = self.find_android_element(element_id='titleTextView', timeout=5)
            if len(data) != 1:
                raise Exception('Customer name not found')
            if data[0].text == customer:
                self.click_android_button(button_name='Chat', button_id='chatButton')
            skip = self.find_android_element(element_id='com.harman.enova.beta:id/skipButton', timeout=5)
            if len(skip) == 1:
                skip[0].click()
                self.log.log('Click [Skip]')
            return
        raise Exception(f'Can not select customer "{customer}"')

    def selectNextCustomer(self):
        data = self.find_android_element(element_id='titleTextView', timeout=5)
        if len(data) != 1:
            raise Exception('Customer name not found')
        prev_title = self.find_customer_name()
        x = data[0].location['x'] + data[0].size['width'] / 2
        y = data[0].location['y'] + data[0].size['height'] / 2
        self.driver.swipe(x, y, 35, y, 200)
        self.pause(1)
        title = self.find_customer_name()
        self.log.log(f'Next Customer: {title}')
        return title != prev_title

    def selectPrevCustomer(self):
        data = self.find_android_element(element_id='titleTextView', timeout=5)
        if len(data) != 1:
            raise Exception('Customer name not found')
        prev_title = self.find_customer_name()
        x = data[0].location['x'] + data[0].size['width'] / 2
        y = data[0].location['y'] + data[0].size['height'] / 2
        self.driver.swipe(0, y, x, y, 200)
        self.pause(1)
        title = self.find_customer_name()
        self.log.log(f'Prev Customer: {title}')
        return title != prev_title

    def find_customer_name(self):
        customer = self.check_android_element(element_id='titleTextView', err_msg='Customer name is not present')
        return customer.text

    def check_choose_customer_screen(self, err_msg='"Choose customer" header is not present'):
        self.check_android_element(element_id='chooseModeTextView', text='Choose customer', err_msg=err_msg)