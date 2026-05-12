def classify_difficulty(question):

    length = len(question.split())

    if length < 8:
        return "Easy"

    elif length < 18:
        return "Medium"

    return "Hard"
