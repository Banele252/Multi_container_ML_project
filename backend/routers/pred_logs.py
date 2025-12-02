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
    prefix='/logs',
    tags=['logs']
)

load_dotenv('secrets/mongo.env')
username = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('LOGS')

##########################################################################################

mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.k3rfzyy.mongodb.net?appName=Cluster0"
# Create a new client and connect to the server
client = AsyncIOMotorClient(mongo_uri)  # This part helps with performing non-blocking (async) processes

# ✅ Access database and collection

db = client[f"{database}"] #If it does not exist, it create the DB.
collection = db["prediction_logs"]

class pred_log(BaseModel):
    salary: float
    age: int
    outcome: str

#log a predictions
@router.post("/prediction_logs/")
async def create_user(pred: pred_log):
    pred_dict = pred.model_dump()  # Updated from .dict()
    result = await collection.insert_one(pred_dict)
    return {"id": str(result.inserted_id), "message": "usage recorded"}

