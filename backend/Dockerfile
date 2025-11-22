#Import a base image. use 3.11-slim to avoid the pyarrow error
FROM python:3.11-slim

#create a work dir within the container

WORKDIR /app

#Update pip to latest version (avoid issues discovered in streamlit deployment)
# --no-cache-dire means do not store the packages on the pip directory inside a container.
RUN pip install --no-cache-dir --upgrade pip 

#copy the requirements txt file to the container
COPY requirements.txt /app

# install every required package to run the application.
# special consideration: the requirement file should be in the same directory
# docker is unable to read files in the parent folder (I am not sure about child folders)
RUN pip install --no-cache-dir -r requirements.txt


# Copy files from the machine to the container (no need to specify the work directory inside container)
COPY . /app/

# Set the port to listen from the container 
EXPOSE 8000

#How to execute the application
CMD ["uvicorn", "main:app","--host","0.0.0.0", "--port", "8000"]


#special considerations : files inside the scripts should be referenced like there is no parent folder 
# e.g., /backend/model.job --> /model.job





