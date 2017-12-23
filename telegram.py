#!/usr/bin/python3


#coding: utf-8

import telepot
from Chatbot import Chatbot

#token stive = "481983440:AAEtfnMsArVAjPqG3h5p8S0FMDBMRdu263I"
#token servius = "468696994:AAFq2Y-jaR4sVP6nUbgZsOdjtbHUmzrog8I"

token = "468696994:AAFq2Y-jaR4sVP6nUbgZsOdjtbHUmzrog8I"
telegram = telepot.Bot(token)
bot = Chatbot("Servius_robot")

#Chatbot.create_table()


def recebendoMsg(msg):
    frase = bot.escuta(frase=msg['text'])
    tipoMsg, tipoChat, chatID = telepot.glance(msg)

    if chatID == 361691746 or chatID == 498763575 or chatID == 339652825 or chatID == 337871713:
        resp = bot.pensa(frase, chatID)
        bot.fala(resp)
        telegram.sendMessage(chatID,resp)
    else:
        tipoMsg, tipoChat, chatID = telepot.glance(msg)
        telegram.sendMessage(chatID, 'Não estou autorizado a falar!')
        print(chatID)

telegram.message_loop(recebendoMsg)

while True:
    pass