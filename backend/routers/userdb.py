from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, Query, APIRouter, HTTPException
from starlette import status
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

router = APIRouter(
    prefix='/users',
    tags=['users']
)

load_dotenv('secrets/mongo.env')
username = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

##########################################################################################

mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.k3rfzyy.mongodb.net?appName=Cluster0"
# Create a new client and connect to the server
client = AsyncIOMotorClient(mongo_uri)  # This part helps with performing non-blocking (async) processes

# ✅ Access database and collection

db = client[f"{database}"]
collection = db["users"]

class User(BaseModel):
    name: str
    age: int
    email: str
#create a single user
@router.post("/users/")
async def create_user(user: User):
    user_dict = user.model_dump()  # Updated from .dict()
    result = await collection.insert_one(user_dict)
    return {"id": str(result.inserted_id), "message": "User created"}

#create multiple users
@router.post("/users/bulk")
async def create_users(users: list[User]):
    users_dict = [user.model_dump() for user in users]  # Updated from .dict()
    result = await collection.insert_many(users_dict)
    return {"count": len(result.inserted_ids), "message": "Users created"}

#get all users
@router.get("/users/")
async def get_all_users():
    users = []
    cursor = collection.find()
    async for document in cursor:
        document["_id"] = str(document["_id"])
        users.append(document)
    return users


#update user based on the id
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: str):
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    return {"error": "User not found"}

#delet user based on id
@router.get("delete/{user_id}",status_code=status.HTTP_200_OK)
async def delete_user(user_id:str):
    try:
        results = await collection.delete_one({'_id':ObjectId(user_id)})
        if results is None:
            raise HTTPException(status_code=404, detail='user not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user ID: {str(e)}")
    


#update user based on id
@router.put("update_user/{user_id}",status_code=status.HTTP_201_CREATED)
async def update_user(user_id:str):
    try:
        results =  await collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set":{"name": "new_name"}}
        )
        if results is None:
            raise HTTPException(status_code=404, detail='details not found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Invalid user ID:{str(e)}')