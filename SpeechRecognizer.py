# !/usr/bin/env python3
import json, string, queue, csv, time, random, re, wave, pyaudio, os, signal, sys


from Config import api_keys
from Phrases import phrases, phrase_repeats
from WordErrorRate import compareWordLists

import Constants as CONSTANTS

import speech_recognition as speech_recognition


class SpeechRecognizer:
    def __init__(self):
        self.results = list()
        self.csv_header = ["Id", "Spoken Phrase", "I", "S", "D", "WA", "WER", "Interpreted Phrase"]
        self.label = "generic"
        self.translator = str.maketrans('', '', string.punctuation)

    def calculateScores(self, reference_phrase, interpreted_phrase):
        if not interpreted_phrase:
            row_of_results = 'N/A' * 6
            self.results.append(row_of_results)
            return

        reference_word_list = reference_phrase.translate(self.translator).lower().split()
        spoken_word_list    = interpreted_phrase.translate(self.translator).lower().split()

        comparison_results = compareWordLists(reference_word_list, spoken_word_list)

        inserted_words      = comparison_results[CONSTANTS.INSERTED_WORD_COUNT]
        substituted_words   = comparison_results[CONSTANTS.SUBSTITUED_WORD_COUNT]
        deleted_words       = comparison_results[CONSTANTS.DELETED_WORD_COUNT]
        total_words         = comparison_results[CONSTANTS.TOTAL_WORD_COUNT]

        word_error_rate = (inserted_words + deleted_words + substituted_words) / total_words
        word_accuracy   = (total_words - deleted_words - substituted_words) / total_words

        # print("reference - " + reference_phrase)
        # print(self.label + " - " + interpreted_phrase)
        #
        # print("Word error rate - " + str(word_error_rate))
        # print("Word accuracy --- " + str(word_accuracy))

        # TODO: Add confidence when possible
        row_of_results = [phrase_dict[CONSTANTS.ID], phrase_dict[CONSTANTS.PHRASE], inserted_words, substituted_words, deleted_words, word_accuracy, word_error_rate, interpreted_phrase]
        self.results.append(row_of_results)

    def printResults(self, subject_results_folder):
        organized_list = self.sortResults(self.results)

        output_file_name = subject_id + "_" + self.label.lower() + ".csv"
        output_file_name_with_path = subject_results_folder + output_file_name
        output_file = open(output_file_name_with_path, 'w', newline='')

        

        with output_file:
            writer = csv.writer(output_file)
            writer.writerow(self.csv_header)
            writer.writerows(organized_list)

        output_file.close()

    def recognizeAudio(self):
        raise NotImplementedError

    def sortResults(self, unsorted_list):
        sorted_list = list()

        while len(unsorted_list) > 0:
            lowest_row = unsorted_list[0]
            lowest_row_id_split = lowest_row[0]
            replace = True

            for row in unsorted_list:
                raw_id = row[0]
                split_id = re.split('(\d+)', raw_id*1000)

                for id_segment, lowest_id_segment in zip(split_id, lowest_row_id_split):
                    if id_segment > lowest_id_segment:
                        replace = False
                        break;

                if replace:
                    lowest_row = row
                    lowest_row_id_split = split_id

            sorted_list.append(lowest_row)
            unsorted_list.remove(lowest_row)

        return sorted_list


class Sphinx(SpeechRecognizer):
    def __init__(self):
        super().__init__()
        self.label = "sphinx"

    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_sphinx(audio)
        except:
            return None


class Google(SpeechRecognizer):
    def __init__(self):
        super().__init__()
        self.label = "google"

    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_google(audio)
        except:
            return None


class GoogleCloud(SpeechRecognizer):
    def __init__(self, json_key):
        super().__init__()
        self.label = "google_cloud"
        self.json_key = json_key

    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_google_cloud(audio, credentials_json=self.json_key)
        except:
            return None


class Bing(SpeechRecognizer):
    def __init__(self, key):
        super().__init__()
        self.label = "bing"
        self.key = key

    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_bing(audio, key=self.key)
        except:
            return None


class Houndify(SpeechRecognizer):
    def __init__(self, id, key):
        super().__init__()
        self.label = "houndify"
        self.id = id  # Houndify client IDs are Base64-encoded strings
        self.key = key  # Houndify client keys are Base64-encoded strings

    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_houndify(audio, client_id=self.id, client_key=self.key)
        except:
            return None


class IBM(SpeechRecognizer):
    def __init__(self, username, password):
        super().__init__()
        self.label = "ibm"
        self.username = username  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        self.password = password  # IBM Speech to Text passwords are mixed-case alphanumeric strings

    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_ibm(audio, username=self.username, password=self.password)
        except:
            return None


class WitAi(SpeechRecognizer):
    def __init__(self, key):
        super().__init__()
        self.label = "wit_ai"
        self.key = key  # Wit.ai keys are 32-character uppercase alphanumeric strings

    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_wit(audio, key=self.key)
        except:
            return None

        return ""

def signal_handler(sig, frame):
        for recognizer in speech_recognizer_list:
            recognizer.printResults(subject_results_folder)
        sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    results_folder = "Results/"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    recognition = speech_recognition.Recognizer()

    speech_recognizer_list = list()
    speech_recognizer_list.append(Sphinx())
    speech_recognizer_list.append(Google())
    
    #if api_keys[CONSTANTS.GOOGLE_CLOUD_JSON]:
        #speech_recognizer_list.append(GoogleCloud(json.dumps(api_keys[CONSTANTS.GOOGLE_CLOUD_JSON])))
    if api_keys[CONSTANTS.BING_SPEECH]:
        speech_recognizer_list.append(Bing(api_keys[CONSTANTS.BING_SPEECH]))
    #if api_keys[CONSTANTS.HOUNDIFY_ID] and api_keys[CONSTANTS.HOUNDIFY_KEY]:
        #speech_recognizer_list.append(Houndify(api_keys[CONSTANTS.HOUNDIFY_ID], api_keys[CONSTANTS.HOUNDIFY_KEY]))
    #if api_keys[CONSTANTS.IBM_USERNAME] and api_keys[CONSTANTS.IBM_PASSWORD]:
       # speech_recognizer_list.append(IBM(api_keys[CONSTANTS.IBM_USERNAME], api_keys[CONSTANTS.IBM_PASSWORD]))
    if api_keys[CONSTANTS.WIT_AI]:
        speech_recognizer_list.append(WitAi(api_keys[CONSTANTS.WIT_AI]))

    subject_results_folder = ""


    while True:
        subject_id = input("Please enter your subject id: ")
        subject_results_folder = results_folder + str(subject_id) + "/"
        if os.path.exists(subject_results_folder):
            print("Subject already exists! Please try another id.")
            continue
        else:
            os.makedirs(subject_results_folder)
            break

    prepared_phrases_dict_list = phrases * phrase_repeats
    random.shuffle(prepared_phrases_dict_list)

    for phrase_dict in prepared_phrases_dict_list:
        reference_phrase = phrase_dict[CONSTANTS.PHRASE]


        with speech_recognition.Microphone() as source:
            print("Please say: " + reference_phrase)
            recorded_audio = recognition.listen(source)

        audio_file_name = ""
        file_name_counter = 0
        while True:
            file_name_counter += 1
            audio_file_name = subject_results_folder + phrase_dict[CONSTANTS.ID] + "_" + str(file_name_counter) + ".wav"
            if not os.path.isfile(audio_file_name):
                break;

        wav_data = recorded_audio.get_wav_data()
        output_file = wave.open(audio_file_name, 'wb')
        output_file.setnchannels(1)
        output_file.setsampwidth(recorded_audio.sample_width)
        output_file.setframerate(recorded_audio.sample_rate)
        output_file.writeframes(wav_data)
        output_file.close()

        for recognizer in speech_recognizer_list:
            interpreted_phrase = recognizer.recognizeAudio(recorded_audio)
            recognizer.calculateScores(reference_phrase, interpreted_phrase)


    for recognizer in speech_recognizer_list:
        recognizer.printResults(subject_results_folder)
