import json
import numpy as np
import math
from argparse import ArgumentParser
import operator

parser = ArgumentParser()
parser.add_argument("-i", "--input_file", dest = "input_file", help = "Pass in a .json filename.")
parser.add_argument("-o", "--output_file", dest = "output_file", help = "Pass in a .json filename.")
args = parser.parse_args()

with open(args.input_file) as f:
	corpus = json.load(f)

'''
corpus (data structure)
    - name -> string
    - total_size -> int
    - vocab_size -> int
    - data_count -> int

    - label_count -> dict
        - label -> count

    - inverted_file -> dict
        - word -> dict
            - count -> int
            - unique_count -> int
            - docs -> list
            - label_count -> dict
                - label -> count

'''

# remove the word that appears < 3 times
rm_list = []
for word, data in corpus["inverted_file"].items():
    if data["unique_count"] <= 3:
        corpus["total_size"] -= data["count"]
        corpus["vocab_size"] -= 1
        rm_list.append(word)

for word in rm_list:
    del corpus["inverted_file"][word]

# calculate chi square
N = corpus["data_count"]
label_N = len(corpus["label_count"])

word_scores = dict()
for word, data in corpus["inverted_file"].items():
    prob_term = data["unique_count"] / N

    chisquare_list = np.zeros(label_N)
    index = 0
    for label, count in corpus["label_count"].items():
        prob_label = count / N

        # term and label
        if label not in data["label_count"]:
            obs_term_and_label = 0
        else:
            obs_term_and_label = data["label_count"][label]

        exp_term_and_label = N * prob_term * prob_label
        chisquare_list[index] += math.pow(obs_term_and_label - exp_term_and_label, 2) / exp_term_and_label

        # term and not label
        obs_term_and_not_label = data["unique_count"] - obs_term_and_label
        exp_term_and_not_label = N * prob_term * (1 - prob_label)
        chisquare_list[index] += math.pow(obs_term_and_not_label - exp_term_and_not_label, 2) / exp_term_and_not_label

        # not term and label
        obs_not_term_and_label = count - obs_term_and_label
        exp_not_term_and_label = N * (1 - prob_term) * prob_label
        chisquare_list[index] += math.pow(obs_not_term_and_label - exp_not_term_and_label, 2) / exp_not_term_and_label

        # not term and not label
        obs_not_term_and_not_label = N - obs_not_term_and_label - obs_term_and_not_label - obs_term_and_label
        exp_not_term_and_not_label = N * (1 - prob_term) * (1 - prob_label)
        chisquare_list[index] += math.pow(obs_not_term_and_not_label - exp_not_term_and_not_label, 2) / exp_not_term_and_not_label

        index += 1

    word_scores[word] = np.max(chisquare_list)

sorted_word_scores = sorted(word_scores.items(), key=operator.itemgetter(1), reverse=True)
sorted_word = [item[0] for item in sorted_word_scores]
print(sorted_word)

with open(args.output_file, "w") as file:
    json.dump(sorted_word, file)

    




