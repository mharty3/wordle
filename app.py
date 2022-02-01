from numpy import can_cast
import streamlit as st


def parse_word(guess, response):
    cant_contain = []
    wrong_spot = {}
    right_spot = {}
    for i, (c, r) in enumerate(zip(guess, response)):
        if r == 'b':
            cant_contain.append(c)

        if r == 'y':
            if c in wrong_spot:
                wrong_spot[c].append(i)
            else:
                wrong_spot[c] = [i]

        if r == 'g':
            right_spot[i] = c
    return cant_contain, wrong_spot, right_spot


def filter_words(wordlist, rules):
    cant_contain = rules[0]
    wrong_spot = rules[1]
    right_spot = rules[2]
    # filter out blacks
    wordlist = [word for word in wordlist if not any(char in word for char in cant_contain)]
    
    for char, indexes in wrong_spot.items():
        for i in indexes:
            wordlist = [w for w in wordlist if char in w and list(w)[i] != char]
    
    for idx, char in right_spot.items():
        print(idx, char)
        wordlist = [word for word in wordlist if list(word)[idx] == char]
    
    return wordlist



st.title('Wordle Hints')
st.sidebar.write('Michael Harty')
guess1 = st.text_input('what was your first guess?')
if guess1:
    assert len(guess1) == 5

st.markdown(body="""
Enter the game's response using
  * "g" to indicate 🟩
  * "y" to indicate 🟨
  * "b" to indicate ⬛

For example: if you got ⬛🟨⬛🟩🟩 enter bybbg""")
response1 = st.text_input("Enter the game's response")
if response1:
    assert len(response1) == 5
    assert set(response1).issubset(set('byg'))

emoji_map = {'b': '⬛', 'y': '🟨', 'g': '🟩'}
table = str.maketrans(emoji_map)
st.write(response1.translate(table))


wordlist = open('sorted_words.txt').readlines()
rules = parse_word(guess1, response1)
if response1:
    st.write('## Some good next guesses:')
    for word in filter_words(wordlist, rules)[:5]:
        st.write(word)