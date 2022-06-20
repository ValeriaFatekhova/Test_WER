from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage


class ChooseCustomerScreen(BasePage):
    CURRENT_CUSTOMER = (By.ID, "com.harman.enova.beta:id/titleTextView")
    CHAT_BUTTON = (By.ID, "com.harman.enova.beta:id/chatButton")
    SHOP_BUTTON = (By.ID, "com.harman.enova.beta:id/shopButton")
    CUSTOMER_CARD = (By.ID, "com.harman.enova.beta:id/modeCardLayout")

    def __int__(self, driver):
        super.__init__(driver)

    def move_to_first_customer(self):
        pass

    def check_current_customer(self):
        current_customer = self.find_element(self.CURRENT_CUSTOMER)
        return self.get_element_text_by_element(current_customer)

    def select_customer(self, customer):
        #self.move_to_first_customer()
        while self.check_current_customer() != customer:
            self.swipe_left_by_element(self.find_element(self.CURRENT_CUSTOMER))

    def open_chatmode_for_customer(self, customer):
        self.select_customer(customer)
        self.do_click_by_locator(self.CHAT_BUTTON)
