#!/usr/bin/env python3
import json

from Config import api_keys
import Settings as SETTINGS

from pprint import pprint
import speech_recognition as sr


class Sphinx():
    def recognizeAudio(self, audio):
        try:
            print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

class Google():
    def recognizeAudio(self, audio):
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Google Speech Recognition results:")
            pprint(r.recognize_google(audio, show_all=True))  # pretty-print the recognition resul
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

class GoogleCloud():
    def __init__(self, api_key_json):
        self.api_key_json = api_key_json

    def recognizeAudio(self, audio):
        try:
            print("Google Cloud Speech recognition results:")
            pprint(r.recognize_google_cloud(audio, credentials_json=self.api_key_json, show_all=True))
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))

class Bing():
    def __init__(self, key):
        self.key = api_keys[SETTINGS.BING_SPEECH]

    def recognizeAudio(self, audio):
        try:
            print("Bing recognition results:")
            pprint(r.recognize_bing(audio, key=self.key, show_all=True))
        except sr.UnknownValueError:
            print("Microsoft Bing Voice Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

class Houndify():
    def __init__(self, id, key):
        self.id = id  # Houndify client IDs are Base64-encoded strings
        self.key = key  # Houndify client keys are Base64-encoded strings

    def recognizeAudio(self, audio):
        try:
            print("Houndify recognition results:")
            pprint(r.recognize_houndify(audio, client_id=self.id, client_key=self.key, show_all=True))
        except sr.UnknownValueError:
            print("Houndify could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Houndify service; {0}".format(e))

class IBM():
    def __init__(self, username, password):
        self.username = username # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        self.password = password  # IBM Speech to Text passwords are mixed-case alphanumeric strings

    def recognizeAudio(self, audio):
        try:
            print("IBM Speech to Text results:")
            pprint(r.recognize_ibm(audio, username=self.username, password=self.password,
                                   show_all=True))  # pretty-print the recognition result
        except sr.UnknownValueError:
            print("IBM Speech to Text could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from IBM Speech to Text service; {0}".format(e))

class WitAi():
    def __init__(self, key):
        self.key = key  # Wit.ai keys are 32-character uppercase alphanumeric strings

    def recognizeAudio(self, audio):
        try:
            print("Wit.ai recognition results:")
            pprint(r.recognize_wit(audio, key=self.key, show_all=True))
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))



if __name__ == '__main__':
    # obtain audio SpeechRecognizer.py:107 the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        recorded_audio = r.listen(source)

    speech_recognizer_list = list()
    speech_recognizer_list.append(Sphinx())
    speech_recognizer_list.append(Google())
    speech_recognizer_list.append(GoogleCloud(json.dumps(api_keys[SETTINGS.GOOGLE_CLOUD_JSON])))
    speech_recognizer_list.append(Bing(api_keys[SETTINGS.BING_SPEECH]))
    speech_recognizer_list.append(Houndify(api_keys[SETTINGS.HOUNDIFY_ID], api_keys[SETTINGS.HOUNDIFY_KEY]))
    speech_recognizer_list.append(IBM(api_keys[SETTINGS.IBM_USERNAME], api_keys[SETTINGS.IBM_PASSWORD]))
    speech_recognizer_list.append(WitAi(api_keys[SETTINGS.WIT_AI]))

    for recognizer in speech_recognizer_list:
        recognizer.recognizeAudio(recorded_audio)
