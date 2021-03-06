# !/usr/bin/env python3
import json, string, queue, csv, time, random, re, wave, pyaudio, os, signal, sys, argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Config as Config
from Phrases import phrases, phrase_repeats
from WordErrorRate import compareWordLists

import Constants as CONSTANTS

import speech_recognition as speech_recognition


# TODO: Change SpeechRecognizer file name to match file name
class SpeechRecognizer:
    def __init__(self):
        self.results = list()
        self.csv_header = ["Id", "Prompted Phrase", "Interpreted Phrase", "I", "S", "D", "WA", "WER"]
        self.label = "generic"
        self.translator = str.maketrans('', '', string.punctuation)

    def calculateScores(self, phrase_dict, interpreted_phrase):
        if not interpreted_phrase:
            row_of_results = [phrase_dict[CONSTANTS.ID], phrase_dict[CONSTANTS.PHRASE], 'na', 'na', 'na', 'na']
            self.results.append(row_of_results)
            return

        reference_phrase = phrase_dict[CONSTANTS.PHRASE]

        reference_word_list = reference_phrase.translate(self.translator).lower().split()
        spoken_word_list = interpreted_phrase.translate(self.translator).lower().split()

        comparison_results = compareWordLists(reference_word_list, spoken_word_list)

        inserted_words = comparison_results[CONSTANTS.INSERTED_WORD_COUNT]
        substituted_words = comparison_results[CONSTANTS.SUBSTITUED_WORD_COUNT]
        deleted_words = comparison_results[CONSTANTS.DELETED_WORD_COUNT]
        total_words = comparison_results[CONSTANTS.TOTAL_WORD_COUNT]

        word_error_rate = (inserted_words + deleted_words + substituted_words) / total_words
        word_accuracy = (total_words - deleted_words - substituted_words) / total_words

        # print("reference - " + reference_phrase)
        # print(self.label + " - " + interpreted_phrase)
        #
        # print("Word error rate - " + str(word_error_rate))
        # print("Word accuracy --- " + str(word_accuracy))

        # TODO: Add confidence when possible
        row_of_results = [phrase_dict[CONSTANTS.ID], phrase_dict[CONSTANTS.PHRASE], interpreted_phrase, inserted_words,
                          substituted_words,
                          deleted_words, word_accuracy, word_error_rate]
        self.results.append(row_of_results)

    def printResults(self, subject_results_folder):
        organized_list = self.sortResults(self.results)

        # output_file_name = subject_id + "_" + self.label.lower() + "new.csv"
        output_file_name = self.label.lower() + ".csv"
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
                split_id = re.split('(\d+)', raw_id * 1000)

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

    def recognizeAudio(self, audio, try_count=0):
        try:
            speech_to_text_results = self.recognizeAudioAPICall(audio)
            return speech_to_text_results

        except Exception as e:
            print(self.label + " threw and error!")
            print(str(e))

            if try_count >= 2:
                print("Giving up for now...")
                return None
            else:
                print("Trying again...")
                self.recognizeAudio(audio, try_count + 1)


class Sphinx(SpeechRecognizer):
    def __init__(self):
        super().__init__()
        self.label = "sphinx"

    def recognizeAudioAPICall(self, audio):
        return recognition.recognize_sphinx(audio)


class Google(SpeechRecognizer):
    def __init__(self):
        super().__init__()
        self.label = "google"

    def recognizeAudioAPICall(self, audio):
        return recognition.recognize_google(audio)


class GoogleCloud(SpeechRecognizer):
    def __init__(self, json_key):
        super().__init__()
        self.label = "google_cloud"
        self.json_key = json_key

    def recognizeAudioAPICall(self, audio):
        return recognition.recognize_google_cloud(audio, credentials_json=self.json_key)


class Bing(SpeechRecognizer):
    def __init__(self, key):
        super().__init__()
        self.label = "bing"
        self.key = key

    def recognizeAudioAPICall(self, audio):
        return recognition.recognize_bing(audio, key=self.key)


class Houndify(SpeechRecognizer):
    def __init__(self, id, key):
        super().__init__()
        self.label = "houndify"
        self.id = id  # Houndify client IDs are Base64-encoded strings
        self.key = key  # Houndify client keys are Base64-encoded strings

    def recognizeAudioAPICall(self, audio):
        return recognition.recognize_houndify(audio, client_id=self.id, client_key=self.key)


class IBM(SpeechRecognizer):
    def __init__(self, username, password):
        super().__init__()
        self.label = "ibm"
        self.username = username  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        self.password = password  # IBM Speech to Text passwords are mixed-case alphanumeric strings

    def recognizeAudioAPICall(self, audio):
        return recognition.recognize_ibm(audio, username=self.username, password=self.password)


class WitAi(SpeechRecognizer):
    def __init__(self, key):
        super().__init__()
        self.label = "wit_ai"
        self.key = key  # Wit.ai keys are 32-character uppercase alphanumeric strings

    def recognizeAudioAPICall(self, audio):
        return recognition.recognize_wit(audio, key=self.key)


def signal_handler(sig, frame):
    for recognizer in speech_recognizer_list:
        recognizer.printResults(subject_results_folder)

    print("Exiting")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument('-s', action="store_true", dest="arg_sphinx")
    # parser.add_argument('-g', action="store_true", dest="arg_google")
    # parser.add_argument('-c', action="store_true", dest="arg_google_cloud")
    # parser.add_argument('-b', action="store_true", dest="arg_bing")
    # parser.add_argument('-i', action="store_true", dest="arg_ibm")
    # parser.add_argument('-w', action="store_true", dest="arg_wit")
    #
    # parser_results = parser.parse_args()
    #
    # print(parser_results.arg_sphinx)
    # print(parser_results.arg_bing)
    # print(parser_results.arg_ibm)

    # for i in range(100):
    #     print(str(i), end='\r')
    #     time.sleep(0.5)

    results_path = "SpeechRecognizerResults/"
    if not os.path.exists(results_path):
        print("No results folder found!")
        sys.exit(0)

    recognition = speech_recognition.Recognizer()

    speech_recognizer_list = list()

    # speech_recognizer_list.append(Sphinx())
    # speech_recognizer_list.append(Google())

    # if CONSTANTS.GOOGLE_CLOUD_JSON in Config.api_keys:
    #     speech_recognizer_list.append(GoogleCloud(json.dumps(Config.api_keys[CONSTANTS.GOOGLE_CLOUD_JSON])))
    # if CONSTANTS.BING_SPEECH in Config.api_keys:
    #     speech_recognizer_list.append(Bing(Config.api_keys[CONSTANTS.BING_SPEECH]))
    if CONSTANTS.IBM_USERNAME in Config.api_keys and CONSTANTS.IBM_PASSWORD in Config.api_keys:
        speech_recognizer_list.append(
            IBM(Config.api_keys[CONSTANTS.IBM_USERNAME], Config.api_keys[CONSTANTS.IBM_PASSWORD]))
    # if CONSTANTS.WIT_AI in Config.api_keys:
    #     speech_recognizer_list.append(WitAi(Config.api_keys[CONSTANTS.WIT_AI]))

    for audio_folder in os.listdir(results_path):
        audio_folder_path = results_path + audio_folder + "/"

        if not os.path.isdir(audio_folder_path):
            continue

        # print(os.listdir(audio_folder_path))
        for audio_file in os.listdir(audio_folder_path):
            print("Working on " + audio_file + "...", end='\r')
            if audio_file[-4:] != ".wav":
                continue

            audio_file_split = audio_file.split("_")
            audio_file_phrase_id = audio_file_split[0]
            audio_file_pass = audio_file_split[1]

            reference_phrase_dict = None

            for phrase in phrases:
                if phrase[CONSTANTS.ID] == audio_file_phrase_id:
                    reference_phrase_dict = phrase

            audio_file_path = audio_folder_path + audio_file

            input_file = speech_recognition.AudioFile(audio_file_path)

            with input_file as source:
                audio_sample = recognition.record(source)

            for recognizer in speech_recognizer_list:
                interpreted_phrase = recognizer.recognizeAudio(audio_sample)
                recognizer.calculateScores(reference_phrase_dict, interpreted_phrase)

            print("Done with " + audio_file + "!")

        for recognizer in speech_recognizer_list:
            recognizer.printResults(audio_folder_path)

        print("Done with " + audio_folder)

    print("SpeechToText complete!")
