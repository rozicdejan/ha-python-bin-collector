ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python3 and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /usr/src/app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt || { echo "[ERROR] Pip install failed." >&2; exit 1; }

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p /data

# Set execution permissions for run script
RUN chmod a+x run.sh

# Add error logging to run.sh
RUN echo '#!/bin/bash\n\n# Run the application with error logging\npython3 /usr/src/app/main.py 2> /usr/src/app/error.log || { echo "[ERROR] Application failed to start. Check error.log for details." >&2; exit 1; }' > run.sh

# Make the script executable
RUN chmod +x run.sh

# Expose the port the app runs on
EXPOSE 8081

# Command to run the application
CMD ["./run.sh"]
