# Use the official Python image
FROM python:3.12.8

# Set the working directory
WORKDIR /docker-for-development

# This command put requirements.txt in container in specific directory
COPY ./requirements.txt /docker-for-development/requirements.txt


# This command will install dependancies in docker container
RUN pip install --no-cache-dir --upgrade -r /docker-for-development/requirements.txt

# copy source code files and directory in docker container
COPY ./app /docker-for-development/app

# this is default command. It will run after container start. It is used for development only
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
