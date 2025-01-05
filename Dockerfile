# Use a Python base image
FROM python:3.9

# Install Chrome and ChromeDriver dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    curl \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Set up Chrome environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV FLASK_APP=MainScores.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1

# Set up working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Create volume mount point
VOLUME /app

# Expose port
EXPOSE 8777

# Entry point to ensure Flask runs on 0.0.0.0
ENTRYPOINT ["python", "-c", "from MainScores import app; app.run(host='0.0.0.0', port=8777, debug=True, use_reloader=False)"]