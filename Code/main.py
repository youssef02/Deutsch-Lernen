import os
import json
import random

flashcards_file_path = "data/flashcards/flashcards.json"
quiz_file_path = "data/quiz/quiz.json"

def input_centered(prompt):
    return input(f"{prompt.center(80)} \n \t \t \t-->")

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_centered(text, width=80):
    print(f"{text.center(width)}\n", end="")

def print_table(header, rows):
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(header, *rows)]
    format_str = ' | '.join(f'{{:<{width}}}' for width in col_widths)
    
    print(format_str.format(*header))
    print('-' * (sum(col_widths) + len(col_widths) * 3 - 1))  # Line separating header and rows
    
    for row in rows:
        print(format_str.format(*row))

def create_menu():
    return [
        {"option": "1", "description": "Start Flashcards Game"},
        {"option": "2", "description": "Start Quiz Game"},
        {"option": "3", "description": "Add Flashcard"},
        {"option": "4", "description": "Add Quiz Question"},
        {"option": "5", "description": "Exit"}
    ]

def print_menu(menu):
    header = ["Option", "Description"]
    rows = [[item["option"], item["description"]] for item in menu]
    print_table(header, rows)

def main_menu():
    while True:
        
        print_centered("Welcome to the German Game!")

        menu = create_menu()
        print_menu(menu)

        choice = input_centered("Select an option (1-5): \n").strip()

        option_handlers = {
            "1": flashcard_game,
            "2": quiz_game,
            "3": add_flashcard,
            "4": add_quiz_question,
            "5": exit_game
        }

        handler = option_handlers.get(choice)
        if handler:
            handler()

def flashcard_game():
    flashcards = load_flashcards()
    if not flashcards:
        return

    german_words = [card["word"] for card in flashcards]
    score = 0

    while german_words:
        current_word = random.choice(german_words)
        display_flashcard(current_word)

        tries = 3
        while tries > 0:
            user_translation = input("Your translation: ").strip().lower()
            correct_translation = next(card["translation"].lower() for card in flashcards if card["word"] == current_word)

            # Calculate Levenshtein distance
            distance = Levenshtein.distance(user_translation, correct_translation)

            if distance == 0:
                print("Correct!\n")
                score += 1
                break
            elif 0 < distance <= 2:
                print(f"Close! The correct translation is: {correct_translation}\n")
                score += 1
                break
            else:
                tries -= 1
                if tries > 0:
                    print(f"Wrong! {tries} {'tries' if tries > 1 else 'try'} left. Try again.")
                else:
                    print(f"Wrong! The correct translation is: {correct_translation}\n")

        german_words.remove(current_word)
    clear_screen()

    print(f"Game Over! Your score: {score}/{len(flashcards)}")


def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON in '{file_path}'.")
        return None

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def load_flashcards():
    flashcards_file_path = "data/flashcards/flashcards.json"
    flashcard_data = load_data(flashcards_file_path)
    if flashcard_data and "flashcards" in flashcard_data:
        return flashcard_data["flashcards"]
    return []

def save_flashcards(flashcards):
    flashcards_file_path = "data/flashcards/flashcards.json"
    flashcard_data = {"flashcards": flashcards, "flashcard_info": {"count": len(flashcards), "level": 1}}
    save_data(flashcards_file_path, flashcard_data)

def display_flashcard(word):
    print(f"Translate: {word}")

def load_quiz():
    quiz_file_path = "data/quiz/quiz.json"
    quiz_data = load_data(quiz_file_path)
    if quiz_data and "quiz" in quiz_data:
        return quiz_data["quiz"]
    return []

def save_quiz(quiz):
    quiz_file_path = "data/quiz/quiz.json"
    quiz_data = {"quiz": quiz, "quiz_info": {"count": len(quiz), "level": 1}}
    save_data(quiz_file_path, quiz_data)

def display_quiz(question, options):
    print(f"Question: {question}")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

def get_user_choice(options_count):
    while True:
        try:
            user_choice = int(input("Your choice (enter the number): ").strip())
            if 1 <= user_choice <= options_count:
                return user_choice
            else:
                print(f"Invalid choice. Please enter a number between 1 and {options_count}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def quiz_game():
    quiz = load_quiz()
    if not quiz:
        print("No quiz questions available. Add quiz questions first.")
        return

    score = 0

    for question_data in quiz:
        question = question_data.get("question", "")
        options = question_data.get("options", [])

        display_quiz(question, options)

        correct_option = question_data.get("correct_option", -1)

        user_choice = get_user_choice(len(options))

        if user_choice == correct_option:
            print("Correct!\n")
            score += 1
        else:
            correct_option_text = options[correct_option - 1]
            print(f"Wrong! The correct option is: {correct_option_text}\n")
    clear_screen()
    print(f"Game Over! Your score: {score}/{len(quiz)}")

def create_flashcard():
    word = input("Enter the German word: ").strip()
    translation = input("Enter the English translation: ").strip()
    return {"word": word, "translation": translation}

def create_quiz_question():
    question = input("Enter the quiz question: ").strip()
    options_count = int(input("Enter the number of options: ").strip())
    
    options = []
    for i in range(options_count):
        option = input(f"Enter option {i + 1}: ").strip()
        options.append(option)

    correct_option = get_user_choice(options_count)

    return {"question": question, "options": options, "correct_option": correct_option}

def add_flashcard():
    flashcards = load_flashcards()
    flashcard = create_flashcard()
    flashcards.append(flashcard)
    save_flashcards(flashcards)
    print("Flashcard added successfully.")

def add_quiz_question():
    quiz = load_quiz()
    question = create_quiz_question()
    quiz.append(question)
    save_quiz(quiz)
    print("Quiz question added successfully.")

def exit_game():
    print("Exiting the game. Goodbye!")
    quit()

if __name__ == "__main__":
    main_menu()
