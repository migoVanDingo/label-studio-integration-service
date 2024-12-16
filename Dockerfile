# Use the official Python 3.10.10 image
FROM python:3.10.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5005

# Set the environment variable for Flask
ENV FLASK_APP=app.py  
#Replace with your Flask apps filename

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
