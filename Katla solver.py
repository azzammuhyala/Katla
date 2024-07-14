"""
Katla solver - Logic concept of finding the right word in Kalta (support from games with the same concept as Wordle)
"""

# importing modules need
from asciiTUI import justify
from os import name, system
from random import choice
from time import sleep
# importing file components
from components.katla_module.json_validator import WordsValidator, SettingsValidator
from components.katla_module.constants import Feedback

# importing getch for input
if name == 'nt':
    from asciiTUI import _getch as getch
else:
    from asciiTUI import getch

# KatlaSolver class for solving the Katla game
class KatlaSolver:

    # Initializing the KatlaSolver class
    def __init__(self, input_type: str = 'color') -> None:
        # Setting the input type
        self.input_type = input_type

        # Defining uppercase letters and feedback colors
        self.uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.upperfcolor = 'RYG'

        # Loading and validating settings
        self.settings = SettingsValidator().load_and_validation()

        # Loading and validating word dictionary
        self.validator_word_dictionary = WordsValidator(lang_id=self.settings['language-word'])
        self.word_dictionary = self.validator_word_dictionary.load_and_validation(readonly=True)
        self.words_list: list[str] = [word.upper() for word in self.word_dictionary[f"length-{self.settings['word-length']}"]]

        # Initializing feedback list and chosen word
        self.feedbacks: list[Feedback] = []
        self.choose_word = ''

    # Method to reset the feedbacks
    def reset(self) -> None:
        print('Feedback reseting...')
        self.feedbacks.clear()

    # Method to validate the format of the feedback string
    def validate_format(self, string: str) -> str | bool:
        item_char = string.split(' ')
        word = ''

        # Check if the feedback length matches the word length
        if len(item_char) != self.settings['word-length']:
            return f"Feedback length is inappropriate. #{self.settings['word-length']}"

        # Check the format of each character in the feedback string
        for item in item_char:
            if len(item) != 3 or item[1] != '.' or item[0] not in self.uppercase or item[2] not in self.upperfcolor:
                return 'Invalid feedback'

            word += item[0].upper()

        # Check if the word exists in the word list
        if (word in self.words_list) or not self.settings['use-valid-word']:
            return True

        return f'The word "{word}" doesn\'t exist'

    # Method to parse the feedback string into a list of dictionaries
    def parse_format(self, vstring: str) -> Feedback:
        item_char = vstring.split(' ')
        feedback = []

        # Map each character and color to the feedback list
        for item in item_char:
            splits = item.split('.')
            char = splits[0]
            color = splits[1]

            if color == 'R':
                color = 'red'
            elif color == 'Y':
                color = 'yellow'
            elif color == 'G':
                color = 'green'

            feedback.append({char: color})

        return feedback

    # Method to find possible words based on the feedback
    def find_possible_words(self, fstring: str) -> list[str]:
        self.feedbacks.append(self.parse_format(fstring))
        possible_words = self.words_list

        # Filter words based on the feedback
        for feedback in self.feedbacks:
            possible_words = self.filter_words(possible_words, feedback)

        return possible_words

    # Method to filter words based on the feedback
    def filter_words(self, words: list[str], feedback: Feedback) -> list[str]:
        filtered_words = []

        # Keep only valid words
        for word in words:
            if self.is_word_valid(word, feedback):
                filtered_words.append(word)

        return filtered_words

    # Method to check if a word is valid based on the feedback
    def is_word_valid(self, word: str, feedback: Feedback) -> bool:
        word_char_frequency = {char: word.count(char) for char in set(word)}

        # First pass to count how many greens and yellows per character
        feedback_char_counts = {'green': {}, 'yellow': {}, 'red': {}}
        for i, attempt_feedback in enumerate(feedback):
            for char, color in attempt_feedback.items():
                feedback_char_counts[color][char] = feedback_char_counts[color].get(char, 0) + 1

        # Second pass to validate word
        for i, attempt_feedback in enumerate(feedback):
            for char, color in attempt_feedback.items():
                if color == 'red':
                    # Red: char should not be in the word, unless it's also yellow / green somewhere else
                    if char == word[i] or (char in word and (feedback_char_counts['green'].get(char, 0) + feedback_char_counts['yellow'].get(char, 0) < word_char_frequency[char])):
                        return False
                elif color == 'green':
                    # Green: char must be at the same position
                    if word[i] != char:
                        return False
                    word_char_frequency[char] -= 1
                elif color == 'yellow':
                    # Yellow: char must be in the word but not at the same position
                    if char not in word or word[i] == char:
                        return False
                    word_char_frequency[char] -= 1

        # Third filter to ensure character frequencies match feedback
        for char in feedback_char_counts['yellow'].keys():
            if word_char_frequency.get(char, 0) < 0:
                return False

        # If it's safe, it means this word is passed
        return True

    # Method to display help information
    def help(self) -> None:
        if self.input_type == 'normal':
            print(
"""
To enter a word, enter the word then continue with a period '.' then proceed with the color type of the word. After that, add a space to the next word.

Example (word HELLO with color RGYRR):

> H.R E.G L.Y L.R O.R
""".strip('\n')
            )
        elif self.input_type == 'color':
            print(
"""
Enter word/letters. If all the word have reached the length limit in the settings, then enter the color type (in ansi color form). If everything has been entered then press enter to continue.

Example (word HELLO with color RGYRR):

#STEP 1:
> HELLO

#STEP 2:
* Pressing 'R'
> \033[31mH\033[0mELLO

#STEP 3:
> \033[31mH\033[32mE\033[33mL\033[31mLO\033[0m
""".strip('\n')
            )
        print(
"""
Meaning of color code:

G: (Green)  Be in the right place.
Y: (Yellow) It's in the chosen word but in the wrong place.
R: (Ed)     Not everywhere.

Button Keys:

1: Reset
2: Reset + clear terminal
3: Open current settings
4: Refresh current settings and words
5: Automatic writing of try word
9: Open this help
0: Exit
"""
        )

    # Method to handle user input
    def input(self) -> str:
        self.input_type = self.input_type.lower()

        if self.input_type == 'normal':
            prompt = f"Feedback #{len(self.feedbacks) + 1} > "
            return input(prompt)

        elif self.input_type == 'color':
            prompt = f"\033[36;3mFeedback\033[0;{35 if len(self.feedbacks) < self.settings['change-guess'] else 31}m #{len(self.feedbacks) + 1}\033[32m > \033[0m"
            enteredLetter = []
            enteredMask = []
            enteredColor = []

            # Method to update the display
            def stdout(end='\033[47m \033[0m \033[?25l') -> None:
                print(f"\r{prompt}{''.join(enteredMask)}", end=end, flush=True)

            def update_stdout() -> None:
                nonlocal enteredMask
                enteredMask = []
                for i, char in enumerate(enteredLetter):
                    if i < len(enteredColor):
                        if enteredColor[i] == 'R':
                            enteredMask.append(f"\033[31m{char}\033[0m")
                        elif enteredColor[i] == 'Y':
                            enteredMask.append(f"\033[33m{char}\033[0m")
                        elif enteredColor[i] == 'G':
                            enteredMask.append(f"\033[32m{char}\033[0m")
                    else:
                        enteredMask.append(char)
                
                stdout()

            # Method to close the display
            def close() -> None:
                stdout('\033[0m ')
                print('\033[?25h')

            stdout()

            while True:
                # get a key
                key = ord(getch())

                # Handle Enter key
                if key == 13 and len(enteredColor) == self.settings['word-length']:
                    close()
                    return ' '.join(f"{char}.{color}" for char, color in zip(enteredLetter, enteredColor))

                # Handle Backspace key
                elif key in (8, 127):
                    if enteredColor:
                        enteredColor.pop()
                    elif enteredLetter:
                        enteredLetter.pop()

                    update_stdout()

                # If user press Ctrl+C it will raise KeyboardInterrupt like input() functionality
                elif key == 3:
                    close()
                    raise KeyboardInterrupt

                # Handle character input
                elif len(enteredColor) <= self.settings['word-length']:
                    char = chr(key).upper()

                    if char in self.uppercase:

                        if len(enteredLetter) >= self.settings['word-length']:
                            if char in self.upperfcolor and len(enteredColor) < self.settings['word-length']:
                                enteredColor.append(char)
                        else:
                            enteredLetter.append(char)

                        update_stdout()

                    elif char == '5' and self.choose_word:
                        enteredColor.clear()
                        enteredLetter.clear()
                        for char in self.choose_word:
                            enteredLetter.append(char)

                        update_stdout()

                    elif char in '123490':
                        close()
                        return char

        else:
            raise TypeError(f'input_type unknown: {self.input_type}')

    # Main method to run the KatlaSolver
    def main(self):
        running = True

        print('KATLA SOLVER - 99.5% PROBABILITY CORRECT - V ~ 1.0.1 BETA\n')
        self.help()

        while running:
            word_input = self.input().strip().upper()
            self.choose_word = ''

            # Reset
            if word_input == '1':
                self.reset()

            # Reset + clear terminal
            elif word_input == '2':
                self.reset()
                system('cls' if name == 'nt' else 'clear')

            # Show display current settings
            elif word_input == '3':
                print(justify('Current settings', 30))
                print('=' * 30)
                print(justify('KEYS', 24, 'left') + 'VALUES')
                print('-' * 30)
                for key, value in self.settings.items():
                    key, value = map(str, [key, value])
                    print(justify(key, 30 - len(value), 'left') + value.upper() + (' #' if key in ('language-word', 'word-length', 'change-guess', 'use-valid-word') else ''))
                print("\n[NOTE] To change the settings, please run the Katla application then change it in Katla settings then the close settings. (Make sure the application position with the main settings file is in the same folder)")

            # Refresh current settings and words
            elif word_input == '4':
                self.settings = SettingsValidator().load_and_validation()
                self.validator_word_dictionary = WordsValidator(lang_id=self.settings['language-word'])
                self.word_dictionary = self.validator_word_dictionary.load_and_validation(readonly=True)
                self.words_list: list[str] = [word.upper() for word in self.word_dictionary[f"length-{self.settings['word-length']}"]]
                self.feedbacks: list[Feedback] = []
                self.choose_word = ''
                sleep(.5)

            # Show display help
            elif word_input == '9':
                self.help()

            # Quit / Exit program
            elif word_input == '0':
                running = False

            else:
                validation = self.validate_format(word_input)

                if validation is True:
                    possible_words = self.find_possible_words(word_input)

                    if len(possible_words) > 1:
                        print('List possibilities: ', end='')
                        for word in possible_words:
                            print(word, end=' ')
                        self.choose_word = choice(possible_words)
                        print('\nTry word:', self.choose_word)

                    elif len(possible_words) == 1:
                        print('Most likely, the word are:', possible_words[0])
                        self.reset()

                    else:
                        print('No possible words')
                        self.reset()

                else:
                    print(validation)

# Run the KatlaSolver if the script is executed directly
if __name__ == '__main__':
    ks = KatlaSolver()
    ks.main()