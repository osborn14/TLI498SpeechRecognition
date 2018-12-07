import csv

from SpeechToText import SpeechRecognizer

if __name__ == '__main__':
    results_path = "Results/"

    #print(os.listdir(results_path))
    for subject_folder in os.listdir(results_path):
        subject_folder_path = results_path + subject_folder + "/"
        results_list = list()

        #print(os.listdir(audio_folder_path))
        for csv_file in os.listdir(subject_folder_path):
            if csv_file[-4:] != ".csv":
                continue

            audio_file_split = audio_file.split("_")
            audio_file_phrase_id = audio_file_split[0]
            audio_file_pass = audio_file_split[1]

            reference_phrase_dict = None

            with open('example.csv') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')
                next(csv_reader)

                speech_recognizer = SpeechRecognizer()
				
                for row in csv_reader:
                    results_dict = {key: value for (key, value) in zip(key_list, value_list)}
                    print(row)
                    print(row[0])
                    print(row[0], row[1], row[2])
                    results_list(results_dict)
					
					for 
					
				
					speech_recognizer.calculateScores(phrase_dict, new_interpreted_phrase)
					
				recognizer.printResults(audio_folder_path, "_cleaned")