#!/usr/bin/env bash

# generate raw corpus
python3 corpus.py -i train.xlsx -o corpus1-brute.json -n 1 -m brute
python3 corpus.py -i train.xlsx -o corpus1-jieba.json -n 1 -m jieba
python3 corpus.py -i train.xlsx -o corpus2-brute.json -n 2 -m brute
python3 corpus.py -i train.xlsx -o corpus2-jieba.json -n 2 -m jieba

# clean data
python3 process.py -i corpus1-jieba.json -o corpus1-jieba-words.json
python3 process.py -i corpus1-brute.json -o corpus1-brute-words.json
python3 process.py -i corpus2-jieba.json -o corpus2-jieba-words.json
python3 process.py -i corpus2-brute.json -o corpus2-brute-words.json