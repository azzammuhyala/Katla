"""
Katla raw - Logic concept of how Katla works in detail and as testing material
"""

# importing modules need
import asciiTUI
import random
import time
import os
# importing file components
from components.katla_module import constants as const
from components.katla_module.json_validator import WordsValidator

# Class to implement the Katla game logic
class Katla:

    def __init__(self, language: str = 'idn', word_length: int = 5, change_guess: int = 6) -> None:

        # Initialize the WordsValidator to load and validate the dictionary
        self.words_validator = WordsValidator(language)
        self.dictionary = self.words_validator.load_and_validation()

        # Initialize game settings
        self.language = language
        self.word_length = word_length
        self.change_guess = change_guess

        # Define color codes for feedback
        self.color_code = {
            'green': '\033[32m',
            'yellow': '\033[33m',
            'red': '\033[31m',
            'gray': '\033[90m'
        }

        # Prepare the list of valid words from the dictionary
        self.words_list = [word.upper() for word in self.dictionary[f'length-{self.word_length}']]
        self.keyboards_feedback_history = []
        self.guess_count = self.change_guess
        self.selected_word = random.choice(self.words_list)
        self.guessed = False

    def reset(self) -> None:
        # Reset the game state to start a new game
        self.keyboards_feedback_history.clear()
        self.guess_count = self.change_guess
        self.selected_word = random.choice(self.words_list)
        self.guessed = False

    def cls(self) -> None:
        # Clear the console screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def printinfo(self, *args, sleep: const.Number = 1, **kwargs) -> None:
        # Print information with a sleep interval
        print(*args, **kwargs)
        time.sleep(sleep)

    def get_feedback_colors(self, guess_word: str) -> const.Feedback:
        feedback = []
        # Calculate the frequency of each character in the guess and the selected word
        guess_char_frequency = {char: guess_word.count(char) for char in set(guess_word)}
        selected_char_frequecy = {char: guess_word.count(char) for char in set(self.selected_word)}

        for i, char in enumerate(guess_word):

            if char not in self.selected_word:
                # Character is not in the selected word
                feedback.append({char: "red"})

            elif char == self.selected_word[i] and selected_char_frequecy[char] > 0:
                # Character is in the correct position
                feedback.append({char: "green"})
                guess_char_frequency[char] -= 1
                selected_char_frequecy[char] -= 1

            elif char in self.selected_word and selected_char_frequecy[char] > 0 and guess_char_frequency[char] > 0:
                # Character is in the word but in the wrong position
                feedback.append({char: "yellow"})
                selected_char_frequecy[char] -= 1

            elif char == self.selected_word[i]:
                # Character is in the correct position but already marked
                for j, item in enumerate(feedback):
                    if list(item.keys())[0] == char:
                        if feedback[j][char] == "yellow":
                            feedback.append({char: "green"})
                            feedback[j][char] = "red"
                            guess_char_frequency[char] -= 1
                            selected_char_frequecy[char] -= 1
                            break

            elif char in self.selected_word:
                # haracter is in the word but in the wrong position and already marked
                for j, item in enumerate(feedback):
                    if list(item.keys())[0] == char:
                        if feedback[j][char] in ["green", "yellow"] and guess_char_frequency[char] > 0:
                            guess_char_frequency[char] -= 1
                            feedback.append({char: "red"})
                            break

        return feedback
    
    def showKeyboard(self) -> None:
        # Display the keyboard with color-coded feedback
        layout_keyboard = const.Keyboard.QWERTY
        keyboard_ascii = '+---------------------+\n'
        keyboard_feedback = {char: 'gray' for line in layout_keyboard for char in line}

        # Update keyboard feedback based on guess history
        for attempt_feedback in self.keyboards_feedback_history:
            for item in attempt_feedback:
                for char, color in item.items():
                    if color in ['green', 'yellow', 'red']:
                        if keyboard_feedback[char] == 'green' or (keyboard_feedback[char] == 'yellow' and color == 'red'):
                            continue
                        keyboard_feedback[char] = color

        # Construct ASCII representation of the keyboard
        for ln, line in enumerate(layout_keyboard):
            keyboard_ascii += '| ' if ln in [0, 2] else '|  '

            for char in line:
                color = keyboard_feedback[char.upper()]

                # Replace backspace and newline characters for display
                if char == '\b':
                    char = '<-'
                elif char == '\n':
                    char = '\\n'

                keyboard_ascii += f'{self.color_code[color]}{char}\033[0m '

            keyboard_ascii += '|\n' if ln in [0, 2] else ' |\n'

        keyboard_ascii += '+---------------------+'

        # Display the keyboard
        for ln in keyboard_ascii.split('\n'):
            print(asciiTUI.justify(ln, asciiTUI.terminal_size('x'), wrap=False))

    def showBoardGame(self) -> None:
        # Display the game board with feedback for each guess
        word_ascii = ''
        empty_feedback = [f'\033[90m{"-" * self.word_length}\033[0m' for _ in range(self.guess_count)]

        # Display feedback for each guess
        for attempt_feedback in self.keyboards_feedback_history:
            for char_feedback in attempt_feedback:
                for char, color in char_feedback.items():
                    word_ascii += f'{self.color_code[color]}{char}\033[0m'
            print(asciiTUI.justify(word_ascii, asciiTUI.terminal_size('x'), wrap=False))
            word_ascii = ''

        # Display remaining empty slots
        for x in empty_feedback:
            print(asciiTUI.justify(x, asciiTUI.terminal_size('x'), wrap=False))

        # Display keyboard below the board
        print()
        self.showKeyboard()
        print()

    def main(self) -> None:
        while True:

            # Main game loop to process guesses
            while not self.guessed:
                # Clear the console and show the game board
                self.cls()
                self.showBoardGame()

                # Check if no guesses left
                if self.guess_count <= 0:
                    print(f'\033[31mGAME OVER - Selected word: "{self.selected_word}"\033[0m\n')
                    input('[Press enter to continue] ')
                    self.reset()
                    continue

                # Get user guess input
                guess = input('\033[36;3mGUESS\033[32m > \033[0m').upper()[:self.word_length]

                # Skip if input is empty
                if guess == '':
                    continue

                # Reset game if input is '#'
                elif guess == '#':
                    self.reset()
                    self.printinfo(f'\033[36mGame Restart\033[0m')
                    continue

                # Validate guess length
                elif len(guess) != self.word_length:
                    self.printinfo(f'\033[31mMust length guess word is {self.word_length}\033[0m')
                    continue

                # Validate if guess is in dictionary
                elif guess not in self.words_list:
                    self.printinfo(f'\033[31m"{guess}" not found in dictionary\033[0m')
                    continue

                # Get feedback for the guess
                feedback = self.get_feedback_colors(guess)
                self.guess_count -= 1
                self.keyboards_feedback_history.append(feedback)

                # Check if the guess is correct
                if guess == self.selected_word:
                    self.guessed = True

            # Display final board state and congratulatory message
            self.cls()
            self.showBoardGame()
            print('\033[32mHORRY! YOU GUESSED THE WORD!\033[0m\n')
            input('[Press enter to continue] ')

            # Reset the game for a new round
            self.reset()

# Start the game if the script is executed directly
if __name__ == '__main__':
    katla = Katla()
    katla.main()