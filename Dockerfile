# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /credit_approval_system

# Copy the dependencies file to the working directory
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# Expose port 8000 for the Django development server
EXPOSE 8000

