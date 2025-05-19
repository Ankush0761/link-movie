from pyrogram import Client, filters
from pymongo import MongoClient
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
STORE_CHANNEL = os.environ.get("STORE_CHANNEL")
MONGO_URI = os.environ.get("MONGO_URI")
GROUP_ID = int(os.environ.get("GROUP_ID"))  # Bot respond karega sirf isi group me

app = Client("filter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URI)
coll = mongo['filter_bot']['posts']

@app.on_message(filters.group & filters.chat(GROUP_ID) & filters.text)
async def group_filter_handler(client, message):
    query = message.text.strip().lower()
    result = coll.find_one({"caption": {"$regex": query, "$options": "i"}})
    if result:
        await app.copy_message(
            chat_id=message.chat.id,
            from_chat_id=int(STORE_CHANNEL),
            message_id=result["message_id"]
        )
    else:
        await message.reply("Sorry, result nahi mila.")

app.run()
