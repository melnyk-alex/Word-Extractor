#!./fw/bin/python

import re
import requests

# CONFIGURATION
MIN_ENTER_SYMBS = 2

MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 5

OVERLAP_LENGTH  = 1

# CHECK CONFIG
if MIN_ENTER_SYMBS < OVERLAP_LENGTH:
    OVERLAP_LENGTH = MIN_ENTER_SYMBS

if __name__ == '__main__':
    word_patt = re.compile('<a href="/word/[\w/^"]+">(?P<word>[\w]+)</a>', re.MULTILINE)

    input_word = ''

    while len(input_word) < MIN_ENTER_SYMBS:
        input_word = input('Type a word longer than [' + str(MIN_ENTER_SYMBS) + '] chars: ')

        if len(input_word) < MIN_ENTER_SYMBS:
            print('Entered word is low.')

    print('PRE WORDS =-=-=-=-=-=-=-=-=-=-=', 'ends with', input_word[:OVERLAP_LENGTH:])
    post_resp = requests.get('http://www.wordfind.com/ends-with/' + input_word[:OVERLAP_LENGTH:] + '/')

    for index, m in enumerate(word_patt.finditer(post_resp.text)):
        found_word = m.group('word').lower()

        if MIN_WORD_LENGTH <= len(found_word) <= MAX_WORD_LENGTH:
            print(found_word + input_word[OVERLAP_LENGTH::], end=" " if index % 5 else "\n")

    print('POST WORDS =-=-=-=-=-=-=-=-=-=-=', 'starts with', input_word[-OVERLAP_LENGTH::])
    pre_resp = requests.get('http://www.wordfind.com/starts-with/' + input_word[-OVERLAP_LENGTH::] + '/')

    for index, m in enumerate(word_patt.finditer(pre_resp.text)):
        found_word = m.group('word').lower()

        if MIN_WORD_LENGTH <= len(found_word) <= MAX_WORD_LENGTH:
            print(input_word[:-OVERLAP_LENGTH:] + found_word, end=" " if index % 5 else "\n")