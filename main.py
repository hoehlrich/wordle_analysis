# !/usr/bin/env
# -*- coding: utf-8 -*-

import json
import string
from json_helpers import *

class Keyboard:
    '''Keyboard Class'''

    def __init__(self):
        self.green = []
        self.yellow = []
        self.grey = list(string.ascii_lowercase)
        self.black = []

        print(self.grey)
    def set_state(self, letter, state, position):
        if state == 'g':
            if (letter, position) not in self.green:
                self.green.append((letter, position))
                try:
                    self.grey.remove(letter)
                except ValueError:
                    pass
        elif state == 'y':
            if (letter, position) not in self.yellow:
                self.yellow.append((letter, position))
                try:
                    self.grey.remove(letter)
                except ValueError:
                    pass
            
        elif state == 'b':
            if not self.in_green(letter):
                self.black.append(letter)
                try:
                    self.grey.remove(letter)
                except ValueError:
                    pass
    
    def in_green(self, letter):
        for current_letter, position in self.green:
            if letter == current_letter:
                return True
        
        return False

    def __str__(self):
        print(f'Green: {self.green}')
        print(f'Yellow: {self.yellow}')
        print(f'Grey: {self.grey}')
        print(f'Black: {self.black}')

        return ''

def trim_words(words, keyboard):
    new_words = list(words)
    
    for word in words:
        # Check if the word has none of the black letters
        for letter in keyboard.black:
            if letter in word:
                new_words.remove(word)
                break
    
    words = list(new_words)
        
    for word in words:
        # Check if the word has all yellow letters
        for letter, position in keyboard.yellow:
            if letter == word[position]:
                new_words.remove(word)
                break

    words = list(new_words)

    for word in words:
        for letter, position in keyboard.green:
            count = 0
            for (current_letter, current_position) in keyboard.green:
                if letter == current_letter:
                    count += 1
            
            if word.count(letter) < count:
                new_words.remove(word)
                break
            elif word.count(letter) == count:
                if word[position] != letter:
                    new_words.remove(word)
                    break
    

    return new_words

def trim_answers(words, keyboard):
    new_words = list(words)
    
    for word in words:
        # Check if the word has none of the black letters
        for letter in keyboard.black:
            if letter in word:
                new_words.remove(word)
                break
    
    words = list(new_words)

    for word in words:
        # Check if the word has all of the greens in the right places
        for letter, position in keyboard.green:
            if word[position] != letter:
                new_words.remove(word)
                break
    
    words = list(new_words)
        
    for word in words:
        # Check if the word has all yellow letters
        for letter, position in keyboard.yellow:
            if letter == word[position]:
                new_words.remove(word)
                break
    
    return new_words


def select_word(words):
    return words[0]

def take_guess_input(word, keyboard):
    for i, letter in enumerate(word):
        state = input(f'What is the color of letter {letter}? ')
        if state not in ['g', 'y', 'b']:
            state = 'b'

        keyboard.set_state(letter, state, i)
    
    return keyboard
        

def main():
    temp = load_asset('Assets/alt_data.json')
    words = []

    for word in temp:
        words.append(word)

    answers = load_asset('Assets/answers.json')['data']

    keyboard = Keyboard()

    for i in range(6):
        word = select_word(words)
        print(f'Enter the word {word}.')
        keyboard = take_guess_input(word, keyboard)
        print(keyboard)
        words = trim_words(words, keyboard)
        answers = trim_answers(answers, keyboard)

        # Check if there is only one answer
        if len(answers) == 1:
            print(f'Enter the word {answers[0]}')
            break

        print(f'Words: {words[:10]}')
        print(f'Answers: {answers[:10]}')


if __name__ == '__main__':
    main()