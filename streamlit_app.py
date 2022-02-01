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
    
    wordlist = [word for word in wordlist if all(list(word)[idx] == char for idx, char in right_spot.items())]
    
    return wordlist


st.set_page_config(page_title='🟩🟩🟩🟩🟩', initial_sidebar_state='collapsed')
st.title('Wordle Hints')
st.sidebar.markdown("""
Michael Harty

[Code Repo](https://github.com/mharty3/wordle/tree/master)""")

guess1 = st.text_input('what was your first guess?')
if guess1:
    guess1 = guess1.lower().strip()
    assert len(guess1) == 5

st.markdown(body="""
Enter the game's response using
  * "g" to indicate 🟩
  * "y" to indicate 🟨
  * "b" to indicate ⬛

For example: if you got ⬛🟨⬛🟩🟩 enter bybgg""")

response1 = st.text_input("Enter the game's response")
if response1:
    response1 = response1.lower().strip()
    assert len(response1) == 5
    assert set(response1).issubset(set('byg'))

emoji_map = {'b': '⬛', 'y': '🟨', 'g': '🟩'}
table = str.maketrans(emoji_map)
st.write(response1.translate(table))


wordlist = open('sorted_words.txt').readlines()
rules1 = parse_word(guess1, response1)
if guess1 and response1:
    st.write('## Some good second guesses:')
    wordlist = filter_words(wordlist, rules1)
    for word in wordlist[:5]:
        st.write(word)


    guess2 = st.text_input('what was your second guess?')
    if guess2:
        guess2 = guess2.lower().strip()
        assert len(guess2) == 5
        
    response2 = st.text_input("Enter the game's second response")
    if response2:
        response2 = response2.lower().strip()
        assert len(response2) == 5
        assert set(response2).issubset(set('byg'))
        st.write(response1.translate(table))
        st.write(response2.translate(table))
        

if response1 and guess2 and response2:
    rules2 = parse_word(guess2, response2)
    st.write(rules2)
    st.write(wordlist)
    st.write('## Some good third guesses:')
    wordlist = filter_words(wordlist, rules2)
    st.write(wordlist)
    for word in wordlist[:5]:
        st.write(word)