FROM python:3.9-slim

WORKDIR /app

RUN pip install flask

COPY MainScores.py .
COPY Scores.txt /Scores.txt

EXPOSE 5000

CMD ["python", "MainScores.py"]