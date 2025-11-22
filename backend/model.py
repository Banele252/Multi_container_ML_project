# Building a logistic regression model
# development approach using function based
# this needs to run once after creating the running instance
# import the required libraries


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline #Must get used to using the Pipeline
from joblib import dump #used to create a running instance of the model (what is converted to a job is the model)


#import the required dataset 
dataset = pd.read_csv('Social_Network_Ads.csv')
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

#split the data between training set and test set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)


# # Scale the dataset
# sc_X = StandardScaler()
# x_train = sc_X.fit_transform(x_train)
# x_test = sc_X.transform(x_test)



# #Create a model object
# classifier = LogisticRegression()
# classifier.fit(x_train,y_train)

# #predict an outcome - This part has to be removed 
# print(classifier.predict(sc_X.transform(([[30,8700]]))))


#Use a pipeline (It is crazy how short this is)
pipeline = Pipeline(
    steps = [
        ('scaler',StandardScaler()),
        ('classifier',LogisticRegression())
    ]
)

pipeline.fit(x_train,y_train)

print(pipeline.predict([[30,8700]]))

# create a running instance of the model (run the below once)
#dump(pipeline,'./model.joblib')