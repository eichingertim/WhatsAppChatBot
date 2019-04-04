# Simple WhatsApp-ChatBot
# Future Plan: integrating machine learning, so the bot can send messages by knowledge
# author: Tim Eichinger
# Requirements: Latest Chrome or Firefox driver for Test-Automation

from selenium import webdriver
import time

# get driver and open web-page
driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com/')

# variable for the length before scanning
global length_before

# variable that saves whether the bot has answered this person or group before
global already_answered

# Bot Answers and helping variables
self_online = False

# groups and chats where the bot should not answer
groups_without_authotization = ['Ersti WiWi', 'Uni Elite und Sascha', 'A-Jugend 2018/2019',
                                'Renate Mehringer', 'WInfo Erstis WS 18/19', ' Spieler SV 22',
                                'Schischule B.-A.-Z. ', 'Silke Eichinger']

# fortnite keywords and answer when they are detected
fortnite_words = ['F?', 'f', 'F', 'f?', 'fortnite', 'Fortnite', 'Fortnite?', 'fortnite?']
fortnite_answer = 'Tim\'s Freizeit ist heute von 16-20 Uhr '

# discord keywords and answer when they are detected
discord_words = ['disc', 'Disc', 'disc?', 'Disc?', 'Discord', 'discord', 'Discord?',
                 'discord?', 'on', 'on?', 'On', 'online', 'Online']
discord_answer = 'Tim ist den ganzen Tag über Discord erreichbar. '

# bad or offensive words that the bot can detect
bad_words = ['Larry', 'larry', 'Spast', 'spast', 'Spasti', 'spasti', 'Depp', 'depp', 'hurensohn',
             'Hurensohn', 'Huansohn', 'huansohn', 'wixer', 'Wixer', 'Sau', 'sau', 'Arsch', 'arsch', 'Arschloch',
             'arschloch']


# machine learning answer
def get_machine_algorithm_answer():
    return ''


# returns the answer the chat bot should print
def get_answer(texts, chat_name):

    if "ChatBot (v1.0)" in str(texts[-1]):
        print("ERROR: Last message was from Bot")
        return ""

    list_splitted_msg = str(texts[-1]).split()

    return_string = ""

    discord_already_in_string = False
    fortnite_already_in_string = False
    bad_words_already_in_string = False

    if 'Tim Eichinger' in str(texts[-1]) or 'Tim' in str(texts[-1]):
        if self_online:
            return_string += get_machine_algorithm_answer()
        else:
            return_string += 'Tim ist zurzeit nicht online. Er antwortet dir/euch innerhalb 20-30 Minuten! '
    elif chat_name not in already_answered:
        return_string += 'Tim ist zurzeit nicht online. Er antwortet dir/euch innerhalb 20-30 Minuten! '
        already_answered.append(chat_name)

    for item in list_splitted_msg:
        if item in bad_words and not bad_words_already_in_string:
            return_string += 'Ich habe eine Beleidigung entdeckt (\"{}\")! Das kann ich nicht tolerieren! '.format(item)
            bad_words_already_in_string = True
        if item in fortnite_words and not fortnite_already_in_string:
            return_string += fortnite_answer
            fortnite_already_in_string = True
        if item in discord_words and not discord_already_in_string:
            return_string += discord_answer
            discord_already_in_string = True

    return return_string


# text dir class: _2S1VP copyable-text selectable-text
# button class: _1aTxu


# Checks, whether the bot can send a message to the specific chat and handles the following send process
def send_text(par_elements, par_msg_box):
    go_to_infos = driver.find_element_by_class_name('_5SiUq')
    go_to_infos.click()

    time.sleep(2)

    chat_name = driver.find_element_by_xpath('//div[@class = "{}"]'.format('_2S1VP copyable-text selectable-text')).text

    if chat_name == "":
        chat_name = driver.find_element_by_xpath('//span[@class = "{}"]'.format('iYPsH')).text

    go_back = driver.find_element_by_xpath('//button[@class = "{}"]'.format('_1aTxu'))
    go_back.click()

    texts = []

    for elem in par_elements:
        texts.append(elem.text)

    answer = get_answer(texts, chat_name)
    print(f'CURRENT CHAT: {chat_name}')

    if chat_name in groups_without_authotization:
        print("ERROR: Bot has no authorization to send the message")
    elif answer == "":
        print("ERROR: No answer generated")
    else:
        par_msg_box.send_keys("*ChatBot (v1.0):* " + answer)
        btn = driver.find_element_by_class_name('_35EW6')
        btn.click()
        print(f'MESSAGE SENT: {answer}')


# sets the length of the array from the last scanning of all messages
def set_length_before():
    # gets all the text elements in a chat
    span_class = 'selectable-text invisible-space copyable-text'
    elements = driver.find_elements_by_xpath('//span[@class = "{}"]'.format(span_class))
    return len(elements)


# checks for a new message in the current chat
def check_for_current_chat_new_message():
    try:
        # includes the message box where users can enter their message
        msg_box = driver.find_element_by_class_name('_1Plpp')

        # gets all the text elements in a chat
        span_class = 'selectable-text invisible-space copyable-text'
        elements = driver.find_elements_by_xpath('//span[@class = "{}"]'.format(span_class))
        if len(elements) > length_before:
            send_text(elements, msg_box)
    except:
        print('ERROR: No new message found in current Chat')


# checks, whether a new messages drops in other chats not in the current chat
def check_for_new_chat_new_message():
    try:
        user = driver.find_element_by_xpath('//span[@class = "{}"]'.format('OUeyt'))
        user.click()

        time.sleep(1)

        # includes the message box where users can enter their message
        msg_box = driver.find_element_by_class_name('_1Plpp')

        # gets all the text elements in a chat
        span_class = 'selectable-text invisible-space copyable-text'
        elements = driver.find_elements_by_xpath('//span[@class = "{}"]'.format(span_class))
        send_text(elements, msg_box)
        return True
    except:
        print('ERROR: No new message found in all chats')
        return False


# starts the bot
def start_bot():
    if check_for_new_chat_new_message():
        print('NEW MESSAGE FOUND IN ALL CHATS')
    else:
        check_for_current_chat_new_message()


if __name__ == '__main__':
    start_bool = input("ChatBot starten [START]: ")
    if start_bool == "START" or start_bool == "start":

        print('\n*** ChatBot wurde gestartet ***\n')

        length_before = 0
        already_answered = []

        while True:
            start_bot()
            print('CHAT LENGTH BEFORE ATTACHING: ' + str(length_before))
            try:
                length_before = set_length_before()
            except:
                print('ERROR: No data for length')
            print('CHAT LENGTH BEFORE ATTACHING: ' + str(length_before))
            print('------------------------------------------')
            print('')
            time.sleep(3)
