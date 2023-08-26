import asyncio
from pyrogram import Client


import random
import sqlite3

api_id =  27348755
api_hash = "190bab1ff00c4f6c4c698cf1157d1493"



csg = Client("acc", api_id, api_hash)

async def fffff():
    async with Client("acc", api_id, api_hash) as csg:
        s = input('File path :')
        await csg.send_document(chat_id=1624519308, document=s)




asyncio.run(fffff())