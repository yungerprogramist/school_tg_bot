from head_app.models import StudentModel, TeacherModel




def check_role(username):
    """
    return 'Учитель' or 'Ученик' or 'Вы не зар...'
    """
    check_teacher = TeacherModel.objects.filter(username=username).exists()
    if check_teacher:
        return 'Учитель'
    check_student = StudentModel.objects.filter(username=username).exists()
    if check_student:
        return 'Ученик'
    return 'Вы не зарегестрированны, пройдите регистрацию. Укажите, кто вы'


def get_teacher_data_DB(username: str) ->list:
    """Возвращает информацию об учителе по username [username, name, subject]"""
    try:
        teacher_list_db = TeacherModel.objects.filter(username=username).values_list('username','name', 'subject')
        teacher_list = list(teacher_list_db[0])
        return teacher_list
    except Exception as ex:
        print(f'Error в функции get_teacher_data_DB - {ex}')
        return 'Упс, что то пошло не так'





def get_student_data_DB(username: str) -> list:
    """Возвращает информацию об ученике по username [name, form]"""
    try:
        student_list_db = StudentModel.objects.filter(username=username).values_list('name', 'form')
        print(student_list_db)
        student_list = list(student_list_db[0])
        print(student_list)
        return student_list
    except Exception as ex:
        print(f'Error в функции get_student_data_DB - {ex}')
        return 'Упс, что то пошло не так'



def TeacherRegistration_DB(teacher_dict: dict, username: str) -> None:
    """
    Регистрирует учителя в бд
    """
    try:
        data_dict = teacher_dict[username]
        chat_id = data_dict['chat_id']
        name = data_dict['name']
        subject = data_dict['subject']
        if TeacherModel.objects.filter(username=username).exists():
            TeacherModel.objects.filter(username=username).update(chat_id=chat_id, username=username, name=name, subject=subject)
        else:
            TeacherModel.objects.create(chat_id=chat_id, username=username, name=name, subject=subject)
        return True
    except Exception as ex:
        print(f'Error на стадии записи учителя в бд - {ex}')
        return False

def StudentRegistration_DB(student_dict : dict, username: str) -> None:
    """
    Регистрирует учителя в бд
    """
    try:
        data_dict = student_dict[username]
        chat_id = data_dict['chat_id']
        name = data_dict['name']
        klass_form = data_dict['form']
        if StudentModel.objects.filter(username=username).exists():
            StudentModel.objects.filter(username=username).update(chat_id=chat_id, username=username, name=name, form =klass_form)
        else:    
            StudentModel.objects.create(chat_id=chat_id ,username=username, name=name, form=klass_form)
        return True
    except Exception as ex:
        print(f'Error на стадии записи ученика в бд - {ex}')
        return False


def GetForms_DB() ->list:
    """Выводит список классов"""
    form_list = StudentModel.objects.all().values_list('form', flat=True)
    print(form_list)
    forms = list(set(form_list))
    print(forms)
    return forms



def filter_student_for_form_DB(form: str) ->list:
    """Выводит всех учеников из заданного класса"""
    try:
        form_list = StudentModel.objects.all().values_list('form', flat=True)
        print(form_list)
        if form in form_list:
            students_chat_id = StudentModel.objects.filter(form=form).values_list('chat_id', flat=True)
            return list(students_chat_id)
        else:
            return f'Такого класса - {form}  не существует'
    except Exception as ex:
        print(f'Error на стадии фильтрации учеников по классу - {ex}')
        return 'Упс, что то пошло не так'



