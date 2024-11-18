# Use the official lightweight Python image
FROM python:3.9-slim

# Set a working directory inside the container
WORKDIR /backend

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /backend/
# Create a directory for SSL certificates
WORKDIR /backend/certs
#Copy Certs
COPY ../certs/fullchain.pem /backend/certs/
COPY ../certs/privkey.pem /backend/certs/
# Running the web service
CMD [ "python","server.py"]