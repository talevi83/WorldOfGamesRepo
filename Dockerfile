FROM python:3.9-slim

WORKDIR /app

RUN pip install flask

COPY Scores.txt /Scores.txt
RUN chmod 644 /Scores.txt

RUN echo 'from flask import Flask, send_file, request\napp = Flask(__name__)\n\n@app.route("/<path:filename>")\ndef scores(filename):\n    if filename.lower() == "scores.txt":\n        return send_file("/Scores.txt")\n    return "File not found", 404' > app.py

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]