from Pages.BasePage import BasePage
from AudioData.CheckAudio import Audio


class EnovaChatPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.a = Audio()

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
