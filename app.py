import logging
from random import randint
logging.basicConfig(filename = f'logs/log_{randint(0, 99999)}.log', level = logging.INFO)

# --------- #



# ------------- dependencies ------------- #
from configuration import API_TOKEN, LEAD_MODERATOR_ID
from additional import *
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from asyncio import run as asyncio_run
from database import Base, User, Question, Answer, Moderator, async_engine, async_session, \
                     select, delete, update, fetchone, fetchmany, insert, execute_stmt
import messages
# ------------- ----------- ------------- #



router = Router()
bot = Bot(API_TOKEN, parse_mode = 'html')
dp = Dispatcher()
dp.include_router(router)



# ------------------------------- #
class QuestionForm(StatesGroup):
    question_text = State()
# ------------------------------- #



# ------------------------------- #
class AnswerForm(StatesGroup):
    answer_text = State()
# ------------------------------- #



# ------- cancel state machine ------- #
@router.message(F.text.casefold() == 'cancel')
async def state_cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state != None:
        await state.clear()
        await message.reply(text = messages.form_cancelled_message, reply_markup = types.ReplyKeyboardRemove())
# ------- -------------------- ------- #



# ------------- ---------------- ------------- #
@dp.message(add_moderator_command)
async def add_moderator_command_handler(message: types.Message) -> None:
    if message.from_user.id == LEAD_MODERATOR_ID:
        command_arguments = message.text.split(' ')
        if len(command_arguments) == 1:
            await message.answer(text = messages.add_moderator_help_message)
        else:
            try: user_telegram_id = int(command_arguments[1])
            except:
                await message.answer(text = messages.add_moderator_help_message)
                return

            async with async_session() as session:
                moderator = await fetchone(select(Moderator).where(Moderator.telegram_user_id == user_telegram_id), session)
                if moderator: await message.answer(text = messages.moderator_already_exists_message)
                else:
                    await insert(Moderator(telegram_user_id = user_telegram_id), session)
                    await message.answer(text = messages.moderator_added_message)
# ------------- ---------------- ------------- #



# ------------- ---------------- ------------- #
@dp.message(delete_moderator_command)
async def delete_moderator_command_handler(message: types.Message) -> None:
    if message.from_user.id == LEAD_MODERATOR_ID:
        command_arguments = message.text.split(' ')
        if len(command_arguments) == 1:
            await message.answer(text = messages.delete_moderator_help_message)
        else:
            try: user_telegram_id = int(command_arguments[1])
            except:
                await message.answer(text = messages.delete_moderator_help_message)
                return

            async with async_session() as session:
                moderator = await fetchone(select(Moderator).where(Moderator.telegram_user_id == user_telegram_id), session)
                if not moderator: await message.answer(text = messages.moderator_doesnt_exist_message)
                else:
                    await execute_stmt(delete(Moderator).where(Moderator.telegram_user_id == user_telegram_id), session)
                    await message.answer(text = messages.moderator_deleted_message)
# ------------- ---------------- ------------- #



# ------------- ---------------- ------------- #
@dp.message(show_moderators_command)
async def show_moderators_command_handler(message: types.Message) -> None:
    async with async_session() as session:
        # I add scalars to the list because a strange thing happens and after checking whether the user’s ID is in the list of moderators’ IDs, the scalars disappear.
        moderators_id_list = list(await fetchmany(select(Moderator.telegram_user_id), session))
        if message.from_user.id in moderators_id_list:
            moderators_list_string = ''
            for moderator_id in moderators_id_list:
                moderators_list_string += f'{moderator_id}\n'
            await message.answer(text = messages.moderators_list_message % (moderators_list_string))
# ------------- ---------------- ------------- #



# ------------- ---------------- ------------- #
@dp.message(start_command)
async def start_command_handler(message: types.Message) -> None:
    async with async_session() as session:
        user = await fetchone(select(User).where(User.telegram_user_id == message.from_user.id), session)
        
        if user is None:
            await insert(User(telegram_user_id = message.from_user.id), session)
    
    bot_info = await bot.get_me()
    await message.answer(text = messages.start_command_message % (bot_info.first_name))
# ------------- ---------------- ------------- #



# ------------- ---------------- ------------- #
@dp.message(help_command)
async def help_command_handler(message: types.Message) -> None:
    await message.answer(text = messages.help_command_message)
    async with async_session() as session:
        moderator = await fetchone(select(Moderator).where(Moderator.telegram_user_id == message.from_user.id), session)
        if moderator: await message.answer(text = messages.help_command_moderator_message)
        if message.from_user.id == LEAD_MODERATOR_ID: await message.answer(text = messages.help_command_lead_message)
# ------------- ---------------- ------------- #



# ------------- ---------------- ------------- #
@dp.message(questions_command)
async def questions_command_handler(message: types.Message) -> None:
    async with async_session() as session:
        user_id = await fetchone(select(User.id).where(User.telegram_user_id == message.from_user.id), session)
        question_id_list = await fetchmany(select(Question.id).where(Question.user_id == user_id), session)

    question_list_markup = generate_question_list_markup(question_id_list)
    if not question_list_markup:
        await message.answer(text = messages.question_list_empty)
    else:
        await message.answer(text = messages.question_list_message, reply_markup = question_list_markup)
# ------------- ---------------- ------------- #



# ------------- ---------------- ------------- #
@dp.message(unban_command)
async def unban_command_handler(message: types.Message) -> None:
    command_arguments = message.text.split(' ')
    if len(command_arguments) == 1:
        await message.answer(text = messages.unban_help_command)
    else:
        try: user_id = int(command_arguments[1])
        except:
            await message.answer(text = messages.unban_help_command)
            return
    
        async with async_session() as session:
            user = await fetchone(select(User).where(User.id == user_id), session)
            if not user: await message.answer(text = messages.user_doesnt_exist_message)
            elif not user.is_banned: await message.answer(text = messages.user_not_banned_message)
            else: 
                await execute_stmt(update(User).where(User.id == user_id).values(is_banned = False), session)
                await message.answer(text = messages.user_unbanned_message)
# ------------- ---------------- ------------- #



# routing for QuestionForm
# ------------- ---------------- ------------- #
@router.message(ask_command)
async def ask_command_handler(message: types.Message, state: FSMContext) -> None:
    async with async_session() as session:
        is_user_banned = await fetchone(select(User.is_banned).where(User.telegram_user_id == message.from_user.id), session)
        if is_user_banned:
            await message.reply(text = messages.user_banned_message)
            return

    await state.set_state(QuestionForm.question_text)
    await message.answer(text = messages.ask_command_message, reply_markup = cancel_markup)

@router.message(QuestionForm.question_text)
async def process_question_text_handler(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    async with async_session() as session:
        user_id = await fetchone(select(User.id).where(User.telegram_user_id == message.from_user.id), session)
        new_question = Question(user_id = user_id, text = message.text)
        await insert(new_question, session)
        
        moderator_id_list = await fetchmany(select(Moderator.telegram_user_id), session)
        for moderator_id in moderator_id_list:
            await message.copy_to(moderator_id, reply_markup = generate_answer_markup(new_question.id, user_id))
    
    await message.answer(text = messages.question_sent_message % (new_question.id), reply_markup = types.ReplyKeyboardRemove())    
# ------------- ---------------- ------------- #



# routing for AnswerForm
# ------------- ---------------- ------------- #
@router.callback_query(F.data.startswith('answer'))
async def answer_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    question_id = int(call.data.split('#')[1])
    async with async_session() as session:
        question = await fetchone(select(Question).where(Question.id == question_id), session)
        if question is None:
            await call.message.reply(text = messages.question_deleted_message)
            return
        elif question.answer_id is not None:
                await call.message.reply(text = messages.question_answered_message)
                return

    await state.update_data({'question_id': question_id, 'question_message_id': call.message.message_id})
    await state.set_state(AnswerForm.answer_text)
    await call.message.reply(text = messages.send_answer_message, reply_markup = cancel_markup)
    
@router.message(AnswerForm.answer_text)
async def process_answer_text_handler(message: types.Message, state: FSMContext) -> None:
    state_data  = await state.get_data()
    question_id = state_data.get('question_id')
    question_message_id = state_data.get('question_message_id')
    
    async with async_session() as session:
        question = await fetchone(select(Question).where(Question.id == question_id), session)
        user = await fetchone(select(User).where(User.id == question.user_id), session)
        answer = Answer(user_id = user.id, question_id = question_id, text = message.text)
        
        await insert(answer, session)
        await execute_stmt(update(Question).where(Question.id == question_id).values(answer_id = answer.id), session)

        question_quote_text = question.text
        if len(question.text) > 15: question_quote_text = question.text[:16] + '...'
        await bot.send_message(chat_id = user.telegram_user_id, text = messages.answer_message % (question_quote_text, question_id, message.text))
        
    await state.clear()
    await bot.delete_message(chat_id = message.chat.id, message_id = question_message_id)
    await message.answer(text = messages.answer_sent_message, reply_markup = types.ReplyKeyboardRemove())
# ------------- ---------------- ------------- #



# ------------- ---------------- ------------- #
@router.callback_query(F.data.startswith('ban'))
async def ban_user_handler(call: types.CallbackQuery) -> None:
    await call.answer()
    user_id = int(call.data.split('#')[1])
    async with async_session() as session:
        await execute_stmt(update(User).where(User.id == user_id).values(is_banned = True), session)
    await call.message.reply(text = messages.user_banned_moderator_message % (user_id))
# ------------- ---------------- ------------- #



# ------------- ---------------- ------------- #
@router.callback_query(F.data.startswith('get_question'))
async def get_question_handler(call: types.CallbackQuery) -> None:
    async with async_session() as session:
        question_id = int(call.data.split('#')[1])
        question = await fetchone(select(Question).where(Question.id == question_id), session)
        
        if question == None: 
            await call.answer(text = messages.question_not_exist_response)
            return
        
        answer_text = await fetchone(select(Answer.text).where(Answer.question_id == question.id), session)
        if answer_text is None: answer_text = messages.no_answer_text
    
    await call.answer()
    await call.message.answer(text = messages.question_and_answer_message % (question.text, answer_text))
# ------------- ---------------- ------------- #



# ------------- ---------------- ------------- #
@router.callback_query(F.data.startswith('clear_question_list'))
async def clear_all_questions_handler(call: types.CallbackQuery) -> None:
    await call.answer()
    async with async_session() as session:
        user_id = await fetchone(select(User.id).where(User.telegram_user_id == call.from_user.id), session)
        await execute_stmt(delete(Question).where(Question.user_id == user_id), session)
        await execute_stmt(delete(Answer).where(Answer.user_id == user_id), session)
        
    await call.message.answer(text = messages.questions_deleted_message)
# ------------- ---------------- ------------- #



# ------------- run bot ------------- #
async def main() -> None:
    print('Creating tables...')
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print('Starting bot... Check logs.')
    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(bot, handle_signals = True)

if __name__ == '__main__':
    asyncio_run(main())
# ------------- ------- ------------- #
