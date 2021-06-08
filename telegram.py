# importing all required libraries
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

#https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e
 
def telegram_sms(): 
    api_id = ''
    api_hash = ''
    token = 'bot token'
    message = "Working..."
    phone = ''
    client = TelegramClient('session', api_id, api_hash)
    
    client.connect()
    
    try:
        receiver = InputPeerUser('user_id', 'user_hash')
        client.send_message(receiver, message, parse_mode='html')
    except Exception as e:
        print(e)
    
    client.disconnect()

telegram_sms()