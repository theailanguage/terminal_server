# Use the official Python 3.11-slim image as the base image.
FROM python:3.11-slim
# This ensures we start with a lightweight, modern Python environment (Python 3.11, which is above 3.10).

# Set the working directory inside the container to /app.
WORKDIR /app
# All subsequent commands will run in this directory.

# Copy all files from the current directory (your terminal_server code) into /app in the container.
COPY . /app
# This transfers your entire server code to the container.

# Install any required Python packages from requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt
# The --no-cache-dir flag helps keep the image small by not caching installation files.
# Ensure your requirements.txt lists all dependencies needed by your terminal server.

# Expose port 5000 so that the container can accept incoming connections.
EXPOSE 5000
# Adjust this port if your server listens on a different port.

# Define the command to run your terminal server.
CMD ["python", "terminal_server.py"]
# This command starts your custom terminal server when the container launches.
