
import random
import sys

from time import sleep

from Utils import screen_cleaner

game_difficulty = 1

def generate_sequence(difficulty):
    global game_difficulty
    game_difficulty = difficulty
    numbers_list = []
    for i in range(game_difficulty):
        numbers_list.append(random.randint(1, 101))

    return numbers_list

def get_list_from_user():
    user_input = input("Enter the numbers you saw separated by spaces: ")
    numbers_list =  list(map(int, user_input.split()))

    print("Checking input length...")
    if len(numbers_list) != game_difficulty:
        print(f"Invalid input. Please enter exactly {game_difficulty} numbers.")
        user_choice = input("Press 'r' to retry or any other key to quit.")
        if user_choice.lower() == 'r':
            return get_list_from_user()
        else:
            return None

    return numbers_list

def is_list_equal(a, b):
    return a == b

def erase_last_line():
    sys.stdout.write('\033[1A')   # Move cursor up one line
    sys.stdout.write('\033[2K')   # Delete the entire line
    sys.stdout.flush()

def play(difficulty):
    print("Welcome to the Memory Game!")

    random_numbers_list = generate_sequence(difficulty)

    print("Numbers will appear for 0.7 second, then you'll have to guess them back.")
    print("Ready?")
    sleep(1)
    print("Get Set!")
    sleep(1)
    print("GO!")
    print(random_numbers_list)
    sleep(0.7)

    screen_cleaner()
    #erase_last_line()

    user_list = get_list_from_user()
    result =  is_list_equal(user_list, random_numbers_list)
    if result:
        print("Congratulations! You guessed the correct sequence.\n\n")
    else:
        print(f"Sorry, the sequence you guessed is incorrect.\nThe right sequence is: {random_numbers_list}\n\n")

    return result
