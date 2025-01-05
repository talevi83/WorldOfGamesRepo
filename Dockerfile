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
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8777
ENV PYTHONUNBUFFERED=1

# Set up working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8777

# Command to run the application
CMD ["python", "MainScores.py"]