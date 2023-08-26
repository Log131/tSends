import asyncio
from pyrogram import Client


import random
import sqlite3

api_id =  27348755
api_hash = "190bab1ff00c4f6c4c698cf1157d1493"



csg = Client("acc", api_id, api_hash)

@csg.on_message()
async def fffff(client, message):
    if message.text == 'sends':
        s = input('File path')
        await csg.send_document(chat_id='me', document=s)









csg.run()