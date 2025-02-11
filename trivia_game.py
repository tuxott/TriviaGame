#!/usr/bin/python3

"""
Trivia Game Script

Author: Tuxott
Description:
    This script implements a Linux CLI trivia game that fetches questions from an SQLite database.
    Users can select answers from multiple-choice options, and the script provides feedback
    on their selections, including whether the answer is correct and an explanation.
    
Usage:
    Run the script from the command line, providing the name of the SQLite database file
    containing the trivia questions as an argument.

Example:
    python3 trivia_game.py trivia_questions.db

Dependencies:
    - sqlite3: For database interaction
    - random: For shuffling questions and options
    - argparse: For command-line argument parsing
"""

import sqlite3
import random
import argparse

class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    RESET = "\033[0m"

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Specify the SQLite database name.')
    parser.add_argument('database_name', type=str, help='The name of the SQLite database file')
    return parser.parse_args()

def get_questions(database_name):
    """Fetch all trivia questions from the database."""
    try:
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT question, answer, explanation, distractor1, distractor2, distractor3, distractor4, distractor5 FROM questions")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"{Colors.RED}Database error: {e}{Colors.RESET}")
        return []

def main():
    """Main function to run the trivia game."""
    args = parse_arguments()
    trivia_questions = get_questions(args.database_name)
    random.shuffle(trivia_questions)

    for question_data in trivia_questions:
        question, answer, explanation, *distractors = question_data
        options = random.sample(distractors, k=min(3, len(distractors))) + [answer]
        random.shuffle(options)

        print(f"\n{question}")
        for idx, option in enumerate(options):
            print(f"{Colors.YELLOW}{idx + 1}.{Colors.RESET} {option}")

        while True:
            user_input = input(f"{Colors.YELLOW}Select an option (1-{len(options)}) or press 'q' to quit: {Colors.RESET}").strip()
            if user_input.lower() == 'q':
                print("Thank you for playing! Goodbye!")
                return  # Exit the game
            try:
                selected_index = int(user_input) - 1
                if 0 <= selected_index < len(options):
                    break
                print(f"{Colors.RED}Invalid selection. Please try again.{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}Please enter a number.{Colors.RESET}")

        selected_answer = options[selected_index]
        print(f"{Colors.GREEN if selected_answer == answer else Colors.RED}{'Correct!' if selected_answer == answer else f'Incorrect. The correct answer is: {answer}'}{Colors.RESET}")
        print(f"{Colors.BLUE}Explanation: {explanation}{Colors.RESET}")
        input(f"{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")

    print("Thank you for playing!")

if __name__ == "__main__":
    main()

