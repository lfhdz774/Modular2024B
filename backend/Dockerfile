# Use the official lightweight Python image
FROM python:3.9-slim

# Set a working directory inside the container
WORKDIR /backend

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /backend/

# Step 4: Copy the Flask app and SSL certificates to the container
COPY /certs/ /backend/certs/

EXPOSE 5000

# Running the web service
CMD [ "python","server.py"]