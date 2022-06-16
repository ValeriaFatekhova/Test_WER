import re
import os
import subprocess
import time
from appium import webdriver
import openpyxl
from Config.config import TestData
from Pages.BasePage import BasePage
from Pages.LoginPage import LoginPage
from Pages.ChooseCustomersScreen import ChooseCustomerScreen
from Logs.Logs import Report
from AudioData.CheckAudio import Audio


report_file = f'reports/report_{time.strftime("%Y_%m_%d_%H_%M_%S")}.xlsx'

report = openpyxl.load_workbook('report_template.xlsx')
report.save(report_file)
report.close()

appium_session = subprocess.Popen('appium', shell=True,
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)

test_data = TestData()
audio = Audio()
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
android = webdriver.Remote("http://localhost:4723/wd/hub", dc)
android.activate_app(package)
base_page = BasePage(android)
login_page = LoginPage(android)
main_screen = ChooseCustomerScreen(android)
log = Report()
login_page.register('US West')
base_page.click_android_button(button_name='Settings', button_id='com.harman.enova.beta:id/settingsBtn')
base_page.pause(2)
base_page.click_android_button(button_name='Common', button_id='com.harman.enova.beta:id/settings_common')
base_page.pause(2)

base_page.click_android_button(button_name='Pause Detection Timeout',
                     button_id='com.harman.enova.beta:id/pauseDetectionTimeoutLayout')
base_page.pause(2)
data = base_page.find_android_element(element_id='com.harman.enova.beta:id/inputField')
if not data:
    raise Exception('"Pause detection timeout" field not found"')
data[0].clear()
data[0].send_keys('5000')
base_page.click_android_button(button_name='Save', button_id='android:id/button1')

data = base_page.find_android_element(element_id='com.harman.enova.beta:id/audioStreamingSwitch')
if not data:
    raise Exception('"Audio Streaming" switch not found"')
if not data[0].get_attribute('checked'):
    data[0].click()

android.back()
base_page.click_android_button(button_name='Language', button_id='com.harman.enova.beta:id/settings_language')
base_page.pause(2)
data = base_page.find_android_element(element_id='com.harman.enova.beta:id/switchDefaultLanguage')
if not data:
    raise Exception('"Set language for all customers" switch not found"')
if data[0].get_attribute('checked'):
    data[0].click()
base_page.pause(2)
base_page.click_android_button(button_name='Enova', button_id='com.harman.enova.beta:id/customerName', button_text='Enova')
base_page.pause(2)
base_page.click_android_button(button_name='Russian', button_id='com.harman.enova.beta:id/languageName', button_text='Russian')
base_page.pause(2)
android.back()
base_page.pause(2)
android.back()

for au in os.listdir('audio'):
    report_data = {}
    if audio.get_file_extension(au) not in ('.wav', '.aac'):
        continue
    log.log(f'Audio: "{au}"')
    report_data['audio'] = au
    reference = os.path.join('audio', f'{audio.get_file_name(au)}.txt')
    if not os.path.exists(reference):
        log.log(f'Reference text file "{reference}" not found. Audio "{au}" ignored')
        continue

    with open(reference, 'r', encoding='utf-8') as f:
        expected = f.read()

    expected = expected.replace('-', ' ')
    expected = re.sub(r'\s+', ' ', expected.strip())
    report_data['nlp'] = {}
    report_data['nlp']['expected'] = expected
    stt_expected = expected.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':', '')
    report_data['stt'] = {}
    report_data['stt']['expected'] = stt_expected
    expected = re.sub(r'\.\.\.', '#', expected)
    expected = re.sub(r' \.', '.', expected)
    expected = re.sub(r' ,', ',', expected)
    expected = re.sub(r' !', '!', expected)
    expected = re.sub(r' \?', '?', expected)
    expected = re.sub(r' :', ':', expected)
    expected = re.sub(r' #', '#', expected)
    expected_words = expected.split(' ')
    expected_upper_case = {}
    expected_lower_case = {}
    for word in expected_words:
        key = word.replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':', '')
        if word[0].isupper():
            if key in expected_upper_case.keys():
                expected_upper_case[key] += 1
            else:
                expected_upper_case[key] = 1
        else:
            if key in expected_lower_case.keys():
                expected_lower_case[key] += 1
            else:
                expected_lower_case[key] = 1

    main_screen.selectCustomer('Enova')
    base_page.click_android_button(button_name='Record', button_id='recordBtn')
    audio.check_recording_start()
    audio.play(os.path.join('audio', au), au)
    audio.check_recording_stop(timeout=60)
    base_page.pause(2)
    data = base_page.find_android_element(element_id='com.harman.enova.beta:id/requestTextView')
    if not data:
        log.log(f'No response. Audio "{au}" ignored')
        continue
    question = data[0].text
    question = re.sub(r'\s+', ' ', question.strip())
    report_data['nlp']['actual'] = question
    stt_actual = question.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':', '')
    report_data['stt']['actual'] = stt_actual
    question = re.sub(r'\.{3}}', '#', question)
    question = re.sub(r' \.', '.', question)
    question = re.sub(r' ,', ',', question)
    question = re.sub(r' !', '!', question)
    question = re.sub(r' \?', '?', question)
    question = re.sub(r' :', ':', question)
    question = re.sub(r' #', '#', question)
    actual_words = question.split(' ')

    actual_upper_case = {}
    actual_lower_case = {}
    for word in actual_words:
        key = word.replace('.', '').replace(',', '').replace('!', '').replace('?', '')
        if word[0].isupper():
            if key in actual_upper_case.keys():
                actual_upper_case[key] += 1
            else:
                actual_upper_case[key] = 1
        else:
            if key in actual_lower_case.keys():
                actual_lower_case[key] += 1
            else:
                actual_lower_case[key] = 1

    log.log(f'stt_expected: "{stt_expected}"')
    log.log(f'  stt_actual: "{stt_actual}"')
    stt_wer = round(audio.wer(stt_actual, stt_expected), 1)
    log.log(f'STT WER: {stt_wer}')
    report_data['wer'] = stt_wer

    tp = 0
    fp = 0
    fn = 0
    support = 0
    for word, counter in expected_upper_case.items():
        support += counter
        if word in actual_upper_case.keys():
            actual_counter = actual_upper_case[word]
        else:
            actual_counter = 0
        if counter >= actual_counter:
            tp += min(counter, actual_counter)
            fn += (counter - actual_counter)
            continue
        if counter <= actual_counter:
            tp += min(counter, actual_counter)
            fp += (actual_counter - counter)
            continue

    for word, counter in actual_upper_case.items():
        if word not in expected_upper_case.keys():
            fp += counter

    if tp > 0:
        precision = round(tp / (tp + fp), 2)
        recall = round(tp / (tp + fn), 2)
        F1_score = round(2 * precision * recall / (precision + recall), 2)
    else:
        precision = 0
        recall = 0
        F1_score = 0

    log.log('Upper case')
    log.log(f'Support: {support}')
    log.log(f'Precision: {precision}')
    log.log(f'Recall: {recall}')
    log.log(f'F1 score: {F1_score}')

    report_data['capitalization'] = {}
    report_data['capitalization']['support'] = support
    report_data['capitalization']['precision'] = precision
    report_data['capitalization']['recall'] = recall
    report_data['capitalization']['f1'] = F1_score

    tp = 0
    fp = 0
    fn = 0
    support = 0
    for word, counter in expected_lower_case.items():
        support += counter
        if word in actual_lower_case.keys():
            actual_counter = actual_lower_case[word]
        else:
            actual_counter = 0
        if counter >= actual_counter:
            tp += min(counter, actual_counter)
            fn += (counter - actual_counter)
            continue
        if counter <= actual_counter:
            tp += min(counter, actual_counter)
            fp += (actual_counter - counter)
            continue

    for word, counter in actual_lower_case.items():
        if word not in expected_lower_case.keys():
            fp += counter

    if tp > 0:
        precision = round(tp / (tp + fp), 2)
        recall = round(tp / (tp + fn), 2)
        F1_score = round(2 * precision * recall / (precision + recall), 2)
    else:
        precision = 0
        recall = 0
        F1_score = 0

    log.log('Lower case')
    log.log(f'Support: {support}')
    log.log(f'Precision: {precision}')
    log.log(f'Recall: {recall}')
    log.log(f'F1 score: {F1_score}')

    report_data['no_capitalization'] = {}
    report_data['no_capitalization']['support'] = support
    report_data['no_capitalization']['precision'] = precision
    report_data['no_capitalization']['recall'] = recall
    report_data['no_capitalization']['f1'] = F1_score

    actual_punctuation = {}
    actual_no_punctuation = {}
    for word in actual_words:
        if word[-1] in ('.', ',', '!', '?', ':', '#'):
            if word in actual_punctuation.keys():
                actual_punctuation[word] += 1
            else:
                actual_punctuation[word] = 1
        else:
            if word in actual_no_punctuation.keys():
                actual_no_punctuation[word] += 1
            else:
                actual_no_punctuation[word] = 1

    expected_punctuation = {}
    expected_no_punctuation = {}
    for word in expected_words:
        if word[-1] in ('.', ',', '!', '?', ':', '#'):
            if word in expected_punctuation.keys():
                expected_punctuation[word] += 1
            else:
                expected_punctuation[word] = 1
        else:
            if word in expected_no_punctuation.keys():
                expected_no_punctuation[word] += 1
            else:
                expected_no_punctuation[word] = 1

    tp = 0
    fp = 0
    fn = 0
    support = 0
    for word, counter in expected_punctuation.items():
        support += counter
        if word in actual_punctuation.keys():
            actual_counter = actual_punctuation[word]
        else:
            actual_counter = 0
        if counter >= actual_counter:
            tp += min(counter, actual_counter)
            fn += (counter - actual_counter)
            continue
        if counter <= actual_counter:
            tp += min(counter, actual_counter)
            fp += (actual_counter - counter)
            continue

    for word, counter in actual_punctuation.items():
        if word not in expected_punctuation.keys():
            fp += counter

    if tp > 0:
        precision = round(tp / (tp + fp), 2)
        recall = round(tp / (tp + fn), 2)
        F1_score = round(2 * precision * recall / (precision + recall), 2)
    else:
        precision = 0
        recall = 0
        F1_score = 0

    log.log('Punctuation (. , ! ? : ...)')
    log.log(f'Support: {support}')
    log.log(f'Precision: {precision}')
    log.log(f'Recall: {recall}')
    log.log(f'F1 score: {F1_score}')

    report_data['punctuation'] = {}
    report_data['punctuation']['support'] = support
    report_data['punctuation']['precision'] = precision
    report_data['punctuation']['recall'] = recall
    report_data['punctuation']['f1'] = F1_score

    tp = 0
    fp = 0
    fn = 0
    support = 0
    for word, counter in expected_no_punctuation.items():
        support += counter
        if word in actual_no_punctuation.keys():
            actual_counter = actual_no_punctuation[word]
        else:
            actual_counter = 0
        if counter >= actual_counter:
            tp += min(counter, actual_counter)
            fn += (counter - actual_counter)
            continue
        if counter <= actual_counter:
            tp += min(counter, actual_counter)
            fp += (actual_counter - counter)
            continue

    for word, counter in actual_no_punctuation.items():
        if word not in expected_no_punctuation.keys():
            fp += counter

    if tp > 0:
        precision = round(tp / (tp + fp), 2)
        recall = round(tp / (tp + fn), 2)
        F1_score = round(2 * precision * recall / (precision + recall), 2)
    else:
        precision = 0
        recall = 0
        F1_score = 0

    log.log('No punctuation (. , ! ? : ...)')
    log.log(f'Support: {support}')
    log.log(f'Precision: {precision}')
    log.log(f'Recall: {recall}')
    log.log(f'F1 score: {F1_score}')

    report_data['no_punctuation'] = {}
    report_data['no_punctuation']['support'] = support
    report_data['no_punctuation']['precision'] = precision
    report_data['no_punctuation']['recall'] = recall
    report_data['no_punctuation']['f1'] = F1_score

    for symbol in '.,!?:#':
        actual_punctuation = {}
        actual_no_punctuation = {}
        for word in actual_words:
            if word.endswith(symbol):
                if word in actual_punctuation.keys():
                    actual_punctuation[word] += 1
                else:
                    actual_punctuation[word] = 1
            else:
                if word in actual_no_punctuation.keys():
                    actual_no_punctuation[word] += 1
                else:
                    actual_no_punctuation[word] = 1

        expected_punctuation = {}
        expected_no_punctuation = {}
        for word in expected_words:
            if word.endswith(symbol):
                if word in expected_punctuation.keys():
                    expected_punctuation[word] += 1
                else:
                    expected_punctuation[word] = 1
            else:
                if word in expected_no_punctuation.keys():
                    expected_no_punctuation[word] += 1
                else:
                    expected_no_punctuation[word] = 1

        tp = 0
        fp = 0
        fn = 0
        support = 0
        punctuation_map = {'.': 'period',
                           ',': 'comma',
                           '?': 'question',
                           '!': 'exclamation',
                           ':': 'column',
                           '#': 'ellipsis'}
        for word, counter in expected_punctuation.items():
            support += counter
            if word in actual_punctuation.keys():
                actual_counter = actual_punctuation[word]
            else:
                actual_counter = 0
            if counter >= actual_counter:
                tp += min(counter, actual_counter)
                fn += (counter - actual_counter)
                continue
            if counter <= actual_counter:
                tp += min(counter, actual_counter)
                fp += (actual_counter - counter)
                continue

        for word, counter in actual_punctuation.items():
            if word not in expected_punctuation.keys():
                fp += counter

        if tp > 0:
            precision = round(tp / (tp + fp), 2)
            recall = round(tp / (tp + fn), 2)
            F1_score = round(2 * precision * recall / (precision + recall), 2)
        else:
            precision = 0
            recall = 0
            F1_score = 0

        if symbol == '#':
            log.log('Punctuation (...)')
        else:
            log.log(f'Punctuation ({symbol})')
        log.log(f'Support: {support}')
        log.log(f'Precision: {precision}')
        log.log(f'Recall: {recall}')
        log.log(f'F1 score: {F1_score}')

        report_data[punctuation_map[symbol]] = {}
        report_data[punctuation_map[symbol]]['support'] = support
        report_data[punctuation_map[symbol]]['precision'] = precision
        report_data[punctuation_map[symbol]]['recall'] = recall
        report_data[punctuation_map[symbol]]['f1'] = F1_score

    log.append_report(report_data)


android.close_app()
android.quit()


def test_change_settings(self):
    self.base_page = BasePage(self.driver)
    self.base_page.click_android_button(button_name='Settings', button_id='com.harman.enova.beta:id/settingsBtn')
    self.base_page.pause(2)
    self.base_page.click_android_button(button_name='Common', button_id='com.harman.enova.beta:id/settings_common')
    self.base_page.pause(2)

    self.base_page.click_android_button(button_name='Pause Detection Timeout',
                                        button_id='com.harman.enova.beta:id/pauseDetectionTimeoutLayout')
    self.base_page.pause(2)
    self.data = self.base_page.find_android_element(element_id='com.harman.enova.beta:id/inputField')
    if not self.data:
        raise Exception('"Pause detection timeout" field not found"')
    self.data[0].clear()
    self.data[0].send_keys('5000')
    self.base_page.click_android_button(button_name='Save', button_id='android:id/button1')

    self.data = self.base_page.find_android_element(element_id='com.harman.enova.beta:id/audioStreamingSwitch')
    if not self.data:
        raise Exception('"Audio Streaming" switch not found"')
    if not self.data[0].get_attribute('checked'):
        self.data[0].click()

    self.driver.back()
    self.base_page.click_android_button(button_name='Language',
                                        button_id='com.harman.enova.beta:id/settings_language')
    self.base_page.pause(2)
    data = self.base_page.find_android_element(element_id='com.harman.enova.beta:id/switchDefaultLanguage')
    if not data:
        raise Exception('"Set language for all customers" switch not found"')
    if data[0].get_attribute('checked'):
        data[0].click()
    self.base_page.pause(2)
    self.base_page.click_android_button(button_name='Enova', button_id='com.harman.enova.beta:id/customerName',
                                        button_text='Enova')
    self.base_page.pause(2)
    self.base_page.click_android_button(button_name='Russian', button_id='com.harman.enova.beta:id/languageName',
                                        button_text='Russian')
    self.base_page.pause(2)
    self.driver.back()
    self.base_page.pause(2)
    self.driver.back()