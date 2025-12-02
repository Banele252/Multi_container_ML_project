from fastapi import FastAPI, Query
from joblib import load
from .routers import prediction,userdb # use this running code locally, do not use when starting a container.
#from routers import prediction,userdb

#create a Main API instance
app = FastAPI()

#Link the sub- API to the main API
app.include_router(prediction.router)
app.include_router(userdb.router)

# Usually a post used pydantic
# class requestPrediction(BaseModel):
#     age:int = Field(gt=10, lt=70)

#if running the code locally, comment pipeline = load('model.joblib') and uncomment next line
#pipeline = load('backend/model.joblib') The change done below is required by docker since it cannot interpret or process parent folders
# pipeline = load('model.joblib')

# @app.get('/makeprediction')
# async def make_prediction(age:int = Query(gt=10,lt=70) ,salary:float = Query(gt=100,lt=100000000)):
#     prediction = pipeline.predict([[age,salary]])
#     return {"prediction": 'will not purchase the product' if int(prediction[0]) == 0 else 'will purchase the product'}
