# Simple WhatsApp-ChatBot
# Future Plan: integrating machine learning, so the bot can send messages by knowledge
# author: Tim Eichinger

from selenium import webdriver
from Calender import Calender
import time

driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com/')

global length_before
global already_answered

# your fullname and firstname, the bot should detect and use
fullname = "<your fullname>"
firstname = "<your firstname>"

# bad or offensive words that the bot can detect
# e.g.: bad_words = ['asshole', 'shithead']
bad_words = []

# groups and persons, the bot should not answer
# e.g.: groups_without_authorization = ['Footballteam 2019', 'Franz Maier']
groups_without_authorization = []

# checks and returns your current event
def get_current_event():
    return Calender.get_current_event()


# returns the answer the chat bot should print
def get_answer(texts, chat_name):

    if "ChatBot (v1.0)" in str(texts[-1]):
        print("ERROR: Last message was from Bot")
        return ""

    list_splitted_msg = str(texts[-1]).split()
    return_string = ""
    bad_words_already_in_string = False

    if fullname in str(texts[-1]) or firstname in str(texts[-1]):
        if chat_name in already_answered:
            return_string += get_current_event()
        else:
            return_string += firstname +  ' is currently not online. I take over! '
            return_string += get_current_event()
            already_answered.append(chat_name)
    elif chat_name not in already_answered:
        return_string += firstname +  ' is currently not online. I take over! '
        return_string += get_current_event()
        already_answered.append(chat_name)

    for item in list_splitted_msg:
        if item in bad_words and not bad_words_already_in_string:
            return_string += 'I discovered an insult (\"{}\")! I can not tolerate that!'.format(item)
            bad_words_already_in_string = True
    return return_string


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

    if chat_name in groups_without_authorization:
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
    start_bool = input("Start ChatBot [START]: ")
    if start_bool == "START" or start_bool == "start":

        print('\n*** ChatBot started ***\n')

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
