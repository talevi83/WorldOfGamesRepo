import random

import requests

def get_usd_to_ils_rate():
    """Fetches the current exchange rate for USD to ILS."""
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['rates']['ILS']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def get_money_interval(usd_amount, difficulty):
    rate = get_usd_to_ils_rate()
    if rate is None:
        return None, None

    total_value = usd_amount * rate
    lower_bound = total_value - (5 - difficulty)
    upper_bound = total_value + (5 - difficulty)

    return lower_bound, upper_bound

def get_guess_from_user(usd_amount):
    try:
        guess = float(input(f"Guess the value in ILS for ${usd_amount}: "))
        return guess
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def play(difficulty):
    usd_amount = random.randint(1, 100)
    print(f"Convert ${usd_amount} to ILS.")

    # Get the interval
    lower_bound, upper_bound = get_money_interval(usd_amount, difficulty)
    if lower_bound is None or upper_bound is None:
        print("Game cannot proceed due to an API error.")
        return False

    # Get the user's guess
    user_guess = get_guess_from_user(usd_amount)

    # Check if the guess is within the interval
    if lower_bound <= user_guess <= upper_bound:
        print("Congratulations! You won!\n\n")
        return True
    else:
        print(f"Sorry, you lost. The correct range was {lower_bound:.2f} to {upper_bound:.2f}.\n\n")
        return False



