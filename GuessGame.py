from difflib import diff_bytes
import random

secret_number = 1
game_difficulty = 1

def generate_number(difficulty):
    global game_difficulty, secret_number
    game_difficulty = difficulty
    secret_number = int(random.randint(1, difficulty))

def get_guess_from_user():
    return int(input(f"Enter number between 1 and {str(game_difficulty)}: "))

def compare_results(guessed_number):
    return secret_number == guessed_number

def play(difficulty):
    print('Welcome to the Guess Game!')

    generate_number(difficulty)
    guessed_number = get_guess_from_user()

    if compare_results(guessed_number):
        print('Congratulations! You guessed the correct number.\n\n')
    else:
        print(f"Sorry, the number you guessed is incorrect.\nThe correct number is: {str(secret_number)}\n\n")

    return



