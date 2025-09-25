# Use an official Python runtime as a parent image
FROM python:3.11-slim
ECHO is off.
# Set the working directory in the container
WORKDIR /usr/src/app
ECHO is off.
# Copy the current directory contents into the container at /usr/src/app
COPY . .
ECHO is off.
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ECHO is off.
# Run main.py when the container launches
CMD ["python", "src/main.py", "--mode", "swarm"]
