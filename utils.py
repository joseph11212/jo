def total_score(midterm_score, terminal_score):
    return midterm_score + terminal_score

def average_score(midterm_score, terminal_score):
    return (midterm_score + terminal_score) / 2

def score_grade(average_score):
    if average_score > 80:
        return "A"
    elif average_score > 65:
        return "B"
    elif average_score > 55:
        return "C"
    elif average_score > 45:
        return "D"
    else:
        return "F"

