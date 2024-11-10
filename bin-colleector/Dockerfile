ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python3 and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /usr/src/app

# Create and activate a virtual environment
RUN python3 -m venv venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

# Copy requirements and install dependencies within the virtual environment
COPY requirements.txt .
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
CMD ["./run.sh"]
