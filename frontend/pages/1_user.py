#create a code for accessing mongoDB
import streamlit as st
from starlette import status
from fastapi import HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv("secrets/backend.env")
backend_container = os.getenv("BACKEND_CONTAINER")

#create a title for the input fields
st.title("User checks")
st.write("Monogo DB connection checks for users")

BASE_API_URL = f"http://{backend_container}:8000/mongodb"

age = st.number_input("Age",min_value= 11, max_value=70, value= 11, step=1)
username = st.text_input(label="Name", max_chars=50, placeholder="user")
email = st.text_input(label="Email", max_chars=50, placeholder="email")
id =  st.text_input(label='id',max_chars=200, placeholder="user_id")
if st.button('check user'):
    try:
         response = requests.get(f"{BASE_API_URL}/users/{id}",params={"_id":id})
         if response.status_code != 200:
             st.error(f"Unable to retrieve the user, user might not exist  {response.status_code}")
             #raise HTTPException(status_code=404, detail='User does not exist')
         if response.status_code == 200:
             result = response.json()
             st.success("successfully retrieved")
             st.write(result)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Bad request")

            





