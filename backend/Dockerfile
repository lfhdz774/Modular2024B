# Use the official lightweight Python image
FROM python:3.9-slim

# Set a working directory inside the container
WORKDIR /backend

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /backend/
# Expose the port Flask runs on
#EXPOSE 5000
# Running the web service
CMD [ "flask","run", "--host", "0.0.0.0"]