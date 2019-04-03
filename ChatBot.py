# Simple WhatsApp-ChatBot, where the bot sends a new message again.
# Future Plan: integrating machine learning, so the bot can send messages by knowledge
# author: Tim Eichinger
# Requirements: Latest Chrome or Firefox driver for Test-Automation

from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com/')

name = input("Enter user or group: ")

input("Enter anything after scanning QR Code")

# includes the element of the specific chat-room. The chat-room is selected by its name
user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
user.click()

# includes the message box where users can enter their message
msg_box = driver.find_element_by_class_name('_1Plpp')

# gets all the text elements in a chat
span_class = 'selectable-text invisible-space copyable-text'
elements = driver.find_elements_by_xpath('//span[@class = "{}"]'.format(span_class))

# the array-length of all the text elements at the first check
elem_len_before = len(elements)


# sends the latest message again to chat
def send_text():
    texts = []
    for elem in elements:
        texts.append(elem.text)
    msg_box.send_keys("ChatBot:\n"+texts[-1])
    btn = driver.find_element_by_class_name('_35EW6')
    btn.click()


# checks if in the chat is new message
while True:
    elements = driver.find_elements_by_xpath('//span[@class = "{}"]'.format(span_class))
    if len(elements) > elem_len_before:
        send_text()
        elem_len_before += 2

    time.sleep(5)
