import re

def check_FIO(text):
    try:
        if len(text) < 100:
            return True
        else:
            return False
    except:
        return False

def check_form(form):
    """Проверяет на правильность и Возвращает коректрный номер и букву класса """
    try:
        class_form = form.replace(' ','')
        letter_form = class_form[-1]
        number_form = class_form.replace(letter_form, '')
        try:
            number_form = int(number_form)
            number_form = str(number_form)
        except:
            return False
        if bool(re.search('[а-яА-Я]', letter_form)):
            if letter_form.isupper():
                if 4 < int(number_form) < 12:
                    return number_form + letter_form
                else:
                    return False
            else:
                letter_form = letter_form.capitalize()
                if 4 < int(number_form) < 12:
                    return number_form + letter_form
                else: 
                    return False
        else:
            return False
    except: 
        return False
