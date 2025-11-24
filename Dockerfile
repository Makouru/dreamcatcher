# use an official python runtime as a parent image
FROM python:3.10-slim

# set the working directory inside the container
WORKDIR /app

# copy all files to this working directory
COPY ./app /app

# install all required libraries given by the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# run the python entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]