import re
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Voice)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, )

from db import TeleDB
import os
from dotenv import load_dotenv

load_dotenv()

db = TeleDB()
db.setup()



AUDIO, NAME, PROFILE, COHORT, PROCESS, PURPOSE, CONTRIBUTION, THREE_PEOPLE, QUALITIES, CONFIRMATION, POINTS= range(11)

# OPTONS
DATE_TIME = [['10 Septemper, 12pm'],['11 Septemper, 12pm'],['12 Septemper, 12pm'],['13 Septemper, 12pm']]
YES_NO_OPTIONS = [['Yes'], ['No']]


def start(update, context):
    id = update.message.chat_id
    update.message.reply_text('''• If you are curious to know about stuff and
crave for a thriving & harmonious planet
based on respect for all life forms, justice and
dignity for all - you have come to the right
place
• First tell us a bit about you, and we maybe
able to help you discover something new
about yourself in a voice note
.''')
    

    return AUDIO



def audio(update, context):
    file = context.bot.get_file(update.message.voice.file_id)
    file.download(f'ReceivedAudio/{update.message.from_user["username"]}.ogg')
    update.message.reply_text('What is your name?')

    return NAME


def name(update, context):
    context.user_data['Name'] = update.message.text
    regex = '[A-Za-z]{2,25}( [A-Za-z]{2,25})?'

    if(re.search(regex, context.user_data['Name'])):
        update.message.reply_text('''• S-Maps is an interactive tool to ease you into
the complexity of any issue that you are
interested in.
• It helps to navigate complexities that we face
within and outside.
• This will be your own unique journey of
discovery but we start of as a Cohort.
• Please answer some questions to register for a cohort. What is your professional profile.''',
                reply_markup=ReplyKeyboardRemove())


    else:
        update.message.reply_text('Please enter a valid Name.',
                reply_markup=ReplyKeyboardRemove())
        return NAME
    
    return PROFILE



def profile(update, context):
    context.user_data['profile'] = update.message.text
    update.message.reply_text('''The introductory process with your Cohort will take 90 minutes (I am open
to suggestions). It will be process of self discovery so choose a date and
time when you know you can give your full attention to the process and
not have any competing commitments. Choose a Cohort that you would like to join (based on the date & time that
is convenient for you)
''',
                    reply_markup=ReplyKeyboardMarkup(DATE_TIME, one_time_keyboard=True))

    return COHORT


def cohort(update, context):
    context.user_data['Date_Time'] = update.message.text
    text = update.message.text

    if [text] in DATE_TIME:
        update.message.reply_text('''There will be 5 questions. You need to give brief answers. Do
not over think before answering. There are no right or wrong
answers – just answer what come to your mind naturally. Describe how you felt in a peak experience. Write 3 words only.''',
                    reply_markup=ReplyKeyboardRemove())

    else:
        update.message.reply_text('Please! select from the given options',
                    reply_markup=ReplyKeyboardMarkup(DATE_TIME, one_time_keyboard=True))
        return COHORT

    return PROCESS


def process(update, context):
    context.user_data['peak_experience'] = update.message.text
    regex = '[A-Z a-z]'

    if(re.search(regex, context.user_data['peak_experience'])):
        update.message.reply_text('''What is my life’s purpose? Write 1 sentence only''',
                reply_markup=ReplyKeyboardRemove())


    else:
        update.message.reply_text('Please enter a valid answer in 3 words only.',
                reply_markup=ReplyKeyboardRemove())
        return PROCESS
    
    return PURPOSE

def purpose(update, context):
    context.user_data['purpose'] = update.message.text
    regex = '[A-Za-z ]?'

    if(re.search(regex, context.user_data['purpose'])):
        update.message.reply_text('''What is going to be my contribution? Specify a measurable
contribution, with fruition time. Think big!''',
                reply_markup=ReplyKeyboardRemove())


    else:
        update.message.reply_text('Please enter a valid answer.',
                reply_markup=ReplyKeyboardRemove())
        return PURPOSE
    
    return CONTRIBUTION

def contribution(update, context):
    context.user_data['contribution'] = update.message.text
    regex = '[A-Za-z]{2,25}( [A-Za-z]{2,25})?'

    if(re.search(regex, context.user_data['contribution'])):
        update.message.reply_text('''Name three people in history, mythology, fiction, science, sport or
religion who you admire. Not anyone you know personally.''',
                reply_markup=ReplyKeyboardRemove())


    else:
        update.message.reply_text('Please enter a valid answer.',
                reply_markup=ReplyKeyboardRemove())
        return CONTRIBUTION
    
    return THREE_PEOPLE

def three_people(update, context):
    context.user_data['three_people'] = update.message.text
    regex = '[A-Za-z]{2,25}( [A-Za-z]{2,25})?'

    if(re.search(regex, context.user_data['three_people'])):
        update.message.reply_text('''What are 3 qualities that you best display in your relationships and
can be counted on for? Write 3 words only.''',
                reply_markup=ReplyKeyboardRemove())


    else:
        update.message.reply_text('Please enter a valid answer.',
                reply_markup=ReplyKeyboardRemove())
        return THREE_PEOPLE
    
    return QUALITIES

def qualities(update, context):
    context.user_data['qualities'] = update.message.text
    regex = '[A-Za-z]{2,25}( [A-Za-z]{2,25})?'

    if(re.search(regex, context.user_data['qualities'])):
        update.message.reply_text(
        f'''
Displayed below are your details,\n\n
Name : {context.user_data['Name']}\n
Profile : {context.user_data['profile']}\n
Date & Time for cohort : {context.user_data['Date_Time']}\n
Peak Experience : {context.user_data['peak_experience']}\n
Purpose : {context.user_data["purpose"]}\n
Contribution : {context.user_data["contribution"]}\n
Three People : {context.user_data["three_people"]}\n
Qualities : {context.user_data["qualities"]}\n
Please let us know if your previous details were correct. 
Press "Yes" to confirm or "No" to fill details again''',
            reply_markup=ReplyKeyboardMarkup(YES_NO_OPTIONS, one_time_keyboard=True))
            
        return CONFIRMATION

    else:
        update.message.reply_text('Please enter a valid answer.',
                reply_markup=ReplyKeyboardRemove())
        return QUALITIES
    
    return CONFIRMATION


   



def confirmation(update, context):

    db.add_item(**context.user_data)

    # Send message to the channel
    context.bot.send_message(chat_id=-1001437510301,text=
        f'''
New Client\n\n
Name : {context.user_data['Name']}\n
Profile : {context.user_data['profile']}\n
Date and Time for Cohort : {context.user_data['Date_Time']}\n
Peak Experience : {context.user_data['peak_experience']}\n
Purpose : {context.user_data["purpose"]}\n
Contribution : {context.user_data["contribution"]}\n
Three People : {context.user_data["three_people"]}\n
Qualities : {context.user_data["qualities"]}\n
'''
    )

    context.bot.send_voice(chat_id=-1001437510301, voice=open(f'ReceivedAudio/{update.message.from_user["username"]}.ogg', 'rb'))




    # links of all groups
    links = {'Level1':'https://t.me/joinchat/OI-x6Ev-ndKYJfVxr95bTA', 'Level2':'https://t.me/joinchat/OI-x6EorSA6kxlF6MQmasw', 'Level3':'https://t.me/joinchat/OI-x6EVah-zYthh7stQzUA'}


    return ConversationHandler.END



def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():

    updater = Updater(
        os.getenv("TELEGRAM_TOKEN",""), use_context=True)

    dp = updater.dispatcher
    

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
         
            AUDIO: [MessageHandler(Filters.voice, audio)],

            NAME: [MessageHandler(Filters.text, name)],

            PROFILE: [MessageHandler(Filters.text, profile)],

            COHORT: [MessageHandler(Filters.text, cohort)],

            PROCESS: [MessageHandler(Filters.text, process)],

            PURPOSE: [MessageHandler(Filters.text, purpose)],

            CONTRIBUTION: [MessageHandler(Filters.text, contribution)],

            
            THREE_PEOPLE: [MessageHandler(Filters.text, three_people)],

            QUALITIES: [MessageHandler(Filters.text, qualities)],

            CONFIRMATION: [MessageHandler(Filters.text, confirmation)],

           

            
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()