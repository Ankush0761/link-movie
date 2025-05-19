from pyrogram import Client, filters
from pymongo import MongoClient
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
STORE_CHANNEL = int(os.environ.get("STORE_CHANNEL"))
MONGO_URI = os.environ.get("MONGO_URI")

app = Client("indexer", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URI)
db = mongo['filter_bot']
coll = db['posts']

@app.on_message(filters.channel & filters.chat(STORE_CHANNEL))
async def index_post(client, message):
    if message.caption:
        coll.update_one(
            {"message_id": message.message_id},
            {"$set": {"caption": message.caption, "message_id": message.message_id}},
            upsert=True
        )

app.run()
