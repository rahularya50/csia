from parser import *


class Paper:
    def __init__(self, p_path, ms_path):
        self.p_text = load_html(p_path)
        self.ms_text = load_html(ms_path)
        self.id = self.create_id()
        self.questions, self.marks = self.get_questions()

    def create_id(self):
        ns = self.ms_text.split('\n')[1].split()
        month_code = "".join([i[0] for i in ns[3].split('/')])
        year, syllabus, paper = ns[4:]
        return "_".join([month_code, year, syllabus, paper])

    def num_questions(self):
        regex = re.compile("\([a-z]\)")
        return len(list(regex.finditer(self.ms_text)))

    def get_questions(self):
        questions = {}
        marks = {}
        get_result = get_questions(self.ms_text, True)
        for q, i, mark in zip(*get_result):
            questions[i] = q
            marks[i] = mark
        return questions, marks
