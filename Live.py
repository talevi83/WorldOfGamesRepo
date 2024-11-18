def welcome(name):
    return (f"Hello {name} and welcome to the World of Games (WoG).\n"
            f"Here you can find many cool games to play.\n")


def validate_user_input(message:str, min:int, max:int):
    while True:
        try:
            user_input = int(input(f"{message} "))
            if user_input >= min and user_input <= max:
                return user_input
            else:
                print(f"Invalid input. Please enter a number between {min} and {max}.\n\n")
        except ValueError:
            print("Invalid input. Please enter a number.\n\n")


def load_game():
        game_choice_message = ("Please choose a game to play or 'q' to quit: \n"
                   "1. Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back\n"
                   "2. Guess Game - guess a number and see if you chose like the computer\n"
                   "3. Currency Roulette - try and guess the value of a random amount of USD in ILS \n")

        game_choice = validate_user_input(game_choice_message, 1, 3)

        difficulty_choice = validate_user_input("Please choose game difficulty from 1 to 5: ",1, 5)

        match game_choice:
            case 1:
                from MemoryGame import play
                play(difficulty_choice)
            case 2:
                from GuessGame import play
                play(difficulty_choice)
            case 3:
                from CurrencyRoletteGame import play
                play(difficulty_choice)




