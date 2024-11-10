ARG BUILD_FROM
FROM $BUILD_FROM

# Add Home Assistant Add-on labels
LABEL \
    io.hass.name="Bin Collection Schedule - Simbio v1" \
    io.hass.description="Displays waste collection schedule for your address - Simbio mode" \
    io.hass.arch="armhf|aarch64|i386|amd64|armv7" \
    io.hass.type="addon" \
    io.hass.version="1.1.90"

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install required packages
RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
        gcc \
        musl-dev \
        python3-dev \
        linux-headers

# Set working directory
WORKDIR /usr/src/app

# Create virtual environment
RUN python3 -m venv venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

# Install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /logs /config /ssl /tmp

# Copy your application files
COPY rootfs /
COPY run.sh /
COPY . .

# Set permissions
RUN chmod a+x /run.sh

# Expose the web interface port
EXPOSE 8081

# Start the application
CMD [ "/run.sh" ]