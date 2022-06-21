import openpyxl
import pytest
from appium import webdriver
from Config.config import TestData
from Pages.BasePage import BasePage
from Pages.ChooseCustomersScreen import ChooseCustomerScreen
from Pages.LoginPage import LoginPage
from Pages.SettingsInApp import SettingsInApp


@pytest.fixture(scope='class')
def init_driver(request):
    test_data = TestData()

    report = openpyxl.load_workbook(test_data.REPORT_TEMPLATE_PATH)
    report.save(test_data.REPORT_PATH)
    report.close()

    package = 'com.harman.enova.beta'
    dc = dict()
    dc['app'] = test_data.APPLICATION
    dc['appPackage'] = package
    dc['appActivity'] = 'com.harman.enova.MainActivity'
    dc['platformName'] = 'Android'
    dc['deviceName'] = test_data.DEVICE
    dc['autoGrantPermissions'] = True
    dc['adbExecTimeout'] = 500000
    dc['newCommandTimeout'] = 500000
    driver = webdriver.Remote("http://localhost:4723/wd/hub", dc)
    driver.activate_app(package)
    request.cls.driver = driver
    yield
    driver.close_app()
    driver.quit()


# @pytest.fixture(scope='function')
# def preparation_for_wer_test():
#     main_screen = ChooseCustomerScreen(driver)
#     settings_page = SettingsInApp(driver)
#     login_page = LoginPage(driver)
#
#     login_page.login(login_data["SERVER"], login_data["USER_NAME"])
#     settings_page.set_settings_for_wer_test(settings["pauseDetectionTimeoutLayout"])
#     main_screen.open_chatmode_for_customer(customer)
