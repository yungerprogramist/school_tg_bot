from school_bot.settings import TELEGRAM_BOT_API_KEI, TEACHER_PASSWORD
from telebot import custom_filters
from django.core.management.base import BaseCommand

import telebot 
from telebot.types import ReplyKeyboardRemove

from head_app.messages import *
from head_app.markups import *
from head_app.some_functions import *
from head_app.DataBase import *

bot = telebot.TeleBot (token=TELEGRAM_BOT_API_KEI) 

class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) 
        bot.load_next_step_handlers()
        bot.add_custom_filter(custom_filters.StateFilter(bot))
        bot.infinity_polling()						
 
 
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.username == 'None':
        bot.send_message(message.chat.id, text='Для использования бота, вам нужно установить username в профиле')
    else:
        role = check_role(message.from_user.username)
        if role == 'Ученик' or role =='Учитель':
            bot.send_message(message.chat.id, text= 'Вы уже зарегистрированны, пройдите далее', reply_markup=enter_main_menu_mar )
        else: 
            bot.send_message(message.chat.id, text=start_mes, reply_markup=start_registration_mar)

#Информация о боте
@bot.callback_query_handler(func=lambda call: call.data=='information_bot')

def information_bot(call):
    bot.send_message(call.message.chat.id, text='Информация о боте', reply_markup=enter_main_menu_mar)

#главное меню
@bot.callback_query_handler(func=lambda call: call.data=='main_menu')
def teacher_registration(call):
    check_user = check_role(username=call.from_user.username)
    if check_user =='Учитель':
        bot.send_message(call.message.chat.id, text='Главное меню - учитель', reply_markup=main_menu_teacher_mar)
    elif check_user == 'Ученик':
        bot.send_message(call.message.chat.id, text='Главное меню - ученик', reply_markup=main_menu_student_mar)
    else:
        bot.send_message(call.message.chat.id, text=check_user, reply_markup=start_registration_mar)


#регистрация учителя
@bot.callback_query_handler(func=lambda call: call.data=='teacher_registration')
def teacher_registration(call):
    mes = bot.send_message(call.message.chat.id, text='Введите пароль')
    bot.register_next_step_handler(mes, enter_teacher_registration)

def enter_teacher_registration(message):
    if message.text == TEACHER_PASSWORD:
        mes = bot.send_message(message.chat.id, text='Введите ваше ФИО')
        bot.register_next_step_handler(mes, name_tacher_registration)
    elif message.text =='/start':
        bot.send_message(message.chat.id, text=start_mes, reply_markup=start_registration_mar)
    else:
        mes = bot.send_message(message.chat.id, text= 'Пароль неверный, попробуйте ввести еще раз или нажмите на команду /start для выхода')
        bot.register_next_step_handler(mes, enter_teacher_registration)


teacher_registration_dict = {} #регистрация учителя ================================================
def name_tacher_registration(message):
    if check_FIO(message.text):
        username = message.from_user.username
        teacher_registration_dict[username] = {} 
        teacher_registration_dict[username]['username'] = username
        teacher_registration_dict[username]['chat_id'] = message.chat.id
        teacher_registration_dict[username]['name'] = message.text

        mes = bot.send_message(message.chat.id, text= 'Введите ваш школьный учебный предмет или предметы через запятую')
        bot.register_next_step_handler(mes, subject_teacher_registration)
    else:
        mes = bot.send_message(message.chat.id, text= 'Упс, что-то пошло не так, попробуйте ввести ФИО еще раз')
        bot.register_next_step_handler(mes, name_tacher_registration)
 
def subject_teacher_registration(message):
    username = message.from_user.username
    teacher_registration_dict[username]['subject'] = message.text
    if TeacherRegistration_DB(teacher_dict=teacher_registration_dict, username=username):
        del teacher_registration_dict[username]
        bot.send_message(message.chat.id, text= 'Регистрация прошла успешно', reply_markup=enter_main_menu_mar)
    else: 
        bot.send_message(message.chat.id, text= 'Что то пошло не так, обратитесь в поддержку @Alexei0212022')


#регистрация ученика
@bot.callback_query_handler(func=lambda call: call.data=='student_registration')
def student_registration(call):
    mes = bot.send_message(call.message.chat.id, text='Введите фаше ФИО')
    bot.register_next_step_handler(mes, name_student_registration)


student_registration_dict = {} #регистрация ученика ================================================
def name_student_registration(message):
    if check_FIO(message.text):
        username = message.from_user.username
        student_registration_dict[username] = {} 
        student_registration_dict[username]['username'] = username
        student_registration_dict[username]['chat_id'] = message.chat.id
        student_registration_dict[username]['name'] = message.text

        mes = bot.send_message(message.chat.id, text= 'Введите номер и букву класса - "11А"')
        bot.register_next_step_handler(mes, subject_student_registration)
    else:
        mes = bot.send_message(message.chat.id, text= 'Упс, что-то пошло не так, попробуйте ввести ФИО еще раз')
        bot.register_next_step_handler(mes, name_student_registration)
 
def subject_student_registration(message):
    form = check_form(message.text)
    if form:
        username = message.from_user.username
        student_registration_dict[username]['form'] = form
        if StudentRegistration_DB(student_dict=student_registration_dict, username=username):
            del student_registration_dict[username]
            bot.send_message(message.chat.id, text= 'Регистрация прошла успешно', reply_markup=enter_main_menu_mar)
        else:
            bot.send_message(message.chat.id, text= 'Что то пошло не так, обратитесь в поддержку @Alexei0212022')
    else:
        mes = bot.send_message(message.chat.id, text= 'Введите коректрный номер и букву класса - "11А"')
        bot.register_next_step_handler(mes, subject_student_registration)




@bot.callback_query_handler(func=lambda call: call.data=='teacher_send_message')
def teacher_send_message(call):
    mes = bot.send_message(call.message.chat.id, text='Выберите класс, которому вы хотите отправить сообщение или введите его в ручную в формате - "11А"', reply_markup=choise_form_mar()) #доделать правильную очередность
    bot.register_next_step_handler(mes, message_class)

message_teacher_text_dict = {} #сообщение учителя  для отправки ученикам
def message_class(message):
    message_teacher_text_dict[message.from_user.username] = message.text
    mes = bot.send_message(message.chat.id, text=f'Напишите сообщение которое хотите отправить - {message.text}', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(mes, spend_teacher_message)

def spend_teacher_message(message):
    username = message.from_user.username
    form = message_teacher_text_dict[username]
    students_list = filter_student_for_form_DB(form)
    info_teacher = get_teacher_data_DB(username)
    for student_chat_id in students_list:
        bot.send_message(student_chat_id, text=f'Сообщение от учителя - {info_teacher[1]} {info_teacher[0]} \n{info_teacher[2]}  \n{message.text}')
    bot.send_message(message.chat.id, text=f'Сообщение {form} Классу отправлено', reply_markup=enter_main_menu_mar)
    
#профиль учителя
@bot.callback_query_handler(func=lambda call: call.data=='teacher_profile')
def teacher_profile(call):
    teacher_data = get_teacher_data_DB(call.from_user.username)
    name = teacher_data[0]
    subject = teacher_data[1]
    bot.send_message(call.message.chat.id, text=f'Ваш профиль: \nИмя - {name} \nПредмет - {subject}', reply_markup=profile_teacher_mar)

#профиль ученика
@bot.callback_query_handler(func=lambda call: call.data=='student_profile')
def student_profile(call):
    print()
    student_data = get_student_data_DB(call.from_user.username)
    name = student_data[0]
    form = student_data[1]
    bot.send_message(call.message.chat.id, text=f'Ваш профиль: \nИмя - {name} \nКласс - {form}', reply_markup=profile_student_mar)


