# ------------- dependences ------------- #
from aiogram.filters import Command
from aiogram import types
# ------------- ----------- ------------- #

# commands
start_command = Command('start')
help_command = Command('help')
ask_command = Command('ask')
questions_command = Command('questions')
unban_command = Command('unban')
show_moderators_command = Command('show_moderators')
add_moderator_command = Command('add_moderator')
delete_moderator_command = Command('delete_moderator')

# buttons and markups
cancel_markup = types.ReplyKeyboardMarkup(resize_keyboard = True, keyboard = [[types.KeyboardButton(text = 'Cancel')]])

def generate_answer_markup(question_id: int, user_telegram_id: int) -> types.InlineKeyboardMarkup:
    answer_button = types.InlineKeyboardButton(text = 'Answer', callback_data = f'answer#{question_id}')
    ban_button = types.InlineKeyboardButton(text = '❌ Ban user', callback_data = f'ban#{user_telegram_id}')
    return types.InlineKeyboardMarkup(inline_keyboard = [[answer_button], [ban_button]])

def generate_question_list_markup(question_id_scalars) -> types.InlineKeyboardMarkup:
    button_list = []
    for question_id in question_id_scalars:
        button_list.append([types.InlineKeyboardButton(text = f'Question {question_id}', callback_data = f'get_question#{question_id}')])
    if not button_list: return None
    button_list.append([types.InlineKeyboardButton(text = 'Clear all', callback_data = 'clear_question_list')])
    return types.InlineKeyboardMarkup(inline_keyboard = button_list)