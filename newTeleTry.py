import logging
from telegram.ext.filters import Filters ##used for adding filters for incoming text,audio,video ...etc

from telegram.ext.messagehandler import MessageHandler 
from telegram import Update # Handles the updates or response coming from telegram

from telegram.ext import (
                          Updater, 
                          CommandHandler,
                          CallbackQueryHandler,
                          CallbackContext,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from instaScraper import getBasicInfo
import tokenkey


EXPECT_NAME, EXPECT_POST, EXPECT_BUTTON_CLICK = range(3)


def start(update: Update, context: CallbackContext):
    ''' Replies to start command '''
    update.message.reply_text('Enter /start_insta to to get the instagram finctions')

def set_name_handler(update: Update, context: CallbackContext):
    ''' Entry point of conversation  this gives  buttons to user'''

    button = [[InlineKeyboardButton("Get Info", callback_data='find_profile_info')],
    [InlineKeyboardButton("Get Post", callback_data='getpost')]]
    markup = InlineKeyboardMarkup(button)

    update.message.reply_text('Select', reply_markup=markup)
    
    return EXPECT_BUTTON_CLICK


def button_click_handler(update: Update, context: CallbackContext):
    ''' This gets executed on button click '''
    query = update.callback_query
    # shows a small notification inside chat
    query.answer(f'button click {query.data} recieved')


    if query.data == 'find_profile_info':
        query.edit_message_text(f'You clicked on "Get Info"')
        # asks for name, and prompts user to reply to it
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send your profile id', reply_markup=ForceReply())
        return EXPECT_NAME

    elif query.data == 'getpost':
        query.edit_message_text(f'You clicked on "Get Post"')
        # asks for name, and prompts user to reply to it
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send your profile id for post', reply_markup=ForceReply())
        return EXPECT_POST


def name_input_by_user(update: Update, context: CallbackContext):
    ''' The user's reply to the name prompt comes here  '''
    name = update.message.text
    count = getBasicInfo(name)
    # saves the name
    context.user_data['name'] = count
    update.message.reply_text(f'Total followers for {name} is {count}')

    # ends this particular conversation flow
    return ConversationHandler.END

def get_user_post(update: Update, context: CallbackContext):
    ''' The user's reply to the name prompt comes here  '''
    name = update.message.text
    count = getBasicInfo(name)
    # saves the name
    context.user_data['name'] = count
    update.message.reply_text(f'You are in get post function')

    # ends this particular conversation flow
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Name Conversation cancelled by user. Bye. Send /set_name to start again')
    return ConversationHandler.END



if __name__ == "__main__":
    updater = Updater(tokenkey.BotToken, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    _handlers = {}

    _handlers['start_handler'] = CommandHandler('start', start)

    _handlers['name_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('start_insta', set_name_handler)],
        states={
            EXPECT_NAME: [MessageHandler(Filters.text, name_input_by_user)],
            EXPECT_POST: [MessageHandler(Filters.text, get_user_post)],
            EXPECT_BUTTON_CLICK: [CallbackQueryHandler(button_click_handler)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    for name, _handler in _handlers.items():
        print(f'Adding handler {name}')
        dispatcher.add_handler(_handler)

    updater.start_polling()

    updater.idle()
