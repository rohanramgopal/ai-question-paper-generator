from difflib import SequenceMatcher


def plagiarism_percentage(text1, text2):

    score = SequenceMatcher(
        None,
        text1.lower(),
        text2.lower()
    ).ratio()

    return round(score * 100, 2)
