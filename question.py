"""
Question Class for storing questions.
"""
from collections import defaultdict
from nlp import filter_tokenize, matches
import numpy as np


# Question structure
class Question:
    def __init__(self, question, qtype, id=None):
        self.question = question
        self.qtype = qtype
        self.id = id
        self.ms = {}

    def __repr__(self):
        return self.question

    def assign_short_ms(self, scheme):
        self.ms = scheme

    def mark_question(self, answer, debug=False):
        answer_tokens = filter_tokenize(answer)
        if debug:
            print(answer_tokens)

        if self.qtype == "definition":
            score_count = np.zeros(3)
            frac_count = np.zeros(3)
            for mark in self.ms.keys():
                if mark == "Do not":
                    continue
                if debug:
                    print("Mark:", mark)
                temp = defaultdict(int)
                temp_frac = defaultdict(int)
                temp[0] = 0
                temp_frac[0] = 0
                scheme = self.ms[mark]
                for i, weight, tokens in scheme:
                    frac, match = matches(tokens, answer_tokens, True, debug=debug)
                    if debug:
                        print("Match:", match, tokens, i)
                    if match:
                        temp[i] += weight * mark
                        temp_frac[i] = frac
                mx = max(temp.values())
                if mx > score_count[mark]:
                    score_count[mark] = mx
                    frac_count[mark] = [temp_frac[i] for i, v in temp.items() if v == mx][0]
            condition = score_count == np.arange(3)
            if debug:
                print(score_count)
                print(score_count[condition])
            mark = np.argmax(score_count[condition])
            donot = matches(answer_tokens, self.ms["Do not"], True, debug=debug)[0] * len(answer_tokens) / max(1, len(
                answer.split()))
            if donot > frac_count[mark]:
                mark = 0
            total = 2

        if self.qtype == "identify":
            tally = 0
            for item in self.ms:
                if debug:
                    print(item)
                match = matches(item, answer_tokens, False, debug=debug)
                if match:
                    tally += 1
            if debug:
                print("Tally:", tally)
            mark = min(2, tally)
            total = 2

        print("Mark:", mark, "out of", total)
        return mark

