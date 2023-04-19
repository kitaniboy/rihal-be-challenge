# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install Poppler
RUN apt-get update && apt-get install -y poppler-utils

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /code/

# Expose port 8000 for the Django development server
EXPOSE 8000

# Adding DB configration variables
ENV DB_NAME=rihal_challenge_db
ENV DB_USER=postgreuser
ENV DB_PASSWORD=SEeVw*r8eMYbdv%koPgiJ105n
ENV DB_HOST=db
ENV DB_PORT=5432

# Make database migrations
RUN python manage.py makemigrations app
RUN python manage.py makemigrations
