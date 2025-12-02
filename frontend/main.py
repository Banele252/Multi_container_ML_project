import streamlit as st
import requests
import os
from dotenv import load_dotenv  # load the environment variables from .env file

load_dotenv('secrets/backend.env')
backend_container = os.getenv('BACKEND_CONTAINER')


API_URL = f"http://{backend_container}:8000/prediction/makeprediction"


st.set_page_config (
    page_title="main",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="auto"
)

#create a title for the input fields
st.title("Purchase prediction app")
st.write("Enter the age and salary of a potential customer to check if they will make a purchase")


age = st.number_input("Age",min_value= 11, max_value=70, value= 11, step=1)
salary = st.number_input("Salary", min_value=101.0, max_value= 9999999.0, value=101.0, step=1000.0)

#prediction button
# Prediction button
if st.button("Make Prediction"):
    try:
        # Make API request
        response = requests.get(API_URL, params={"age": age, "salary": salary})
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            prediction = result["prediction"]
            
            # Display result
            st.success("Prediction successful!")
            
            if prediction == 'will not purchase the product':
                st.write("### ❌ Prediction: **Will NOT Purchase**")
                
            else:
                st.write("###  🎯 Prediction: **Will Purchase**")
                st.balloons()
            
            # Display input details
            st.write("---")
            st.write("**Input Details:**")
            st.write(f"- Age: {age}")
            st.write(f"- Salary: ${salary:,.2f}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure FastAPI is running on http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add information section
st.sidebar.title("About")
st.sidebar.info(
    "This app uses a Logistic Regression model to predict whether a customer "
    "will make a purchase based on their age and salary."
)
st.sidebar.write("**API Status**")
try:
    response = requests.get(f"http://{backend_container}:8000/docs")
    if response.status_code == 200:
        st.sidebar.success("✅ API is running")
    else:
        st.sidebar.error("❌ API is not responding")
except:
    st.sidebar.error("❌ API is not running")

