from Utils import SCORES_FILE_NAME
from flask import Flask

app = Flask(__name__)

@app.route('/')
def score_server():
    try:
        with open(SCORES_FILE_NAME, "r") as file:
            scores = float(file.read().strip())
            return add_to_html(scores)
    except FileNotFoundError as e:
        return add_to_html(str(e))

@app.route('/health')
def health_check():
    return 'OK', 200

def add_to_html(score):
    return f"""<html>
    <head>
    <title>Scores Game</title>
    </head>
    <body>
    <h1>The score is <div id="score">{score}</div></h1>
    </body>
    </html>"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8777, debug=True, use_reloader=False)