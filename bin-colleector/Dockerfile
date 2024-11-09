FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /usr/src/app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p /data

# Set execution permissions for run script
RUN chmod a+x run.sh

# Expose the port the app runs on
EXPOSE 8081

# Command to run the application
CMD [ "./run.sh" ]