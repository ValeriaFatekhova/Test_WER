import openpyxl
import pytest
from appium import webdriver
from Config.config import TestData


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
