# 1. THE BASE LAYER
# Start with a lightweight version of Python 3.10 (Linux)
FROM python:3.10-slim

# 2. THE SETUP
# Create a folder inside the container
WORKDIR /app

# 3. THE REQUIREMENTS
# Copy only the requirements file first (for caching speed)
# (We will create requirements.txt in a second)
COPY requirements.txt .

# Install the libraries inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 4. THE CODE
# Copy everything from your laptop folder to the container folder
COPY . .

# 5. THE COMMAND
# Tell the container what to do when it starts
# (Run your Startup API)
CMD ["python", "startup_api.py"]