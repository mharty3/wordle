from numpy import can_cast
import streamlit as st

st.title('Wordle')

guess1 = st.text_input('what did u guess')

response1 = st.text_input('what did it say b for black, y for yellow or g for green')

emoji_map = {'b': '⬛', 'y': '🟨', 'g': '🟩'}
table = str.maketrans(emoji_map)
st.write(response1.translate(table))


def parse_word(guess, response):
    cant_contain = []
    does_contain = []
    locked_in = {}
    for i, (c, r) in enumerate(zip(guess, response)):
        if r == 'b':
            cant_contain.append(c)
        if r == 'y':
            does_contain.append(c)
        if r == 'g':
            locked_in[i] = c
    return cant_contain, does_contain, locked_in



def filter_words(wordlist, rules):
    cant_contain = rules[0]
    does_contain = rules[1]
    locked_in = rules[2]
    wordlist = [word for word in wordlist if not any(char in word for char in cant_contain)]
    if does_contain:
        wordlist = [word for word in wordlist if any(char in word for char in does_contain)]
    
    for idx, char in locked_in.items():
        print(idx, char)
        wordlist = [word for word in wordlist if list(word)[idx] == char]
    
    return wordlist


wordlist = open('wordlist.txt').readlines()
rules = parse_word(guess1, response1)
st.write(rules)
st.write(filter_words(wordlist, rules))