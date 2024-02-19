# How the bot works?
**For convenience, I will divide the explanation into three parts - the user-side, the moderator-side and the lead-side.**
## User-side.
* ┏ Commands
* ┣  /start - *get start message.*
* ┣  /help - *get help message.*
* ┣  /ask - *ask a question.*
* ┣  /questions - *get a list of asked questions.*

### /ask
To send a question to moderators, you must first send the **/ask** command. If you change your mind about sending a message, you can click on the "*Cancel*" button at any time.
### /questions
To see the list of questions that you have asked the moderators, you can send the **/questions** command, after which the bot will respond to you with a message with inline-buttons (*if, of course, there are questions available*). 

When you click on the inline-button, the bot will send a response - showing your message and the answer to it.

The user also has the opportunity to delete asked questions by clicking on the inline-button "*Clear all*"

## Moderator-side.
* ┏ Commands
* ┣  /show_moderators - *get a list of moderators. Returns a list of telegram IDs of moderators.*
* ┣  /unban - *unban a user.*

### /unban
To unban a user you need to write **/unban** and the *user ID*, like `/unban 31`.

**Note:** NOT the telegram ID, but the *user ID* that is stored in the database. **The bot writes it when the moderator blocks someone.**

When a user sends a question to the moderators, all moderators receive a message with the question and with two inline-buttons:
"*Answer*" and "*❌ Ban user*". 

When you click on "*Answer*" button, the bot begins to wait for an answer message, which can be canceled by clicking on the "*Cancel*" button. **A question cannot be answered if another moderator has already answered it**. After answering a message in the chat, the message with the question will be deleted.

When you click on the "*❌ Ban user*" button, the user is blocked, and the moderator is informed of the user ID (the ID that is in the bot database)

## Lead-side.
* ┏ Commands
* ┣  /add_moderator - *add new moderator.*
* ┣  /delete_moderator - *delete moderator from the database.*
