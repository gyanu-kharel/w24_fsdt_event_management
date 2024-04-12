uri = "mongodb+srv://gyanmanikharel:mysecretpassword@w24ems.xf8fku0.mongodb.net/?retryWrites=true&w=majority&appName=w24ems"

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(uri)

db = client.w24ems

events_db_collection = db.get_collection("events")