from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage
from AudioData.CheckAudio import Audio


class EnovaChatPage(BasePage):
    SKIP_TUTORIAL_BUTTON = (By.ID, "com.harman.enova.beta:id/skipButton")
    MIC_BUTTON = (By.ID, "com.harman.enova.beta:id/recordBtn")
    LISTENING_STAY_BUTTON = (By.ID, "com.harman.enova.beta:id/listeningView")
    SERVER_PROCESSING_BUTTON = (By.ID, "com.harman.enova.beta:id/processingView")
    BACK_BUTTON = (By.ID, "com.harman.enova.beta:id/closeBtn")

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
        if self.is_element_by_locator(self.LISTENING_STAY_BUTTON):
            return True
        else:
            return False

    def is_listening_mode_off(self):
        if self.is_element_by_locator(self.MIC_BUTTON):
            return True
        else:
            return False

    def exit_from_chatmode(self):
        self.do_click_by_locator(self.BACK_BUTTON)

    def recording_start(self, err_msg='Recording was not started', timeout=15):
        self.log.log('check_recording status...')
        self.check_android_element(element_id='com.harman.enova.beta:id/listeningView', err_msg=err_msg, timeout=timeout)
        self.log.log(f'Recording started...')

    def recording_stop(self, err_msg='Recording was not stopped', timeout=30):
        self.log.log(f'check_recording status...')
        self.check_android_element(element_id='com.harman.enova.beta:id/recordBtn', err_msg=err_msg, timeout=timeout)
        self.log.log(f'Recording stopped')

    def play_audio_in_chat(self, audio):
        self.click_android_button(button_name='Record', button_id='recordBtn')
        self.recording_start()
        self.a.play(audio)
        self.recording_stop(timeout=60)
        self.pause(2)
        return self.find_android_element(element_id='com.harman.enova.beta:id/requestTextView')
