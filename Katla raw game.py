import asciiTUI
import random
import time
import os
from components import constants as const
from components.json_validator import WordsValidator

class Katla:

    def __init__(

            self,
            language: str = 'idn',
            word_length: int = 5,
            change_guess: int = 6

        ) -> None:

        self.words_validator = WordsValidator(language)
        self.dictionary = self.words_validator.load_and_validation()
        self.language = language
        self.word_length = word_length
        self.change_guess = change_guess
        self.color_code = {
            'green': '\033[32m',
            'yellow': '\033[33m',
            'red': '\033[31m',
            'gray': '\033[90m'
        }
        self.words_list = [word.upper() for word in self.dictionary[f'length-{self.word_length}']]
        self.keyboards_feedback_history = []

        self.guess_count = self.change_guess
        self.selected_word = random.choice(self.words_list)
        self.guessed = False

    def reset(self) -> None:
        self.keyboards_feedback_history.clear()
        self.guess_count = self.change_guess
        self.selected_word = random.choice(self.words_list)
        self.guessed = False

    def cls(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def printinfo(self, *args, sleep: const.Number = 1, **kwargs) -> None:
        print(*args, **kwargs)
        time.sleep(sleep)

    def get_feedback_colors(self, guess_word: str) -> list[dict[str, str]]:
        feedback = []
        guess_char_frequency = {char: guess_word.count(char) for char in set(guess_word)}
        selected_char_frequecy = {char: guess_word.count(char) for char in set(self.selected_word)}

        for i, char in enumerate(guess_word):

            if char not in self.selected_word:
                feedback.append({char: "red"})

            elif char == self.selected_word[i] and selected_char_frequecy[char] > 0:
                feedback.append({char: "green"})
                guess_char_frequency[char] -= 1
                selected_char_frequecy[char] -= 1

            elif char in self.selected_word and selected_char_frequecy[char] > 0 and guess_char_frequency[char] > 0:
                feedback.append({char: "yellow"})
                selected_char_frequecy[char] -= 1

            elif char == self.selected_word[i]:
                for j, item in enumerate(feedback):
                    if list(item.keys())[0] == char:
                        if feedback[j][char] == "yellow":
                            feedback.append({char: "green"})
                            feedback[j][char] = "red"
                            guess_char_frequency[char] -= 1
                            selected_char_frequecy[char] -= 1
                            break

            elif char in self.selected_word:
                for j, item in enumerate(feedback):
                    if list(item.keys())[0] == char:
                        if feedback[j][char] in ["green", "yellow"] and guess_char_frequency[char] > 0:
                            guess_char_frequency[char] -= 1
                            feedback.append({char: "red"})
                            break

        return feedback
    
    def showKeyboard(self) -> None:
        layout_keyboard = const.Keyboard.QWERTY
        keyboard_ascii = '+---------------------+\n'
        keyboard_feedback = {char: 'gray' for line in layout_keyboard for char in line}

        for attempt_feedback in self.keyboards_feedback_history:
            for item in attempt_feedback:
                for char, color in item.items():
                    if color in ['green', 'yellow', 'red']:
                        if keyboard_feedback[char] == 'green' or (keyboard_feedback[char] == 'yellow' and color == 'red'):
                            continue
                        keyboard_feedback[char] = color

        for ln, line in enumerate(layout_keyboard):
            keyboard_ascii += '| ' if ln in [0, 2] else '|  '

            for char in line:
                color = keyboard_feedback[char.upper()]

                if char == '\b':
                    char = '<-'
                elif char == '\n':
                    char = '\\n'

                keyboard_ascii += f'{self.color_code[color]}{char}\033[0m '

            keyboard_ascii += '|\n' if ln in [0, 2] else ' |\n'

        keyboard_ascii += '+---------------------+'
        for ln in keyboard_ascii.split('\n'):
            print(asciiTUI.justify(ln, asciiTUI.terminal_size('x'), wrap=False))

    def showBoardGame(self) -> None:
        word_ascii = ''
        empty_feedback = [f'\033[90m{"-" * self.word_length}\033[0m' for _ in range(self.guess_count)]

        for attempt_feedback in self.keyboards_feedback_history:
            for char_feedback in attempt_feedback:
                for char, color in char_feedback.items():
                    word_ascii += f'{self.color_code[color]}{char}\033[0m'
            print(asciiTUI.justify(word_ascii, asciiTUI.terminal_size('x'), wrap=False))
            word_ascii = ''

        for x in empty_feedback:
            print(asciiTUI.justify(x, asciiTUI.terminal_size('x'), wrap=False))

        print()
        self.showKeyboard()
        print()

    def main(self) -> None:
        while True:

            while not self.guessed:
                self.cls()
                self.showBoardGame()

                if self.guess_count <= 0:
                    print(f'\033[31mGAME OVER - Selected word: "{self.selected_word}"\033[0m\n')
                    input('[Press enter to continue] ')
                    self.reset()
                    continue

                guess = input('\033[36;3mGUESS\033[32m > \033[0m').upper()[:self.word_length]

                if guess == '':
                    continue

                elif guess == '#':
                    self.reset()
                    self.printinfo(f'\033[36mGame Restart\033[0m')
                    continue

                elif len(guess) != self.word_length:
                    self.printinfo(f'\033[31mMust length guess word is {self.word_length}\033[0m')
                    continue

                elif guess not in self.words_list:
                    self.printinfo(f'\033[31m"{guess}" not found in dictionary\033[0m')
                    continue

                feedback = self.get_feedback_colors(guess)
                self.guess_count -= 1
                self.keyboards_feedback_history.append(feedback)

                if guess == self.selected_word:
                    self.guessed = True

            self.cls()
            self.showBoardGame()
            print('\033[32mHORRY! YOU GUESSED THE WORD!\033[0m\n')
            input('[Press enter to continue] ')
            self.reset()

katla = Katla()
katla.main()