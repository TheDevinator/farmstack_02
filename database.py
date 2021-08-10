from model import *
import motor.motor_asyncio
from dotenv import dotenv_values
import os
import pymongo


print("os.environ", os.environ)
env = os.environ.get("PYTHON_ENV")
print("Process env", env)
if(env =="production"):
   DATABASE_URI = os.environ.get("DATABASE_URI")
   print("DATABASE_URI PROD", DATABASE_URI)
else :
    config = dotenv_values(".env")
    DATABASE_URI = config.get("DATABASE_URI")
    print("DATABASE_URI DEV", DATABASE_URI)

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
print("client Final", client)
print("DATABASE_URI Final", DATABASE_URI)


# client = pymongo.MongoClient("mongodb+srv://rekyou:n%40%40h95xg4pR%2APiQMONGODB@rekyou01db-hbv8l.mongodb.net/farmstack01?retryWrites=true&w=majority")
# print("client 2", client)

database = client.TodoDatabase
collection = database.todos

async def fetch_all_todos():
    todos = []
    cursor = collection.find()
    async for doc in cursor:
        todos.append(Todo(**doc))
    return todos

async def fetch_one_todo(nanoid):
    doc = await collection.find_one({"nanoid": nanoid}, {"_id": 0})
    return doc

async def create_todo(todo):
    doc = todo.dict()
    await collection.insert_one(doc)
    result = await fetch_one_todo(todo.nanoid)
    return result

async def change_todo(nanoid, title, desc, checked):
    await collection.update_one({"nanoid": nanoid}, {"$set": {"title": title, "desc": desc, "checked": checked}})
    result = await fetch_one_todo(nanoid)
    return result

async def remove_todo(nanoid):
    await collection.delete_one({"nanoid": nanoid})
    return True