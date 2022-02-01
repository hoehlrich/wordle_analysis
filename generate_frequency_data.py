# !/usr/bin/env
# -*- coding: utf-8 -*-

import json
import string
from json_helpers import *

def calculate_score(word, answer):
    '''
    Scores:
    green: 3
    yellow: 2
    grey: 1
    double grey: 0
    '''
    
    score = 0

    # Init letters dict
    letters = {}
    for letter in string.ascii_lowercase:
        letters[letter] = 0
    
    # Green pass
    for i, letter in enumerate(word):
        if letter == answer[i]:
            letters[letter] += 1
            score += 3

    # Yellow pass
    for i, letter in enumerate(word):
        if letter != answer[i]:
            if letters[letter] < answer.count(letter):
                score += 2
                letters[letter] += 1
    
    # Grey pass
    for i, letter in enumerate(word):
        if letter not in answer:
            # Check if it is a repeated grey
            if letters[letter] == 0:
                score += 1
    
    # Remove score for really bad letters
    bad_letters = ['z', 'q', 'x']
    for bad_letter in bad_letters:
        if bad_letter in word:
            score -= 4000

    return score

def main():
    words = load_asset('Assets/words.json')['data']
    answers = load_asset('Assets/answers.json')['data']

    word_data = {}
    for word in words:
        score = 0
        for answer in answers:
            score += calculate_score(word, answer)
        word_data[word] = score
    
    temp = []
    for word, score in word_data.items():
        temp.append((score, word))
    
    temp.sort(reverse=True)

    word_data = {}
    for score, word in temp:
        word_data[word] = score
    

    write_data('Assets/alt_data.json', word_data)
if __name__ == '__main__':
    main()