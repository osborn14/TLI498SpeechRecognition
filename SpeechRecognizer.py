# !/usr/bin/env python3
import json, string, queue, csv, time, random, re, wave, pyaudio, os, signal, sys


import Config as Config
from Phrases import phrases, phrase_repeats
from WordErrorRate import compareWordLists

import Constants as CONSTANTS

import speech_recognition as speech_recognition


if __name__ == '__main__':
    results_folder = "Results/"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    recognition = speech_recognition.Recognizer()

    subject_results_folder = ""

    while True:
        subject_id = input("Please enter your subject id: ")

        try:
            subject_results_folder = results_folder + str(subject_id) + "_" + Config.physical_microphone_name + "/"
        except AttributeError:
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

            print("Before microphone")
            recorded_audio = recognition.listen(source)
            print("After microphone")

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

