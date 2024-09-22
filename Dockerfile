# Step 1: Use a base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy requirements.txt to the container
COPY requirements.txt .

# Step 4: Install the required packages
RUN pip install -r requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . .

# Step 6: Expose the port the app runs on (e.g., 5000 for a Flask app)
EXPOSE 5000

# Step 7: Define the command to run the application
CMD ["python"]
