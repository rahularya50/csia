from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, words
# from PyDictionary import PyDictionary
import pickle as pkl

# Word Embeddings
with open("data/glove.txt", "rb") as f:
    glove = pkl.load(f)

# Suffixes
suffixes = ["ing", "ship", "ed", "ly", "er", "s"]

# Stopword whitelist
whitelist = ["own"]


def filter_tokenize(text):
    for char in punctuation:
        text = text.lower().replace(char, " ")
    tokens = word_tokenize(text)
    for i in range(len(tokens)):
        token = tokens[i]
        for suffix in suffixes:
            if len(token) - len(suffix) < 2:
                continue
            if token[-1 * len(suffix):] == suffix:
                temp = token[:-1 * len(suffix)]
                if temp in words.words('en'):
                    tokens[i] = temp
    return [i for i in tokens if i in glove and len(i) > 1 and (i not in stopwords.words() or i in whitelist)]


def matches(scheme, inp, return_frac=False, match_threshold=0.45, sim_threshold=0.8, debug=False):
    tally = 0
    for token in scheme:
        if " " in token or token not in glove:
            continue
        if token in inp:
            tally += 1
            continue
        mx = 0
        for t in inp:
            if t not in glove:
                continue
            similarity = glove.similarity(t, token)
            if similarity > sim_threshold:
                if debug:
                    print(t, token, similarity)
                if similarity > mx:
                    mx = similarity
        tally += mx
    fraction = tally / max(1, len(scheme))
    if debug:
        print("Final fraction:", fraction)
    if return_frac:
        return fraction, fraction > match_threshold
    return fraction > match_threshold
