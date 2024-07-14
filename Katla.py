"""
Katla - Kata game

```md
+---+ +---+ +---+ +---+ +---+
| P | | I | | T | | O | | N |
+---+ +---+ +---+ +---+ +---+
+---+ +---+ +---+ +---+ +---+
| K | | A | | T | | L | | A |
+---+ +---+ +---+ +---+ +---+
----------- pygame - Python 3
```

(C) Copyright 2024 - 2026 [ Azzamuhyala ]

Works pretty well on Windows platforms and on Python version 3.10 and above.
It is not recommended to use old versions of pygame and SDL.

"""

import pygame
from random                                 import choice
from threading                              import Thread
from tkinter                                import messagebox
from string                                 import ascii_uppercase
from datetime                               import datetime, timedelta
from pyuac                                  import isUserAdmin, runAsAdmin
from platform                               import python_version
from components.module.pygamebutton         import button_color, Button, Range, set_cursor_buttons
from components.module.format_number        import NumberFormat
from components.module.wraptext_pygame      import wrap_text
from components.module.pygamegif            import GIF
from components.katla_module                import constants as const
from components.katla_module.logs           import Logs
from components.katla_module.scroller       import ScrollerY
from components.katla_module.popup          import Popup, Notification
from components.katla_module.json_validator import Languages, Themes, WordsValidator, SettingsValidator, GameDataValidator

logs = Logs()

logs.log(f"pygame {pygame.ver} (SDL {'.'.join(map(str, pygame.get_sdl_version()))}, Python {python_version()})")

class Katla:

    """
    # Katla - pygame - Python 3

    Supported software - Perangkat lunak yang didukung:
    - Android: pydroid3 -> Python [VERSION] 3.10+
    - Windows, ...etc: Python [VERSION] 3.10+

    ENGLISH - US
    ------------
    This class is part of the main structure of the game `Katla`.
    Please do not misuse the methods or attributes that exist for
    avoid fatal mistakes that could occur.

    INDONESIAN - INDONESIA
    ----------------------
    Kelas ini merupakan bagian struktur utama dari permainan `Katla`.
    Harap tidak menyalah gunakan metode atau atribut yang ada untuk
    menghindari adanya kesalahan fatal yang bisa terjadi.
    """

    __version__       = [const.MAJOR, const.MINOR, const.PATCH]
    __label_version__ = const.VERSION
    __license__       = const.LICENSE

    def __init__(self) -> None:
        logs.log('-- Katla logs --')
        const.os.environ['SDL_VIDEO_CENTERED'] = '1'

        logs.log('Initialization pygame init, and font.init')
        pygame.init()
        pygame.font.init()

        try:
            logs.log('Initialization pygame mixer.init')
            pygame.mixer.init()
            self.init_mixer = True
        except:
            logs.log('Initialization pygame mixer.init failed', 'warn')
            self.init_mixer = False

        logs.log('Initialization languages, and katla data')
        self.validator_languages = Languages()
        self.validator_themes    = Themes()
        self.validator_settings  = SettingsValidator(logs)
        self.validator_game_data = GameDataValidator(logs)

        logs.log('Load and validation katla data')
        self.settings  = self.validator_settings .load_and_validation()
        self.game_data = self.validator_game_data.load_and_validation()

        self.theme          : str   = self.settings['theme']
        self.keyboard_layout: str   = self.settings['keyboard-layout']
        self.sound_volume   : int   = self.settings['sound-volume']
        self.music_volume   : int   = self.settings['music-volume']
        self.change_guess   : int   = self.settings['change-guess']
        self.word_length    : int   = self.settings['word-length']
        self.fps            : int   = self.settings['fps']
        self.geomatry       : float = self.settings['geomatry']
        self.language       : str   = self.settings['language']
        self.language_word  : str   = self.settings['language-word']
        self.use_valid_word : bool  = self.settings['use-valid-word']
        self.show_keyboard  : bool  = self.settings['show-keyboard']

        logs.log(f'Initialization words, with id: {self.language_word}')
        self.validator_word_dictionary = WordsValidator(self.language_word)

        logs.log('Load and validation words, and load languages')
        self.word_dictionary = self.validator_word_dictionary.load_and_validation()
        self.languages       = self.validator_languages      .load(self.language)
        self.themes          = self.validator_themes         .load(self.theme)

        logs.log('Initialization NumberFormat, and Scroller')
        self.num_format                = NumberFormat(self.languages['exponents-number'], decimal_places=2, rounded=False, reach=(3, 'thousand'))
        self.scroller_tile             = ScrollerY(self, (0, 130 * self.geomatry), reversed=True)
        self.scroller_tile.direction   = 130 * self.geomatry

        logs.log('Load attributes game')
        self.keyboards                : dict[str, const.KeyboardList] = {key: getattr(const.Keyboard, key) for key in const.Keyboard.__all__}
        self.keyboard_feedback        : dict[str, str]       = {char: 'not-inputed' for line in self.keyboards[self.keyboard_layout] for char in line}
        self.running                  : bool                 = True
        self.detected_time_cheat      : bool                 = False
        self.coins                    : const.Number         = self.game_data['coins']
        self.last_geomatry            : float                = self.geomatry
        self.guess_count              : int                  = self.change_guess
        self.play_lose_or_win         : int                  = 0
        self.last_win_line            : int                  = 0
        self.words_list               : list[str]            = [word.upper()  for word in self.word_dictionary[f'length-{self.word_length}']]
        self.correct_char_tile        : list[str]            = ['not-inputed' for _ in range(self.word_length)]
        self.correct_char_keyboard    : list[str]            = []
        self.hint_tile                : list[str]            = []
        self.hint_keyboard            : list[str]            = []
        self.feedback_history         : list[const.Feedback] = []
        self.feedback_history_keyboard: list[const.Feedback] = []
        self.input_history            : list[list[str]]      = [[]]
        self.input_point              : list[int, int]       = [0, 0]
        self.selected_word            : str                  = choice(self.words_list)
        self.last_word_input          : str                  = ''

        if self.detect_time_cheat():
            logs.log("Detected suspicion of cheating: Current time with larger game data time.", 'warn')
            self.detected_time_cheat = True

        self.new_streak()

        self.isshow_NotInDictionary         : bool = False
        self.isshow_NotEnoughLength         : bool = False
        self.isshow_TileIsEmpty             : bool = False
        self.isshow_AllKeyboardHintsProvided: bool = False
        self.isshow_AllTileHintsProvided    : bool = False
        self.isshow_Win                     : bool = False
        self.isshow_Lose                    : bool = False
        self.isshow_Reset                   : bool = False
        self.isshow_Unfullscreen            : bool = False
        self.isshow_Settings                : bool = False
        self.isshow_Logs                    : bool = False

        self.isshow_popup_warn: list[bool, bool, bool] = [False, False, False]

        self.last_time_reset            = self.get_tick()
        self.last_time_close_settings   = self.get_tick()
        self.timeanimation_notification = self.get_tick()
        self.timeanimation_popup        = self.get_tick()

        logs.log('Set screen')
        self.dinfo          = pygame.display.Info()
        self.minsize_screen = (const.MIN_SCREEN_X, const.MIN_SCREEN_Y)
        self.maxsize_screen = (min(self.dinfo.current_w - 75, const.MAX_SCREEN_X), min(self.dinfo.current_h - 50, const.MAX_SCREEN_Y))
        init_screen         = self.settings['screen-size']

        if init_screen == 'FULL':
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        elif init_screen[0] < const.MIN_SCREEN_X or init_screen[1] < const.MIN_SCREEN_Y:
            self.screen = pygame.display.set_mode(self.minsize_screen, pygame.RESIZABLE)

        elif init_screen[0] > self.maxsize_screen[0] or init_screen[1] > self.maxsize_screen[1]:
            init_screen[0] = self.maxsize_screen[0] if init_screen[0] > self.maxsize_screen[0] else init_screen[0]
            init_screen[1] = self.maxsize_screen[1] if init_screen[1] > self.maxsize_screen[1] else init_screen[1]
            self.screen    = pygame.display.set_mode(init_screen, pygame.RESIZABLE)

        else:
            self.screen = pygame.display.set_mode(init_screen, pygame.RESIZABLE)

        logs.log(f'Screen sized: (W={self.screen.get_width()}, H={self.screen.get_height()})')

        size_confetti           = 500 * self.geomatry
        self.init_rect          = pygame.Rect(0, 0, 0, 0)
        self.boardRect_keyboard = self.init_rect
        self.confetti_rect      = pygame.Rect(const.math.get_center(self.screen.get_width(), size_confetti), self.screen.get_height() - size_confetti, size_confetti, size_confetti)

        self.file = const.File()
        images    = self.file.Images(self.theme)

        self.fullscreen_attr          : dict[const.Literal['full', 'last-size'], const.Any]
        self.gif_win                  : GIF
        self.sound_music              : pygame.mixer.Sound
        self.sound_key                : pygame.mixer.Sound
        self.sound_key_backspace_enter: pygame.mixer.Sound
        self.sound_button_click       : pygame.mixer.Sound
        self.sound_win                : pygame.mixer.Sound
        self.sound_lose               : pygame.mixer.Sound

        def load_assets() -> None:
            self.fullscreen_attr = {
                'full': init_screen == 'FULL',
                'last-size': list(self.screen.get_size() if init_screen != 'FULL' else self.maxsize_screen)
            }

            logs.log('Load gif')
            self.gif_win = GIF(images.WIN_GIF, self.confetti_rect, 25)

            logs.log('Load images')
            self.image_close         = pygame.image.load(images.CLOSE)
            self.image_backspace     = pygame.image.load(images.BACKSPACE)
            self.image_enter         = pygame.image.load(images.ENTER)
            self.image_question_mark = pygame.image.load(images.QUESTION_MARK)
            self.image_stats         = pygame.image.load(images.STATS)
            self.image_reset         = pygame.image.load(images.RESET)
            self.image_settings      = pygame.image.load(images.SETTINGS)
            self.image_coin_bag      = pygame.image.load(images.COIN_BAG)
            self.image_lamp          = pygame.image.load(images.LAMP)
            self.image_keyboard      = pygame.image.load(images.KEYBOARD)
            self.image_hammer        = pygame.image.load(images.HAMMER)
            self.image_right_arrow   = pygame.image.load(images.RIGHT_ARROW)
            self.image_check         = pygame.image.load(images.CHECK)

            if self.init_mixer:
                logs.log('Load sounds')
                self.sound_music               = pygame.mixer.Sound(self.file.SOUND_MUSIC)
                self.sound_key                 = pygame.mixer.Sound(self.file.SOUND_KEY)
                self.sound_key_backspace_enter = pygame.mixer.Sound(self.file.SOUND_KEY_BACKSPACE_ENTER)
                self.sound_button_click        = pygame.mixer.Sound(self.file.SOUND_BUTTON_CLICK)
                self.sound_win                 = pygame.mixer.Sound(self.file.SOUND_WIN)
                self.sound_lose                = pygame.mixer.Sound(self.file.SOUND_LOSE)

            self.margin_tile    = 10 * self.geomatry
            self.size_tile      = 80 * self.geomatry
            self.last_size_tile = self.size_tile

            logs.log('Load fonts')
            self.font_tile         = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(self.size_tile))
            self.font_textbar      = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(20 * self.geomatry))
            self.font_keyboard     = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(35 * self.geomatry))
            self.font_katla        = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,   int(40 * self.geomatry))
            self.font_notification = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(30 * self.geomatry))
            self.font_coins        = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(35 * self.geomatry))

            logs.log('Initialization Button')
            self.buttonKeyboard = Button(
                surface_screen = self.screen,
                rect           = self.init_rect,
                text_color     = button_color(*[self.themes['keyboard']['text'] for _ in range(3)]),
                click_speed    = 0
            )
            self.buttonOutlineKeyboard = self.buttonKeyboard.copy(
                color = button_color(
                    self.themes['keyboard']['button']['outline']['inactive'],
                    self.themes['keyboard']['button']['outline']['active']
                )
            )
            self.buttonHowToPlay = Button(
                surface_screen = self.screen,
                rect           = self.init_rect,
                hide           = True,
                image          = self.image_question_mark,
                click_speed    = 0
            )
            self.buttonStats        = self.buttonHowToPlay.copy(image=self.image_stats)
            self.buttonAutoWrite    = self.buttonHowToPlay.copy(image=self.image_right_arrow, click_speed=250)
            self.buttonReset        = self.buttonHowToPlay.copy(image=self.image_reset,       click_speed=500)
            self.buttonSettings     = self.buttonHowToPlay.copy(image=self.image_settings)
            self.buttonDailyCoins   = self.buttonHowToPlay.copy(image=self.image_coin_bag)
            self.buttonLetterHint   = self.buttonHowToPlay.copy(image=self.image_lamp)
            self.buttonKeyboardHint = self.buttonHowToPlay.copy(image=self.image_keyboard)
            self.buttonDeletedEntry = self.buttonHowToPlay.copy(image=self.image_hammer)

            logs.log('Initialization Notification, and Popup')
            self.notification = Notification(self)
            self.popup        = Popup(self)

        thread_load     = Thread(target=load_assets)
        sizeload        = 50 * self.geomatry
        sizeicon        = 100 * self.geomatry
        load_rect       = pygame.Rect(const.math.get_center(self.screen.get_width(), sizeload), self.screen.get_height() - 80 * self.geomatry, sizeload, sizeload)
        gif_load        = GIF(images.LOAD_GIF, load_rect, 100)
        self.image_icon = pygame.image.load(images.ICON)
        icon            = pygame.transform.scale(self.image_icon, (sizeicon, sizeicon))
        self.clock      = pygame.time.Clock()

        pygame.display.set_icon(self.image_icon)
        pygame.display.set_caption("Katla - Loading...")

        try:
            logs.log('Thread and loading screen starting')
            thread_load.start()
            runwait = True

            while runwait:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        runwait      = False
                        self.running = False

                        thread_load.join(.01)

                    self.handle_screen_resize(event)

                if not thread_load.is_alive() and runwait:
                    runwait = False

                sizescreen    = self.screen.get_size()
                gif_load.rect = pygame.Rect(const.math.get_center(sizescreen[0], sizeload), sizescreen[1] - 80 * self.geomatry, sizeload, sizeload)

                self.screen.fill(self.themes['screen'])

                self.screen.blit(icon, (const.math.get_center(sizescreen[0], sizeicon), const.math.get_center(sizescreen[1], sizeicon)))

                gif_load.draw_and_update(self.screen)

                pygame.display.flip()

                self.clock.tick(self.fps)

            self.threadgif = Thread(target=self.gif_win.convert_gif)

            self.set_volume()

            pygame.display.set_caption("Katla")

        except Exception as e:
            logs.log(f'An unexpected exception occurred during loading the assets. {e}', 'error')
            thread_load.join(.01)

            self.running = False

        logs.log('Initialization completed')

    def __call__(self) -> None:
        self.Appmainloop()

    def __str__(self) -> str:
        return self.__license__

    def reset(self) -> None:
        self.correct_char_keyboard    .clear()
        self.hint_keyboard            .clear()
        self.hint_tile                .clear()
        self.feedback_history         .clear()
        self.feedback_history_keyboard.clear()
        self.words_list               = [word.upper()  for word in self.word_dictionary[f'length-{self.word_length}']]
        self.correct_char_tile        = ['not-inputed' for _ in range(self.word_length)]
        self.input_point              = [0, 0]
        self.input_history            = [[]]
        self.guess_count              = self.change_guess
        self.selected_word            = choice(self.words_list)
        self.last_word_input          = ''

        self.reset_isshow()
        self.update_correct_tile()
        self.update_keyboard_feedback()

    def reset_isshow(self) -> None:
        self.isshow_NotInDictionary          = False
        self.isshow_NotEnoughLength          = False
        self.isshow_AllTileHintsProvided     = False
        self.isshow_AllKeyboardHintsProvided = False
        self.isshow_TileIsEmpty              = False
        self.isshow_Win                      = False
        self.isshow_Lose                     = False
        self.isshow_Reset                    = False
        self.isshow_Unfullscreen             = False

    def update_correct_tile(self) -> None:
        self.correct_char_tile = ['not-inputed' for _ in range(self.word_length)]
        ln                     = self.input_point[1]
        correct_input          = self.get_correct_char()

        for i in range(len(self.input_history[ln])):
            if correct_input[i] == self.input_history[ln][i] and i <= self.input_point[0]:
                self.correct_char_tile[i] = 'green'

    def update_keyboard_feedback(self) -> None:
        self.keyboard_feedback = {char: 'not-inputed' for line in self.keyboards[self.keyboard_layout] for char in line}

        for attempt_feedback in self.feedback_history_keyboard:
            for item in attempt_feedback:
                for char, color in item.items():
                    if self.keyboard_feedback[char] == 'green' or (self.keyboard_feedback[char] == 'yellow' and color == 'red') and char not in self.hint_keyboard:
                        continue
                    if char in self.hint_keyboard:
                        self.correct_char_keyboard.append(char)
                        self.keyboard_feedback[char] = 'green'
                    else:
                        if color == 'green':
                            self.correct_char_keyboard.append(char)
                        self.keyboard_feedback[char] = color

        for char, color in self.keyboard_feedback.items():
            if color == 'not-inputed':
                if char in self.hint_keyboard:
                    self.keyboard_feedback[char] = 'green'
                    if char not in self.correct_char_keyboard:
                        self.correct_char_keyboard.append(char)

    def get_feedback_colors(self, guess_word: str) -> const.Feedback:
        feedback               = []
        guess_char_frequency   = {char: guess_word.count(char)         for char in set(guess_word)}
        selected_char_frequecy = {char: self.selected_word.count(char) for char in set(self.selected_word)}

        for i, char in enumerate(guess_word):

            if char not in self.selected_word:
                feedback.append({char: "red"})

            elif char == self.selected_word[i] and selected_char_frequecy[char] > 0:
                feedback.append({char: "green"})
                guess_char_frequency[char]   -= 1
                selected_char_frequecy[char] -= 1

            elif char in self.selected_word and selected_char_frequecy[char] > 0 and guess_char_frequency[char] > 0:
                feedback.append({char: "yellow"})
                selected_char_frequecy[char] -= 1

            elif char == self.selected_word[i]:
                for j, item in enumerate(feedback):
                    if list(item.keys())[0] == char:
                        if feedback[j][char] == "yellow":
                            feedback.append({char: "green"})
                            feedback[j][char]             = "red"
                            guess_char_frequency[char]   -= 1
                            selected_char_frequecy[char] -= 1
                            break

            elif char in self.selected_word:
                for j, item in enumerate(feedback):
                    if list(item.keys())[0] == char:
                        if feedback[j][char] in ["green", "yellow"] and guess_char_frequency[char] > 0:
                            feedback.append({char: "red"})
                            guess_char_frequency[char] -= 1
                            break

        return feedback

    def get_correct_char(self) -> list[str | None]:
        correct_input = [self.hint_tile[i] if i < len(self.hint_tile) else None for i in range(self.word_length)]

        for attempt_feedback in self.feedback_history_keyboard:
            for i, item in enumerate(attempt_feedback):
                for char, color in item.items():
                    if color == 'green':
                        correct_input[i] = char

        return correct_input

    def get_daily_countdown(self) -> str | bool:
        last_time_int       = [int(timeday) for timeday in self.game_data['prize-claim-time'].split('/')]
        last_claim_datetime = datetime(last_time_int[5], last_time_int[4], last_time_int[3], last_time_int[0], last_time_int[1], last_time_int[2])
        time_difference     = datetime.now() - last_claim_datetime
        countdown           = timedelta(days=1) - time_difference if time_difference < timedelta(days=1) else timedelta(0)

        return True if countdown == timedelta(0) else f"{countdown.seconds // 3600:02}:{(countdown.seconds % 3600) // 60:02}:{(countdown.seconds % 3600) % 60:02}"

    def get_tick(self) -> float:
        return pygame.time.get_ticks() / 1000

    def detect_time_cheat(self, use_date: const.Literal['prize-claim-time', 'played-time'] = 'prize-claim-time') -> bool:
        last_time_int       = [int(timeday) for timeday in self.game_data[use_date].split('/')]
        last_claim_datetime = datetime(last_time_int[5], last_time_int[4], last_time_int[3], last_time_int[0], last_time_int[1], last_time_int[2])
        current_time        = datetime.now()
        time_difference     = current_time - last_claim_datetime

        return time_difference.total_seconds() < 0

    def new_streak(self) -> bool:
        last_time_int       = [int(timeday) for timeday in self.game_data['played-time'].split('/')]
        last_claim_datetime = datetime(last_time_int[5], last_time_int[4], last_time_int[3], last_time_int[0], last_time_int[1], last_time_int[2])
        time_difference     = datetime.now() - last_claim_datetime

        if time_difference > timedelta(days=1):
            self.game_data['wins']['streak'] = 0
            self.game_data['played-time']    = datetime.now().strftime(r'%H/%M/%S/%d/%m/%Y')
            return True

        return False

    def set_volume(self) -> None:
        if self.init_mixer:
            self.sound_music              .set_volume(self.music_volume / 100)
            self.sound_key                .set_volume(self.sound_volume / 100)
            self.sound_key_backspace_enter.set_volume(self.sound_volume / 100)
            self.sound_button_click       .set_volume(self.sound_volume / 100)
            self.sound_win                .set_volume(self.sound_volume / 100)
            self.sound_lose               .set_volume(self.sound_volume / 100)

    def save_game(self, win: bool = False, line: str = '', lose: bool = False, prize_taken: bool = False, hint_coins_price: int | bool = False) -> None:
        self.update_keyboard_feedback()
        self.new_streak()

        self.game_data['coins'] = self.coins

        if win:
            self.game_data['wins'][line]     += 1
            self.game_data['wins']['streak'] += 1
            self.game_data['wins']['total']  += 1
            self.game_data['have-played']    += 1

            if self.game_data['wins']['streak'] > self.game_data['wins']['max-streak']:
                self.game_data['wins']['max-streak'] = self.game_data['wins']['streak']

        elif lose:
            self.game_data['losses']        += 1
            self.game_data['have-played']   += 1
            self.game_data['wins']['streak'] = 0

        elif prize_taken:
            self.game_data['prize-taken'] += 1

        elif hint_coins_price:
            self.game_data['hint']['count'] += 1
            self.game_data['hint']['coins'] += hint_coins_price

        if self.detect_time_cheat():
            self.detected_time_cheat = True

        if not self.detected_time_cheat:
            self.validator_game_data.encrypt_data(self.game_data)
        else:
            logs.log('Cannot save data. Please close the application and reopen it', 'warn')

    def input_event(self, event: pygame.event.Event) -> tuple[const.Literal['key', 'shortcut'] | None, str | None]:
        if event.type == pygame.KEYDOWN:
            key = event.key

            if   key == pygame.K_a: return 'key', 'A'
            elif key == pygame.K_b: return 'key', 'B'
            elif key == pygame.K_c: return 'key', 'C'
            elif key == pygame.K_d: return 'key', 'D'
            elif key == pygame.K_e: return 'key', 'E'
            elif key == pygame.K_f: return 'key', 'F'
            elif key == pygame.K_g: return 'key', 'G'
            elif key == pygame.K_h: return 'key', 'H'
            elif key == pygame.K_i: return 'key', 'I'
            elif key == pygame.K_j: return 'key', 'J'
            elif key == pygame.K_k: return 'key', 'K'
            elif key == pygame.K_l: return 'key', 'L'
            elif key == pygame.K_m: return 'key', 'M'
            elif key == pygame.K_n: return 'key', 'N'
            elif key == pygame.K_o: return 'key', 'O'
            elif key == pygame.K_p: return 'key', 'P'
            elif key == pygame.K_q: return 'key', 'Q'
            elif key == pygame.K_r: return 'key', 'R'
            elif key == pygame.K_s: return 'key', 'S'
            elif key == pygame.K_t: return 'key', 'T'
            elif key == pygame.K_u: return 'key', 'U'
            elif key == pygame.K_v: return 'key', 'V'
            elif key == pygame.K_w: return 'key', 'W'
            elif key == pygame.K_x: return 'key', 'X'
            elif key == pygame.K_y: return 'key', 'Y'
            elif key == pygame.K_z: return 'key', 'Z'
            elif key == pygame.K_BACKSPACE: return 'key', const.BACKSPACE
            elif key == pygame.K_RETURN:    return 'key', const.ENTER
            elif key == pygame.K_1: return 'shortcut', '1'
            elif key == pygame.K_2: return 'shortcut', '2'
            elif key == pygame.K_3: return 'shortcut', '3'
            elif key == pygame.K_4: return 'shortcut', '4'
            elif key == pygame.K_5: return 'shortcut', '5'
            elif key == pygame.K_6: return 'shortcut', '6'
            elif key == pygame.K_7: return 'shortcut', '7'
            elif key == pygame.K_8: return 'shortcut', '8'
            elif key == pygame.K_9: return 'shortcut', '9'
            elif key == pygame.K_0: return 'shortcut', '0'

        return None, None

    def handle_screen_resize(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            key = event.key

            if key == pygame.K_F11:
                self.fullscreen_attr['full'] = not self.fullscreen_attr['full']

                if self.fullscreen_attr['full']:
                    self.screen                  = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    self.settings['screen-size'] = 'FULL'
                    self.validator_settings.encrypt_data(self.settings)

                else:
                    self.screen                  = pygame.display.set_mode(self.fullscreen_attr['last-size'], pygame.RESIZABLE)
                    self.settings['screen-size'] = self.fullscreen_attr['last-size']
                    self.validator_settings.encrypt_data(self.settings)

            elif key == pygame.K_TAB:

                if self.fullscreen_attr['full']:
                    self.reset_isshow()
                    self.isshow_Unfullscreen        = True
                    self.timeanimation_notification = self.get_tick()

                else:
                    self.screen                       = pygame.display.set_mode(self.minsize_screen, pygame.RESIZABLE)
                    self.settings['screen-size']      = list(self.minsize_screen)
                    self.fullscreen_attr['last-size'] = list(self.minsize_screen)
                    self.validator_settings.encrypt_data(self.settings)

        elif event.type == pygame.VIDEORESIZE and not self.fullscreen_attr['full']:
            x, y        = event.size
            self.screen = pygame.display.set_mode(
                (
                    max(const.MIN_SCREEN_X, x),
                    max(const.MIN_SCREEN_Y, y)
                ), pygame.RESIZABLE
            )
            screen_size = list(self.screen.get_size())

            if screen_size[0] > self.maxsize_screen[0]:
                screen_size[0] = self.maxsize_screen[0]
            if screen_size[1] > self.maxsize_screen[1]:
                screen_size[1] = self.maxsize_screen[1]

            self.settings['screen-size']      = screen_size
            self.fullscreen_attr['last-size'] = screen_size
            self.validator_settings.encrypt_data(self.settings)

    def handle_sound(self, stype: const.Literal['backsound', 'key', 'key-bn', 'click', 'win', 'lose'], do: const.Literal['play', 'stop']) -> None:

        def handle_do(sound: pygame.mixer.Sound) -> None:
            if do == 'play':
                if stype == 'backsound':
                    sound.play(-1)
                else:
                    sound.play()
            elif do == 'stop':
                sound.stop()

        if self.init_mixer:
            if stype == 'backsound':
                handle_do(self.sound_music)
            elif stype == 'key':
                handle_do(self.sound_key)
            elif stype == 'key-bn':
                handle_do(self.sound_key_backspace_enter)
            elif stype == 'click':
                handle_do(self.sound_button_click)
            elif stype == 'win':
                handle_do(self.sound_win)
            elif stype == 'lose':
                handle_do(self.sound_lose)

    def handle_input(self, char: str) -> None:
        ln     = self.input_point[1]
        len_ln = len(self.input_history[ln])

        self.showKeyboard(char, True)
        pygame.display.flip()
        pygame.time.delay(25)

        if char in const.ALL_KEY:
            self.handle_sound('key-bn', 'play')

        if char == const.BACKSPACE:

            if len_ln > 0:
                self.input_history[ln].pop()

                if len_ln != self.word_length:
                    self.input_point[0] -= 1

        elif char == const.ENTER:

            if len_ln == self.word_length:
                guess_word = ''.join(self.input_history[ln])

                if guess_word in self.words_list or not self.use_valid_word:
                    feedback = self.get_feedback_colors(guess_word)

                    self.input_history            .append([])
                    self.feedback_history         .append(feedback)
                    self.feedback_history_keyboard.append(feedback)

                    for i, attempt_feedback in enumerate(feedback):
                        if list(attempt_feedback.values())[0] == 'green' and i > len(self.hint_tile) - 1:
                            self.hint_tile.append(list(attempt_feedback.keys())[0])
                        elif i > len(self.hint_tile) - 1:
                            break

                    self.input_point[0]  = 0
                    self.input_point[1] += 1
                    self.guess_count    -= 1
                    self.update_keyboard_feedback()

                else:
                    self.reset_isshow()
                    self.last_word_input            = guess_word
                    self.isshow_NotInDictionary     = True
                    self.timeanimation_notification = self.get_tick()

                if guess_word == self.selected_word:
                    self.reset_isshow()
                    line                            = ln + 1
                    self.coins                     += const.WIN_COINS_REWAND(self.word_length)
                    self.last_win_line              = line
                    self.last_word_input            = guess_word
                    self.isshow_Win                 = True
                    self.timeanimation_notification = self.get_tick()
                    self.save_game(win=True, line=str(line))

                elif self.guess_count <= 0:
                    self.reset_isshow()
                    self.last_word_input            = guess_word
                    self.isshow_Lose                = True
                    self.timeanimation_notification = self.get_tick()
                    self.save_game(lose=True)

            else:
                self.reset_isshow()
                self.isshow_NotEnoughLength     = True
                self.timeanimation_notification = self.get_tick()

        elif char in ascii_uppercase:
            self.handle_sound('key', 'play')

            if len_ln < self.word_length:
                self.input_history[ln].append(char)

                if self.input_point[0] < self.word_length - 1:
                    self.input_point[0] += 1

        self.update_correct_tile()

    def handle_popup(self, shortcut_key: str | None, can_inputed: bool) -> None:
        if self.validator_game_data.file_corrupt and not self.isshow_popup_warn[0]:
            WLANG = self.languages['popup']['errors']['data-game']
            self.isshow_popup_warn[0] = True
            self.show_info_popup(WLANG['title'], WLANG['message'], self.languages['popup']['errors']['button-ok'])

        if self.validator_settings.file_corrupt and not self.isshow_popup_warn[1]:
            WLANG = self.languages['popup']['errors']['data-settings']
            self.isshow_popup_warn[1] = True
            self.show_info_popup(WLANG['title'], WLANG['message'], self.languages['popup']['errors']['button-ok'])

        if not (self.init_mixer or self.isshow_popup_warn[2]):
            WLANG = self.languages['popup']['errors']['sound-mixer']
            self.isshow_popup_warn[2] = True
            self.show_info_popup(WLANG['title'], WLANG['message'], self.languages['popup']['errors']['button-ok'])

        if self.buttonHowToPlay.button_event.value or shortcut_key == '1':
            self.handle_sound('click', 'play')
            self.popup.edit_param(type='how-to-play')
            self.popup()

        elif self.buttonStats.button_event.value or shortcut_key == '2':
            self.handle_sound('click', 'play')
            self.popup.edit_param(type='stats')
            self.popup()

        elif self.buttonDailyCoins.button_event.value or shortcut_key == '7':

            def take_coins() -> None:
                if self.get_daily_countdown() is True:
                    self.coins                        += const.DAILY_COINS
                    self.game_data['prize-claim-time'] = datetime.now().strftime(r'%H/%M/%S/%d/%m/%Y')
                    self.save_game(prize_taken=True)

            self.handle_sound('click', 'play')
            self.popup.edit_param(type='daily-coins', take_coins_function=take_coins)
            self.popup()

        elif (self.buttonAutoWrite.button_event.value or shortcut_key == '3') and can_inputed:
            self.handle_sound('click', 'play')

            ln            = self.input_point[1]
            line          = self.input_history[ln]
            correct_input = self.get_correct_char()
            result        = []

            for i in range(self.word_length):
                if correct_input[i]:
                    result.append(correct_input[i])
                elif i < len(line):
                    result.append(line[i])
                else:
                    result.append(None)

            while result and result[-1] is None:
                result.pop()

            self.input_history[ln] = [item or 'X' for item in result]
            self.input_point[0]    = len(self.input_history[ln]) - (0 if len(self.input_history[ln]) < self.word_length else 1)

            self.update_correct_tile()

        elif (self.buttonLetterHint.button_event.value or shortcut_key == '8') and can_inputed:
            LANG_LETTER_HINT = self.languages['popup']['hint-letter']
            COINS_PRICE      = const.PRICE_LETTER_HINT(self.word_length)

            self.handle_sound('click', 'play')
            self.popup.edit_param(
                type         = 'hint',
                title        = LANG_LETTER_HINT['title'],
                label        = LANG_LETTER_HINT['label'],
                button_label = LANG_LETTER_HINT['button-coins'].replace('<COINS-PRICE>', str(COINS_PRICE), 1)
            )
            isbuy = self.popup()

            if isbuy == 'buy':
                if self.coins < COINS_PRICE:
                    self.show_not_enough_coin_popup()

                else:
                    if len(self.hint_tile) < self.word_length:
                        ln = self.input_point[1]

                        for attempt_feedback in self.feedback_history:
                            for i, item in enumerate(attempt_feedback):
                                for char, color in item.items():
                                    if color == 'green' and i == len(self.hint_tile):
                                        self.hint_tile.append(char)

                        index  = len(self.hint_tile) if len(self.hint_tile) < self.word_length - 1 else -1
                        letter = self.selected_word[index]

                        if len(self.hint_tile) < len(self.selected_word):
                            self.hint_tile.append(letter)
                            if letter not in self.hint_keyboard:
                                self.hint_keyboard.append(letter)

                        self.input_history[ln] = self.hint_tile.copy()
                        self.input_point[0]    = len(self.input_history[ln]) - (0 if len(self.input_history[ln]) < self.word_length else 1)

                        self.update_correct_tile()

                        self.coins -= COINS_PRICE
                        self.save_game(hint_coins_price=COINS_PRICE)

                    else:
                        self.reset_isshow()
                        self.isshow_AllTileHintsProvided = True
                        self.timeanimation_notification  = self.get_tick()

        elif (self.buttonKeyboardHint.button_event.value or shortcut_key == '9') and can_inputed:
            LANG_KEYBOARD_HINT = self.languages['popup']['hint-keyboard']
            COINS_PRICE        = const.PRICE_KEYBOARD_HINT(self.word_length)

            self.handle_sound('click', 'play')
            self.popup.edit_param(
                type         = 'hint',
                title        = LANG_KEYBOARD_HINT['title'],
                label        = LANG_KEYBOARD_HINT['label'],
                button_label = LANG_KEYBOARD_HINT['button-coins'].replace('<COINS-PRICE>', str(COINS_PRICE), 1)
            )
            isbuy = self.popup()

            if isbuy == 'buy':
                if self.coins < COINS_PRICE:
                    self.show_not_enough_coin_popup()

                else:
                    double_letter = 0
                    end_loop      = False

                    for char_selected in self.selected_word:
                        if char_selected in self.correct_char_keyboard:
                            double_letter += 1
                        if char_selected not in self.correct_char_keyboard and char_selected not in self.hint_tile and not end_loop:
                            self.hint_keyboard.append(char_selected)
                            end_loop = True

                    if double_letter != len(self.selected_word):
                        self.coins -= COINS_PRICE
                        self.save_game(hint_coins_price=COINS_PRICE)

                    else:
                        self.reset_isshow()
                        self.isshow_AllKeyboardHintsProvided = True
                        self.timeanimation_notification      = self.get_tick()

        elif (self.buttonDeletedEntry.button_event.value or shortcut_key == '0') and can_inputed:
            LANG_DEL_TILE = self.languages['popup']['delete-tile']
            COINS_PRICE   = const.PRICE_DEL_ENTRY(self.word_length)

            self.handle_sound('click', 'play')
            self.popup.edit_param(
                type         = 'hint',
                title        = LANG_DEL_TILE['title'],
                label        = LANG_DEL_TILE['label'],
                button_label = LANG_DEL_TILE['button-coins'].replace('<COINS-PRICE>', str(COINS_PRICE), 1)
            )
            isbuy = self.popup()

            if isbuy == 'buy' and self.input_point[1] > 0:
                if self.coins < COINS_PRICE:
                    self.show_not_enough_coin_popup()

                else:
                    self.guess_count += 1
                    self.input_history    .pop(-2)
                    self.input_history[-1].clear()
                    self.feedback_history .pop()
                    self.input_point[0] = 0
                    self.input_point[1] -= 1

                    self.coins -= COINS_PRICE
                    self.save_game(hint_coins_price=COINS_PRICE)

            elif isbuy == 'buy' and self.input_point[1] <= 0:
                self.reset_isshow()
                self.isshow_TileIsEmpty         = True
                self.timeanimation_notification = self.get_tick()

        elif (self.buttonReset.button_event.value or shortcut_key == '4') and self.last_time_reset + 0.5 <= self.get_tick() and can_inputed:
            self.handle_sound('click', 'play')
            self.reset()
            self.last_time_reset            = self.get_tick()
            self.timeanimation_notification = self.get_tick()
            self.isshow_Reset               = True

        elif (self.buttonSettings.button_event.value or shortcut_key == '5') and can_inputed:
            self.handle_sound('click', 'play')
            self.showSettings()
            self.last_time_close_settings = self.get_tick()

        elif shortcut_key == '6' and can_inputed:
            self.handle_sound('click', 'play')
            self.showLogs()

    def handle_notification(self) -> None:
        if (
                self.isshow_NotInDictionary or
                self.isshow_NotEnoughLength or
                self.isshow_AllTileHintsProvided or
                self.isshow_AllKeyboardHintsProvided or
                self.isshow_TileIsEmpty or
                self.isshow_Reset or
                self.isshow_Win or
                self.isshow_Lose or
                self.isshow_Unfullscreen
            ):

            LANG = self.languages['notification']
            self.notification.static_time = 3

            if self.isshow_Win:

                self.notification.static_time = 5
                self.notification.ntype = 'win'
                self.notification.text = LANG['win']

                if self.play_lose_or_win != 2:
                    self.play_lose_or_win = 1

                if self.play_lose_or_win == 1:
                    self.handle_sound('win', 'play')
                    self.gif_win.reset_frame()
                    self.play_lose_or_win = 2

                size                    = 500 * self.geomatry
                sizescreen              = self.screen.get_size()
                self.confetti_rect.left = const.math.get_center(sizescreen[0], size)
                self.confetti_rect.top  = sizescreen[1] - size

                self.gif_win.draw_and_update(self.screen)

                if self.notification():
                    self.reset()
                    self.notification.ntype = 'default'
                    self.play_lose_or_win = 0

            elif self.isshow_Lose:
                self.notification.static_time = 5
                self.notification.ntype = 'lose'
                self.notification.text = LANG['lose'].replace('<WORD>', self.selected_word, 1)

                if self.play_lose_or_win != 2:
                    self.play_lose_or_win = 1

                if self.play_lose_or_win == 1:
                    self.handle_sound('lose', 'play')
                    self.play_lose_or_win = 2

                if self.notification():
                    self.reset()
                    self.notification.ntype = 'default'
                    self.play_lose_or_win = 0

            elif self.isshow_NotInDictionary:
                self.notification.text = LANG['not-in-dictionary'].replace('<WORD>', self.last_word_input, 1)
                if self.notification():
                    self.isshow_NotInDictionary = False

            elif self.isshow_NotEnoughLength:
                self.notification.text = LANG['less-letter-length']
                if self.notification():
                    self.isshow_NotEnoughLength = False

            elif self.isshow_AllTileHintsProvided:
                self.notification.text = LANG['tile-hint-provided']
                if self.notification():
                    self.isshow_AllTileHintsProvided = False

            elif self.isshow_AllKeyboardHintsProvided:
                self.notification.text = LANG['keyboard-hint-provided']
                if self.notification():
                    self.isshow_AllKeyboardHintsProvided = False

            elif self.isshow_TileIsEmpty:
                self.notification.text = LANG['tile-empty']
                if self.notification():
                    self.isshow_TileIsEmpty = False

            elif self.isshow_Reset:
                self.notification.text = LANG['reset']
                if self.notification():
                    self.isshow_Reset = False

            elif self.isshow_Unfullscreen:
                self.notification.text = LANG['unfullscreen']
                if self.notification():
                    self.isshow_Unfullscreen = False

    def show_info_popup(self, title: str, message: str, button_ok: str = 'OK') -> None:
        self.popup.edit_param(
            type      = 'info',
            title     = title,
            label     = message,
            button_ok = button_ok
        )
        self.popup()

    def show_not_enough_coin_popup(self) -> None:
        LANG_NOT_ENOUGH_COIN = self.languages['popup']['not-enough-coin']
        self.show_info_popup(LANG_NOT_ENOUGH_COIN['title'], LANG_NOT_ENOUGH_COIN['label'], LANG_NOT_ENOUGH_COIN['button-ok'])

    def showTextBar(self) -> None:
        LANG       = self.languages['text-bar']
        sizescreen = self.screen.get_size()
        text       = self.font_textbar.render(
            '{} | {} | {} | {}'.format(
                self.__label_version__,
                LANG['word']               .replace('<WORD-ID>',    self.language_word.upper(), 1),
                LANG['valid-word']['label'].replace('<VALID-WORD>', LANG['valid-word'][str(self.use_valid_word).lower()], 1),
                LANG['fps']                .replace('<FPS>',        self.num_format.parse(self.clock.get_fps()), 1)
            ), True, self.themes['barMenu']['text'], self.themes['barMenu']['background']
        )

        text.set_alpha(200)

        self.screen.blit(text, text.get_rect(
            left = const.math.get_center(sizescreen[0], text.get_width()),
            top  = sizescreen[1] - text.get_height() - const.math.get_center(sizescreen[1] - self.boardRect_keyboard.bottom, text.get_height())
        ))

    def showKeyboard(self, letter_typing: str | None = None, justshow: bool = False, letter_hovered: str | None = None) -> tuple[bool, str | None, bool]:
        sizescreen     = self.screen.get_size()
        margin         = 10 * self.geomatry
        marginlr       = 40 * self.geomatry
        buttonSize     = (50 * self.geomatry, 70 * self.geomatry)
        inputDetected  = (False, None, False)
        totalButtonKey = lambda keys_total, xy : keys_total * buttonSize[xy] + margin * (keys_total - 1)
        max_buttonkey  = (totalButtonKey(10, 0), totalButtonKey(3, 1))
        keyboards      = self.keyboards[self.keyboard_layout]

        self.boardRect_keyboard = pygame.Rect(
            (sizescreen[0] - marginlr - max_buttonkey[0]) / 2,
            (sizescreen[1] - marginlr - max_buttonkey[1]) - 60 * self.geomatry,
            marginlr + max_buttonkey[0],
            marginlr + max_buttonkey[1]
        )

        if self.show_keyboard:
            img_backspace = pygame.transform.scale(self.image_backspace, ((buttonSize[0] + buttonSize[0] / 2) / 1.8, buttonSize[1] / 2))
            img_enter     = pygame.transform.scale(self.image_enter,     img_backspace.get_size())

            backspace_and_enter_left_pos = {
                const.BACKSPACE: marginlr / 2,
                const.ENTER    : self.boardRect_keyboard.width - marginlr / 2 - (buttonSize[0] + buttonSize[0] / 2 + margin / 2)
            }

            pygame.draw.rect(self.screen, self.themes['keyboard']['background'], self.boardRect_keyboard)

            for row, line in enumerate(keyboards):
                for col, letter in enumerate(line):

                    keyRect = pygame.Rect(
                        self.boardRect_keyboard.left + (const.math.get_center(self.boardRect_keyboard.width,  totalButtonKey(len(keyboards[row]), 0)) + (col * (buttonSize[0] + margin)) if letter not in const.ALL_KEY else backspace_and_enter_left_pos[letter]),
                        self.boardRect_keyboard.top  +  const.math.get_center(self.boardRect_keyboard.height, max_buttonkey[1]) + (row * (buttonSize[1] + margin)),
                        buttonSize[0] + buttonSize[0] / 2 + margin / 2 if letter in const.ALL_KEY else buttonSize[0],
                        buttonSize[1]
                    )

                    color       = self.keyboard_feedback[letter.upper()]
                    mousePos    = pygame.mouse.get_pos()
                    isMouseOver = keyRect.collidepoint(*mousePos)
                    button_keyboard_color = button_color(
                        inactive_color = self.themes['keyboard']['button'][color]['inactive'],
                        active_color   = self.themes['keyboard']['button'][color]['active'],
                        hover_color    = self.themes['keyboard']['button'][color]['hover']
                    )

                    self.buttonOutlineKeyboard.rect = const.math.Rect_outline(keyRect, 4 * self.geomatry)

                    self.buttonKeyboard.rect  = keyRect
                    self.buttonKeyboard.text  = letter if letter not in const.ALL_KEY else ''
                    self.buttonKeyboard.font  = self.font_keyboard
                    self.buttonKeyboard.color = button_keyboard_color

                    if letter_typing == letter:
                        self.buttonOutlineKeyboard.draw_active()

                    if isMouseOver and not justshow:
                        self.buttonOutlineKeyboard.draw_active()
                        self.buttonKeyboard.draw_and_update()

                        if letter == letter_hovered:
                            inputDetected = (False, None, self.buttonKeyboard.button_event.ismousehover)

                        if self.buttonKeyboard.button_event.value:
                            inputDetected = (True, letter, inputDetected[2])

                    else:
                        if letter_typing != letter:
                            self.buttonOutlineKeyboard.draw_inactive()

                        self.buttonKeyboard.draw_inactive()

                    if letter == const.BACKSPACE:
                        self.screen.blit(img_backspace, img_backspace.get_rect(center=keyRect.center))
                    elif letter == const.ENTER:
                        self.screen.blit(img_enter,     img_enter    .get_rect(center=keyRect.center))

        return inputDetected

    def showTile(self, justshow: bool = False, tile_point_preview: bool = False) -> None:
        wscreen          = self.screen.get_width()
        self.margin_tile = 10 * self.geomatry
        self.size_tile   = 80 * self.geomatry

        if self.word_length * self.size_tile + self.margin_tile * (self.word_length - 1) > wscreen - self.margin_tile * 2:
            self.size_tile = (wscreen - self.margin_tile) / self.word_length - self.margin_tile

        if self.last_size_tile != self.size_tile:
            self.font_tile      = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(self.size_tile))
            self.last_size_tile = self.size_tile

        for row in range(self.change_guess):
            for col in range(self.word_length):

                letter = None
                color  = 'not-inputed'

                if row <= len(self.input_history) - 1:
                    ln = self.input_history[row]
                    if col <= len(ln) - 1:
                        letter = ln[col]

                if row <= len(self.feedback_history) - 1:
                    ln = self.feedback_history[row]
                    if col <= len(ln) - 1:
                        color = list(ln[col].values())[0]

                if row == self.input_point[1]:
                    color = self.correct_char_tile[col]

                tile_rect = pygame.Rect(
                    (wscreen - self.word_length * (self.size_tile + self.margin_tile) + self.margin_tile) / 2 + col * (self.size_tile + self.margin_tile),
                    (row * (self.size_tile + self.margin_tile)) + self.scroller_tile.direction,
                    self.size_tile,
                    self.size_tile
                )

                pygame.draw.rect(self.screen, self.themes['boxEntryTile']['box']['outline'][
                        'point-active' if [col, row] == self.input_point and ((int(self.get_tick() * 2) % 2 == 0 and not (justshow or self.isshow_Win or self.isshow_Lose)) or tile_point_preview) else 'point-inactive'
                    ], const.math.Rect_outline(tile_rect, 4 * self.geomatry)
                )
                pygame.draw.rect(self.screen, self.themes['boxEntryTile']['box'][color], tile_rect)

                if letter is not None:
                    showLetter = self.font_tile.render(letter, True, self.themes['boxEntryTile']['text'])
                    self.screen.blit(showLetter, showLetter.get_rect(center=tile_rect.center))

    def showBarMenu(self, justshow: bool = False) -> None:
        wscreen                     = self.screen.get_width()
        barTop_rect                 = pygame.Rect(const.math.get_center(wscreen,   (wscreen - 10 * self.geomatry)), 5 * self.geomatry, wscreen - 10 * self.geomatry, 60 * self.geomatry)
        barBottom_rect              = pygame.Rect(barTop_rect.left,                barTop_rect.bottom + 5 * self.geomatry,             barTop_rect.width,            50 * self.geomatry)
        size_button_and_icon_top    = barTop_rect.height    - 10 * self.geomatry
        size_button_and_icon_bottom = barBottom_rect.height - 10 * self.geomatry
        button_howToPlay_rect       = pygame.Rect(barTop_rect.left           + 10 * self.geomatry,                               barTop_rect.top + const.math.get_center(barTop_rect.height, size_button_and_icon_top),          size_button_and_icon_top,    size_button_and_icon_top)
        button_stats_rect           = pygame.Rect(button_howToPlay_rect.left + size_button_and_icon_top + 10 * self.geomatry,    barTop_rect.top + const.math.get_center(barTop_rect.height, size_button_and_icon_top),          size_button_and_icon_top,    size_button_and_icon_top)
        button_settings_rect        = pygame.Rect(barTop_rect.right          - size_button_and_icon_top - 10 * self.geomatry,    barTop_rect.top + const.math.get_center(barTop_rect.height, size_button_and_icon_top),          size_button_and_icon_top,    size_button_and_icon_top)
        button_reset_rect           = pygame.Rect(button_settings_rect.left  - size_button_and_icon_top - 10 * self.geomatry,    barTop_rect.top + const.math.get_center(barTop_rect.height, size_button_and_icon_top),          size_button_and_icon_top,    size_button_and_icon_top)
        button_auto_write_rect      = pygame.Rect(button_reset_rect.left     - size_button_and_icon_top - 10 * self.geomatry,    barTop_rect.top + const.math.get_center(barTop_rect.height, size_button_and_icon_top),          size_button_and_icon_top,    size_button_and_icon_top)
        button_bag_coin_rect        = pygame.Rect(barBottom_rect.left        + 10 * self.geomatry,                               barBottom_rect.top + const.math.get_center(barBottom_rect.height, size_button_and_icon_bottom), size_button_and_icon_bottom, size_button_and_icon_bottom)
        button_hammer_rect          = pygame.Rect(barTop_rect.right          - size_button_and_icon_bottom - 10 * self.geomatry, barBottom_rect.top + const.math.get_center(barBottom_rect.height, size_button_and_icon_bottom), size_button_and_icon_bottom, size_button_and_icon_bottom)
        button_keyboard_rect        = pygame.Rect(button_hammer_rect.left    - size_button_and_icon_bottom - 20 * self.geomatry, barBottom_rect.top + const.math.get_center(barBottom_rect.height, size_button_and_icon_bottom), size_button_and_icon_bottom, size_button_and_icon_bottom)
        button_lamp_rect            = pygame.Rect(button_keyboard_rect.left  - size_button_and_icon_bottom - 20 * self.geomatry, barBottom_rect.top + const.math.get_center(barBottom_rect.height, size_button_and_icon_bottom), size_button_and_icon_bottom, size_button_and_icon_bottom)

        if not self.show_keyboard:
            button_lamp_rect = button_keyboard_rect

        self.buttonHowToPlay   .edit_param(rect=button_howToPlay_rect,  image_transform=2.5 * self.geomatry)
        self.buttonDailyCoins  .edit_param(rect=button_bag_coin_rect,   image_transform=self.buttonHowToPlay.image_transform)
        self.buttonStats       .edit_param(rect=button_stats_rect,      image_transform=self.buttonHowToPlay.image_transform)
        self.buttonAutoWrite   .edit_param(rect=button_auto_write_rect, image_transform=self.buttonHowToPlay.image_transform)
        self.buttonReset       .edit_param(rect=button_reset_rect,      image_transform=self.buttonHowToPlay.image_transform)
        self.buttonSettings    .edit_param(rect=button_settings_rect,   image_transform=self.buttonHowToPlay.image_transform)
        self.buttonLetterHint  .edit_param(rect=button_lamp_rect,       image_transform=self.buttonHowToPlay.image_transform)
        self.buttonDeletedEntry.edit_param(rect=button_hammer_rect,     image_transform=self.buttonHowToPlay.image_transform)

        if self.show_keyboard:
            self.buttonKeyboardHint.edit_param(rect=button_keyboard_rect,   image_transform=self.buttonHowToPlay.image_transform)

        pygame.draw.rect(self.screen, self.themes['barMenu']['background'], barTop_rect)
        pygame.draw.rect(self.screen, self.themes['barMenu']['background'], barBottom_rect)

        if not justshow:
            self.buttonHowToPlay   .draw_and_update()
            self.buttonStats       .draw_and_update()
            self.buttonSettings    .draw_and_update()
            self.buttonAutoWrite   .draw_and_update()
            self.buttonReset       .draw_and_update()
            self.buttonDailyCoins  .draw_and_update()
            self.buttonLetterHint  .draw_and_update()
            self.buttonDeletedEntry.draw_and_update()

            if self.show_keyboard:
                self.buttonKeyboardHint.draw_and_update()

        else:
            self.buttonHowToPlay   .draw_inactive()
            self.buttonStats       .draw_inactive()
            self.buttonSettings    .draw_inactive()
            self.buttonAutoWrite   .draw_inactive()
            self.buttonReset       .draw_inactive()
            self.buttonDailyCoins  .draw_inactive()
            self.buttonLetterHint  .draw_inactive()
            self.buttonDeletedEntry.draw_inactive()

            if self.show_keyboard:
                self.buttonKeyboardHint.draw_inactive()

        if self.get_daily_countdown() is True:
            pygame.draw.circle(self.screen, self.themes['barMenu']['indicator'], (button_bag_coin_rect.right, button_bag_coin_rect.top), radius=7 * self.geomatry)

        showKatla = self.font_katla.render(f'KATLA #{self.word_length}',                                                   True, self.themes['barMenu']['text'])
        showCoins = self.font_coins.render(self.num_format.parse(self.coins) if not const.isinf(self.coins) else '\u221e', True, self.themes['barMenu']['text'])

        self.screen.blit(showKatla, showKatla.get_rect(center=barTop_rect.center))
        self.screen.blit(showCoins, showCoins.get_rect(left=button_bag_coin_rect.right + 20 * self.geomatry, top=button_bag_coin_rect.top + (button_bag_coin_rect.height - showCoins.get_height()) / 2))

    def showFreezeKatla(self, tile_point_preview: bool = False) -> None:
        self.scroller_tile.min_max_scrolled = (-((self.size_tile + self.margin_tile) * (self.change_guess - 1) - self.margin_tile / 2), self.screen.get_height() - (self.size_tile + self.margin_tile / 2))

        if self.scroller_tile.direction < self.scroller_tile.min_max_scrolled[0]:
            self.scroller_tile.direction = self.scroller_tile.min_max_scrolled[0]
        elif self.scroller_tile.direction > self.scroller_tile.min_max_scrolled[1]:
            self.scroller_tile.direction = self.scroller_tile.min_max_scrolled[1]

        self.screen.fill (self.themes['screen'])

        self.showTile    (justshow=True, tile_point_preview=tile_point_preview)
        self.showBarMenu (justshow=True)
        self.showKeyboard(justshow=True)
        self.showTextBar ()

        self.handle_notification()

    def showLogs(self) -> None:
        self.isshow_Logs   = True
        scroller           = ScrollerY(self, (0, 1))
        close_button       = Button(
            surface_screen  = self.screen,
            rect            = self.init_rect,
            image           = self.image_close,
            outline_size    = 4 * self.geomatry,
            color           = button_color(
                self.themes['logs']['button']['inactive'],
                self.themes['logs']['button']['active'],
                self.themes['logs']['button']['hover']
            ),
            outline_color   = button_color(*[self.themes['logs']['button']['outline'] for _ in range(3)]),
            inactive_cursor = pygame.SYSTEM_CURSOR_ARROW,
            active_cursor   = pygame.SYSTEM_CURSOR_HAND,
            only_click      = 'l'
        )
        font_log         = pygame.font.Font(self.file.FONT_ROBOTO_MONO_REGULAR, int(15 * self.geomatry))
        font_warn        = pygame.font.Font(self.file.FONT_ROBOTO_MONO_BOLD,    int(20 * self.geomatry))
        height_font      = font_log.size(const.HELLO)[1]
        last_message     = logs.messages.copy()
        warnings         = 0
        errors           = 0
        wraped_text      = []
        last_size_screen = (0, 0)

        while self.isshow_Logs:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running         = False
                    self.isshow_Logs     = False
                    self.isshow_Settings = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isshow_Logs = False

                scroller.event(event)

                self.handle_screen_resize(event)

                close_button.handle_event(event)

            screen_size = self.screen.get_size()

            close_rect         = pygame.Rect(screen_size[0] - 70 * self.geomatry, screen_size[1] - 70 * self.geomatry, 50 * self.geomatry, 50 * self.geomatry)
            background_surface = pygame.Surface(screen_size)

            background_surface.fill(self.themes['logs']['background'])
            background_surface.set_alpha(150)

            close_button.edit_param(rect=close_rect, image_transform=5 * self.geomatry)

            self.showFreezeKatla()

            if [last_size_screen, last_message] != [screen_size, logs.messages]:
                warnings     = 0
                errors       = 0
                last_message = logs.messages.copy()
                wraped_text.clear()

                for line in logs.messages:
                    line_type = line['type']
                    line_time = line['time']

                    stringinfo = f"[{line_time}] [{line_type.upper()}] {line['message']}" if line_type != 'license' else line['message']

                    if line_type == 'warn':
                        warnings += 1
                    elif line_type == 'error':
                        errors += 1

                    for line_wrap in wrap_text(font_log, stringinfo, screen_size[0] - 10 * self.geomatry):
                        wraped_text.append({'line': line_wrap, 'type': line_type})

                last_size_screen = screen_size

            scroller.min_max_scrolled = (0, len(wraped_text) * height_font + 5 * self.geomatry)

            scroller.update()

            self.screen.blit(background_surface, (0, 0))

            visible_start = int(scroller.direction // height_font)
            visible_end   = int(visible_start + (screen_size[1] // height_font))

            for i in range(visible_start, min(visible_end, len(wraped_text))):
                ln     = wraped_text[i]
                text   = ln['line']
                typeln = ln['type']

                surface_text = font_log.render(text, True, self.themes['logs']['text'][typeln])
                self.screen.blit(surface_text, surface_text.get_rect(left=5 * self.geomatry, top=5 * self.geomatry + i * surface_text.get_height() - scroller.direction))

            close_button.draw_and_update()

            warn_text = font_warn.render("Warnings: {} | Errors: {} | Total, Lines: {}, {}".format(
                    self.num_format.parse(warnings),
                    self.num_format.parse(errors),
                    self.num_format.parse(len(logs.messages)),
                    self.num_format.parse(len(wraped_text))
                ), True, self.themes['logs']['text']['label-color'], self.themes['logs']['text']['label-background']
            )

            self.screen.blit(warn_text, surface_text.get_rect(left=5 * self.geomatry, top=screen_size[1] - (5 * self.geomatry) - warn_text.get_height()))

            if close_button.button_event.value:
                self.handle_sound('click', 'play')
                self.isshow_Logs = False

            pygame.display.flip()

            self.clock.tick(self.fps)

    def showSettings(self) -> None:
        LANG                 = self.languages['settings']
        self.isshow_Settings = True

        theme           = self.settings['theme']
        keyboard_layout = self.settings['keyboard-layout']
        sound_volume    = self.settings['sound-volume']
        music_volume    = self.settings['music-volume']
        change_guess    = self.settings['change-guess']
        word_length     = self.settings['word-length']
        fps             = self.settings['fps']
        geomatry        = self.settings['geomatry'] * 10
        language        = self.settings['language']
        language_word   = self.settings['language-word']
        use_valid_word  = self.settings['use-valid-word']
        show_keyboard   = self.settings['show-keyboard']

        languages_id_list       = self.validator_languages      .get_lang_id ()
        theme_id_list           = self.validator_themes         .get_theme_id()
        languages_word_id_list  = self.validator_word_dictionary.get_lang_id ()
        language_name_list      = self.validator_languages      .get_lang_name()
        language_word_name_list = self.validator_word_dictionary.get_lang_name()

        index_lang_word       = languages_word_id_list.index(language_word)
        index_lang            = languages_id_list     .index(language)
        index_theme           = theme_id_list         .index(theme)
        index_keyboard_layout = const.Keyboard.__all__.index(keyboard_layout)

        last_configuration  = [index_theme, index_keyboard_layout, sound_volume, music_volume, change_guess, word_length, fps, geomatry, index_lang, index_lang_word, use_valid_word, show_keyboard]
        first_configuration = last_configuration.copy()

        background_rect      = pygame.Rect(0, 0, 0, 0)
        navbar_rect          = background_rect.copy()
        last_background_rect = background_rect.copy()

        font_title       = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,      int(35 * self.geomatry))
        font_license     = pygame.font.Font(self.file.FONT_ROBOTO_MONO_BOLD, int(15 * self.geomatry))
        label_group_font = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,      int(32 * self.geomatry))
        label_font       = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(25 * self.geomatry))
        nav_font         = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(35 * self.geomatry))
        font1            = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(30 * self.geomatry))
        surface_title    = font_title.render(LANG['title'], True, self.themes['settings']['text'])

        buttonClose = Button(
            surface_screen  = self.screen,
            rect            = self.init_rect,
            hide            = True,
            image           = self.image_close,
            image_transform = 0,
            click_speed     = 0
        )
        buttonLang = Button(
            surface_screen = self.screen,
            rect           = self.init_rect,
            font           = label_font,
            outline_size   = 4 * self.geomatry,
            text_color     = button_color(*[self.themes['settings']['text'] for _ in range(3)]),
            color          = button_color(
                self.themes['settings']['button']['set']['inactive'],
                self.themes['settings']['button']['set']['active'],
                self.themes['settings']['button']['set']['hover']
            ),
            outline_color  = button_color(*[self.themes['settings']['outline'] for _ in range(3)]),
            only_click     = 'rl',
            click_speed    = 500
        )
        buttonLangWord        = buttonLang      .copy()
        buttonOxfordWord      = buttonLang      .copy(only_click='l', click_speed=50)
        buttonWordLen         = buttonLang      .copy(font=font1, click_speed=100)
        buttonChangeGuess     = buttonWordLen   .copy()
        buttonTheme           = buttonLang      .copy(click_speed=100)
        buttonTypeKeyboard    = buttonTheme     .copy()
        buttonShowKeyboard    = buttonOxfordWord.copy()
        buttonGeomatry        = buttonTheme     .copy()
        buttonFps             = buttonTheme     .copy()
        buttonLogs            = buttonTheme     .copy()
        buttonNav_lang        = {'l': buttonLang .copy(only_click='l', text='<', font=nav_font), 'r': buttonLang .copy(only_click='l', text='>', font=nav_font)}
        buttonNav_langword    = {'l': buttonLang .copy(only_click='l', text='<', font=nav_font), 'r': buttonLang .copy(only_click='l', text='>', font=nav_font)}
        buttonNav_wordlen     = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_changeguess = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_theme       = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_typekeyb    = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_geomarty    = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_fps         = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        rangeSound = Range(
            surface_screen   = self.screen,
            rect             = self.init_rect,
            thumb_color      = button_color(
                self.themes['settings']['range']['thumb']['inactive'],
                self.themes['settings']['range']['thumb']['active'],
                self.themes['settings']['range']['thumb']['hover']
            ),
            track_color      = button_color(
                self.themes['settings']['range']['track']['inactive'],
                self.themes['settings']['range']['track']['active'],
                self.themes['settings']['range']['track']['hover']
            ),
            track_fill_color = button_color(
                self.themes['settings']['range']['track-fill']['inactive'],
                self.themes['settings']['range']['track-fill']['active'],
                self.themes['settings']['range']['track-fill']['hover']
            ),
            drag_scroller_mouse = False,
            max_value           = const.MAX_SOUND,
            min_value           = const.MIN_SOUND,
            value               = sound_volume,
            step                = const.STEP_SOUND,
            range_value_output  = int,
            click_speed         = 0
        )
        rangeMusic = rangeSound.copy(
            max_value = const.MAX_MUSIC,
            min_value = const.MIN_MUSIC,
            value     = music_volume,
            step      = const.STEP_MUSIC
        )

        font_license_size = font_license.size(const.HELLO)
        wrap_license      = wrap_text(font_license, self.__license__, background_rect.width - 10 * self.geomatry)
        scroller          = ScrollerY(self, (0, 1000 * self.geomatry + font_license_size[1] * len(wrap_license)))
        nfgeomatry        = NumberFormat(self.languages['exponents-number'], decimal_places=1, rounded=False, anchor_decimal_places=True, reach=(3, 'thousand'))

        def label(label_text: str, type: const.Literal['group', 'label'], index: const.Number) -> None:
            if   type == 'group': surface_text = label_group_font.render(label_text, True, self.themes['settings']['text'])
            elif type == 'label': surface_text = label_font      .render(label_text, True, self.themes['settings']['text'])
            self.screen.blit(surface_text, surface_text.get_rect(left=background_rect.left + 10 * self.geomatry, top=index))

        def button_edit(button_edit_param: Button, button_get_param: Button, kw: dict | None = None) -> None:
            button_edit_param.edit_param(**((button_get_param.get_param() | kw) if kw is not None else button_get_param.get_param()))

        def ternary(condination: bool, expression1: const.Any, expression2: const.Any) -> const.Any:
            return expression1 if bool(condination) else expression2

        while self.isshow_Settings:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                    self.isshow_Settings = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isshow_Settings = False

                scroller.event(event)

                self.handle_screen_resize(event)

                buttonClose               .handle_event(event)
                buttonLang                .handle_event(event)
                buttonLangWord            .handle_event(event)
                buttonOxfordWord          .handle_event(event)
                buttonWordLen             .handle_event(event)
                buttonChangeGuess         .handle_event(event)
                buttonTheme               .handle_event(event)
                buttonTypeKeyboard        .handle_event(event)
                buttonShowKeyboard        .handle_event(event)
                buttonGeomatry            .handle_event(event)
                buttonFps                 .handle_event(event)
                buttonLogs                .handle_event(event)
                buttonNav_lang['l']       .handle_event(event)
                buttonNav_lang['r']       .handle_event(event)
                buttonNav_langword['l']   .handle_event(event)
                buttonNav_langword['r']   .handle_event(event)
                buttonNav_wordlen['l']    .handle_event(event)
                buttonNav_wordlen['r']    .handle_event(event)
                buttonNav_changeguess['l'].handle_event(event)
                buttonNav_changeguess['r'].handle_event(event)
                buttonNav_theme['l']      .handle_event(event)
                buttonNav_theme['r']      .handle_event(event)
                buttonNav_typekeyb['l']   .handle_event(event)
                buttonNav_typekeyb['r']   .handle_event(event)
                buttonNav_geomarty['l']   .handle_event(event)
                buttonNav_geomarty['r']   .handle_event(event)
                buttonNav_fps['l']        .handle_event(event)
                buttonNav_fps['r']        .handle_event(event)

            scroller.min_max_scrolled = (0, 1060 * self.geomatry + font_license_size[1] * len(wrap_license))
            mouse_pos                 = pygame.mouse.get_pos()
            sizescreen                = self.screen.get_size()

            scroller.update(anchor=(
                not background_rect       .collidepoint(*mouse_pos)  or
                navbar_rect               .collidepoint(*mouse_pos)  or
                rangeSound                .button_event.isdragging   or
                rangeMusic                .button_event.isdragging   or
                buttonLang                .button_event.ismousehover or
                buttonLangWord            .button_event.ismousehover or
                buttonOxfordWord          .button_event.ismousehover or
                buttonWordLen             .button_event.ismousehover or
                buttonChangeGuess         .button_event.ismousehover or
                buttonTheme               .button_event.ismousehover or
                buttonTypeKeyboard        .button_event.ismousehover or
                buttonShowKeyboard        .button_event.ismousehover or
                buttonGeomatry            .button_event.ismousehover or
                buttonFps                 .button_event.ismousehover or
                buttonLogs                .button_event.ismousehover or
                buttonNav_lang['l']       .button_event.ismousehover or
                buttonNav_lang['r']       .button_event.ismousehover or
                buttonNav_langword['l']   .button_event.ismousehover or
                buttonNav_langword['r']   .button_event.ismousehover or
                buttonNav_wordlen['l']    .button_event.ismousehover or
                buttonNav_wordlen['r']    .button_event.ismousehover or
                buttonNav_changeguess['l'].button_event.ismousehover or
                buttonNav_changeguess['r'].button_event.ismousehover or
                buttonNav_theme['l']      .button_event.ismousehover or
                buttonNav_theme['r']      .button_event.ismousehover or
                buttonNav_typekeyb['l']   .button_event.ismousehover or
                buttonNav_typekeyb['r']   .button_event.ismousehover or
                buttonNav_geomarty['l']   .button_event.ismousehover or
                buttonNav_geomarty['r']   .button_event.ismousehover or
                buttonNav_fps['l']        .button_event.ismousehover or
                buttonNav_fps['r']        .button_event.ismousehover
            ))

            background_rect        = pygame.Rect(const.math.get_center(sizescreen[0], sizescreen[0] - 100 * self.geomatry), 0,                                        sizescreen[0] - 100 * self.geomatry, sizescreen[1])
            buttonClose.rect       = pygame.Rect(background_rect.right - 50 * self.geomatry,                                background_rect.top + 10 * self.geomatry, 40 * self.geomatry,                 40 * self.geomatry)
            navbar_rect            = pygame.Rect(background_rect.left,                                                      background_rect.top,                      background_rect.width,              buttonClose.rect.bottom + 10 * self.geomatry)
            mainBackground_rect    = const.math.Rect_outline(background_rect, 10 * self.geomatry)
            mainBackground_surface = pygame.Surface((mainBackground_rect.width, mainBackground_rect.height))
            background_surface     = pygame.Surface((background_rect.width,     mainBackground_rect.height))

            buttonLang                .rect = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 45 * self.geomatry - scroller.direction,  250 * self.geomatry,   50 * self.geomatry)
            buttonLangWord            .rect = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 105 * self.geomatry - scroller.direction, 250 * self.geomatry,   50 * self.geomatry)
            buttonOxfordWord          .rect = pygame.Rect(background_rect.right - 45 * self.geomatry,  navbar_rect.bottom + 420 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonWordLen             .rect = pygame.Rect(background_rect.right - 45 * self.geomatry,  navbar_rect.bottom + 470 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonChangeGuess         .rect = pygame.Rect(background_rect.right - 45 * self.geomatry,  navbar_rect.bottom + 520 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonTheme               .rect = pygame.Rect(background_rect.right - 155 * self.geomatry, navbar_rect.bottom + 635 * self.geomatry - scroller.direction, 150 * self.geomatry,   50 * self.geomatry)
            buttonTypeKeyboard        .rect = pygame.Rect(background_rect.right - 155 * self.geomatry, navbar_rect.bottom + 695 * self.geomatry - scroller.direction, 150 * self.geomatry,   50 * self.geomatry)
            buttonShowKeyboard        .rect = pygame.Rect(background_rect.right - 45 * self.geomatry,  navbar_rect.bottom + 755 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonGeomatry            .rect = pygame.Rect(background_rect.right - 155 * self.geomatry, navbar_rect.bottom + 875 * self.geomatry - scroller.direction, 150 * self.geomatry,   50 * self.geomatry)
            buttonFps                 .rect = pygame.Rect(background_rect.right - 155 * self.geomatry, navbar_rect.bottom + 935 * self.geomatry - scroller.direction, 150 * self.geomatry,   50 * self.geomatry)
            buttonLogs                .rect = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 995 * self.geomatry - scroller.direction, 250 * self.geomatry,   50 * self.geomatry)
            buttonNav_lang['l']       .rect = pygame.Rect(background_rect.right - 355 * self.geomatry, navbar_rect.bottom + 50 * self.geomatry - scroller.direction,  40 * self.geomatry,    40 * self.geomatry)
            buttonNav_lang['r']       .rect = pygame.Rect(background_rect.right - 305 * self.geomatry, navbar_rect.bottom + 50 * self.geomatry - scroller.direction,  40 * self.geomatry,    40 * self.geomatry)
            buttonNav_langword['l']   .rect = pygame.Rect(background_rect.right - 355 * self.geomatry, navbar_rect.bottom + 110 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_langword['r']   .rect = pygame.Rect(background_rect.right - 305 * self.geomatry, navbar_rect.bottom + 110 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_wordlen['l']    .rect = pygame.Rect(background_rect.right - 145 * self.geomatry, navbar_rect.bottom + 470 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_wordlen['r']    .rect = pygame.Rect(background_rect.right - 95 * self.geomatry,  navbar_rect.bottom + 470 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_changeguess['l'].rect = pygame.Rect(background_rect.right - 145 * self.geomatry, navbar_rect.bottom + 520 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_changeguess['r'].rect = pygame.Rect(background_rect.right - 95 * self.geomatry,  navbar_rect.bottom + 520 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_theme['l']      .rect = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 640 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_theme['r']      .rect = pygame.Rect(background_rect.right - 205 * self.geomatry, navbar_rect.bottom + 640 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_typekeyb['l']   .rect = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 700 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_typekeyb['r']   .rect = pygame.Rect(background_rect.right - 205 * self.geomatry, navbar_rect.bottom + 700 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_geomarty['l']   .rect = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 880 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_geomarty['r']   .rect = pygame.Rect(background_rect.right - 205 * self.geomatry, navbar_rect.bottom + 880 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_fps['l']        .rect = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 940 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            buttonNav_fps['r']        .rect = pygame.Rect(background_rect.right - 205 * self.geomatry, navbar_rect.bottom + 940 * self.geomatry - scroller.direction, 40 * self.geomatry,    40 * self.geomatry)
            rangeSound                .rect = pygame.Rect(background_rect.right - 315 * self.geomatry, navbar_rect.bottom + 250 * self.geomatry - scroller.direction, 300 * self.geomatry,   14 * self.geomatry)
            rangeMusic                .rect = pygame.Rect(rangeSound.rect.left,                        navbar_rect.bottom + 300 * self.geomatry - scroller.direction, rangeSound.rect.width, rangeSound.rect.height)
            buttonLang                .text = language_name_list[index_lang]
            buttonLangWord            .text = language_word_name_list[index_lang_word]
            buttonWordLen             .text = str(word_length)
            buttonChangeGuess         .text = str(change_guess)
            buttonTheme               .text = LANG['display']['buttons-label']['app-theme'][theme]
            buttonTypeKeyboard        .text = keyboard_layout
            buttonGeomatry            .text = nfgeomatry.parse(geomatry / 10) + "x"
            buttonFps                 .text = str(fps)
            buttonLogs                .text = LANG['additional-settings']['label']['logs']['button-label']

            buttonClose     .edit_param()
            rangeSound      .edit_param(thumb_size=(20 * self.geomatry, 20 * self.geomatry))
            rangeMusic      .edit_param(thumb_size=rangeSound.thumb_size)
            buttonOxfordWord.edit_param(
                color = button_color(
                    self.themes['settings']['button']['switch'][str(use_valid_word).lower()]['inactive'],
                    self.themes['settings']['button']['switch'][str(use_valid_word).lower()]['active'],
                    self.themes['settings']['button']['switch'][str(use_valid_word).lower()]['hover']
                ),
                **({
                    'image': self.image_check,
                    'image_transform': 5 * self.geomatry
                } if use_valid_word else {
                    'image': None,
                    'image_transform': None
                })
            )
            buttonShowKeyboard.edit_param(
                color = button_color(
                    self.themes['settings']['button']['switch'][str(show_keyboard).lower()]['inactive'],
                    self.themes['settings']['button']['switch'][str(show_keyboard).lower()]['active'],
                    self.themes['settings']['button']['switch'][str(show_keyboard).lower()]['hover']
                ),
                **({
                    'image': self.image_check,
                    'image_transform': 5 * self.geomatry
                } if show_keyboard else {
                    'image': None,
                    'image_transform': None
                })
            )

            mainBackground_surface.fill(self.themes['settings']['outline'])
            background_surface    .fill(self.themes['settings']['background'])
            mainBackground_surface.set_alpha(125)

            self.showFreezeKatla(tile_point_preview=True)

            mainBackground_surface.blit(background_surface,     (const.math.get_center(mainBackground_rect.width, background_rect.width), background_rect.top))
            self.screen           .blit(mainBackground_surface, mainBackground_rect)

            set_cursor_buttons(
                buttonClose,
                buttonLang,
                buttonLangWord,
                buttonOxfordWord,
                buttonWordLen,
                buttonChangeGuess,
                buttonTheme,
                buttonTypeKeyboard,
                buttonShowKeyboard,
                buttonGeomatry,
                buttonFps,
                buttonLogs,
                buttonNav_lang['l'],
                buttonNav_lang['r'],
                buttonNav_langword['l'],
                buttonNav_langword['r'],
                buttonNav_wordlen['l'],
                buttonNav_wordlen['r'],
                buttonNav_changeguess['l'],
                buttonNav_changeguess['r'],
                buttonNav_theme['l'],
                buttonNav_theme['r'],
                buttonNav_typekeyb['l'],
                buttonNav_typekeyb['r'],
                buttonNav_geomarty['l'],
                buttonNav_geomarty['r'],
                buttonNav_fps['l'],
                buttonNav_fps['r'],
                rangeSound,
                rangeMusic,
                inactive_cursor = pygame.SYSTEM_CURSOR_ARROW,
                active_cursor   = pygame.SYSTEM_CURSOR_HAND
            )

            if not navbar_rect.collidepoint(*mouse_pos):
                buttonNav_lang['l']       .draw_and_update()
                buttonNav_lang['r']       .draw_and_update()
                buttonNav_langword['l']   .draw_and_update()
                buttonNav_langword['r']   .draw_and_update()
                buttonNav_wordlen['l']    .draw_and_update()
                buttonNav_wordlen['r']    .draw_and_update()
                buttonNav_changeguess['l'].draw_and_update()
                buttonNav_changeguess['r'].draw_and_update()
                buttonNav_theme['l']      .draw_and_update()
                buttonNav_theme['r']      .draw_and_update()
                buttonNav_geomarty['l']   .draw_and_update()
                buttonNav_geomarty['r']   .draw_and_update()
                buttonNav_fps['l']        .draw_and_update()
                buttonNav_fps['r']        .draw_and_update()
                buttonLang                .draw_and_update()
                buttonLangWord            .draw_and_update()
                buttonOxfordWord          .draw_and_update()
                buttonWordLen             .draw_and_update()
                buttonChangeGuess         .draw_and_update()
                buttonTheme               .draw_and_update()
                buttonShowKeyboard        .draw_and_update()
                buttonGeomatry            .draw_and_update()
                buttonFps                 .draw_and_update()
                buttonLogs                .draw_and_update()

                if show_keyboard:
                    buttonTypeKeyboard     .draw_and_update()
                    buttonNav_typekeyb['l'].draw_and_update()
                    buttonNav_typekeyb['r'].draw_and_update()
                else:
                    buttonTypeKeyboard.draw_inactive()

                if self.init_mixer:
                    rangeSound.draw_and_update()
                    rangeMusic.draw_and_update()
                else:
                    rangeSound.draw_inactive()
                    rangeMusic.draw_inactive()

            else:
                buttonNav_lang['l']       .draw_inactive()
                buttonNav_lang['r']       .draw_inactive()
                buttonNav_langword['l']   .draw_inactive()
                buttonNav_langword['r']   .draw_inactive()
                buttonNav_wordlen['l']    .draw_inactive()
                buttonNav_wordlen['r']    .draw_inactive()
                buttonNav_changeguess['l'].draw_inactive()
                buttonNav_changeguess['r'].draw_inactive()
                buttonNav_theme['l']      .draw_inactive()
                buttonNav_theme['r']      .draw_inactive()
                buttonNav_geomarty['l']   .draw_inactive()
                buttonNav_geomarty['r']   .draw_inactive()
                buttonNav_fps['l']        .draw_inactive()
                buttonNav_fps['r']        .draw_inactive()
                buttonLang                .draw_inactive()
                buttonLangWord            .draw_inactive()
                buttonOxfordWord          .draw_inactive()
                buttonWordLen             .draw_inactive()
                buttonChangeGuess         .draw_inactive()
                buttonTheme               .draw_inactive()
                buttonTypeKeyboard        .draw_inactive()
                buttonShowKeyboard        .draw_inactive()
                buttonGeomatry            .draw_inactive()
                buttonFps                 .draw_inactive()
                buttonLogs                .draw_inactive()
                rangeSound                .draw_inactive()
                rangeMusic                .draw_inactive()

                if show_keyboard:
                    buttonNav_typekeyb['l'].draw_inactive()
                    buttonNav_typekeyb['r'].draw_inactive()

                if not buttonClose.button_event.ismousehover:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            label(LANG['languages']['title'],                            'group', navbar_rect.bottom + 10 * self.geomatry  - scroller.direction)
            label(LANG['languages']['label']['app-language'],            'label', navbar_rect.bottom + 55 * self.geomatry  - scroller.direction)
            label(LANG['languages']['label']['word-language'],           'label', navbar_rect.bottom + 115 * self.geomatry - scroller.direction)

            label(LANG['sounds']['title'],                               'group', navbar_rect.bottom + 190 * self.geomatry - scroller.direction)
            label(LANG['sounds']['label']['sound'],                      'label', navbar_rect.bottom + 242.5 * self.geomatry - scroller.direction)
            label(LANG['sounds']['label']['music'],                      'label', navbar_rect.bottom + 292.5 * self.geomatry - scroller.direction)

            label(LANG['game-rules']['title'],                           'group', navbar_rect.bottom + 370 * self.geomatry - scroller.direction)
            label(LANG['game-rules']['label']['only-in-dictionary'],     'label', navbar_rect.bottom + 425 * self.geomatry - scroller.direction)
            label(LANG['game-rules']['label']['word-length'],            'label', navbar_rect.bottom + 475 * self.geomatry - scroller.direction)
            label(LANG['game-rules']['label']['change-guess'],           'label', navbar_rect.bottom + 525 * self.geomatry - scroller.direction)

            label(LANG['display']['title'],                              'group', navbar_rect.bottom + 600 * self.geomatry - scroller.direction)
            label(LANG['display']['label']['app-theme'],                 'label', navbar_rect.bottom + 645 * self.geomatry - scroller.direction)
            label(LANG['display']['label']['keyboard-layout'],           'label', navbar_rect.bottom + 705 * self.geomatry - scroller.direction)
            label(LANG['display']['label']['show-keyboard'],             'label', navbar_rect.bottom + 760 * self.geomatry - scroller.direction)

            label(LANG['additional-settings']['title'],                  'group', navbar_rect.bottom + 840 * self.geomatry - scroller.direction)
            label(LANG['additional-settings']['label']['geomatry'],      'label', navbar_rect.bottom + 885 * self.geomatry - scroller.direction)
            label(LANG['additional-settings']['label']['fps'],           'label', navbar_rect.bottom + 945 * self.geomatry - scroller.direction)
            label(LANG['additional-settings']['label']['logs']['label'], 'label', navbar_rect.bottom + 1005 * self.geomatry - scroller.direction)

            for i, ln in enumerate(wrap_license):
                surface_text = font_license.render(ln, True, self.themes['settings']['text'])
                self.screen.blit(surface_text, surface_text.get_rect(left=background_rect.left + 5, top=1120 * self.geomatry + i * surface_text.get_height() - scroller.direction))

            pygame.draw.rect(self.screen, self.themes['settings']['navbar'], navbar_rect)

            buttonClose.draw_and_update()

            self.screen.blit(surface_title, surface_title.get_rect(center=navbar_rect.center))

            if rangeSound.button_event.value:
                sound_volume = rangeSound.button_event.range_value
            if rangeMusic.button_event.value:
                music_volume = rangeMusic.button_event.range_value

            if (clk := buttonLang.button_event.value) or buttonNav_lang['l'].button_event.value or buttonNav_lang['r'].button_event.value:
                self.handle_sound('click', 'play')
                index_lang = (index_lang + ternary(clk == 'l' or buttonNav_lang['r'].button_event.value, 1, -1)) % len(languages_id_list)

            elif (clk := buttonLangWord.button_event.value) or buttonNav_langword['l'].button_event.value or buttonNav_langword['r'].button_event.value:
                self.handle_sound('click', 'play')
                index_lang_word = (index_lang_word + ternary(clk == 'l' or buttonNav_langword['r'].button_event.value, 1, -1)) % len(languages_word_id_list)

            elif buttonOxfordWord.button_event.value:
                self.handle_sound('click', 'play')
                use_valid_word = not use_valid_word

            elif (clk := buttonWordLen.button_event.value) or buttonNav_wordlen['l'].button_event.value or buttonNav_wordlen['r'].button_event.value:
                self.handle_sound('click', 'play')
                word_length += ternary(clk == 'l' or buttonNav_wordlen['r'].button_event.value, 1, -1)

            elif (clk := buttonChangeGuess.button_event.value) or buttonNav_changeguess['l'].button_event.value or buttonNav_changeguess['r'].button_event.value:
                self.handle_sound('click', 'play')
                change_guess += ternary(clk == 'l' or buttonNav_changeguess['r'].button_event.value, 1, -1)

            elif (clk := buttonTheme.button_event.value) or buttonNav_theme['l'].button_event.value or buttonNav_theme['r'].button_event.value:
                self.handle_sound('click', 'play')
                index_theme = (index_theme + ternary(clk == 'l' or buttonNav_theme['r'].button_event.value, 1, -1)) % len(theme_id_list)

            elif (clk := buttonTypeKeyboard.button_event.value) or buttonNav_typekeyb['l'].button_event.value or buttonNav_typekeyb['r'].button_event.value:
                self.handle_sound('click', 'play')
                index_keyboard_layout = (index_keyboard_layout + ternary(clk == 'l' or buttonNav_typekeyb['r'].button_event.value, 1, -1)) % len(const.Keyboard.__all__)

            elif buttonShowKeyboard.button_event.value:
                self.handle_sound('click', 'play')
                show_keyboard = not show_keyboard

            elif (clk := buttonFps.button_event.value) or buttonNav_fps['l'].button_event.value or buttonNav_fps['r'].button_event.value:
                self.handle_sound('click', 'play')
                fps += ternary(clk == 'l' or buttonNav_fps['r'].button_event.value, const.STEP_FPS, -const.STEP_FPS)

            elif (clk := buttonGeomatry.button_event.value) or buttonNav_geomarty['l'].button_event.value or buttonNav_geomarty['r'].button_event.value:
                self.handle_sound('click', 'play')
                geomatry += ternary(clk == 'l' or buttonNav_geomarty['r'].button_event.value, 1, -1)

            if buttonClose.button_event.value:
                self.handle_sound('click', 'play')
                self.isshow_Settings = False

            elif buttonLogs.button_event.value:
                self.handle_sound('click', 'play')
                self.showLogs()

            if last_background_rect.width != background_rect.width:
                wrap_license         = wrap_text(font_license, self.__license__, background_rect.width - 10 * self.geomatry)
                last_background_rect = background_rect.copy()

            if last_configuration != [index_theme, index_keyboard_layout, sound_volume, music_volume, change_guess, word_length, fps, geomatry, index_lang, index_lang_word, use_valid_word, show_keyboard]:

                if [last_configuration[2], last_configuration[3]] == [sound_volume, music_volume]:

                    if word_length < const.MIN_WORD_LENGTH:
                        word_length = const.MAX_WORD_LENGTH
                    elif word_length > const.MAX_WORD_LENGTH:
                        word_length = const.MIN_WORD_LENGTH
                    elif change_guess < const.MIN_CHANGE_GUESS:
                        change_guess = const.MAX_CHANGE_GUESS(use_valid_word)
                    elif change_guess > const.MAX_CHANGE_GUESS(use_valid_word):
                        change_guess = const.MIN_CHANGE_GUESS
                    elif fps < const.MIN_FPS:
                        fps = const.MAX_FPS
                    elif fps > const.MAX_FPS:
                        fps = const.MIN_FPS
                    elif geomatry < int(const.MIN_GEOMATRY * 10):
                        geomatry = int(const.MAX_GEOMATRY * 10)
                    elif geomatry > int(const.MAX_GEOMATRY * 10):
                        geomatry = int(const.MIN_GEOMATRY * 10)

                    language        = languages_id_list     [index_lang]
                    theme           = theme_id_list         [index_theme]
                    language_word   = languages_word_id_list[index_lang_word]
                    keyboard_layout = const.Keyboard.__all__[index_keyboard_layout]

                self.settings['theme']           = self.theme           = theme
                self.settings['keyboard-layout'] = self.keyboard_layout = keyboard_layout
                self.settings['language-word']   = self.language_word   = language_word
                self.settings['language']        = self.language        = language
                self.settings['sound-volume']    = self.sound_volume    = sound_volume
                self.settings['music-volume']    = self.music_volume    = music_volume
                self.settings['change-guess']    = self.change_guess    = change_guess
                self.settings['word-length']     = self.word_length     = word_length
                self.settings['fps']             = self.fps             = fps
                self.settings['geomatry']        = self.geomatry        = geomatry / 10
                self.settings['use-valid-word']  = self.use_valid_word  = use_valid_word
                self.settings['show-keyboard']   = self.show_keyboard   = show_keyboard

                self.set_volume()

                if [last_configuration[0], last_configuration[7], last_configuration[8]] != [index_theme, geomatry, index_lang]:
                    scroller          .edit_param(katla=self)
                    self.scroller_tile.edit_param(katla=self)

                    self.languages  = self.validator_languages.load(self.language)
                    self.themes     = self.validator_themes   .load(self.theme)
                    LANG            = self.languages['settings']
                    self.num_format = NumberFormat(self.languages['exponents-number'], decimal_places=2, rounded=False, reach=(3, 'thousand'))
                    nfgeomatry      = NumberFormat(self.languages['exponents-number'], decimal_places=1, rounded=False, anchor_decimal_places=True, reach=(3, 'thousand'))

                    self.font_textbar      = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(20 * self.geomatry))
                    self.font_keyboard     = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(35 * self.geomatry))
                    self.font_katla        = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,      int(40 * self.geomatry))
                    self.font_coins        = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(35 * self.geomatry))
                    self.font_notification = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(30 * self.geomatry))
                    font_license           = pygame.font.Font(self.file.FONT_ROBOTO_MONO_BOLD, int(15 * self.geomatry))
                    label_group_font       = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,      int(32 * self.geomatry))
                    label_font             = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(25 * self.geomatry))
                    nav_font               = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(35 * self.geomatry))
                    font_title             = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,      int(35 * self.geomatry))
                    font1                  = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(30 * self.geomatry))

                    images                   = self.file.Images(self.theme)
                    self.image_backspace     = pygame.image.load(images.BACKSPACE)
                    self.image_enter         = pygame.image.load(images.ENTER)
                    self.image_question_mark = pygame.image.load(images.QUESTION_MARK)
                    self.image_stats         = pygame.image.load(images.STATS)
                    self.image_reset         = pygame.image.load(images.RESET)
                    self.image_settings      = pygame.image.load(images.SETTINGS)
                    self.image_coin_bag      = pygame.image.load(images.COIN_BAG)
                    self.image_lamp          = pygame.image.load(images.LAMP)
                    self.image_keyboard      = pygame.image.load(images.KEYBOARD)
                    self.image_hammer        = pygame.image.load(images.HAMMER)
                    self.image_close         = pygame.image.load(images.CLOSE)
                    self.image_right_arrow   = pygame.image.load(images.RIGHT_ARROW)
                    self.image_check         = pygame.image.load(images.CHECK)

                    font_license_size = font_license.size(const.HELLO)

                    buttonClose.edit_param(image=self.image_close)
                    buttonLang .edit_param(
                        font          = label_font,
                        outline_size  = 4 * self.geomatry,
                        text_color    = button_color(*[self.themes['settings']['text'] for _ in range(3)]),
                        color         = button_color(
                            self.themes['settings']['button']['set']['inactive'],
                            self.themes['settings']['button']['set']['active'],
                            self.themes['settings']['button']['set']['hover']
                        ),
                        outline_color = button_color(*[self.themes['settings']['outline'] for _ in range(3)]),
                        click_speed   = 500
                    )
                    button_edit(buttonOxfordWord,           buttonLang, {'text': '', 'only_click': 'l', 'click_speed': 100})
                    button_edit(buttonWordLen,              buttonLang, {'font': font1, 'click_speed': 100})
                    button_edit(buttonTheme,                buttonLang, {'click_speed': 100})
                    button_edit(buttonLangWord,             buttonLang)
                    button_edit(buttonChangeGuess,          buttonWordLen)
                    button_edit(buttonTypeKeyboard,         buttonTheme)
                    button_edit(buttonShowKeyboard,         buttonOxfordWord)
                    button_edit(buttonGeomatry,             buttonTheme)
                    button_edit(buttonFps,                  buttonTheme)
                    button_edit(buttonLogs,                 buttonTheme)
                    button_edit(buttonNav_lang['l'],        buttonLang,          {'only_click': 'l', 'text': '<', 'font': nav_font})
                    button_edit(buttonNav_lang['r'],        buttonNav_lang['l'], {'text': '>'})
                    button_edit(buttonNav_langword['l'],    buttonNav_lang['l'])
                    button_edit(buttonNav_langword['r'],    buttonNav_lang['r'])
                    button_edit(buttonNav_wordlen['l'],     buttonNav_langword['l'], {'click_speed': 100})
                    button_edit(buttonNav_wordlen['r'],     buttonNav_langword['r'], {'click_speed': 100})
                    button_edit(buttonNav_changeguess['l'], buttonNav_wordlen['l'])
                    button_edit(buttonNav_changeguess['r'], buttonNav_wordlen['r'])
                    button_edit(buttonNav_theme['l'],       buttonNav_wordlen['l'])
                    button_edit(buttonNav_theme['r'],       buttonNav_wordlen['r'])
                    button_edit(buttonNav_typekeyb['l'],    buttonNav_wordlen['l'])
                    button_edit(buttonNav_typekeyb['r'],    buttonNav_wordlen['r'])
                    button_edit(buttonNav_geomarty['l'],    buttonNav_wordlen['l'])
                    button_edit(buttonNav_geomarty['r'],    buttonNav_wordlen['r'])
                    button_edit(buttonNav_fps['l'],         buttonNav_wordlen['l'])
                    button_edit(buttonNav_fps['r'],         buttonNav_wordlen['r'])

                    surface_title = font_title.render(LANG['title'], True, self.themes['settings']['text'])
                    self.buttonKeyboard = Button(
                        surface_screen = self.screen,
                        rect           = self.buttonKeyboard.rect,
                        text_color     = button_color(*[self.themes['keyboard']['text'] for _ in range(3)]),
                        click_speed    = 0,
                    )
                    self.buttonOutlineKeyboard = self.buttonKeyboard.copy(
                        color = button_color(
                            self.themes['keyboard']['button']['outline']['inactive'],
                            self.themes['keyboard']['button']['outline']['active'],
                            'black'
                        )
                    )
                    self.buttonHowToPlay = Button(
                        surface_screen = self.screen,
                        rect           = self.buttonHowToPlay.rect,
                        hide           = True,
                        image          = self.image_question_mark,
                        click_speed    = 0,
                    )
                    self.buttonStats        = self.buttonHowToPlay.copy(image=self.image_stats)
                    self.buttonAutoWrite    = self.buttonHowToPlay.copy(image=self.image_right_arrow, click_speed=250)
                    self.buttonReset        = self.buttonHowToPlay.copy(image=self.image_reset,       click_speed=500)
                    self.buttonSettings     = self.buttonHowToPlay.copy(image=self.image_settings)
                    self.buttonDailyCoins   = self.buttonHowToPlay.copy(image=self.image_coin_bag)
                    self.buttonLetterHint   = self.buttonHowToPlay.copy(image=self.image_lamp)
                    self.buttonKeyboardHint = self.buttonHowToPlay.copy(image=self.image_keyboard)
                    self.buttonDeletedEntry = self.buttonHowToPlay.copy(image=self.image_hammer)
                    rangeSound.edit_param(
                        thumb_color    = button_color(
                            self.themes['settings']['range']['thumb']['inactive'],
                            self.themes['settings']['range']['thumb']['active'],
                            self.themes['settings']['range']['thumb']['hover']
                        ),
                        track_color    = button_color(
                            self.themes['settings']['range']['track']['inactive'],
                            self.themes['settings']['range']['track']['active'],
                            self.themes['settings']['range']['track']['hover']
                        ),
                        track_fill_color = button_color(
                            self.themes['settings']['range']['track-fill']['inactive'],
                            self.themes['settings']['range']['track-fill']['active'],
                            self.themes['settings']['range']['track-fill']['hover']
                        )
                    )
                    rangeMusic.edit_param(
                        thumb_color    = button_color(
                            self.themes['settings']['range']['thumb']['inactive'],
                            self.themes['settings']['range']['thumb']['active'],
                            self.themes['settings']['range']['thumb']['hover']
                        ),
                        track_color    = button_color(
                            self.themes['settings']['range']['track']['inactive'],
                            self.themes['settings']['range']['track']['active'],
                            self.themes['settings']['range']['track']['hover']
                        ),
                        track_fill_color = button_color(
                            self.themes['settings']['range']['track-fill']['inactive'],
                            self.themes['settings']['range']['track-fill']['active'],
                            self.themes['settings']['range']['track-fill']['hover']
                        )
                    )

                    wrap_license      = wrap_text(font_license, self.__license__, background_rect.width - 10 * self.geomatry)
                    self.notification = Notification(self)
                    self.popup        = Popup(self)

                if last_configuration[9] != index_lang_word:
                    self.validator_word_dictionary = WordsValidator(language_word)
                    self.word_dictionary           = self.validator_word_dictionary.load_and_validation()

                if [change_guess, word_length, index_lang_word, use_valid_word] != [last_configuration[4], last_configuration[5], last_configuration[9], last_configuration[10]]:
                    self.reset()

                last_configuration = [index_theme, index_keyboard_layout, sound_volume, music_volume, change_guess, word_length, fps, geomatry, index_lang, index_lang_word, use_valid_word, show_keyboard]

            pygame.display.flip()

            self.clock.tick(self.fps)

        if first_configuration != last_configuration:
            self.validator_settings.encrypt_data(self.settings)

    def Appmainloop(self) -> None:
        last_time_backspace = self.get_tick()
        pressed_backspace   = False
        hold_backspace      = False
        pressed_key         = False
        last_letter         = None

        self.handle_sound('backsound', 'play')

        while self.running:

            keyboard_letter = None
            shortcut_key    = None
            can_inputed     = not (self.isshow_Lose or self.isshow_Win or self.last_time_close_settings + 0.5 > self.get_tick())

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                self.scroller_tile.event(event)

                self.handle_screen_resize(event)

                self.buttonHowToPlay   .handle_event(event)
                self.buttonStats       .handle_event(event)
                self.buttonAutoWrite   .handle_event(event)
                self.buttonSettings    .handle_event(event)
                self.buttonReset       .handle_event(event)
                self.buttonDailyCoins  .handle_event(event)
                self.buttonLetterHint  .handle_event(event)
                self.buttonKeyboardHint.handle_event(event)
                self.buttonDeletedEntry.handle_event(event)

                typeinput, getinput = self.input_event(event)

                if getinput and typeinput == 'key':
                    keyboard_letter = getinput
                elif getinput and typeinput == 'shortcut':
                    shortcut_key = getinput

            sizescreen = self.screen.get_size  ()
            mouse_pos  = pygame.mouse.get_pos  ()
            getkeys    = pygame.key.get_pressed()

            barTop_rect = pygame.Rect(
                const.math.get_center(sizescreen[0], sizescreen[0] - 10),
                5 * self.geomatry,
                sizescreen[0] - 10,
                115 * self.geomatry
            )

            self.scroller_tile.min_max_scrolled = (-((self.size_tile + self.margin_tile) * (self.change_guess - 1) - self.margin_tile / 2), sizescreen[1] - (self.size_tile + self.margin_tile / 2))

            self.scroller_tile.update(anchor=(self.boardRect_keyboard.collidepoint(*mouse_pos) if self.show_keyboard else False) or barTop_rect.collidepoint(*mouse_pos))

            set_cursor_buttons(
                self.buttonHowToPlay,
                self.buttonStats,
                self.buttonAutoWrite,
                self.buttonReset,
                self.buttonSettings,
                self.buttonDailyCoins,
                self.buttonLetterHint,
                self.buttonKeyboardHint,
                self.buttonDeletedEntry,
                active_cursor   = pygame.SYSTEM_CURSOR_HAND,
                inactive_cursor = pygame.SYSTEM_CURSOR_ARROW
            )

            self.screen.fill(self.themes['screen'])

            self.showTile   ()
            self.showBarMenu()
            click_detected, keyboard_visual_letter, letter_hovered = self.showKeyboard(letter_hovered=last_letter)
            self.showTextBar()

            self.handle_notification()
            self.handle_popup       (shortcut_key, can_inputed)

            if self.last_geomatry != self.geomatry and not self.threadgif.is_alive():
                size                      = 500 * self.geomatry
                self.last_geomatry        = self.geomatry
                self.confetti_rect.width  = size
                self.confetti_rect.height = size

                self.threadgif = Thread(target=self.gif_win.convert_gif)
                self.threadgif.start()

            pygame.display.flip()

            self.clock.tick(self.fps)

            get_k_backspace = getkeys[pygame.K_BACKSPACE]

            if (get_k_backspace or click_detected) and can_inputed:
                current_tick = self.get_tick()

                if not pressed_backspace:
                    last_time_backspace = current_tick

                pressed_backspace = True

                if last_time_backspace + 0.5 <= current_tick and (get_k_backspace or keyboard_visual_letter == const.BACKSPACE) and self.input_point[0] != 0:
                    hold_backspace = True
                    self.handle_input(const.BACKSPACE)
                    continue

            else:
                pressed_backspace = False

            if click_detected and not pressed_key and can_inputed:
                last_letter = keyboard_visual_letter
                pressed_key = True

            elif not click_detected and pressed_key and can_inputed:
                if letter_hovered and not hold_backspace:
                    self.handle_input(last_letter)

                last_letter = None
                pressed_key = False

            elif keyboard_letter and can_inputed:
                self.handle_input(keyboard_letter)

            elif hold_backspace and not pressed_backspace:
                hold_backspace = False

        pygame.quit()

def main() -> int:
    try:

        logs.log('Test permission')

        t = const.test_read_write_delete(logs)

        if t[1] is not None:
            logs.log(f'Test completed with errors -> {type(t[1]).__name__}', 'warn')
            raise t[1]

        logs.log('Test completed with no errors')

        katla = Katla()
        logs.log('\n' + str(katla) + '\n', 'license')

        if katla.running and pygame.get_init():
            katla.Appmainloop()
            return 0

        return 1

    except PermissionError:
        pygame.quit()
        msg = f'PERMISSION ERROR: Unable to save / write data due to administrator issues. Run Katla application with administrator or not and move application folder to environment without needing administrator?'

        logs.log(msg, 'warn')
        runasadmin = messagebox.askyesnocancel('Katla - Permission error', msg)
        if runasadmin:

            try:

                if not isUserAdmin():
                    runAsAdmin()
                else:
                    main()

            except Exception as e:
                msgdenied = f'Failed to run Katla as administrator. Please try again later. {str(e).capitalize()}'

                logs.log(msgdenied, 'error')
                messagebox.showerror('Katla - Access denied', msgdenied)
                return -2

        else:
            logs.log('Administrator request denied', 'error')
            return -1

    except Exception as e:
        pygame.quit()
        msg = f'EXCEPTION ERROR: {type(e).__name__}: {e}'

        logs.log(msg, 'error')
        messagebox.showerror('Katla - Exception unexpected', msg)
        raise

if __name__ == '__main__':
    exitcode = main()
    print("ExitCode: " + (f'\033[33m{exitcode}\033[0m' if exitcode != 0 else '0'))
    del exitcode
else:
    raise Exception("__name__ is not eq <str '__main__'>")