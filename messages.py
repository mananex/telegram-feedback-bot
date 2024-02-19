start_command_message = '''
<b>👋 Welcome to bot %s!</b>

You can ask any questions you want and our moderators will answer you as quickly as possible. Use <b>/help</b> for more information about available commands.

<b>Thank you!</b>
'''

help_command_message = '''
<b>Here's a list of available commands and their descriptions.</b>

/start - <i>start message.</i>
/ask - <i>ask a question.</i>
/questions - <i>list of your questions.</i>
/help - <i>this message.</i>

<b>You can use them by simply clicking on them.</b>
'''

help_command_moderator_message = '''
<b>For moderators.</b>

/show_moderators - <i>show list of moderators</i>
/unban - <i>unban a user.</i>
'''

help_command_lead_message = '''
<b>For lead.</b>

/add_moderator - <i>add new moderator</i>
/delete_moderator - <i>delete moderator</i>
'''

ask_command_message = '''
Okay, what is your question?
'''

form_cancelled_message = '''
<b>The process was interrupted.</b>
'''

question_sent_message = '''
<b>Your message has been sent to moderators.</b> Question number: %s
'''

send_answer_message = '''
Write an answer for this question.
'''

answer_message = '''
Here's answer for your question "%s" <b>(question number %s)</b>\n\n%s
'''

answer_sent_message = '''
<b>Your answer has been sent to the user.</b>
'''

question_list_message = '''
<b>Here's a list of all your questions.</b>
'''

question_and_answer_message = '''
<b>Your question:</b>\n%s\n\n<b>The answer:</b>\n%s
'''

questions_deleted_message = '''
<b>Your questions have been successfully deleted.</b>
'''

question_deleted_message = '''
<b>Unable to answer, question has been deleted.</b>
'''

question_answered_message = '''
The question has already been answered.
'''

question_not_exist_response = '''
The question doesn't exist.
'''

question_list_empty = '''
You don't have any questions asked yet.
'''

no_answer_text = '''No answer yet.'''

user_banned_message = '''
❗️ <b>You're banned and can't send a question.</b>
'''

user_banned_moderator_message = '''
User with ID <code>%s</code> has been blocked.
'''

unanswered_questions_list_message = '''
<b>Here is a list of unanswered questions</b>
'''

unban_help_command = '''
<b>Usage:</b> /unban <i>user_id</i>
<b>Example:</b> /unban 41
'''

user_doesnt_exist_message = '''
There is no user with this ID.
'''

user_not_banned_message = '''
The user is not blocked.
'''

user_unbanned_message = '''
<b>🟢 The user has been unblocked.</b>
'''

add_moderator_help_message = '''
<b>Usage:</b> /add_moderator <i>user_telegram_id</i>
<b>Example:</b> /add_moderator 1560748091
'''

moderator_already_exists_message = '''
There is already such a moderator.
'''

moderator_added_message = '''
<b>Moderator has been added.</b>
'''

delete_moderator_help_message = '''
<b>Usage:</b> /delete_moderator <i>user_telegram_id</i>
<b>Example:</b> /delete_moderator 1170108702
'''

moderator_doesnt_exist_message = '''
There is no such moderator.
'''

moderator_deleted_message = '''
<b>Moderator has been deleted.</b>
'''

moderators_list_message = '''
<b>Here's a list of moderators.</b>\n\n%s
'''