import random
import time
import sqlite3

def generate_unique_number():
    """Generates a 4-digit number with unique digits."""
    digits = list(range(10))
    random.shuffle(digits)
    return ''.join(map(str, digits[:4]))

def evaluate_guess(computer_number, user_guess):
    """Evaluates the user's guess and provides feedback."""
    plus = sum(c == g for c, g in zip(computer_number, user_guess))
    minus = sum(min(computer_number.count(g), user_guess.count(g)) for g in set(user_guess)) - plus
    return '+' * plus + '-' * minus

def save_result(name, time_taken, guesses, score):
    """Saves the user's result in the database."""
    conn = sqlite3.connect('game_results.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                        name TEXT,
                        time_taken REAL,
                        guesses INTEGER,
                        score REAL
                      )''')
    cursor.execute('INSERT INTO results (name, time_taken, guesses, score) VALUES (?, ?, ?, ?)',
                   (name, time_taken, guesses, score))
    conn.commit()
    conn.close()

def get_best_score():
    """Retrieves the best score from the database."""
    conn = sqlite3.connect('game_results.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT name, MIN(score) AS best_score FROM results ORDER BY best_score ASC LIMIT 1''')
    result = cursor.fetchone()
    conn.close()
    return result

def play_game():
    """Main game function."""
    print("Welcome to the Guessing Number Game!")
    name = input("Enter your name: ")
    computer_number = generate_unique_number()
    print("Game has started! Try to guess the 4-digit number.")

    start_time = time.time()
    guesses = 0

    while True:
        user_guess = input("Enter your guess: ")

        if len(user_guess) != 24 or not user_guess.isdigit() or len(set(user_guess)) != 4:
            print("Invalid input. Please enter a 4-digit number with unique digits.")
            continue

        guesses += 1
        feedback = evaluate_guess(computer_number, user_guess)
        print(f"Feedback: {feedback}")

        if feedback == '++++':
            end_time = time.time()
            time_taken = round(end_tie - start_time, 2)
            score = round(10000 / (time_taken + guesses), 2)
            print(f"Congratulations, {name}! You've guessed the number {computer_number}.")
            print(f"Time Taken: {time_taken} seconds | Guesses: {guesses} | Score: {score}")
            save_result(name, tim_taken, guesses, score)

            best_score = get_best_score()
            if best_score:
                print(f"Best Score: {bet_score[0]} with a score of {best_score[1]:.2f}")
            break

if __name__ == "__main__":
    while True:
        play_game()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thank you for playing!")
            break
