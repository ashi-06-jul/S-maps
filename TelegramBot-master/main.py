import re
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Voice)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, )

from teleBotDatabase import TeleDB
import os
from dotenv import load_dotenv

load_dotenv()

db = TeleDB()
db.setup()



FILL, AUDIO, SUBMIT, NAME, COLLEGE, SIDEPROJECT, EXPLEVEL, LINUX, PLANGUAGE, PROGRAMMINGEXP, FRAMEWORK, STORAGE, INTERESTS, LEADERSHIP, GITHUB, POINTS= range(16)

# OPTONS
SOURCE_OPTIONS = [['Friends'],['Whatsapp Group'],['LinkedIn'],['Facebook']]
EXPERIENCE_OPTIONS = [['Beginner'],['Intermediate'],['Advance']]
LINUX_BEGINNER = [['Have used linux once but never again'],['Had tried to install linux once but faced issues']]
LINUX_INTERMEDIATE = [['Using Linux as the primary operating system'], ['Have used command line tools but not very comfortable']]
LINUX_ADVANCE = [['Have logged into a remote server'], ['Comfortable with few command line tools']]
PROGRAMMING_LANGUAGE_OPTIONS = [['Done'],['Java'],['JavaScript'],['Python'],['CSS'],['C++'],['C'],['C#'],['HTML'],['HTML5'],['PHP'],['Objective C'],['SQL'],['R'],['Ruby']]
PROGRAMMING_BEGINNER = [['Have written a simple hello world in a programming language'], ['Have written only 100 lines of code in any language'], ['Comfortable with loops and functions']]
PROGRAMMING_INTERMEDIATE = [['Have written more than 500 lines of code'], ['Comfortable with file handling and libraries'], ['Have collaborated with a team of programmers']]
PROGRAMMING_ADVANCE = [['Have written more than 1000 lines of code'], ['Have made a project']]
FRAMEWORK_OPTIONS = [['Done'],['Ruby on Rails'],['Flask'],['React'],['Django'],['Angular'],['ASP.NET'],['METEOR'],['Laravel'],['Express'],['Spring'],['PLAY'],['CodeIgniter']]

STORAGE_BEGINNER = [["Can read from a file using code"], ['Can write to a file using code']]
STORAGE_INTERMEDIATE = [['Used arrays, json or xml like nested data structures'], ['Used a database but only know basics']]
STORAGE_ADVANCE = [['Installed and comfortable with databases'], ['Used more than one databases - (mysql, sqlite, mongodb, elasticsearch)']]
INTERESTS_OPTONS = [["Backend"], ['Frontend'], ['App Development'], ['Communication'], ['Marketting']]
LEADERSHIP_OPTIONS = [['1'], ['2'], ['3'], ['4'], ['5']]
YES_NO_OPTIONS = [['Yes'], ['No']]


def start(update, context):
    id = update.message.chat_id
    update.message.reply_text('Listen audio carefully.')
    context.bot.send_voice(chat_id=id, voice=open('audio/Introductory.ogg', 'rb'))
    update.message.reply_text('Press /fillup to Continue')

    return FILL

def fill(update, context):
    text = update.message.text
    if text == '/fillup':
        update.message.reply_text('If you are interested to work with us. You have to send a recorded audio '
        'describing yourself, what techcnologies you know and on which platform you have worked.\n\n'
        'Send Reacorded Audio')
    elif text == 'Change':
        update.message.reply_text('Send audio again.')
    else:
        update.message.reply_text('Press /fillup to send us about yourself')
        return FILL

    return AUDIO



def audio(update, context):
    file = context.bot.get_file(update.message.voice.file_id)
    file.download(f'ReceivedAudio/{update.message.from_user["username"]}.ogg')

    reply_keyboard = [['Submit'], ['Change']]
    update.message.reply_text('Want to change the audio or submit it?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    

    return SUBMIT


def submit_audio(update, context):
    text = update.message.text
    if text == 'Submit':
        update.message.reply_text('What is your name?')

    elif text == 'No' and 'Name' in context.user_data:
        del context.user_data['Programming_language']
        del context.user_data['Framework']
        update.message.reply_text('Please, Fillup your details carefully!')
        update.message.reply_text('What is your name?')
    
    return NAME

        


def name(update, context):
    context.user_data['Name'] = update.message.text
    regex = '[A-Za-z]{2,25}( [A-Za-z]{2,25})?'

    if(re.search(regex, context.user_data['Name'])):
        update.message.reply_text('Which college are you from?',
                reply_markup=ReplyKeyboardRemove())


    else:
        update.message.reply_text('Please enter a valid Name.',
                reply_markup=ReplyKeyboardRemove())
        return NAME
    
    return COLLEGE



def college(update, context):
    context.user_data['College'] = update.message.text
    update.message.reply_text('How did you get to know about SideProjects?',
                    reply_markup=ReplyKeyboardMarkup(SOURCE_OPTIONS, one_time_keyboard=True))

    return SIDEPROJECT


def side_project(update, context):
    context.user_data['Source'] = update.message.text
    text = update.message.text

    if [text] in SOURCE_OPTIONS:
        update.message.reply_text('Select your proficiency level in your stream?',
                    reply_markup=ReplyKeyboardMarkup(EXPERIENCE_OPTIONS, one_time_keyboard=True))

    else:
        update.message.reply_text('Please! select from the given options',
                    reply_markup=ReplyKeyboardMarkup(SOURCE_OPTIONS, one_time_keyboard=True))
        return SIDEPROJECT

    return EXPLEVEL


def experience_level(update, context):
    text = update.message.text

    if [text] in EXPERIENCE_OPTIONS:
        context.user_data['Experience_level'] = update.message.text
        
        if context.user_data['Experience_level'] == 'Beginner':
            context.user_data['Points'] = 0
            update.message.reply_text('Ok! Choose one option according to your experience in linux',
                        reply_markup=ReplyKeyboardMarkup(LINUX_BEGINNER, one_time_keyboard=True))

        elif context.user_data['Experience_level'] == 'Intermediate':
            context.user_data['Points'] = 5
            update.message.reply_text('Ok! Choose one option according to your experience in linux',
                        reply_markup=ReplyKeyboardMarkup(LINUX_INTERMEDIATE, one_time_keyboard=True))

        elif context.user_data['Experience_level'] == 'Advance':
            context.user_data['Points'] = 10
            update.message.reply_text('Ok! Choose one option according to your experience in linux',
                        reply_markup=ReplyKeyboardMarkup(LINUX_ADVANCE, one_time_keyboard=True))


    else:
        update.message.reply_text('Please! select from the given options',
                    reply_markup=ReplyKeyboardMarkup(EXPERIENCE_OPTIONS, one_time_keyboard=True))
        return EXPLEVEL
    
    return LINUX


    


# LINUX

def linux(update, context):
    text = update.message.text
    if [text] in LINUX_BEGINNER or [text] in LINUX_INTERMEDIATE or [text] in LINUX_ADVANCE:

        update.message.reply_text('Which programming languages do you know?',
                    reply_markup=ReplyKeyboardMarkup(PROGRAMMING_LANGUAGE_OPTIONS))
        context.user_data['Linux'] = text

    else:
        if context.user_data['Experience_level'] == 'Beginner':
            reply_keyboard = LINUX_BEGINNER
        elif context.user_data['Experience_level'] == 'Intermediate':
            reply_keyboard = LINUX_INTERMEDIATE
        else:
            reply_keyboard = LINUX_ADVANCE
        
        update.message.reply_text('Please! select from the given options',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LINUX

    return PLANGUAGE   



# PROGRAMMNG LANGUAGE                

def multiple_select(update, context):
    if "Programming_language" in context.user_data:
        context.user_data['Programming_language'] += "," + update.message.text
    else:
        context.user_data['Programming_language'] = update.message.text


    return PLANGUAGE
    


def programming_language(update, context):
    if context.user_data['Experience_level'] == 'Beginner':
        update.message.reply_text('Choose one option according to your experience in programming language',
                    reply_markup=ReplyKeyboardMarkup(PROGRAMMING_BEGINNER, one_time_keyboard=True))

    elif context.user_data['Experience_level'] == 'Intermediate':
        update.message.reply_text('Tell us your experience in programming language',
                    reply_markup=ReplyKeyboardMarkup(PROGRAMMING_INTERMEDIATE, one_time_keyboard=True))    

    elif context.user_data['Experience_level'] == 'Advance':
        update.message.reply_text('Tell us your experience about programming language',
                    reply_markup=ReplyKeyboardMarkup(PROGRAMMING_ADVANCE, one_time_keyboard=True))

    
    if 'Programming_language' in context.user_data:
        context.user_data["Programming_language"] = list(set(context.user_data["Programming_language"].split(",")))
    else:
        context.user_data['Programming_language'] = ['None']
    
    return PROGRAMMINGEXP



def programming_experience(update, context):
    ReplyKeyboardRemove()
    text = update.message.text
    
    if [text] in PROGRAMMING_BEGINNER or [text] in PROGRAMMING_INTERMEDIATE or [text] in PROGRAMMING_ADVANCE:

        context.user_data['Programming_experience'] = update.message.text
        # About Framework
        update.message.reply_text("Select Framework on which you've worked",
                    reply_markup=ReplyKeyboardMarkup(FRAMEWORK_OPTIONS))
        
    
    else:
        if context.user_data['Experience_level'] == 'Beginner':
            reply_keyboard = PROGRAMMING_BEGINNER
        elif context.user_data['Experience_level'] == 'Intermediate':
            reply_keyboard = PROGRAMMING_INTERMEDIATE
        else:
            reply_keyboard = PROGRAMMING_ADVANCE

        update.message.reply_text('Please! select from the given options',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return PROGRAMMINGEXP
    
    context.user_data['Programming_language'] = ', '.join(context.user_data['Programming_language'])

    
    return FRAMEWORK




def multi_select_framework(update, context):
    if "Framework" in context.user_data:
        context.user_data['Framework'] += "," + update.message.text
    else:
        context.user_data['Framework'] = update.message.text
        
    return FRAMEWORK


def framework(update, context):
    if context.user_data['Experience_level'] == 'Beginner':
        update.message.reply_text('Select your proficiency in file handling?',
                    reply_markup=ReplyKeyboardMarkup(STORAGE_BEGINNER, one_time_keyboard=True))

    elif context.user_data['Experience_level'] == 'Intermediate':
        update.message.reply_text('Select your proficiency in Data Structure?',
                    reply_markup=ReplyKeyboardMarkup(STORAGE_INTERMEDIATE, one_time_keyboard=True))

    elif context.user_data['Experience_level'] == 'Advance':
        update.message.reply_text('Select your proficiency in Database?',
                    reply_markup=ReplyKeyboardMarkup(STORAGE_ADVANCE, one_time_keyboard=True))



    if 'Framework' in context.user_data:
        context.user_data['Framework'] = list(set(context.user_data['Framework'].split(",")))
    else:
        context.user_data['Framework'] = ['None']

    return STORAGE


# Storage

def storage(update, context):
    ReplyKeyboardRemove()

    text = update.message.text
    if [text] in STORAGE_BEGINNER or [text] in STORAGE_INTERMEDIATE or [text] in STORAGE_ADVANCE:
        context.user_data['Storage'] = update.message.text
        update.message.reply_text('What is your field of interest in the given?',
                    reply_markup=ReplyKeyboardMarkup(INTERESTS_OPTONS, one_time_keyboard=True))

    else:
        if context.user_data['Experience_level'] == 'Beginner':
            reply_keyboard = STORAGE_BEGINNER
        elif context.user_data['Experience_level'] == 'Intermediate':
            reply_keyboard = STORAGE_INTERMEDIATE
        else:
            reply_keyboard = STORAGE_ADVANCE

        update.message.reply_text('Please! select from the given options',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return STORAGE
    
    context.user_data['Framework'] = ', '.join(context.user_data['Framework'])
    

    return INTERESTS




def intersets(update, context):
    ReplyKeyboardRemove()
    context.user_data['Interest'] = update.message.text
    text = update.message.text
    
    if [text] in INTERESTS_OPTONS:
        update.message.reply_text('Rate your self in leadership quality out of 5',
                        reply_markup=ReplyKeyboardMarkup(LEADERSHIP_OPTIONS, one_time_keyboard=True))
    
    else:
        update.message.reply_text('Please! select from the given options',
                    reply_markup=ReplyKeyboardMarkup(INTERESTS_OPTONS, one_time_keyboard=True))
        return INTERESTS
    
    return LEADERSHIP



def leadership(update, context):
    ReplyKeyboardRemove()
    context.user_data['Leadership'] = update.message.text
    text = update.message.text

    if [text] in LEADERSHIP_OPTIONS:
        update.message.reply_text('Please share your github repository for us to keep a track of your work if you have.\n\n.'
            'Otherwise, Press /No.')
    
    else:
        update.message.reply_text('Please! select from the given options',
                    reply_markup=ReplyKeyboardMarkup(LEADERSHIP_OPTIONS, one_time_keyboard=True))
        return LEADERSHIP

    return GITHUB




def github_repository(update, context):
    if update.message.text != "/No":
        context.user_data['Github'] = update.message.text
    else:
        context.user_data['Github'] = 'Not Provided'

    
    

    update.message.reply_text(
        f'''
Displayed below are your details,\n\n
Name : {context.user_data['Name']}\n
College : {context.user_data['College']}\n
Source : {context.user_data['Source']}\n
Programming Language : {context.user_data["Programming_language"]}\n
Framework : {context.user_data["Framework"]}\n
Leadership: {context.user_data['Leadership']}\n
Interest : {context.user_data['Interest']}\n
Github Id : {context.user_data['Github']}\n\n
Please let us know if your previous details were correct. 
Press "Yes" to confirm or "No" to fill details again''',
            reply_markup=ReplyKeyboardMarkup(YES_NO_OPTIONS, one_time_keyboard=True))
            
    return POINTS



def points(update, context):

    # linux
    if context.user_data['Linux'] in ['Have used linux once but never again', 'Using Linux as the primary operating system', 'Have logged into a remote server'] :
        context.user_data['Points'] += 1
    else:
        context.user_data['Points'] += 2

    # programming_experience
    if context.user_data['Programming_experience'] in ['Have written a simple hello world in a programming language', 'Have written more than 500 lines of code', 'Have written more than 1000 lines of code'] :
        context.user_data['Points'] += 1
    elif context.user_data['Programming_experience'] in ['Have written only 100 lines of code in any language', 'Comfortable with file handling and libraries']:
        context.user_data['Points'] += 2
    else:
        context.user_data['Points'] += 3
    
    # programming_language
    if len(context.user_data['Programming_language'].split(',')) < 3:
        context.user_data['Points'] += len(context.user_data['Programming_language'].split(','))
    else:
        context.user_data['Points'] += 3


    # framework
    if len(context.user_data['Framework'].split(',')) < 3:
        context.user_data['Points'] += len(context.user_data['Framework'].split(','))
    else:
        context.user_data['Points'] += 3

    # storage
    if context.user_data['Storage'] in ["Can read from a file using code", 'Used arrays, json or xml like nested data structures', 'Installed and comfortable with databases'] :
        context.user_data['Points'] += 1
    else:
        context.user_data['Points'] += 2



    db.add_item(**context.user_data)

    # Send message to the channel
    context.bot.send_message(chat_id=-1001467021890,text=
        f'''
New Candidate\n\n
Name : {context.user_data['Name']}\n
College : {context.user_data['College']}\n
Source : {context.user_data['Source']}\n
Experience_level : {context.user_data['Experience_level']}\n
Linux Experience : {context.user_data['Linux']}\n
Programming Language : {context.user_data["Programming_language"]}\n
programming Experience : {context.user_data["Programming_experience"]}\n
Framework : {context.user_data["Framework"]}\n
Storage : {context.user_data["Storage"]}\n
Interest : {context.user_data['Interest']}\n
Leadership: {context.user_data['Leadership']}\n
Github Id : {context.user_data['Github']}\n
'''
    )

    context.bot.send_voice(chat_id=-1001467021890, voice=open(f'ReceivedAudio/{update.message.from_user["username"]}.ogg', 'rb'))



    # decide level
    if context.user_data['Points'] > 18:
        level = 'Level3'
    elif 12 < context.user_data['Points'] <= 18:
        level = 'Level2'
    else:
        level = 'Level1'


    # links of all groups
    links = {'Level1':'https://t.me/joinchat/OI-x6Ev-ndKYJfVxr95bTA', 'Level2':'https://t.me/joinchat/OI-x6EorSA6kxlF6MQmasw', 'Level3':'https://t.me/joinchat/OI-x6EVah-zYthh7stQzUA'}

    update.message.reply_text('Based on your skills and experience, we feel you should join the SideProjects levelling process at:'
    f' - {level}\n\n'
    f'Click to join Telgram group {links[level]}\n\n'
    'Please further communicate with SideProjects admin. Happy Coding!')

    id = update.message.chat_id

    # sending documents and audio
    context.bot.send_document(chat_id=id, document=open('documents/{}.pdf'.format(level), 'rb'))
    context.bot.send_voice(chat_id=id, voice=open('audio/Instruction.ogg', 'rb'))
    

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
            FILL: [MessageHandler(Filters.text, fill)],

            AUDIO: [MessageHandler(Filters.voice, audio)],

            SUBMIT: [MessageHandler(Filters.regex('Submit'), submit_audio),
                    MessageHandler(Filters.regex('Change'), fill)
                    ],

            NAME: [MessageHandler(Filters.text, name)],

            COLLEGE: [MessageHandler(Filters.text, college)],

            SIDEPROJECT: [MessageHandler(Filters.text, side_project)],

            EXPLEVEL: [MessageHandler(Filters.text, experience_level)],

            LINUX: [MessageHandler(Filters.text, linux)],

            PLANGUAGE: [MessageHandler(Filters.regex('^(Java|JavaScript|Python|CSS|C\+\+|C|C#|HTML|HTML5|PHP|Objective C|SQL|R|Ruby)$'), multiple_select),
                        MessageHandler(Filters.regex('Done$'), programming_language)
                        ],
            
            
            PROGRAMMINGEXP: [MessageHandler(Filters.text, programming_experience)],
            

            FRAMEWORK: [MessageHandler(Filters.regex('^(Ruby on Rails|Flask|React|Django|Angular|ASP.NET|METEOR|Laravel|Express|Spring|PLAY|CodeIgniter)$'), multi_select_framework),
                            MessageHandler(Filters.regex('Done$'), framework)
                            ],

            STORAGE: [MessageHandler(Filters.text, storage)],

            INTERESTS: [MessageHandler(Filters.text, intersets)],

            LEADERSHIP: [MessageHandler(Filters.text, leadership)],
    
            GITHUB: [MessageHandler(Filters.text, github_repository)],

            POINTS: [MessageHandler(Filters.regex('^Yes$'), points),
                    MessageHandler(Filters.regex('^No$'), submit_audio),
                    ],

            
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
