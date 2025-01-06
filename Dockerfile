FROM python:3.9-slim

# Install Chrome and ChromeDriver dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set essential environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV FLASK_APP=MainScores.py
ENV FLASK_DEBUG=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8777

ENTRYPOINT ["python", "-c", "from MainScores import app; app.run(host='0.0.0.0', port=8777, debug=True, use_reloader=False)"]