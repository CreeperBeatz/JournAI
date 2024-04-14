# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Get g++ for hnsw library compilation
RUN apt-get update && apt-get install -y g++
ENV CXXFLAGS="-std=c++11"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]