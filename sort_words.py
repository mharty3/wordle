from collections import Counter
with open('wordlist.txt') as f:
    letters = f.read().replace('\n', '')
    f.seek(0)
    words = f.readlines()

c = Counter(letters)

def score_word(word, c):
    score = 0
    for l in set(word):
        score += c[l]
    return score


words.sort(key=lambda x: score_word(x, c), reverse=True)

with open('sorted_words.txt', 'w') as f:
    f.writelines(words)