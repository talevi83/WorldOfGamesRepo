from Utils import SCORES_FILE_NAME


def add_score(difficulty):
        try:
            with open(SCORES_FILE_NAME, "r") as file:
                content = float(file.read().strip())
                content = content + (difficulty * 3) + 5
        except FileNotFoundError:
            content = (difficulty * 3) + 5

        with open(SCORES_FILE_NAME, "w") as file:
            file.write(str(content))

