import os, csv

from Phrases import phrases
import Constants as CONSTANTS


class Phrase:
    def __init__(self, id):
        self.id = id
        self.results = list()

    def gatherAllFloatValuesByKey(self, key):
        results_without_nulls = list(filter(lambda result: result[key] is not None, self.results))
        return list(map(lambda result: float(result[key]), results_without_nulls))


class API:
    def __init__(self, name):
        self.name = name
        self.results = list()
        self.results_by_phrase = list()
        self.phrase_dict_list = list()

    def printResults(self, output_path):
        output_file_name = self.name.lower() + "_complete" + ".csv"
        output_file_name_with_path = output_path + output_file_name
        # output_file_str = open(output_file_name_with_path, 'w', newline='')

        with open(output_file_name_with_path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, self.results[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(self.results)

        output_file.close()

    def printSummary(self, output_path):
        output_file_name = self.name.lower() + "_summary" + ".csv"
        output_file_name_with_path = output_path + output_file_name

        with open(output_file_name_with_path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, self.phrase_dict_list[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(self.phrase_dict_list)

        output_file.close()

    def gatherSummaryByPhrase(self):
        for result in self.results:
            phrase_id = result[CONSTANTS.ID]

            if not self.findIfPhraseExistsAlready(phrase_id):
                self.results_by_phrase.append(Phrase(phrase_id))

            for phrase in self.results_by_phrase:
                if phrase.id == phrase_id:
                    phrase.results.append(result)

        for phrase in self.results_by_phrase:
            word_error_rate_list = phrase.gatherAllFloatValuesByKey(CONSTANTS.WORD_ERROR_RATE)
            mean_word_error_rate = sum(word_error_rate_list) / len(word_error_rate_list)

            word_accuracy_list = phrase.gatherAllFloatValuesByKey(CONSTANTS.WORD_ACCURACY)
            mean_word_accuracy = sum(word_accuracy_list) / len(word_accuracy_list)

            results_counted = len(word_error_rate_list)

            phrase_dict = {
                CONSTANTS.ID: phrase.id,
                CONSTANTS.RESULTS_COUNTED: results_counted,
                CONSTANTS.MEAN_WORD_ACCURACY: mean_word_accuracy,
                CONSTANTS.MEAN_WORD_ERROR_RATE: mean_word_error_rate
            }

            self.phrase_dict_list.append(phrase_dict)


    def findIfPhraseExistsAlready(self, id):
        for phrase in self.results_by_phrase:
            if phrase.id == id:
                return True

        return False


def findIfClassExistsAlready(temp_api_list, api_name):
    for api_class in temp_api_list:
        if api_class.name == api_name:
            return True

    return False


if __name__ == '__main__':
    results_path = "PostResults/"
    csv_header = ["Id", "Prompted Phrase", "Interpreted Phrase", "I", "S", "D", "WA", "WER"]
    api_list = list()

    # TODO: Throw a notice if data is invalid
    for subject_folder in os.listdir(results_path):
        subject_folder_path = results_path + subject_folder + "/"

        if not os.path.isdir(subject_folder_path):
            continue

        for csv_file_str in os.listdir(subject_folder_path):
            csv_file_path = subject_folder_path + "/" + csv_file_str

            if csv_file_str[-4:] != ".csv":
                continue

            csv_file_split = csv_file_str.split(".")
            csv_file_api = csv_file_split[0]

            if not findIfClassExistsAlready(api_list, csv_file_api):
                api_list.append(API(csv_file_api))

            # audio_file_pass = audio_file_split[1]

            # reference_phrase_dict = None
            single_subject_results_list = list()

            with open(csv_file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                # next(csv_reader)

                for row in csv_reader:
                    # results_dict[CONSTANTS.SUBJECT] = subject_folder
                    # results_dict = {key: value for (key, value) in zip(csv_header, row)}

                    results_dict = {
                        CONSTANTS.SUBJECT: subject_folder,
                        CONSTANTS.ID: row[CONSTANTS.ID],
                        CONSTANTS.PROMPTED_PHRASE: row[CONSTANTS.PROMPTED_PHRASE],
                        CONSTANTS.SPEECH_TO_TEXT: row[CONSTANTS.INTERPRETED_PHRASE],
                        CONSTANTS.I: row[CONSTANTS.I],
                        CONSTANTS.S: row[CONSTANTS.S],
                        CONSTANTS.D: row[CONSTANTS.D],
                        CONSTANTS.WORD_ACCURACY: row[CONSTANTS.WA],
                        CONSTANTS.WORD_ERROR_RATE: row[CONSTANTS.WER]
                    }

                    # print(row)
                    # print(results_dict)
                    single_subject_results_list.append(results_dict)

            csv_file.close()

            for api in api_list:
                if api.name == csv_file_api:
                    for row in single_subject_results_list:
                        api.results.append(row)

    summary_dict = dict()
    for api in api_list:
        api.printResults(results_path)
        api.gatherSummaryByPhrase()
        api.printSummary(results_path)

