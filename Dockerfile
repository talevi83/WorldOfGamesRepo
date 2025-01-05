FROM python:3.9-slim

WORKDIR /app

RUN pip install flask

COPY MainScores.py .
COPY Utils.py .
COPY Scores.txt .

EXPOSE 5000

ENV FLASK_APP=MainScores.py
CMD ["python", "MainScores.py"]