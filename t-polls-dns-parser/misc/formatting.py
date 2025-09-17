import re


def clean_comment(text):
    if text is None:
        return " "
    cleaned_text = re.sub(r'</?p>', '', text)
    return cleaned_text


def characteristicGrades_for_text(characteristicGrades):
    s = ""
    for i in range(len(characteristicGrades)):
        s += f"{characteristicGrades[i]['title']}: {characteristicGrades[i]['value']}; "
    return s
