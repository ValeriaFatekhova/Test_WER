from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage
from AudioData.CheckAudio import Audio


class EnovaChatPage(BasePage):
    SKIP_TUTORIAL_BUTTON = (By.ID, "com.harman.enova.beta:id/skipButton")
    MIC_BUTTON = (By.ID, "com.harman.enova.beta:id/recordBtn")
    LISTENING_STATE_BUTTON = (By.ID, "com.harman.enova.beta:id/listeningView")
    SERVER_PROCESSING_BUTTON = (By.ID, "com.harman.enova.beta:id/processingView")
    BACK_BUTTON = (By.ID, "com.harman.enova.beta:id/closeBtn")
    CHAT_TEXT = (By.ID, "com.harman.enova.beta:id/requestTextView")

    def __init__(self, driver):
        super().__init__(driver)
        self.a = Audio()

    def skip_tutorial(self):
        self.do_click_by_locator(self.SKIP_TUTORIAL_BUTTON)

    def listening_mode_on(self):
        if self.is_element_by_locator(self.SKIP_TUTORIAL_BUTTON):
            self.skip_tutorial()
        if self.is_listening_mode_off():
            self.do_click_by_locator(self.MIC_BUTTON)

    def is_listening_mode_on(self):
        if self.is_element_by_locator(self.LISTENING_STATE_BUTTON):
            return True
        else:
            return False

    def is_listening_mode_off(self):
        if self.is_element_by_locator(self.MIC_BUTTON):
            return True
        else:
            return False

    def is_server_processing_state(self):
        if self.is_element_by_locator(self.SERVER_PROCESSING_BUTTON):
            return True
        else:
            return False

    def exit_from_chatmode(self):
        self.do_click_by_locator(self.BACK_BUTTON)

    def play_audio_in_chat(self, audio):
        if self.is_listening_mode_on():
            self.a.play(audio)
        while not self.is_listening_mode_off():
            self.pause(10)
        return self.get_element_text_by_locator(self.CHAT_TEXT)
