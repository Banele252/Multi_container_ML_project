from fastapi import FastAPI, Query, APIRouter, HTTPException
from joblib import load
from starlette import status

router = APIRouter(
    prefix='/prediction',
    tags=['prediction']
)

# Usually a Base Model is used in a post request.
# class requestPrediction(BaseModel):
#     age:int = Field(gt=10, lt=70)

#if running the code locally, comment pipeline = load('model.joblib') and uncomment next line
pipeline = load('backend/model.joblib') #The change done below is required by docker since it cannot interpret or process parent folders
#pipeline = load('model.joblib')

@router.get('/makeprediction',status_code=status.HTTP_200_OK)
async def make_prediction(age:int = Query(gt=10,lt=70),salary:float = Query(gt=100,lt=100000000)):
    try:
        prediction = pipeline.predict([[age,salary]])
        return {"prediction": 'will not purchase the product' if int(prediction[0]) == 0 else 'will purchase the product'}
    except:
        raise HTTPException(status_code=400, detail='Error encountered during processing')
