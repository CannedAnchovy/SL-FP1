import pandas as pd
import numpy as np
import jieba
import json
from argparse import ArgumentParser
from collections import Counter

parser = ArgumentParser()
parser.add_argument("-i", "--input_file", dest = "input_file", help = "Pass in a .xlsx filename.")
parser.add_argument("-o", "--output_file", dest = "output_file", help = "Pass in a .json filename.")
parser.add_argument("-n", "--corpus_num", dest = "corpus_num", help = "Pass in 1 or 2.")
parser.add_argument("-m", "--cut_method", dest = "cut_method", help = "Pass in jieba or brute.")
args = parser.parse_args()

def jieba_cut(str):
    ret = list(jieba.cut(str))
    if len(str) <= 3:
        ret.append(str)
    return ret

def brute_cut(str, max_window=3):
    ret = []
    for window in range(1, max_window+1):
        if len(str) >= window:
            for i in range(len(str) - window + 1):
                ret.append(str[i:i+window])
    return ret

train = np.array(pd.read_excel(args.input_file))

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
# define corpus
corpus = {}
corpus["name"] = "行業corpus"
corpus["total_size"] = 0
corpus["vocab_size"] = 0
corpus["data_count"] = len(train)
label_count = {}
inverted_file = {}

line_num = 0
for id, label1, label2, x1, x2, x3, x4, x5, fix in train:

    if args.corpus_num == "1":
        label = label1
        feature_set = [x1, x2]
    elif args.corpus_num == "2":
        label = label2
        feature_set = [x3, x4, x5]

    if args.cut_method == "jieba":
        cut_method = jieba_cut
    elif args.cut_method == "brute":
        cut_method = brute_cut

    print(id, label, feature_set)

    # label
    if label not in label_count:
        label_count[label] = 1
    else:
        label_count[label] += 1

    # word
    word_count = Counter()
    for x in feature_set:
        words = [word.lower() for word in cut_method(x)]
        word_count.update(words)


    for word, count in word_count.items():
        if word in "無****,./()（），、。？":
            continue
        corpus["total_size"] += count

        # inverted_file
        if word not in inverted_file:
            inverted_file[word] = {}
            inverted_file[word]['count'] = count
            inverted_file[word]['unique_count'] = 1
            inverted_file[word]['docs'] = []
            inverted_file[word]['label_count'] = {}
        else:
            inverted_file[word]['count'] += count
            inverted_file[word]['unique_count'] += 1
        
        doc_dict = {}
        doc_dict["line_num"] = line_num
        doc_dict["count"] = count
        inverted_file[word]['docs'].append(doc_dict)
        if label1 not in inverted_file[word]['label_count']:
            inverted_file[word]['label_count'][label] = 1
        else:
            inverted_file[word]['label_count'][label] += 1
        
    line_num += 1

corpus['vocab_size'] = len(inverted_file)
corpus['label_count'] = label_count
corpus['inverted_file'] = inverted_file


with open(args.output_file, 'w') as file:
    json.dump(corpus, file, indent=2)
