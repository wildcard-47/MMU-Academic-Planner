#function to get the grade letter from the score
def percent_to_letter(score):
    if score < 0 or score > 100:
        return "Invalid score"
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 75:
        return "A-"
    elif score >= 70:
        return "B+"
    elif score >= 65:
        return "B"
    elif score >= 60:
        return "B-"
    elif score >= 55:
        return "C+"
    elif score >= 50:
        return "C"
    elif score >= 47:
        return "C-"
    elif score >= 44:
        return "D+"
    elif score >= 40:
        return "D"
    else:
        return "F"