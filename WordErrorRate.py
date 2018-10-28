# Code was taken from:
# https://github.com/zszyellow/WER-in-python
# Variable names have been changed for readability

import sys, numpy
import Constants as CONSTANTS

def editDistance(reference_word_list, hypothesis_word_list):
    distance = numpy.zeros((len(reference_word_list) + 1) * (len(hypothesis_word_list) + 1), dtype=numpy.uint8).reshape(
        (len(reference_word_list) + 1, len(hypothesis_word_list) + 1))

    for reference_word_count in range(len(reference_word_list) + 1):
        for hypothesis_word_count in range(len(hypothesis_word_list) + 1):
            if reference_word_count == 0:
                distance[0][hypothesis_word_count] = hypothesis_word_count
            elif hypothesis_word_count == 0:
                distance[reference_word_count][0] = reference_word_count

    for reference_word_count in range(1, len(reference_word_list) + 1):
        for hypothesis_word_count in range(1, len(hypothesis_word_list) + 1):
            if reference_word_list[reference_word_count - 1] == hypothesis_word_list[hypothesis_word_count - 1]:
                distance[reference_word_count][hypothesis_word_count] = distance[reference_word_count - 1][hypothesis_word_count - 1]
            else:
                substitute  = distance[reference_word_count - 1][hypothesis_word_count - 1] + 1
                insert      = distance[reference_word_count][hypothesis_word_count - 1] + 1
                delete      = distance[reference_word_count - 1][hypothesis_word_count] + 1

                distance[reference_word_count][hypothesis_word_count] = min(substitute, insert, delete)

    return distance


def compareWordLists(reference_word_list, hypothesis_word_list, distance=None):
    if distance is None:
        distance = editDistance(reference_word_list, hypothesis_word_list)

    x = len(reference_word_list)
    y = len(hypothesis_word_list)

    inserted_word_count = substituted_word_count = deleted_word_count = 0

    while True:
        if x == 0 and y == 0:
            break
        elif x >= 1 and y >= 1 and distance[x][y] == distance[x-1][y-1] and reference_word_list[x-1] == hypothesis_word_list[y-1]:
            x = x - 1
            y = y - 1
        elif y >= 1 and distance[x][y] == distance[x][y-1]+1:
            inserted_word_count += 1
            x = x
            y = y - 1
        elif x >= 1 and y >= 1 and distance[x][y] == distance[x-1][y-1]+1:
            substituted_word_count += 1
            x = x - 1
            y = y - 1
        else:
            deleted_word_count += 1
            x = x - 1
            y = y

    comparison_results = {
        CONSTANTS.INSERTED_WORD_COUNT: inserted_word_count,
        CONSTANTS.SUBSTITUED_WORD_COUNT: substituted_word_count,
        CONSTANTS.DELETED_WORD_COUNT: deleted_word_count,
        CONSTANTS.TOTAL_WORD_COUNT: len(reference_word_list)
    }

    return comparison_results
