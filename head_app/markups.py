from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from head_app.DataBase import GetForms_DB


#переход в главное меню
enter_main_menu_mar = InlineKeyboardMarkup()
but1= InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
but2 = InlineKeyboardButton(text='Информация', callback_data='information_bot')
enter_main_menu_mar.add(but1, but2)


#регистрация 
start_registration_mar = InlineKeyboardMarkup()
but1 = InlineKeyboardButton(text='Учитель', callback_data='teacher_registration')
but2 = InlineKeyboardButton(text='Ученик', callback_data='student_registration')
start_registration_mar.add(but1, but2)


#главное меню учителя
main_menu_teacher_mar = InlineKeyboardMarkup(row_width=1)
but1 = InlineKeyboardButton(text='Профиль', callback_data='teacher_profile')
but2 = InlineKeyboardButton(text='Отправить сообщение', callback_data='teacher_send_message')
but3 = InlineKeyboardButton(text='Инфо', callback_data='information_bot')
main_menu_teacher_mar.add(but1,but2)


#главное меню ученика
main_menu_student_mar = InlineKeyboardMarkup()
but1 = InlineKeyboardButton(text='Профиль', callback_data='student_profile')
but2 = InlineKeyboardButton(text='Инфо', callback_data='information_bot')
main_menu_student_mar.add(but1,but2)

#Профиль ученика 
profile_student_mar = InlineKeyboardMarkup()
but1 = InlineKeyboardButton(text='Изменить данные профиля', callback_data='student_registration')
but2 = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')
profile_student_mar.add(but1,but2)

#Профиль учителя
profile_teacher_mar = InlineKeyboardMarkup()
but1 = InlineKeyboardButton(text='Изменить данные профиля', callback_data='teacher_registration')
but2 = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')
profile_teacher_mar.add(but1,but2)


#выбор класса 
def choise_form_mar():
    choise_form_mar = ReplyKeyboardMarkup(resize_keyboard=True)
    all_form = GetForms_DB()
    for form in all_form:
        choise_form_mar.add(KeyboardButton(f'{form}'))
    return choise_form_mar
    
