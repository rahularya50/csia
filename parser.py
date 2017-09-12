from bs4 import BeautifulSoup
from nlp import filter_tokenize
from collections import defaultdict
import re


def load_html(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
    bs = BeautifulSoup(html)
    text = bs.text
    text = text.replace("â€™", "'")
    text = text.replace("â€“", "-")
    text = text.replace("â€˜", "'")
    text = text.replace("Ã", " ")
    text = text.replace("(cid:127)", "$$BULLET$$")
    return text


def create_id(ms_text):
    ns = ms_text.split('\n')[1].split()
    month_code = "".join([i[0] for i in ns[3].split('/')])
    year, syllabus, paper = ns[4:]
    return "_".join([month_code, year, syllabus, paper])


def num_questions(ms_text):
    regex = re.compile("\([a-h]\)")
    return len(list(regex.finditer(ms_text)))


def get_questions(ms_text, return_marks=True):
    regex = re.compile("\([a-h]\)")
    matches = list(regex.finditer(ms_text))
    questions = []
    marks = []
    question_ids = []
    qnum = 0
    for m in matches:
        start = m.span()[1]
        letter = ms_text[start - 2]
        if letter == "a":
            qnum += 1
        question_ids.append(str(qnum) + "/" + letter)
        span = ms_text[start:]
        questions.append(span[:span.index('[')])
        marks.append(int(span[span.index('[') + 1]))
    if return_marks:
        return [" ".join(q.split()) for q in questions], question_ids, marks
    return [" ".join(q.split()) for q in questions], question_ids


def get_question_type(questions, marks, qtype):
    if qtype == "definition":
        return [i for i in range(len(questions)) if "What is meant by" in questions[i] and marks[i] == 2]
    if qtype == "identify":
        return [i for i in range(len(questions)) if "Identify" in questions[i] and marks[i] == 2]
    if qtype == "explain":
        return [i for i in range(len(questions)) if "explain" in questions[i] and marks[i] in [4, 6]]


def get_scheme(question_id, ms_text):
    regex = re.compile("\([a-h]\)")
    matches = list(regex.finditer(ms_text))
    start = matches[question_id].span()[1]
    start = ms_text[start:].index(']') + start + 1
    end = None
    if question_id < num_questions(ms_text) - 1:
        end = matches[question_id + 1].span()[0]
    span = ms_text[start:end]
    return span


def parse_ms(qtype, ms):
    if qtype == "definition":
        return parse_definition_ms(ms)
    if qtype == "identify":
        return parse_identify_ms(ms)


def parse_definition_ms(scheme):
    prompts = ['clear understanding', 'some understanding']
    ms = defaultdict(list)
    for i in range(2):
        mark = 2 - i
        p = prompts.pop(0)
        index = scheme.lower().index(p) + len(p)
        idxs = [scheme.lower().index(j) for j in prompts]
        if "Do not" in scheme[index:]:
            idxs = idxs + [scheme[index:].index("Do not") + index]
        end = None
        if len(idxs) > 0:
            end = min(idxs)
        text = scheme[index:end]
        filtered = text[text.index(']') + 1:]
        parts = re.split("\] or", filtered.lower())
        parts = [re.split("[1-2]\]", x) for x in parts]
        for ix in range(len(parts)):
            subscheme = []
            for part in parts[ix]:
                tokens = filter_tokenize(part)
                if len(tokens) < 1:
                    continue
                subscheme.append(tokens)
                # tuple([id, weight, [tokens]])
            subscheme = [(ix, 1 / len(subscheme), i) for i in subscheme]
            ms[mark] += subscheme
    if end:
        donots = scheme[end:].split("Do not")[1:]
        for item in donots:
            splitted = item.split("'")
            if len(splitted) == 3:
                ms["Do not"] = filter_tokenize(splitted[1])
    return ms


def parse_identify_ms(scheme):
    points = scheme.split(":")[1]
    splitted = re.split(",|\n", points)
    ms = []
    for i in splitted:
        tokens = filter_tokenize(i)
        if len(tokens) > 0 and not (len(tokens) == 1 and (tokens[0] == "note" or tokens[0] == "bullet")):
            ms.append(tokens)
    return ms
