from parser import *
from question import Question


class Paper:
    def __init__(self, ms_path, p_path):
        if p_path is not None:
            self.p_text = load_html(p_path)
        self.ms_text = load_html(ms_path)
        self.id = self.create_id()
        self.questions = self.get_questions()

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
        valid_types = ["definition", "identify", "explain"]
        qs, qis, qms = get_questions(self.ms_text, True)
        for t in valid_types:
            qids = get_question_type(qs, qms, t)
            for i in qids:
                question = Question(qs[i], t, qms[i], qis[i])
                schm = get_scheme(i, self.ms_text)
                question.assign_short_ms(parse_ms(t, schm))
                questions[question.id] = question
        return questions
