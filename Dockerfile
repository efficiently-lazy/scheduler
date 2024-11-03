# Start with a base image that includes Python
FROM python:3.9-slim

# Set environment variables for unbuffered output (optional for debugging)
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY src/ /app/src

# Default to an interactive shell
CMD ["bash"]
