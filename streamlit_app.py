from numpy import can_cast
import streamlit as st


def parse_word(guess, response):
    """
    Given a word and the games response, generate a tuple of rules

    Parameters:
      guess: str The guess
      response: str the response from the game. Must be one of G, Y or B
          Y - represents yellow
          B - represents black
          G - represents green

    Returns: tuple
    A tuple of rules that contains three items:
        * cant_contain: list of "black" letters that can't be in the word
        * wrong_spot: dict of {str: List[int]} indicating "yellow" letters 
              that are in the word and the indexes of the word they can't be in
        * right_spot: dict {int: str} "green boxes" the index in the word and
              the letter that goes there
    """

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
    """
    Given a list of words and a set of rules, filter the wordlist to only words 
    that follow the rules.

    Parameters:
      wordlist: List[str]
      rules: Tuple[List[str], Dict[str: int], Dict[int: str]]

    Returns: List[str] a filtered list of words

    """
    cant_contain = rules[0]
    wrong_spot = rules[1]
    right_spot = rules[2]

    # filter out letters that don't exist in the word
    wordlist = [word for word in wordlist if not any(char in word for char in cant_contain)]
    
    # filter out words that don't meet the yellow criteria
    for char, indexes in wrong_spot.items():
        for i in indexes:
            wordlist = [w for w in wordlist if char in w and list(w)[i] != char]
    
    # filter words that don't meet green criteria
    wordlist = [word for word in wordlist if all(list(word)[idx] == char for idx, char in right_spot.items())]
    
    return wordlist


emoji_map = {'b': '⬛', 'y': '🟨', 'g': '🟩'}
table = str.maketrans(emoji_map)

st.set_page_config(page_title='🟩🟩🟩🟩🟩', initial_sidebar_state='collapsed')
st.title('Wordle Hints')
st.sidebar.markdown("""
Michael Harty

[Code Repo](https://github.com/mharty3/wordle/tree/master)""")

# guess 1
guess1 = st.text_input('what was your first guess?')
if guess1:
    guess1 = guess1.lower().strip()
    if not len(guess1) == 5:
        st.warning('Guess must be 5 letters long')

st.markdown(body="""
Enter the game's response using
  * "g" to indicate 🟩
  * "y" to indicate 🟨
  * "b" to indicate ⬛

For example: if you got ⬛🟨⬛🟩🟩 enter bybgg""")

response1 = st.text_input("Enter the game's response")
if response1:
    response1 = response1.lower().strip()
    if not len(response1) == 5:
        st.warning('Response must be 5 letters long')

    if not set(response1).issubset(set('byg')):
        st.warning('Response can only contain Y, G, or B')


# write emojis
st.write(response1.translate(table))

# guess 2
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
        if not len(guess2) == 5:
            st.warning('Guess must be 5 letters long')
            
    response2 = st.text_input("Enter the game's second response")
    if response2:
        response2 = response2.lower().strip()
        assert len(response2) == 5
        assert set(response2).issubset(set('byg'))

        # write emojis
        st.write(response1.translate(table))
        st.write(response2.translate(table))
        

    if response2:
        rules2 = parse_word(guess2, response2)
        st.write('## Some good third guesses:')
        wordlist = filter_words(wordlist, rules2)
        for word in wordlist[:5]:
            st.write(word)