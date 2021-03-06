import pytest
import os
from Tests.test_base import BaseTest
from Pages.BasePage import BasePage
from Pages.LoginPage import LoginPage
from Pages.ChooseCustomersScreen import ChooseCustomerScreen
from Logs.Logs import Report
from AudioData.CheckAudio import Audio
from Config.config import TestData
from Pages.SettingsInApp import SettingsInApp
from Pages.EnovaChatPage import EnovaChatPage


class TestWer(BaseTest):

    @pytest.mark.parametrize("login_data", [TestData.LOGIN_DATA])
    def test_login(self, login_data):
        self.login_page = LoginPage(self.driver)
        self.settings = SettingsInApp(self.driver)
        self.customers_page = ChooseCustomerScreen(self.driver)
        self.base_page = BasePage(self.driver)

        self.login_page.login(login_data["SERVER"], login_data["USER_NAME"])

        flag = self.base_page.is_element_by_locator(self.customers_page.CUSTOMER_CARD)
        assert flag

        server_name = self.settings.get_server()
        assert server_name == login_data["SERVER"]

    @pytest.mark.parametrize("customer, settings, audio_path, report_path", [
        (TestData.CUSTOMER, TestData.SETTINGS_DATA, TestData.AUDIO_PATH, TestData.REPORT_PATH)
    ])
    def test_wer(self, customer, settings, audio_path, report_path):
        #self.base_page = BasePage(self.driver)
        self.main_screen = ChooseCustomerScreen(self.driver)
        self.settings_page = SettingsInApp(self.driver)
        self.enova_chat_page = EnovaChatPage(self.driver)
        self.log = Report()
        self.a = Audio()

        self.settings_page.set_settings_for_wer_test(settings["pauseDetectionTimeoutLayout"])
        self.main_screen.open_chatmode_for_customer(customer)
        self.enova_chat_page.listening_mode_on()

        for audio in os.listdir(audio_path):
            expected_path = os.path.join(audio_path, f'{self.a.get_file_name(audio)}.txt')
            with open(expected_path, 'r', encoding='utf-8') as f:
                expected_text = f.read()
            actual_text = self.enova_chat_page.play_audio_in_chat(os.path.join(audio_path, audio))
            report_data = self.a.calculate_data_for_wer_report(audio, expected_text, actual_text)
            self.log.append_report(report_data, report_path)
