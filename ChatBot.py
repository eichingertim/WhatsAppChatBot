# Simple WhatsApp-ChatBot
# Future Plan: integrating machine learning, so the bot can send messages by knowledge
# author: Tim Eichinger
# Requirements: Latest Chrome or Firefox driver for Test-Automation

from selenium import webdriver
import time
import random

# get driver and open web-page
driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com/')

# variable for the length before scanning
global length_before

bad_words = ['Larry', 'larry', 'Spast', 'spast', 'Spasti', 'spasti', 'Depp', 'depp', 'hurensohn',
             'Hurensohn', 'Huansohn', 'huansohn', 'wixer', 'Wixer']


def get_answer(texts):
    list_splitted_msg = str(texts[-1]).split()
    for item in list_splitted_msg:
        if item in bad_words:
            i = random.randint(0, len(bad_words) - 1)
            return 'Ich habe eine Beleidigung entdeckt ({})! Du {}!'.format(item, bad_words[i])
    for message in texts:
        if 'Tim Eichinger' in str(message):
            return 'Tim ist zurzeit nicht online.'


def send_text(par_elements, par_msg_box):
    texts = []
    for elem in par_elements:
        texts.append(elem.text)
    par_msg_box.send_keys("*ChatBot (v1.0):* " + get_answer(texts))
    btn = driver.find_element_by_class_name('_35EW6')
    btn.click()


def set_length_before():
    # gets all the text elements in a chat
    span_class = 'selectable-text invisible-space copyable-text'
    elements = driver.find_elements_by_xpath('//span[@class = "{}"]'.format(span_class))
    return len(elements)


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
        print('No new message')


def check_for_new_chat_new_message():
    user = driver.find_element_by_xpath('//span[@class = "{}"]'.format('OUeyt'))
    user.click()

    time.sleep(1)

    # includes the message box where users can enter their message
    msg_box = driver.find_element_by_class_name('_1Plpp')

    # gets all the text elements in a chat
    span_class = 'selectable-text invisible-space copyable-text'
    elements = driver.find_elements_by_xpath('//span[@class = "{}"]'.format(span_class))
    send_text(elements, msg_box)


def start_bot():
    try:
        check_for_new_chat_new_message()
    except:
        check_for_current_chat_new_message()
    print('No new message from any chatroom')


if __name__ == '__main__':
    start_bool = input("ChatBot starten [START]: ")
    if start_bool == "START":
        length_before = 0
        while True:
            start_bot()
            print('Length before attaching: ' + str(length_before))
            try:
                length_before = set_length_before()
            except:
                print('No data for length')
            print('Length after attaching: ' + str(length_before))
            time.sleep(3)
