#!/usr/bin/env python3
import json, string, threading, queue, csv, time

from Config import api_keys
from Phrases import phrases
from WordErrorRate import compareWordLists

import Settings as SETTINGS
import Constants as CONSTANTS

import speech_recognition as speech_recognition

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class SpeechRecognizer:
    def __init__(self):
        self.results = list()
        self.results.append(["Id", "WA", "WER"])
        self.label = "generic"
        self.audio_queue = queue.Queue()

    # def recognizeAudio(self, audio):
    #     self.audio_queue.put(audio)
    #     self._recognizeAudio()

    def calculateScores(self, reference_word_list, spoken_phrase):
        spoken_word_list = spoken_phrase.lower().split()

        comparison_results = compareWordLists(reference_word_list, spoken_word_list)

        inserted_words = comparison_results[CONSTANTS.INSERTED_WORD_COUNT]
        substituted_words = comparison_results[CONSTANTS.SUBSTITUED_WORD_COUNT]
        deleted_words = comparison_results[CONSTANTS.DELETED_WORD_COUNT]
        total_words = comparison_results[CONSTANTS.TOTAL_WORD_COUNT]

        word_error_rate = (inserted_words + deleted_words + substituted_words) / total_words
        word_accuracy = (total_words - deleted_words - substituted_words) / total_words

        print("Phrase - " + phrase_str.translate(translator))
        print("Sphinx - " + spoken_phrase)

        print("Word error rate - " + str(word_error_rate))
        print("Word accuracy --- " + str(word_accuracy))

        row_of_results = [phrase_dict[CONSTANTS.ID], word_accuracy, word_error_rate]
        self.results.append(row_of_results)

    def printResults(self):
        output_file_name = subject_id + "_" + self.label.lower() + ".csv"
        output_file = open(output_file_name, 'w')
        with output_file:
            writer = csv.writer(output_file)
            writer.writerows(self.results)


    # def _recognizeAudio(self):
    #     while True:
    @threaded
    def run(self):
        while True:
            if not self.audio_queue.empty():
                audio_data = self.audio_queue.get()
                if audio_data[CONSTANTS.COMMAND] == CONSTANTS.RECOGNIZE_AUDIO:
                    spoken_phrase = self.recognizeAudio(audio_data[CONSTANTS.AUDIO_DATA])
                    self.calculateScores(audio_data[CONSTANTS.PHRASE], spoken_phrase)

                elif audio_data[CONSTANTS.COMMAND] == CONSTANTS.PRINT_AND_QUIT:
                    self.printResults()
                    break;

            time.sleep(.1)




class Sphinx(SpeechRecognizer):
    def __init__(self):
        super().__init__()
        self.label = "sphinx"

    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_sphinx(audio)
        except speech_recognition.UnknownValueError:
            return ""
        except speech_recognition.RequestError as e:
            return None

        return ""


class Google():
    def __init__(self):
        super().__init__()
        self.label = "google"

    @threaded
    def recognizeAudio(self, audio):
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            return recognition.recognize_google(audio)
        except speech_recognition.UnknownValueError:
            return ""
        except speech_recognition.RequestError as e:
            return None

        return ""


class GoogleCloud():
    def __init__(self, api_key_json):
        super().__init__()
        self.label = "google_cloud"
        self.api_key_json = api_key_json

    @threaded
    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_google_cloud(audio, credentials_json=self.api_key_json)
        except speech_recognition.UnknownValueError:
            return ""
        except speech_recognition.RequestError as e:
            return None

        return ""

class Bing():
    def __init__(self, key):
        super().__init__()
        self.label = "bing"
        self.key = api_keys[SETTINGS.BING_SPEECH]

    @threaded
    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_bing(audio, key=self.key)
        except speech_recognition.UnknownValueError:
            return ""
        except speech_recognition.RequestError as e:
            return None

        return ""


class Houndify():
    def __init__(self, id, key):
        super().__init__()
        self.label = "houndify"
        self.id = id  # Houndify client IDs are Base64-encoded strings
        self.key = key  # Houndify client keys are Base64-encoded strings

    @threaded
    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_houndify(audio, client_id=self.id, client_key=self.key)
        except speech_recognition.UnknownValueError:
            return ""
        except speech_recognition.RequestError as e:
            return None

        return ""


class IBM():
    def __init__(self, username, password):
        super().__init__()
        self.label = "ibm"
        self.username = username # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        self.password = password  # IBM Speech to Text passwords are mixed-case alphanumeric strings

    @threaded
    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_ibm(audio, username=self.username, password=self.password)
        except speech_recognition.UnknownValueError:
            return ""
        except speech_recognition.RequestError as e:
            return None

        return ""


class WitAi():
    def __init__(self, key):
        super().__init__()
        self.label = "wit_ai"
        self.key = key  # Wit.ai keys are 32-character uppercase alphanumeric strings

    @threaded
    def recognizeAudio(self, audio):
        try:
            return recognition.recognize_wit(audio, key=self.key)
        except speech_recognition.UnknownValueError:
            return ""
        except speech_recognition.RequestError as e:
            return None

        return ""


if __name__ == '__main__':
    # obtain audio SpeechRecognizer.py:107 the microphone
    recognition = speech_recognition.Recognizer()

    speech_recognizer_list = list()
    speech_recognizer_list.append(Sphinx())
    # speech_recognizer_list.append(Google())
    # speech_recognizer_list.append(GoogleCloud(json.dumps(api_keys[SETTINGS.GOOGLE_CLOUD_JSON])))
    # speech_recognizer_list.append(Bing(api_keys[SETTINGS.BING_SPEECH]))
    # speech_recognizer_list.append(Houndify(api_keys[SETTINGS.HOUNDIFY_ID], api_keys[SETTINGS.HOUNDIFY_KEY]))
    # speech_recognizer_list.append(IBM(api_keys[SETTINGS.IBM_USERNAME], api_keys[SETTINGS.IBM_PASSWORD]))
    # speech_recognizer_list.append(WitAi(api_keys[SETTINGS.WIT_AI]))

    for recognizer in speech_recognizer_list:
        recognizer.run()

    translator = str.maketrans('', '', string.punctuation)

    subject_id = input("Please enter your subject id: ")
    recognizer_results = list()
    #TODO: Create seperate "recognizer_results" per object

    for phrase_dict in phrases:
        phrase_str = phrase_dict[CONSTANTS.PHRASE]
        reference_word_list = phrase_str.translate(translator).lower().split()

        with speech_recognition.Microphone() as source:
            print("Please say: " + phrase_str)
            recorded_audio = recognition.listen(source)
            #TODO: Print out audio to file

        audio_dict = {
            CONSTANTS.COMMAND: CONSTANTS.RECOGNIZE_AUDIO,
            CONSTANTS.PHRASE: reference_word_list,
            CONSTANTS.AUDIO_DATA: recorded_audio
        }

        for recognizer in speech_recognizer_list:
            spoken_phrase = recognizer.audio_queue.put(audio_dict)

    quit_dict = {
        CONSTANTS.COMMAND: CONSTANTS.PRINT_AND_QUIT
    }

    for recognizer in speech_recognizer_list:
        recognizer.audio_queue.put(quit_dict)








