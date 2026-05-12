from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def evaluate_answer(student_answer, model_answer):

    score = similarity(student_answer, model_answer)

    if score > 0.9:
        return 10

    elif score > 0.75:
        return 8

    elif score > 0.6:
        return 6

    elif score > 0.4:
        return 4

    return 2
