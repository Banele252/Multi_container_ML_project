from fastapi import FastAPI, Query, APIRouter, HTTPException
from joblib import load
from starlette import status
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv('secrets/mongo.env')
logs = os.getenv("LOGS")


router = APIRouter(
    prefix='/prediction',
    tags=['prediction']
)

load_dotenv('secrets/mongo.env')
username = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.k3rfzyy.mongodb.net?appName=Cluster0"
# Create a new client and connect to the server
client = AsyncIOMotorClient(mongo_uri)  # This part helps with performing non-blocking (async) processes

# Access database and collection

db = client[f"{database}"] #If it does not exist, it create the DB.
collection = db["prediction_logs"]


# Usually a Base Model is used in a post request.
# class requestPrediction(BaseModel):
#     age:int = Field(gt=10, lt=70)

#if running the code locally, comment pipeline = load('model.joblib') and uncomment next line
#pipeline = load('backend/model.joblib') #The change done below is required by docker since it cannot interpret or process parent folders
pipeline = load('model.joblib')

@router.get('/makeprediction',status_code=status.HTTP_200_OK)
async def make_prediction(age:int = Query(gt=10,lt=70),salary:float = Query(gt=100,lt=100000000)):
    try:
        prediction = pipeline.predict([[age,salary]])
        pred_dict = {'age':age, 'salary':salary,\
                    "outcome": 'will not purchase the product' if int(prediction[0]) == 0 else 'will purchase the product'}  # Updated from .dict()
        await collection.insert_one(pred_dict)
        return {"prediction": 'will not purchase the product' if int(prediction[0]) == 0 else 'will purchase the product'}
    except:
        raise HTTPException(status_code=400, detail='Error encountered during processing')
