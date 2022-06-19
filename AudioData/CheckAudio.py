import os
import numpy as np
from playsound import playsound
import re
from Logs.Logs import Report


class Audio:

    def __init__(self):
        self.log = Report()

    def play(self, audio_path):
            playsound(audio_path)

    def wer(self, r, h):
        if not r:
            if not h:
                return 100.0
            else:
                return 0.0
        if not h:
            return 100.0

        r = r.split(' ')
        h = h.split(' ')
        d = np.zeros((len(r) + 1) * (len(h) + 1), dtype=np.uint8)
        d = d.reshape((len(r) + 1, len(h) + 1))

        for i in range(len(r) + 1):
            d[i][0] = i

        for j in range(len(h) + 1):
            d[0][j] = j

        for i in range(1, len(r) + 1):
            for j in range(1, len(h) + 1):
                if r[i - 1] == h[j - 1]:
                    d[i][j] = d[i - 1][j - 1]
                else:
                    substitution = d[i - 1][j - 1] + 1
                    insertion = d[i][j - 1] + 1
                    deletion = d[i - 1][j] + 1
                    d[i][j] = min(substitution, insertion, deletion)

        return d[len(r)][len(h)] / len(r) * 100

    def get_file_extension(self, file):
        return os.path.splitext(file)[1].lower()

    def get_file_name(self, file):
        return os.path.basename(os.path.splitext(file)[0]).lower()

    def create_metriks_from_text(self, text):
        res_data = {}
        text = text.replace('-', ' ')
        res = re.sub(r'\s+', ' ', text.strip())
        res_data['nlp'] = {}
        res_data['nlp']['res'] = res
        stt_res = res.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(
            ':', '')
        res_data['stt'] = {}
        res_data['stt']['res'] = stt_res
        res = re.sub(r'\.\.\.', '#', res)
        res = re.sub(r' \.', '.', res)
        res = re.sub(r' ,', ',', res)
        res = re.sub(r' !', '!', res)
        res = re.sub(r' \?', '?', res)
        res = re.sub(r' :', ':', res)
        res = re.sub(r' #', '#', res)
        res_data['res_words'] = res.split(' ')
        res_data['res_upper_case'] = {}
        res_data['res_lower_case'] = {}
        for word in res_data['res_words']:
            key = word.replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':', '')
            if word[0].isupper():
                if key in res_data['res_upper_case'].keys():
                    res_data['res_upper_case'][key] += 1
                else:
                    res_data['res_upper_case'][key] = 1
            else:
                if key in res_data['res_lower_case'].keys():
                    res_data['res_lower_case'][key] += 1
                else:
                    res_data['res_lower_case'][key] = 1
        return res_data

    def create_capitalization_metriks(self, expected_cap_data, actual_cap_data, mark):
        res_data = {}
        tp = 0
        fp = 0
        fn = 0
        support = 0
        for word, counter in expected_cap_data.items():
            support += counter
            if word in actual_cap_data.keys():
                actual_counter = actual_cap_data[word]
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

        for word, counter in actual_cap_data.items():
            if word not in expected_cap_data.keys():
                fp += counter

        if tp > 0:
            precision = round(tp / (tp + fp), 2)
            recall = round(tp / (tp + fn), 2)
            F1_score = round(2 * precision * recall / (precision + recall), 2)
        else:
            precision = 0
            recall = 0
            F1_score = 0

        self.log.log(mark)
        self.log.log(f'Support: {support}')
        self.log.log(f'Precision: {precision}')
        self.log.log(f'Recall: {recall}')
        self.log.log(f'F1 score: {F1_score}')

        res_data['support'] = support
        res_data['precision'] = precision
        res_data['recall'] = recall
        res_data['f1'] = F1_score

        return res_data

    def calculate_punctuation(self, word_list):
        res_punctuation = {}
        res_no_punctuation = {}
        for word in word_list:
            if word[-1] in ('.', ',', '!', '?', ':', '#'):
                if word in res_punctuation.keys():
                    res_punctuation[word] += 1
                else:
                    res_punctuation[word] = 1
            else:
                if word in res_no_punctuation.keys():
                    res_no_punctuation[word] += 1
                else:
                    res_no_punctuation[word] = 1
        return res_punctuation, res_no_punctuation

    def calculate_data_for_wer_report(self, audio, expected_text, actual_text):
            report_data = {}
            report_data['nlp'] = {}
            report_data['stt'] = {}
            report_data['capitalization'] = {}
            report_data['no_capitalization'] = {}
            report_data['punctuation'] = {}
            report_data['no_punctuation'] = {}
            report_data['audio'] = None
            report_data['nlp']['expected'] = None
            report_data['stt']['expected'] = None
            report_data['nlp']['actual'] = None
            report_data['stt']['actual'] = None
            report_data['wer'] = None
            report_data['capitalization']['support'] = None
            report_data['capitalization']['precision'] = None
            report_data['capitalization']['recall'] = None
            report_data['capitalization']['f1'] = None
            report_data['no_capitalization']['support'] = None
            report_data['no_capitalization']['precision'] = None
            report_data['no_capitalization']['recall'] = None
            report_data['no_capitalization']['f1'] = None
            report_data['punctuation']['support'] = None
            report_data['punctuation']['precision'] = None
            report_data['punctuation']['recall'] = None
            report_data['punctuation']['f1'] = None
            report_data['no_punctuation']['support'] = None
            report_data['no_punctuation']['precision'] = None
            report_data['no_punctuation']['recall'] = None
            report_data['no_punctuation']['f1'] = None

            self.log.log(f'Audio: "{audio}"')
            report_data['audio'] = audio

            expected_data = self.create_metriks_from_text(expected_text)

            report_data['nlp']['expected'] = expected_data['nlp']['res']
            report_data['stt']['expected'] = expected_data['stt']['res']
            expected_words = expected_data['res_words']
            expected_upper_case = expected_data['res_upper_case']
            expected_lower_case = expected_data['res_upper_case']

            actual_data = self.create_metriks_from_text(actual_text)
            report_data['nlp']['actual'] = actual_data['nlp']['res']
            report_data['stt']['actual'] = actual_data['stt']['res']
            actual_words = actual_data['res_words']
            actual_upper_case = actual_data['res_upper_case']
            actual_lower_case = actual_data['res_upper_case']

            self.log.log(f"stt_expected: {report_data['stt']['expected']}")
            self.log.log(f"  stt_actual: {report_data['stt']['actual']}")
            stt_wer = round(self.wer(report_data['stt']['actual'], report_data['stt']['expected']), 1)
            self.log.log(f'STT WER: {stt_wer}')
            report_data['wer'] = stt_wer

            upper_cap_data = self.create_capitalization_metriks(expected_upper_case, actual_upper_case, 'Upper case')
            report_data['capitalization']['support'] = upper_cap_data['support']
            report_data['capitalization']['precision'] = upper_cap_data['precision']
            report_data['capitalization']['recall'] = upper_cap_data['recall']
            report_data['capitalization']['f1'] = upper_cap_data['f1']

            lower_cap_data = self.create_capitalization_metriks(expected_lower_case, actual_lower_case, 'Lower case')
            report_data['no_capitalization']['support'] = lower_cap_data['support']
            report_data['no_capitalization']['precision'] = lower_cap_data['precision']
            report_data['no_capitalization']['recall'] = lower_cap_data['recall']
            report_data['no_capitalization']['f1'] = lower_cap_data['f1']

            actual_punctuation, actual_no_punctuation = self.calculate_punctuation(actual_words)
            expected_punctuation, expected_no_punctuation = self.calculate_punctuation(expected_words)

            punctuation_data = self.create_capitalization_metriks(expected_punctuation, actual_punctuation, 'Punctuation (. , ! ? : ...)')
            report_data['punctuation']['support'] = punctuation_data['support']
            report_data['punctuation']['precision'] = punctuation_data['precision']
            report_data['punctuation']['recall'] = punctuation_data['recall']
            report_data['punctuation']['f1'] = punctuation_data['f1']

            no_punctuation_data = self.create_capitalization_metriks(expected_no_punctuation, actual_no_punctuation, 'No punctuation (. , ! ? : ...)')
            report_data['no_punctuation']['support'] = no_punctuation_data['support']
            report_data['no_punctuation']['precision'] = no_punctuation_data['precision']
            report_data['no_punctuation']['recall'] = no_punctuation_data['recall']
            report_data['no_punctuation']['f1'] = no_punctuation_data['f1']

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
                    self.log.log('Punctuation (...)')
                else:
                    self.log.log(f'Punctuation ({symbol})')
                self.log.log(f'Support: {support}')
                self.log.log(f'Precision: {precision}')
                self.log.log(f'Recall: {recall}')
                self.log.log(f'F1 score: {F1_score}')

                report_data[punctuation_map[symbol]] = {}
                report_data[punctuation_map[symbol]]['support'] = support
                report_data[punctuation_map[symbol]]['precision'] = precision
                report_data[punctuation_map[symbol]]['recall'] = recall
                report_data[punctuation_map[symbol]]['f1'] = F1_score

            return report_data
