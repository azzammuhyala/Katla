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

--[ Works pretty well on Windows platforms and on Python version 1.10 and above ]--
"""

import pygame
from random                                 import choice
from threading                              import Thread
from tkinter                                import messagebox
from string                                 import ascii_uppercase
from datetime                               import datetime, timedelta
from pyuac                                  import isUserAdmin, runAsAdmin
from components.module.wraptext_pygame      import wrap_text
from components.module.format_number        import NumberFormat
from components.module.pygamegif            import AnimatedGIF
from components.module.pygamebutton         import button_color, Button, Range, SetAllCursorButtons
from components.katla_module                import constants as const
from components.katla_module.scroller       import ScrollerY
from components.katla_module.popup          import Popup, Notification
from components.katla_module.json_validator import Languages, WordsValidator, SettingsValidator, GameDataValidator

class Katla:

    """
    # Katla - pygame - Python 3

    Supported software - Perangkat lunak yang didukung:
    - Android: [APP] pydroid3
    - [OS -> Windows, ...etc] Python: [VERSION] 3.10+

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
        const.os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.init_mixer = False

        pygame.init()
        pygame.font.init()

        try:
            pygame.mixer.init()
            self.init_mixer = True
        except:
            self.init_mixer = False

        self.languages_object    = Languages()
        self.validator_settings  = SettingsValidator()
        self.validator_game_data = GameDataValidator()

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

        self.validator_word_dictionary = WordsValidator(self.language_word)
        self.word_dictionary           = self.validator_word_dictionary.load_and_validation()
        self.languages                 = self.languages_object         .load(self.language)
        self.num_format                = NumberFormat(self.languages['exponents-number'], decimal_places=2, rounded=False)
        self.scroller_tile             = ScrollerY(self, (0, 130 * self.geomatry), reversed=(True, True, True))
        self.scroller_tile.direction   = 130 * self.geomatry

        self.keyboards                : dict[str, const.KeyboardList] = {key: getattr(const.Keyboard, key) for key in const.LiteralConst.all_keyboard}
        self.running                  : bool                 = True
        self.coins                    : const.Number         = self.game_data['coins']
        self.play_lose_or_win         : int                  = 0
        self.last_geomatry            : int                  = self.geomatry
        self.guess_count              : int                  = self.change_guess
        self.words_list               : list[str]            = [word.upper() for word in self.word_dictionary[f'length-{self.word_length}']]
        self.feedback_history         : list[const.Feedback] = []
        self.feedback_history_keyboard: list[const.Feedback] = []
        self.hint_tile                : list[str]            = []
        self.hint_keyboard            : list[str]            = []
        self.correct_char_keyboard    : list[str]            = []
        self.correct_char_tile        : list[str]            = ['not-inputed' for _ in range(self.word_length)]
        self.input_history            : list[list[str]]      = [[]]
        self.input_point              : list[int, int]       = [0, 0]
        self.selected_word            : str                  = choice(self.words_list)
        self.last_word_input          : str                  = ''
        self.keyboard_feedback        : dict[str, str]       = {char: 'not-inputed' for line in self.keyboards[self.keyboard_layout] for char in line}

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

        self.timeanimation_notification = self.get_time()
        self.timeanimation_popup        = self.get_time()

        self.dinfo          = pygame.display.Info()
        self.minsize_screen = (550, 700)
        self.maxsize_screen = (self.dinfo.current_w - 75, self.dinfo.current_h - 50)
        init_screen         = self.settings['screen-size']

        if init_screen == 'FULL':
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        elif init_screen[0] < self.minsize_screen[0] or init_screen[1] < self.minsize_screen[1]:
            self.screen = pygame.display.set_mode(self.minsize_screen, pygame.RESIZABLE)

        elif init_screen[0] > self.maxsize_screen[0] or init_screen[1] > self.maxsize_screen[1]:
            init_screen[0] = self.maxsize_screen[0] if init_screen[0] > self.maxsize_screen[0] else init_screen[0]
            init_screen[1] = self.maxsize_screen[1] if init_screen[1] > self.maxsize_screen[1] else init_screen[1]
            self.screen    = pygame.display.set_mode(init_screen, pygame.RESIZABLE)

        else:
            self.screen = pygame.display.set_mode(init_screen, pygame.RESIZABLE)

        size = 500 * self.geomatry

        self.boardRect_keyboard = pygame.Rect(0, 0, 0, 0)
        self.confetti_rect      = pygame.Rect(const.math.get_center(self.screen.get_width(), size), self.screen.get_height() - size, size, size)

        self.file   = const.File()
        self.colors = const.Color(self.theme)
        images      = self.file.Images(self.theme)

        self.image_icon = pygame.image.load(images.ICON)

        self.fullscreen_attr          : dict[str, const.Any]
        self.gif_confetti             : AnimatedGIF
        self.sound_music              : pygame.mixer.Sound
        self.sound_key                : pygame.mixer.Sound
        self.sound_key_backspace_enter: pygame.mixer.Sound
        self.sound_button_click       : pygame.mixer.Sound
        self.sound_win                : pygame.mixer.Sound
        self.sound_lose               : pygame.mixer.Sound

        def load_assets() -> None:
            self.fullscreen_attr = {'full': init_screen == 'FULL', 'last-size': list(self.screen.get_size() if init_screen != 'FULL' else self.maxsize_screen)}

            self.gif_confetti        = AnimatedGIF(images.WINS_GIF, self.confetti_rect, 25)
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
                self.sound_music               = pygame.mixer.Sound(self.file.SOUND_MUSIC)
                self.sound_key                 = pygame.mixer.Sound(self.file.SOUND_KEY)
                self.sound_key_backspace_enter = pygame.mixer.Sound(self.file.SOUND_KEY_BACKSPACE_ENTER)
                self.sound_button_click        = pygame.mixer.Sound(self.file.SOUND_BUTTON_CLICK)
                self.sound_win                 = pygame.mixer.Sound(self.file.SOUND_WIN)
                self.sound_lose                = pygame.mixer.Sound(self.file.SOUND_LOSE)

            self.margin_tile    = 10 * self.geomatry
            self.size_tile      = 80 * self.geomatry
            self.last_size_tile = self.size_tile

            self.font_tile         = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(self.size_tile))
            self.font_textbar      = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(20 * self.geomatry))
            self.font_keyboard     = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(35 * self.geomatry))
            self.font_katla        = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,   int(40 * self.geomatry))
            self.font_notification = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(30 * self.geomatry))
            self.font_coins        = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(35 * self.geomatry))

            self.buttonKeyboard = Button(
                surface_screen = self.screen,
                text_color     = button_color(*[self.colors.keyboard['text'] for _ in range(3)]),
                click_speed    = 0
            )
            self.buttonOutlineKeyboard = self.buttonKeyboard.copy(
                color = button_color(
                    self.colors.keyboard['button']['outline']['inactive'],
                    self.colors.keyboard['button']['outline']['active']
                )
            )
            self.buttonhowToPlay = Button(
                surface_screen = self.screen,
                color          = button_color(*[self.colors.barMenu['background'] for _ in range(3)]),
                click_speed    = 0
            )
            self.buttonStats        = self.buttonhowToPlay.copy()
            self.buttonAutoWrite    = self.buttonhowToPlay.copy(click_speed=250)
            self.buttonReset        = self.buttonhowToPlay.copy(click_speed=500)
            self.buttonSettings     = self.buttonhowToPlay.copy()
            self.buttonDailyCoins   = self.buttonhowToPlay.copy()
            self.buttonLetterHint   = self.buttonhowToPlay.copy()
            self.buttonKeyboardHint = self.buttonhowToPlay.copy()
            self.buttonDeletedEntry = self.buttonhowToPlay.copy()

            self.notification = Notification(
                self,
                static_time    = 3,
                move_down_time = 0.25,
                move_up_time   = 0.25,
                color          = self.colors.notification['default']['background'],
                color_outline  = self.colors.notification['default']['outline'],
                color_text     = self.colors.notification['default']['text']
            )
            self.popup = Popup(self)

        thread_load = Thread(target=load_assets)

        icon = pygame.transform.scale(self.image_icon, (100 * self.geomatry, 100 * self.geomatry))

        pygame.display.set_icon(self.image_icon)
        pygame.display.set_caption("Katla - Loading assets...")

        try:
            thread_load.start()
            runwait = True

            while runwait:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        runwait      = False
                        self.running = False

                        thread_load.join(.01)

                    self.handle_screen_resize(event)

                if not thread_load.is_alive():
                    runwait = False

                self.screen.fill(self.colors.screen)

                self.screen.blit(icon, (const.math.get_center(self.screen.get_width(), icon.get_width()), const.math.get_center(self.screen.get_height(), icon.get_height())))

                pygame.display.flip()

            self.threadgif = Thread(target=self.gif_confetti.convert_gif)
            self.clock = pygame.time.Clock()

            pygame.display.set_caption("Katla")

        except Exception as e:

            if not self.running:
                pass
            else:
                const.warn(str(e))

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
        self.correct_char_tile        = ['not-inputed' for _ in range(self.word_length)]
        self.words_list               = [word.upper() for word in self.word_dictionary[f'length-{self.word_length}']]
        self.input_history            = [[]]
        self.input_point              = [0, 0]
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
        last_claim_time     = self.game_data['prize-claim-time'].split('/')
        last_time_int       = [int(timeday) for timeday in last_claim_time]
        last_claim_datetime = datetime(last_time_int[5], last_time_int[4], last_time_int[3], last_time_int[0], last_time_int[1], last_time_int[2])
        time_difference     = datetime.now() - last_claim_datetime
        countdown           = timedelta(days=1) - time_difference if time_difference < timedelta(days=1) else timedelta(0)
        return True if countdown == timedelta(0) else f"{countdown.seconds // 3600:02}:{(countdown.seconds % 3600) // 60:02}:{(countdown.seconds % 3600) % 60:02}"

    def get_time(self) -> float:
        return pygame.time.get_ticks() / 1000

    def set_notification_default(self) -> None:
        self.notification.edit_param(
            start_time    = self.timeanimation_notification,
            static_time   = 3,
            color         = self.colors.notification['default']['background'],
            color_outline = self.colors.notification['default']['outline'],
            color_text    = self.colors.notification['default']['text']
        )

    def set_volume(self) -> None:
        if self.init_mixer:
            self.sound_music              .set_volume(self.music_volume / 100)
            self.sound_key                .set_volume(self.sound_volume / 100)
            self.sound_key_backspace_enter.set_volume(self.sound_volume / 100)
            self.sound_button_click       .set_volume(self.sound_volume / 100)
            self.sound_win                .set_volume(self.sound_volume / 100)
            self.sound_lose               .set_volume(self.sound_volume / 100)

    def save_game(self, win: bool = False, line: str = '', lose: bool = False, prize_taken: bool = False, hint_coins_price: int | bool = False) -> None:
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

        self.update_keyboard_feedback()
        self.validator_game_data.encrypt_data(self.game_data)

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

    def update_pos_gif(self) -> None:
        size = 500 * self.geomatry

        self.confetti_rect.left = const.math.get_center(self.screen.get_width(), size)
        self.confetti_rect.top  = self.screen.get_height() - size

    def input_event(self, event: pygame.event.Event) -> tuple[str | None, str | None]:
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
            elif key == pygame.K_BACKSPACE: return 'key', '\b'
            elif key == pygame.K_RETURN:    return 'key', '\n'

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

                self.update_pos_gif()

            elif key == pygame.K_TAB:

                if self.fullscreen_attr['full']:
                    self.reset_isshow()
                    self.isshow_Unfullscreen        = True
                    self.timeanimation_notification = self.get_time()

                else:
                    self.screen                       = pygame.display.set_mode(self.minsize_screen, pygame.RESIZABLE)
                    self.settings['screen-size']      = list(self.minsize_screen)
                    self.fullscreen_attr['last-size'] = list(self.minsize_screen)

                    self.update_pos_gif()

                    self.validator_settings.encrypt_data(self.settings)

        elif event.type == pygame.VIDEORESIZE and not self.fullscreen_attr['full']:
            x, y        = event.size
            self.screen = pygame.display.set_mode(
                (
                    max(self.minsize_screen[0], x),
                    max(self.minsize_screen[1], y)
                ), pygame.RESIZABLE
            )
            screen_size = list(self.screen.get_size())

            if screen_size[0] > self.maxsize_screen[0]:
                screen_size[0] = self.maxsize_screen[0]
            if screen_size[1] > self.maxsize_screen[1]:
                screen_size[1] = self.maxsize_screen[1]

            self.settings['screen-size']      = screen_size
            self.fullscreen_attr['last-size'] = screen_size

            self.update_pos_gif()

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
            else:
                ValueError('do:', do)

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
            else:
                ValueError('stype:', stype)

    def handle_input(self, char: str) -> None:
        ln     = self.input_point[1]
        len_ln = len(self.input_history[ln])

        self.showKeyboard(char, True)
        pygame.display.flip()
        pygame.time.delay(25)

        if char in '\b\n':
            self.handle_sound('key-bn', 'play')

        if char == '\b':

            if len_ln > 0:
                self.input_history[ln].pop(-1)

                if len_ln != self.word_length:
                    self.input_point[0] -= 1

        elif char == '\n':

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
                    self.timeanimation_notification = self.get_time()

                if guess_word == self.selected_word:
                    self.reset_isshow()
                    self.coins                     += 1
                    self.last_word_input            = guess_word
                    self.isshow_Win                 = True
                    self.timeanimation_notification = self.get_time()
                    self.save_game(win=True, line=str(ln + 1))

                elif self.guess_count <= 0:
                    self.reset_isshow()
                    self.last_word_input            = guess_word
                    self.isshow_Lose                = True
                    self.timeanimation_notification = self.get_time()
                    self.save_game(lose=True)

            else:
                self.reset_isshow()
                self.isshow_NotEnoughLength     = True
                self.timeanimation_notification = self.get_time()

        elif char in ascii_uppercase:
            self.handle_sound('key', 'play')

            if len_ln < self.word_length:
                self.input_history[ln].append(char)

                if self.input_point[0] < self.word_length - 1:
                    self.input_point[0] += 1

        self.update_correct_tile()

    def handle_notification(self) -> None:
        if any([
                self.isshow_NotInDictionary,
                self.isshow_NotEnoughLength,
                self.isshow_AllTileHintsProvided,
                self.isshow_AllKeyboardHintsProvided,
                self.isshow_TileIsEmpty,
                self.isshow_Reset,
                self.isshow_Win,
                self.isshow_Lose,
                self.isshow_Unfullscreen
            ]):

            LANG = self.languages['notification']

            if self.isshow_Win:
                self.notification.edit_param(
                    start_time     = self.timeanimation_notification,
                    static_time    = 5,
                    text           = LANG['win'],
                    color          = self.colors.notification['win']['background'],
                    color_outline  = self.colors.notification['win']['outline'],
                    color_text     = self.colors.notification['win']['text']
                )

                if self.play_lose_or_win != 2:
                    self.play_lose_or_win = 1
                    self.gif_confetti.reset_frame()

                if self.play_lose_or_win == 1:
                    self.handle_sound('win', 'play')
                    self.play_lose_or_win = 2

                self.gif_confetti.draw_and_update(self.screen)

                if self.notification():
                    self.reset()
                    self.play_lose_or_win = 0

            elif self.isshow_Lose:
                self.notification.edit_param(
                    start_time     = self.timeanimation_notification,
                    static_time    = 5,
                    text           = LANG['lose'].replace('<WORD>', self.selected_word, 1),
                    color          = self.colors.notification['lose']['background'],
                    color_outline  = self.colors.notification['lose']['outline'],
                    color_text     = self.colors.notification['lose']['text']
                )

                if self.play_lose_or_win != 2:
                    self.play_lose_or_win = 1

                if self.play_lose_or_win == 1:
                    self.handle_sound('lose', 'play')
                    self.play_lose_or_win = 2

                if self.notification():
                    self.reset()
                    self.play_lose_or_win = 0

            elif self.isshow_NotInDictionary:
                self.set_notification_default()
                self.notification.edit_param(text=LANG['not-in-dictionary'].replace('<WORD>', self.last_word_input, 1))
                if self.notification():
                    self.isshow_NotInDictionary = False

            elif self.isshow_NotEnoughLength:
                self.set_notification_default()
                self.notification.edit_param(text=LANG['less-letter-length'])
                if self.notification():
                    self.isshow_NotEnoughLength = False

            elif self.isshow_AllTileHintsProvided:
                self.set_notification_default()
                self.notification.edit_param(text=LANG['tile-hint-provided'])
                if self.notification():
                    self.isshow_AllTileHintsProvided = False

            elif self.isshow_AllKeyboardHintsProvided:
                self.set_notification_default()
                self.notification.edit_param(text=LANG['keyboard-hint-provided'])
                if self.notification():
                    self.isshow_AllKeyboardHintsProvided = False

            elif self.isshow_TileIsEmpty:
                self.set_notification_default()
                self.notification.edit_param(text=LANG['tile-empty'])
                if self.notification():
                    self.isshow_TileIsEmpty = False

            elif self.isshow_Reset:
                self.set_notification_default()
                self.notification.edit_param(text=LANG['reset'])
                if self.notification():
                    self.isshow_Reset = False

            elif self.isshow_Unfullscreen:
                self.set_notification_default()
                self.notification.edit_param(text=LANG['unfullscreen'])
                if self.notification():
                    self.isshow_Unfullscreen = False

    def showTextBar(self) -> None:
        LANG  = self.languages['text-bar']
        hscrn = self.screen.get_height()
        text  = self.font_textbar.render(
            '{} | {} | {} | {}'
                .format(
                    self.__label_version__,
                    LANG['word']               .replace('<WORD-ID>',    self.language_word.upper(), 1),
                    LANG['valid-word']['label'].replace('<VALID-WORD>', LANG['valid-word'][str(self.use_valid_word).lower()], 1),
                    LANG['fps']                .replace('<FPS>',        self.num_format.parse(self.clock.get_fps()), 1)
                ),
            True, self.colors.barMenu['text'], self.colors.barMenu['background']
        )

        text.set_alpha(200)

        self.screen.blit(text, text.get_rect(
            left = const.math.get_center(self.screen.get_width(), text.get_width()),
            top  = hscrn - text.get_height() - const.math.get_center(hscrn - self.boardRect_keyboard.bottom, text.get_height())
        ))

    def showKeyboard(self, letter_typing: str | None = None, justshow: bool = False) -> tuple[bool, str | None]:
        inputDetected           = (False, None)
        margin                  = 10
        buttonSize              = (50 * self.geomatry, 70 * self.geomatry)
        totalButtonKey          = lambda keys_total, xy : keys_total * buttonSize[xy] + margin * (keys_total - 1)
        marginlr                = 40 * self.geomatry
        keyboards               = self.keyboards[self.keyboard_layout]
        img_backspace           = pygame.transform.scale(self.image_backspace, ((buttonSize[0] + buttonSize[0] / 2) / 1.8, buttonSize[1] / 2))
        img_enter               = pygame.transform.scale(self.image_enter,     img_backspace.get_size())
        self.boardRect_keyboard = pygame.Rect(
            (self.screen.get_width()  - marginlr - totalButtonKey(10, 0)) / 2,
            (self.screen.get_height() - marginlr - totalButtonKey(3, 1)) - 60 * self.geomatry,
            marginlr + totalButtonKey(10, 0),
            marginlr + totalButtonKey(3, 1)
        )
        backspace_and_enter_left_pos = {
            '\b': marginlr / 2,
            '\n': self.boardRect_keyboard.width - marginlr / 2 - (buttonSize[0] + buttonSize[0] / 2 + margin / 2)
        }

        pygame.draw.rect(self.screen, self.colors.keyboard['background'], self.boardRect_keyboard)

        for row, line in enumerate(keyboards):
            for col, letter in enumerate(line):

                keyRect = pygame.Rect(
                    self.boardRect_keyboard.left + (const.math.get_center(self.boardRect_keyboard.width, totalButtonKey(len(keyboards[row]), 0)) + (col * (buttonSize[0] + margin)) if letter not in ['\b', '\n'] else backspace_and_enter_left_pos[letter]),
                    self.boardRect_keyboard.top + const.math.get_center(self.boardRect_keyboard.height, totalButtonKey(3, 1)) + (row * (buttonSize[1] + margin)),
                    buttonSize[0] + buttonSize[0] / 2 + margin / 2 if letter in '\b\n' else buttonSize[0],
                    buttonSize[1]
                )

                color       = self.keyboard_feedback[letter.upper()]
                mousePos    = pygame.mouse.get_pos()
                isMouseOver = keyRect.collidepoint(*mousePos)
                button_keyboard_color = button_color(
                    inactive_color = self.colors.keyboard['button'][color]['inactive'],
                    active_color   = self.colors.keyboard['button'][color]['active'],
                    hover_color    = self.colors.keyboard['button'][color]['hover']
                )

                self.buttonOutlineKeyboard.edit_param(rect=const.math.Rect_outline(keyRect, 4))

                if letter_typing == letter:
                    self.buttonOutlineKeyboard.draw_active()

                if isMouseOver and not justshow:
                    self.buttonOutlineKeyboard.draw_active()
                    self.buttonKeyboard.edit_param(
                        rect  = keyRect,
                        text  = letter if letter not in '\b\n' else '',
                        font  = self.font_keyboard,
                        color = button_keyboard_color
                    )
                    self.buttonKeyboard.draw_and_update()

                    if self.buttonKeyboard.button_event.value:
                        inputDetected = (True, letter)

                else:
                    if letter_typing != letter:
                        self.buttonOutlineKeyboard.draw_inactive()

                    self.buttonKeyboard.edit_param(
                        rect  = keyRect,
                        text  = letter if letter not in '\b\n' else '',
                        font  = self.font_keyboard,
                        color = button_keyboard_color
                    )
                    self.buttonKeyboard.draw_inactive()

                if letter == '\b':
                    self.screen.blit(img_backspace, img_backspace.get_rect(center=keyRect.center))
                elif letter == '\n':
                    self.screen.blit(img_enter,     img_enter    .get_rect(center=keyRect.center))

        return inputDetected

    def showTile(self, justshow: bool = False) -> None:
        self.margin_tile = 10
        self.size_tile   = 80 * self.geomatry

        if self.word_length * self.size_tile + self.margin_tile * (self.word_length - 1) > self.screen.get_width() - self.margin_tile * 2:
            self.size_tile = (self.screen.get_width() - self.margin_tile) / self.word_length - self.margin_tile

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
                    (self.screen.get_width() - self.word_length * (self.size_tile + self.margin_tile) + self.margin_tile) / 2 + col * (self.size_tile + self.margin_tile),
                    (row * (self.size_tile + self.margin_tile)) + self.scroller_tile.direction,
                    self.size_tile,
                    self.size_tile
                )

                pygame.draw.rect(self.screen, self.colors.boxEntryTile['box']['outline']['point-active' if [col, row] == self.input_point and int(self.get_time() * 2) % 2 == 0 and not (justshow or self.isshow_Win or self.isshow_Lose) else 'point-inactive'], const.math.Rect_outline(tile_rect, 4))
                pygame.draw.rect(self.screen, self.colors.boxEntryTile['box'][color], tile_rect)

                if letter is not None:
                    showLetter = self.font_tile.render(letter, True, self.colors.boxEntryTile['text'])
                    self.screen.blit(showLetter, showLetter.get_rect(center=tile_rect.center))

    def showBarMenu(self, justshow: bool = False) -> None:
        barTop_rect                 = pygame.Rect((self.screen.get_width() - (self.screen.get_width() - 10)) / 2, 5 * self.geomatry,                      self.screen.get_width() - 10, 60 * self.geomatry)
        barBottom_rect              = pygame.Rect(barTop_rect.left,                                               barTop_rect.bottom + 5 * self.geomatry, barTop_rect.width,            50 * self.geomatry)
        size_button_and_icon_top    = barTop_rect.height - 10 * self.geomatry
        size_button_and_icon_bottom = barBottom_rect.height - 10 * self.geomatry
        button_howToPlay_rect       = pygame.Rect(barTop_rect.left           + 10, barTop_rect.top             + (barTop_rect.height - size_button_and_icon_top) / 2,       size_button_and_icon_top, size_button_and_icon_top)
        button_stats_rect           = pygame.Rect(button_howToPlay_rect.left +     size_button_and_icon_top    + 10,                                                        barTop_rect.top    + (barTop_rect.height - size_button_and_icon_top) / 2,       size_button_and_icon_top, size_button_and_icon_top)
        button_settings_rect        = pygame.Rect(barTop_rect.right          -     size_button_and_icon_top    - 10,                                                        barTop_rect.top    + (barTop_rect.height - size_button_and_icon_top) / 2,       size_button_and_icon_top, size_button_and_icon_top)
        button_reset_rect           = pygame.Rect(button_settings_rect.left  -     size_button_and_icon_top    - 10,                                                        barTop_rect.top    + (barTop_rect.height - size_button_and_icon_top) / 2,       size_button_and_icon_top, size_button_and_icon_top)
        button_auto_write_rect      = pygame.Rect(button_reset_rect.left     -     size_button_and_icon_top    - 10,                                                        barTop_rect.top    + (barTop_rect.height - size_button_and_icon_top) / 2,       size_button_and_icon_top, size_button_and_icon_top)
        button_bag_coin_rect        = pygame.Rect(barBottom_rect.left        + 10, barBottom_rect.top          + (barBottom_rect.height - size_button_and_icon_bottom) / 2, size_button_and_icon_bottom,                                                    size_button_and_icon_bottom)
        button_hammer_rect          = pygame.Rect(barTop_rect.right          -     size_button_and_icon_bottom - 10,                                                        barBottom_rect.top + (barBottom_rect.height - size_button_and_icon_bottom) / 2, size_button_and_icon_bottom, size_button_and_icon_bottom)
        button_keyboard_rect        = pygame.Rect(button_hammer_rect.left    -     size_button_and_icon_bottom - 20,                                                        barBottom_rect.top + (barBottom_rect.height - size_button_and_icon_bottom) / 2, size_button_and_icon_bottom, size_button_and_icon_bottom)
        button_lamp_rect            = pygame.Rect(button_keyboard_rect.left  -     size_button_and_icon_bottom - 20,                                                        barBottom_rect.top + (barBottom_rect.height - size_button_and_icon_bottom) / 2, size_button_and_icon_bottom, size_button_and_icon_bottom)

        self.buttonhowToPlay   .edit_param(rect=button_howToPlay_rect,  image=self.image_question_mark, image_transform=(size_button_and_icon_top - 2.5 * self.geomatry,    size_button_and_icon_top - 2.5 * self.geomatry))
        self.buttonDailyCoins  .edit_param(rect=button_bag_coin_rect,   image=self.image_coin_bag,      image_transform=(size_button_and_icon_bottom - 2.5 * self.geomatry, size_button_and_icon_bottom - 2.5 * self.geomatry))
        self.buttonStats       .edit_param(rect=button_stats_rect,      image=self.image_stats,         image_transform=self.buttonhowToPlay.image_transform)
        self.buttonAutoWrite   .edit_param(rect=button_auto_write_rect, image=self.image_right_arrow,   image_transform=self.buttonhowToPlay.image_transform)
        self.buttonReset       .edit_param(rect=button_reset_rect,      image=self.image_reset,         image_transform=self.buttonhowToPlay.image_transform)
        self.buttonSettings    .edit_param(rect=button_settings_rect,   image=self.image_settings,      image_transform=self.buttonhowToPlay.image_transform)
        self.buttonLetterHint  .edit_param(rect=button_lamp_rect,       image=self.image_lamp,          image_transform=self.buttonDailyCoins.image_transform)
        self.buttonKeyboardHint.edit_param(rect=button_keyboard_rect,   image=self.image_keyboard,      image_transform=self.buttonDailyCoins.image_transform)
        self.buttonDeletedEntry.edit_param(rect=button_hammer_rect,     image=self.image_hammer,        image_transform=self.buttonDailyCoins.image_transform)

        pygame.draw.rect(self.screen, self.colors.barMenu['background'], barTop_rect)
        pygame.draw.rect(self.screen, self.colors.barMenu['background'], barBottom_rect)

        if not justshow:
            self.buttonhowToPlay   .draw_and_update()
            self.buttonStats       .draw_and_update()
            self.buttonSettings    .draw_and_update()
            self.buttonAutoWrite   .draw_and_update()
            self.buttonReset       .draw_and_update()
            self.buttonDailyCoins  .draw_and_update()
            self.buttonLetterHint  .draw_and_update()
            self.buttonKeyboardHint.draw_and_update()
            self.buttonDeletedEntry.draw_and_update()
        else:
            self.buttonhowToPlay   .draw_inactive()
            self.buttonStats       .draw_inactive()
            self.buttonSettings    .draw_inactive()
            self.buttonAutoWrite   .draw_inactive()
            self.buttonReset       .draw_inactive()
            self.buttonDailyCoins  .draw_inactive()
            self.buttonLetterHint  .draw_inactive()
            self.buttonKeyboardHint.draw_inactive()
            self.buttonDeletedEntry.draw_inactive()

        if self.get_daily_countdown() is True:
            pygame.draw.circle(self.screen, self.colors.barMenu['indicator'], (button_bag_coin_rect.right, button_bag_coin_rect.top), radius=7 * self.geomatry)

        showKatla = self.font_katla.render(f'KATLA #{self.word_length}',                                                   True, self.colors.barMenu['text'])
        showCoins = self.font_coins.render(self.num_format.parse(self.coins) if not const.isinf(self.coins) else '\u221e', True, self.colors.barMenu['text'])

        self.screen.blit(showKatla, showKatla.get_rect(center=barTop_rect.center))
        self.screen.blit(showCoins, showCoins.get_rect(left=button_bag_coin_rect.right + 20 * self.geomatry, top=button_bag_coin_rect.top + (button_bag_coin_rect.height - showCoins.get_height()) / 2))

    def showFreezeKatla(self) -> None:
        self.scroller_tile.min_max_scrolled = (-((self.size_tile + self.margin_tile) * (self.change_guess - 1) - self.margin_tile / 2), self.screen.get_height() - (self.size_tile + self.margin_tile / 2))

        if self.scroller_tile.direction < self.scroller_tile.min_max_scrolled[0]:
            self.scroller_tile.direction = self.scroller_tile.min_max_scrolled[0]
        elif self.scroller_tile.direction > self.scroller_tile.min_max_scrolled[1]:
            self.scroller_tile.direction = self.scroller_tile.min_max_scrolled[1]

        self.screen.fill(self.colors.screen)

        self.showTile    (justshow=True)
        self.showBarMenu (justshow=True)
        self.showKeyboard(justshow=True)
        self.showTextBar()

        self.handle_notification()

    def showSettings(self) -> None:
        LANG                 = self.languages['settings']
        self.isshow_Settings = True
        scroller             = ScrollerY(self, (0, 930 * self.geomatry))

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

        languages_id_list       = self.languages_object          .get_lang_id()
        languages_word_id_list  = self.validator_word_dictionary .get_lang_id()
        language_name_list      = self.languages_object          .get_lang_name()
        language_word_name_list = self.validator_word_dictionary .get_lang_name()

        index_lang_word       = languages_word_id_list         .index(language_word)
        index_lang            = languages_id_list              .index(language)
        index_theme           = const.LiteralConst.all_theme   .index(theme)
        index_keyboard_layout = const.LiteralConst.all_keyboard.index(keyboard_layout)

        last_configuration  = [index_theme, index_keyboard_layout, sound_volume, music_volume, change_guess, word_length, fps, geomatry, index_lang, index_lang_word, use_valid_word]
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
        surface_title    = font_title.render(LANG['title'], True, self.colors.settings['text'])

        buttonClose = Button(
            surface_screen = self.screen,
            color          = button_color(*[self.colors.settings['button']['close'] for _ in range(3)]),
            click_speed    = 0
        )
        buttonLang = Button(
            surface_screen = self.screen,
            font           = label_font,
            outline_size   = 4,
            text_color     = button_color(*[self.colors.settings['text'] for _ in range(3)]),
            color          = button_color(
                self.colors.settings['button']['set']['inactive'],
                self.colors.settings['button']['set']['active'],
                self.colors.settings['button']['set']['hover']
            ),
            outline_color  = button_color(*[self.colors.settings['outline'] for _ in range(3)]),
            only_click     = 'rl',
            click_speed    = 500
        )
        buttonLangWord        = buttonLang   .copy()
        buttonOxfordWord      = buttonLang   .copy(only_click='l', click_speed=50)
        buttonWordLen         = buttonLang   .copy(font=font1, click_speed=100)
        buttonChangeGuess     = buttonWordLen.copy()
        buttonTheme           = buttonLang   .copy(click_speed=100)
        buttontTypeKeyboard   = buttonTheme  .copy()
        buttonGeomatry        = buttonTheme  .copy()
        buttonFps             = buttonTheme  .copy()
        buttonNav_lang        = {'l': buttonLang .copy(only_click='l', text='<', font=nav_font), 'r': buttonLang .copy(only_click='l', text='>', font=nav_font)}
        buttonNav_langword    = {'l': buttonLang .copy(only_click='l', text='<', font=nav_font), 'r': buttonLang .copy(only_click='l', text='>', font=nav_font)}
        buttonNav_wordlen     = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_changeguess = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_theme       = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_typekeyb    = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_geomarty    = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        buttonNav_fps         = {'l': buttonTheme.copy(only_click='l', text='<', font=nav_font), 'r': buttonTheme.copy(only_click='l', text='>', font=nav_font)}
        rangeSound = Range(
            surface_screen = self.screen,
            thumb_color    = button_color(
                self.colors.settings['range']['thumb']['inactive'],
                self.colors.settings['range']['thumb']['active'],
                self.colors.settings['range']['thumb']['hover']
            ),
            track_color    = button_color(
                self.colors.settings['range']['track']['inactive'],
                self.colors.settings['range']['track']['active'],
                self.colors.settings['range']['track']['hover']
            ),
            track_fill_color = button_color(
                self.colors.settings['range']['track-fill']['inactive'],
                self.colors.settings['range']['track-fill']['active'],
                self.colors.settings['range']['track-fill']['hover']
            ),
            value       = sound_volume,
            click_speed = 0
        )
        rangeMusic = rangeSound.copy(value=music_volume)
        wrap_license = wrap_text(font_license, self.__license__, background_rect.width - 10 * self.geomatry)

        def label(label_text: str, type: str, index: const.Number) -> None:
            if   type == 'group': surface_text = label_group_font.render(label_text, True, self.colors.settings['text'])
            elif type == 'label': surface_text = label_font      .render(label_text, True, self.colors.settings['text'])
            self.screen.blit(surface_text, surface_text.get_rect(left=background_rect.left + 10 * self.geomatry, top=index))

        def button_edit(button_edit_param: Button, button_get_param: Button, kw: dict | None = None) -> None:
            button_edit_param.edit_param(**((button_get_param.get_param() | kw) if kw is not None else button_get_param.get_param()))

        def ternary(condination: bool, expression1: const.Any, expression2: const.Any) -> const.Any:
            return expression1 if bool(condination) else expression2

        def scrolling_settings(mousepos: tuple[const.Number, const.Number]) -> None:
            nonlocal background_rect, navbar_rect, scroller, navbar_rect
            background_rect              = pygame.Rect(const.math.get_center(self.screen.get_width(), self.screen.get_width() - 100), 0, self.screen.get_width() - 100, self.screen.get_height())
            close_rect                   = pygame.Rect(background_rect.right - 50 * self.geomatry,  background_rect.top + 10 * self.geomatry,                    40 * self.geomatry,         40 * self.geomatry)
            navbar_rect                  = pygame.Rect(background_rect.left,                        background_rect.top,                                         background_rect.width,      close_rect.bottom + 10 * self.geomatry)
            buttonlang_rect              = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 45 * self.geomatry - scroller.direction,  250 * self.geomatry,        50 * self.geomatry)
            buttonlangword_rect          = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 105 * self.geomatry - scroller.direction, 250 * self.geomatry,        50 * self.geomatry)
            buttonoxforddictionary_rect  = pygame.Rect(background_rect.right - 45 * self.geomatry,  navbar_rect.bottom + 420 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonwordlen_rect           = pygame.Rect(background_rect.right - 45 * self.geomatry,  navbar_rect.bottom + 470 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonchangeguess_rect       = pygame.Rect(background_rect.right - 45 * self.geomatry,  navbar_rect.bottom + 520 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttontheme_rect             = pygame.Rect(background_rect.right - 155 * self.geomatry, navbar_rect.bottom + 635 * self.geomatry - scroller.direction, 150 * self.geomatry,        50 * self.geomatry)
            buttontypekeyboard_rect      = pygame.Rect(background_rect.right - 155 * self.geomatry, navbar_rect.bottom + 695 * self.geomatry - scroller.direction, 150 * self.geomatry,        50 * self.geomatry)
            buttongeomatry_rect          = pygame.Rect(background_rect.right - 155 * self.geomatry, navbar_rect.bottom + 815 * self.geomatry - scroller.direction, 150 * self.geomatry,        50 * self.geomatry)
            buttonfps_rect               = pygame.Rect(background_rect.right - 155 * self.geomatry, navbar_rect.bottom + 875 * self.geomatry - scroller.direction, 150 * self.geomatry,        50 * self.geomatry)
            buttonNav_r_lang_rect        = pygame.Rect(background_rect.right - 305 * self.geomatry, navbar_rect.bottom + 50 * self.geomatry - scroller.direction,  40 * self.geomatry,         40 * self.geomatry)
            buttonNav_l_lang_rect        = pygame.Rect(background_rect.right - 355 * self.geomatry, navbar_rect.bottom + 50 * self.geomatry - scroller.direction,  40 * self.geomatry,         40 * self.geomatry)
            buttonNav_r_langword_rect    = pygame.Rect(background_rect.right - 305 * self.geomatry, navbar_rect.bottom + 110 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_l_langword_rect    = pygame.Rect(background_rect.right - 355 * self.geomatry, navbar_rect.bottom + 110 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_r_wordlen_rect     = pygame.Rect(background_rect.right - 95 * self.geomatry,  navbar_rect.bottom + 470 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_l_wordlen_rect     = pygame.Rect(background_rect.right - 145 * self.geomatry, navbar_rect.bottom + 470 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_r_changeguess_rect = pygame.Rect(background_rect.right - 95 * self.geomatry,  navbar_rect.bottom + 520 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_l_changeguess_rect = pygame.Rect(background_rect.right - 145 * self.geomatry, navbar_rect.bottom + 520 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_r_theme_rect       = pygame.Rect(background_rect.right - 205 * self.geomatry, navbar_rect.bottom + 640 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_l_theme_rect       = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 640 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_r_typekeyb_rect    = pygame.Rect(background_rect.right - 205 * self.geomatry, navbar_rect.bottom + 700 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_l_typekeyb_rect    = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 700 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_r_geomarty_rect    = pygame.Rect(background_rect.right - 205 * self.geomatry, navbar_rect.bottom + 820 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_l_geomarty_rect    = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 820 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_r_fps_rect         = pygame.Rect(background_rect.right - 205 * self.geomatry, navbar_rect.bottom + 880 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            buttonNav_l_fps_rect         = pygame.Rect(background_rect.right - 255 * self.geomatry, navbar_rect.bottom + 880 * self.geomatry - scroller.direction, 40 * self.geomatry,         40 * self.geomatry)
            rangetracksound_rect         = pygame.Rect(background_rect.right - 315 * self.geomatry, navbar_rect.bottom + 250 * self.geomatry - scroller.direction, 300 * self.geomatry,        14 * self.geomatry)
            rangetrackmusic_rect         = pygame.Rect(rangetracksound_rect.left,                   navbar_rect.bottom + 300 * self.geomatry - scroller.direction, rangetracksound_rect.width, rangetracksound_rect.height)
            backgroundOutline_rect       = const.math.Rect_outline(background_rect, 10)
            backgroundOutline_surface    = pygame.Surface((backgroundOutline_rect.width, backgroundOutline_rect.height))
            background_surface           = pygame.Surface((background_rect.width,        background_rect.height))
            image_oxford_kw = ({
                'image': self.image_check,
                'image_transform': 5 * self.geomatry
            } if use_valid_word else {
                'image': None,
                'image_transform': None
            })

            buttonLang      .edit_param(rect=buttonlang_rect,     text=language_name_list[index_lang])
            buttonLangWord  .edit_param(rect=buttonlangword_rect, text=language_word_name_list[index_lang_word])
            buttonOxfordWord.edit_param(
                rect  = buttonoxforddictionary_rect,
                color = button_color(
                    self.colors.settings['button']['switch'][str(use_valid_word).lower()]['inactive'],
                    self.colors.settings['button']['switch'][str(use_valid_word).lower()]['active'],
                    self.colors.settings['button']['switch'][str(use_valid_word).lower()]['hover']
                ),
                **image_oxford_kw
            )
            buttonClose               .edit_param(rect=close_rect,                                     image=self.image_close, image_transform=0)
            buttonWordLen             .edit_param(rect=buttonwordlen_rect,                             text=str(word_length))
            buttonChangeGuess         .edit_param(rect=buttonchangeguess_rect,                         text=str(change_guess))
            buttonTheme               .edit_param(rect=buttontheme_rect,                               text=LANG['theme-type']['buttons-label']['app-theme'][theme])
            buttontTypeKeyboard       .edit_param(rect=buttontypekeyboard_rect,                        text=keyboard_layout)
            buttonGeomatry            .edit_param(rect=buttongeomatry_rect,                            text=str(int(geomatry) - 8))
            buttonFps                 .edit_param(rect=buttonfps_rect,                                 text=str(fps))
            rangeSound                .edit_param(thumb_size=(20 * self.geomatry, 20 * self.geomatry), rect_track=rangetracksound_rect)
            rangeMusic                .edit_param(thumb_size=rangeSound.thumb_size,                    rect_track=rangetrackmusic_rect)
            buttonNav_lang['l']       .edit_param(rect=buttonNav_l_lang_rect)
            buttonNav_lang['r']       .edit_param(rect=buttonNav_r_lang_rect)
            buttonNav_langword['l']   .edit_param(rect=buttonNav_l_langword_rect)
            buttonNav_langword['r']   .edit_param(rect=buttonNav_r_langword_rect)
            buttonNav_wordlen['l']    .edit_param(rect=buttonNav_l_wordlen_rect)
            buttonNav_wordlen['r']    .edit_param(rect=buttonNav_r_wordlen_rect)
            buttonNav_changeguess['l'].edit_param(rect=buttonNav_l_changeguess_rect)
            buttonNav_changeguess['r'].edit_param(rect=buttonNav_r_changeguess_rect)
            buttonNav_theme['l']      .edit_param(rect=buttonNav_l_theme_rect)
            buttonNav_theme['r']      .edit_param(rect=buttonNav_r_theme_rect)
            buttonNav_typekeyb['l']   .edit_param(rect=buttonNav_l_typekeyb_rect)
            buttonNav_typekeyb['r']   .edit_param(rect=buttonNav_r_typekeyb_rect)
            buttonNav_geomarty['l']   .edit_param(rect=buttonNav_l_geomarty_rect)
            buttonNav_geomarty['r']   .edit_param(rect=buttonNav_r_geomarty_rect)
            buttonNav_fps['l']        .edit_param(rect=buttonNav_l_fps_rect)
            buttonNav_fps['r']        .edit_param(rect=buttonNav_r_fps_rect)

            backgroundOutline_surface.fill(self.colors.settings['outline'])
            background_surface       .fill(self.colors.settings['background'])
            backgroundOutline_surface.set_alpha(160)
            background_surface       .set_alpha(160)

            self.screen.blit(backgroundOutline_surface, backgroundOutline_rect)
            self.screen.blit(background_surface,        background_rect)

            SetAllCursorButtons(
                buttonClose,
                buttonLang,
                buttonLangWord,
                buttonOxfordWord,
                buttonWordLen,
                buttonChangeGuess,
                buttonTheme,
                buttontTypeKeyboard,
                buttonGeomatry,
                buttonFps,
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

            if not navbar_rect.collidepoint(*mousepos):
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
                buttonNav_typekeyb['l']   .draw_and_update()
                buttonNav_typekeyb['r']   .draw_and_update()
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
                buttontTypeKeyboard       .draw_and_update()
                buttonGeomatry            .draw_and_update()
                buttonFps                 .draw_and_update()
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
                buttonNav_typekeyb['l']   .draw_inactive()
                buttonNav_typekeyb['r']   .draw_inactive()
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
                buttontTypeKeyboard       .draw_inactive()
                buttonGeomatry            .draw_inactive()
                buttonFps                 .draw_inactive()
                rangeSound                .draw_inactive()
                rangeMusic                .draw_inactive()

                if not buttonClose.button_event.ismousehover:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            label(LANG['languages']['title'],                        'group', navbar_rect.bottom + 10 * self.geomatry  - scroller.direction)
            label(LANG['languages']['label']['app-language'],        'label', navbar_rect.bottom + 60 * self.geomatry  - scroller.direction)
            label(LANG['languages']['label']['word-language'],       'label', navbar_rect.bottom + 110 * self.geomatry - scroller.direction)

            label(LANG['sounds']['title'],                           'group', navbar_rect.bottom + 190 * self.geomatry - scroller.direction)
            label(LANG['sounds']['label']['sound'],                  'label', navbar_rect.bottom + 240 * self.geomatry - scroller.direction)
            label(LANG['sounds']['label']['music'],                  'label', navbar_rect.bottom + 290 * self.geomatry - scroller.direction)

            label(LANG['game-rules']['title'],                       'group', navbar_rect.bottom + 370 * self.geomatry - scroller.direction)
            label(LANG['game-rules']['label']['only-in-dictionary'], 'label', navbar_rect.bottom + 420 * self.geomatry - scroller.direction)
            label(LANG['game-rules']['label']['word-length'],        'label', navbar_rect.bottom + 470 * self.geomatry - scroller.direction)
            label(LANG['game-rules']['label']['change-guess'],       'label', navbar_rect.bottom + 520 * self.geomatry - scroller.direction)

            label(LANG['theme-type']['title'],                       'group', navbar_rect.bottom + 600 * self.geomatry - scroller.direction)
            label(LANG['theme-type']['label']['app-theme'],          'label', navbar_rect.bottom + 650 * self.geomatry - scroller.direction)
            label(LANG['theme-type']['label']['keyboard-layout'],    'label', navbar_rect.bottom + 700 * self.geomatry - scroller.direction)

            label(LANG['additional-settings']['title'],              'group', navbar_rect.bottom + 780 * self.geomatry - scroller.direction)
            label(LANG['additional-settings']['label']['geomatry'],  'label', navbar_rect.bottom + 830 * self.geomatry - scroller.direction)
            label(LANG['additional-settings']['label']['fps'],       'label', navbar_rect.bottom + 880 * self.geomatry - scroller.direction)

            for i, ln in enumerate(wrap_license):
                surface_text = font_license.render(ln, True, self.colors.settings['text'])
                self.screen.blit(surface_text, surface_text.get_rect(left=background_rect.left + 5, top=1010 * self.geomatry + i * surface_text.get_height() - scroller.direction))

            pygame.draw.rect(self.screen, self.colors.settings['navbar'], navbar_rect)

            buttonClose.draw_and_update()

            self.screen.blit(surface_title, surface_title.get_rect(center=navbar_rect.center))

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
                buttontTypeKeyboard       .handle_event(event)
                buttonGeomatry            .handle_event(event)
                buttonFps                 .handle_event(event)
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

            scroller.min_max_scrolled = (0, 990 * self.geomatry)
            mouse_pos                 = pygame.mouse.get_pos()

            scroller.update(anchor=any([
                not background_rect       .collidepoint(*mouse_pos),
                navbar_rect               .collidepoint(*mouse_pos),
                rangeSound                .button_event.isdragging,
                rangeMusic                .button_event.isdragging,
                buttonLang                .button_event.ismousehover,
                buttonLangWord            .button_event.ismousehover,
                buttonOxfordWord          .button_event.ismousehover,
                buttonWordLen             .button_event.ismousehover,
                buttonChangeGuess         .button_event.ismousehover,
                buttonTheme               .button_event.ismousehover,
                buttontTypeKeyboard       .button_event.ismousehover,
                buttonGeomatry            .button_event.ismousehover,
                buttonFps                 .button_event.ismousehover,
                buttonNav_lang['l']       .button_event.ismousehover,
                buttonNav_lang['r']       .button_event.ismousehover,
                buttonNav_langword['l']   .button_event.ismousehover,
                buttonNav_langword['r']   .button_event.ismousehover,
                buttonNav_wordlen['l']    .button_event.ismousehover,
                buttonNav_wordlen['r']    .button_event.ismousehover,
                buttonNav_changeguess['l'].button_event.ismousehover,
                buttonNav_changeguess['r'].button_event.ismousehover,
                buttonNav_theme['l']      .button_event.ismousehover,
                buttonNav_theme['r']      .button_event.ismousehover,
                buttonNav_typekeyb['l']   .button_event.ismousehover,
                buttonNav_typekeyb['r']   .button_event.ismousehover,
                buttonNav_geomarty['l']   .button_event.ismousehover,
                buttonNav_geomarty['r']   .button_event.ismousehover,
                buttonNav_fps['l']        .button_event.ismousehover,
                buttonNav_fps['r']        .button_event.ismousehover
            ]))

            self.showFreezeKatla()

            scrolling_settings(mouse_pos)

            if (clk := buttonLang.button_event.value) or buttonNav_lang['l'].button_event.value or buttonNav_lang['r'].button_event.value:
                self.handle_sound('click', 'play')
                index_lang += ternary(clk == 'l' or buttonNav_lang['r'].button_event.value, 1, -1)
            elif (clk := buttonLangWord.button_event.value) or buttonNav_langword['l'].button_event.value or buttonNav_langword['r'].button_event.value:
                self.handle_sound('click', 'play')
                index_lang_word += ternary(clk == 'l' or buttonNav_langword['r'].button_event.value, 1, -1)
            elif rangeSound.button_event.value:
                sound_volume = int(rangeSound.button_event.range_value)
            elif rangeMusic.button_event.value:
                music_volume = int(rangeMusic.button_event.range_value)
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
                index_theme += ternary(clk == 'l' or buttonNav_theme['r'].button_event.value, 1, -1)
            elif (clk := buttontTypeKeyboard.button_event.value) or buttonNav_typekeyb['l'].button_event.value or buttonNav_typekeyb['r'].button_event.value:
                self.handle_sound('click', 'play')
                index_keyboard_layout += ternary(clk == 'l' or buttonNav_typekeyb['r'].button_event.value, 1, -1)
            elif (clk := buttonFps.button_event.value) or buttonNav_fps['l'].button_event.value or buttonNav_fps['r'].button_event.value:
                self.handle_sound('click', 'play')
                fps += ternary(clk == 'l' or buttonNav_fps['r'].button_event.value, 5, -5)
            elif (clk := buttonGeomatry.button_event.value) or buttonNav_geomarty['l'].button_event.value or buttonNav_geomarty['r'].button_event.value:
                self.handle_sound('click', 'play')
                geomatry += ternary(clk == 'l' or buttonNav_geomarty['r'].button_event.value, 1, -1)

            if buttonClose.button_event.value:
                self.handle_sound('click', 'play')
                self.isshow_Settings = False

            if last_background_rect.width != background_rect.width:
                wrap_license         = wrap_text(font_license, self.__license__, background_rect.width - 10 * self.geomatry)
                last_background_rect = background_rect.copy()

            if last_configuration != [index_theme, index_keyboard_layout, sound_volume, music_volume, change_guess, word_length, fps, geomatry, index_lang, index_lang_word, use_valid_word]:

                if [last_configuration[2], last_configuration[3]] == [sound_volume, music_volume]:

                    if index_lang < 0:
                        index_lang = len(languages_id_list) - 1
                    elif index_lang > len(languages_id_list) - 1:
                        index_lang = 0
                    elif index_lang_word < 0:
                        index_lang_word = len(languages_word_id_list) - 1
                    elif index_lang_word > len(languages_word_id_list) - 1:
                        index_lang_word = 0
                    elif change_guess < 4:
                        change_guess = 10
                    elif change_guess > 10:
                        change_guess = 4
                    elif word_length < 4:
                        word_length = 9
                    elif word_length > 9:
                        word_length = 4
                    elif index_theme < 0:
                        index_theme = len(const.LiteralConst.all_theme) - 1
                    elif index_theme > len(const.LiteralConst.all_theme) - 1:
                        index_theme = 0
                    elif index_keyboard_layout < 0:
                        index_keyboard_layout = len(const.LiteralConst.all_keyboard) - 1
                    elif index_keyboard_layout > len(const.LiteralConst.all_keyboard) - 1:
                        index_keyboard_layout = 0
                    elif fps < 10:
                        fps = 120
                    elif fps > 120:
                        fps = 10
                    elif geomatry < 9:
                        geomatry = 22
                    elif geomatry > 22:
                        geomatry = 9

                    language        = languages_id_list              [index_lang]
                    theme           = const.LiteralConst.all_theme   [index_theme]
                    language_word   = languages_word_id_list         [index_lang_word]
                    keyboard_layout = const.LiteralConst.all_keyboard[index_keyboard_layout]

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

                self.set_volume()

                if [last_configuration[0], last_configuration[7], last_configuration[8]] != [index_theme, geomatry, index_lang]:
                    scroller          .edit_param(katla=self, min_max_scrolled=(0, 930 * self.geomatry))
                    self.scroller_tile.edit_param(katla=self)

                    self.languages  = self.languages_object.load(self.language)
                    self.colors     = const.Color(self.theme)
                    self.num_format = NumberFormat(self.languages['exponents-number'], decimal_places=2, rounded=False)
                    LANG            = self.languages['settings']

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

                    buttonClose.edit_param(color=button_color(*[self.colors.settings['button']['close'] for _ in range(3)]))
                    buttonLang .edit_param(
                        font          = label_font,
                        text_color    = button_color(*[self.colors.settings['text'] for _ in range(3)]),
                        color         = button_color(
                            self.colors.settings['button']['set']['inactive'],
                            self.colors.settings['button']['set']['active'],
                            self.colors.settings['button']['set']['hover']
                        ),
                        outline_color = button_color(*[self.colors.settings['outline'] for _ in range(3)]),
                        click_speed   = 500
                    )
                    button_edit(buttonOxfordWord,           buttonLang,              {'text': '', 'only_click': 'l', 'click_speed': 100})
                    button_edit(buttonWordLen,              buttonLang,              {'font': font1, 'click_speed': 100})
                    button_edit(buttonTheme,                buttonLang,              {'click_speed': 100})
                    button_edit(buttonLangWord,             buttonLang)
                    button_edit(buttonChangeGuess,          buttonWordLen)
                    button_edit(buttontTypeKeyboard,        buttonTheme)
                    button_edit(buttonGeomatry,             buttonTheme)
                    button_edit(buttonFps,                  buttonTheme)
                    button_edit(buttonNav_lang['l'],        buttonLang,              {'only_click': 'l', 'text': '<', 'font': nav_font})
                    button_edit(buttonNav_lang['r'],        buttonNav_lang['l'],     {'text': '>'})
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

                    surface_title = font_title.render(LANG['title'], True, self.colors.settings['text'])
                    self.buttonKeyboard = Button(
                        surface_screen = self.screen,
                        text_color     = button_color(*[self.colors.keyboard['text'] for _ in range(3)]),
                        click_speed    = 0,
                    )
                    self.buttonOutlineKeyboard = self.buttonKeyboard.copy(
                        color = button_color(
                            self.colors.keyboard['button']['outline']['inactive'],
                            self.colors.keyboard['button']['outline']['active'],
                            'black'
                        )
                    )
                    self.buttonhowToPlay = Button(
                        surface_screen = self.screen,
                        color          = button_color(*[self.colors.barMenu['background'] for _ in range(3)]),
                        click_speed    = 0,
                    )
                    self.buttonStats        = self.buttonhowToPlay.copy()
                    self.buttonAutoWrite    = self.buttonhowToPlay.copy(click_speed=250)
                    self.buttonReset        = self.buttonhowToPlay.copy(click_speed=500)
                    self.buttonSettings     = self.buttonhowToPlay.copy()
                    self.buttonDailyCoins   = self.buttonhowToPlay.copy()
                    self.buttonLetterHint   = self.buttonhowToPlay.copy()
                    self.buttonKeyboardHint = self.buttonhowToPlay.copy()
                    self.buttonDeletedEntry = self.buttonhowToPlay.copy()
                    rangeSound.edit_param(
                        thumb_color    = button_color(
                            self.colors.settings['range']['thumb']['inactive'],
                            self.colors.settings['range']['thumb']['active'],
                            self.colors.settings['range']['thumb']['hover']
                        ),
                        track_color    = button_color(
                            self.colors.settings['range']['track']['inactive'],
                            self.colors.settings['range']['track']['active'],
                            self.colors.settings['range']['track']['hover']
                        ),
                        track_fill_color = button_color(
                            self.colors.settings['range']['track-fill']['inactive'],
                            self.colors.settings['range']['track-fill']['active'],
                            self.colors.settings['range']['track-fill']['hover']
                        )
                    )
                    rangeMusic.edit_param(
                        thumb_color    = button_color(
                            self.colors.settings['range']['thumb']['inactive'],
                            self.colors.settings['range']['thumb']['active'],
                            self.colors.settings['range']['thumb']['hover']
                        ),
                        track_color    = button_color(
                            self.colors.settings['range']['track']['inactive'],
                            self.colors.settings['range']['track']['active'],
                            self.colors.settings['range']['track']['hover']
                        ),
                        track_fill_color = button_color(
                            self.colors.settings['range']['track-fill']['inactive'],
                            self.colors.settings['range']['track-fill']['active'],
                            self.colors.settings['range']['track-fill']['hover']
                        )
                    )
                    wrap_license = wrap_text(font_license, self.__license__, background_rect.width - 10 * self.geomatry)

                    self.notification = Notification(
                        self,
                        static_time    = 3,
                        move_down_time = 0.25,
                        move_up_time   = 0.25,
                        color          = self.colors.notification['default']['background'],
                        color_outline  = self.colors.notification['default']['outline'],
                        color_text     = self.colors.notification['default']['text']
                    )
                    self.popup = Popup(self)

                if last_configuration[9] != index_lang_word:
                    self.validator_word_dictionary = WordsValidator(language_word)
                    self.word_dictionary           = self.validator_word_dictionary.load_and_validation()

                if [change_guess, word_length, index_lang_word, use_valid_word] != [last_configuration[4], last_configuration[5], last_configuration[9], last_configuration[10]]:
                    self.reset()

                last_configuration = [index_theme, index_keyboard_layout, sound_volume, music_volume, change_guess, word_length, fps, geomatry, index_lang, index_lang_word, use_valid_word]

            pygame.display.flip()

            self.clock.tick(self.fps)

        if first_configuration != last_configuration:
            self.validator_settings.encrypt_data(self.settings)

    def Appmainloop(self) -> None:
        last_time_reset          = self.get_time()
        last_time_close_settings = self.get_time()
        last_time_backspace      = self.get_time()
        pressed_backspace        = False
        pressed_key              = False
        done_warn                = [False, False, False]

        def show_info_popup(title: str, message: str, button_ok: str = 'OK') -> None:
            self.popup.edit_param(
                type      = 'info',
                title     = title,
                label     = message,
                button_ok = button_ok
            )
            self.popup()

        def showNotEnoughCoin() -> None:
            LANG_NOT_ENOUGH_COIN = self.languages['popup']['not-enough-coin']
            show_info_popup(LANG_NOT_ENOUGH_COIN['title'], LANG_NOT_ENOUGH_COIN['label'], LANG_NOT_ENOUGH_COIN['button-ok'])

        self.set_volume()

        self.handle_sound('backsound', 'play')

        while self.running:

            barTop_rect = pygame.Rect(
                const.math.get_center(self.screen.get_width(), self.screen.get_width() - 10),
                5 * self.geomatry,
                self.screen.get_width() - 10,
                115 * self.geomatry
            )
            keyboard_letter = None
            shortcut_key    = None
            can_inputed     = not any([self.isshow_Lose, self.isshow_Win, last_time_close_settings + 0.5 > self.get_time()])

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                self.scroller_tile.event(event)

                self.handle_screen_resize(event)

                self.buttonhowToPlay   .handle_event(event)
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

            mouse_pos = pygame.mouse.get_pos()
            getkeys   = pygame.key.get_pressed()
            self.scroller_tile.min_max_scrolled = (-((self.size_tile + self.margin_tile) * (self.change_guess - 1) - self.margin_tile / 2), self.screen.get_height() - (self.size_tile + self.margin_tile / 2))

            self.scroller_tile.update(anchor=self.boardRect_keyboard.collidepoint(*mouse_pos) or barTop_rect.collidepoint(*mouse_pos))

            self.screen.fill(self.colors.screen)

            self.showTile()
            self.showBarMenu()
            click_detected, keyboard_visual_letter = self.showKeyboard()
            self.showTextBar()

            SetAllCursorButtons(
                self.buttonhowToPlay,
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

            self.handle_notification()

            if self.last_geomatry != self.geomatry and not self.threadgif.is_alive():
                self.update_pos_gif()
                size                      = 500 * self.geomatry
                self.last_geomatry        = self.geomatry
                self.confetti_rect.width  = size
                self.confetti_rect.height = size

                self.threadgif = Thread(target=self.gif_confetti.convert_gif)
                self.threadgif.start()

            if self.validator_game_data.file_corrupt and not done_warn[0]:
                done_warn[0] = True
                WLANG        = self.languages['popup']['errors']['data-game']
                show_info_popup(WLANG['title'], WLANG['message'], self.languages['popup']['errors']['button-ok'])

            if self.validator_settings.file_corrupt and not done_warn[1]:
                done_warn[1] = True
                WLANG        = self.languages['popup']['errors']['data-settings']
                show_info_popup(WLANG['title'], WLANG['message'], self.languages['popup']['errors']['button-ok'])

            if not (self.init_mixer or done_warn[2]):
                done_warn[2] = True
                WLANG        = self.languages['popup']['errors']['sound-mixer']
                show_info_popup(WLANG['title'], WLANG['message'], self.languages['popup']['errors']['button-ok'])

            if self.buttonhowToPlay.button_event.value or shortcut_key == '1':
                self.popup.edit_param(type='how-to-play')
                self.handle_sound('click', 'play')
                self.popup()

            elif self.buttonStats.button_event.value or shortcut_key == '2':
                self.popup.edit_param(type='stats')
                self.handle_sound('click', 'play')
                self.popup()

            elif self.buttonDailyCoins.button_event.value or shortcut_key == '7':
                DAILY_COINS = 50
                HOURS = 24
                COINS_REWAND = 1

                def take_coins() -> None:
                    if self.get_daily_countdown() is True:
                        self.coins += DAILY_COINS
                        self.game_data['prize-claim-time'] = datetime.now().strftime(r'%H/%M/%S/%d/%m/%Y')
                        self.save_game(prize_taken=True)

                self.popup.edit_param(
                    type         = 'daily-coins',
                    daily_coins  = DAILY_COINS,
                    hours        = HOURS,
                    coins_rewand = COINS_REWAND,
                    take_coins_function = take_coins
                )
                self.handle_sound('click', 'play')
                self.popup()

            elif (self.buttonAutoWrite.button_event.value or shortcut_key == '3') and can_inputed:
                self.handle_sound('click', 'play')
                ln            = self.input_point[1]
                correct_input = self.get_correct_char()

                cp = correct_input.copy()
                cp.reverse()

                for i, item in enumerate(cp):
                    if item is None:
                        correct_input.pop(-1)
                    else:
                        break

                self.input_history[ln] = [item or 'X' for item in correct_input]
                self.input_point[0]    = len(self.input_history[ln]) - (0 if len(self.input_history[ln]) < self.word_length else 1)

                self.update_correct_tile()

            elif (self.buttonLetterHint.button_event.value or shortcut_key == '8') and can_inputed:
                LANG_LETTER_HINT = self.languages['popup']['hint-letter']
                COINS_PRICE = 35
                self.popup.edit_param(
                    type         = 'hint',
                    title        = LANG_LETTER_HINT['title'],
                    label        = LANG_LETTER_HINT['label'],
                    button_label = LANG_LETTER_HINT['button-coins'].replace('<COINS-PRICE>', str(COINS_PRICE), 1)
                )
                self.handle_sound('click', 'play')
                isbuy = self.popup()

                if isbuy == 'buy':
                    if self.coins < COINS_PRICE:
                        showNotEnoughCoin()

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
                            self.timeanimation_notification  = self.get_time()

            elif (self.buttonKeyboardHint.button_event.value or shortcut_key == '9') and can_inputed:
                LANG_KEYBOARD_HINT = self.languages['popup']['hint-keyboard']
                COINS_PRICE = 25
                self.popup.edit_param(
                    type         = 'hint',
                    title        = LANG_KEYBOARD_HINT['title'],
                    label        = LANG_KEYBOARD_HINT['label'],
                    button_label = LANG_KEYBOARD_HINT['button-coins'].replace('<COINS-PRICE>', str(COINS_PRICE), 1)
                )
                self.handle_sound('click', 'play')
                isbuy = self.popup()

                if isbuy == 'buy':
                    if self.coins < COINS_PRICE:
                        showNotEnoughCoin()

                    else:
                        double_letter = 0
                        end_loop = False

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
                            self.timeanimation_notification      = self.get_time()

            elif (self.buttonDeletedEntry.button_event.value or shortcut_key == '0') and can_inputed:
                LANG_DEL_TILE = self.languages['popup']['delete-tile']
                COINS_PRICE = 10
                self.popup.edit_param(
                    type         = 'hint',
                    title        = LANG_DEL_TILE['title'],
                    label        = LANG_DEL_TILE['label'],
                    button_label = LANG_DEL_TILE['button-coins'].replace('<COINS-PRICE>', str(COINS_PRICE), 1)
                )
                self.handle_sound('click', 'play')
                isbuy = self.popup()

                if isbuy == 'buy' and self.input_point[1] > 0:
                    if self.coins < COINS_PRICE:
                        showNotEnoughCoin()

                    else:
                        self.guess_count += 1
                        self.input_history    .pop(-2)
                        self.input_history[-1].clear()
                        self.feedback_history .pop(-1)
                        self.input_point[0] = 0
                        self.input_point[1] -= 1

                        self.coins -= COINS_PRICE
                        self.save_game(hint_coins_price=COINS_PRICE)

                elif isbuy == 'buy' and self.input_point[1] <= 0:
                    self.reset_isshow()
                    self.isshow_TileIsEmpty         = True
                    self.timeanimation_notification = self.get_time()

            elif (self.buttonReset.button_event.value or shortcut_key == '4') and last_time_reset + 0.5 <= self.get_time() and can_inputed:
                self.handle_sound('click', 'play')
                self.reset()
                last_time_reset                 = self.get_time()
                self.timeanimation_notification = self.get_time()
                self.isshow_Reset               = True

            elif (self.buttonSettings.button_event.value or shortcut_key == '5') and can_inputed:
                self.handle_sound('click', 'play')
                self.showSettings()
                last_time_close_settings = self.get_time()

            pygame.display.flip()

            self.clock.tick(self.fps)

            if (getkeys[pygame.K_BACKSPACE] or click_detected) and can_inputed:
                if not pressed_backspace:
                    last_time_backspace = self.get_time()

                pressed_backspace = True

                if last_time_backspace + 0.5 <= self.get_time() and (getkeys[pygame.K_BACKSPACE] or keyboard_visual_letter == '\b') and self.input_point[0] != 0:
                    self.handle_input('\b')
                    continue

            else:
                pressed_backspace = False

            if click_detected and not pressed_key and can_inputed:
                self.handle_input(keyboard_visual_letter)
                pressed_key = True

            elif keyboard_letter and can_inputed:
                self.handle_input(keyboard_letter)

            elif pressed_key and not click_detected and can_inputed:
                pressed_key = False

        pygame.quit()

def main() -> None:
    try:

        print('Test permission... ', end='')

        t = const.test_read_write_delete()

        print('Done')

        if t[1] is not None:
            print(f'Test completed with errors -> {type(t[1]).__name__}')
            raise t[1]

        print('Test completed with no errors')

        katla = Katla()
        print('\n' + str(katla) + '\n')

        if katla.running and pygame.get_init():
            katla.Appmainloop()

    except PermissionError:
        msg = f'PERMISSION ERROR: Unable to save / write data due to administrator issues. Run Katla application with administrator or not and move application folder to environment without needing administrator?'
        pygame.quit()
        print(msg)
        runasadmin = messagebox.askyesnocancel('Katla - Permission error', msg)
        if runasadmin:

            try:

                if not isUserAdmin():
                    runAsAdmin()
                else:
                    main()

            except Exception as e:
                msgdenied = f'Failed to run Katla as administrator. Please try again later. {str(e).capitalize()}'
                print(msgdenied)
                messagebox.showerror('Katla - Access denied', msgdenied)

    except Exception as e:
        msg = f'EXCEPTION ERROR: {type(e).__name__}: {e}'
        pygame.quit()
        print(msg)
        messagebox.showerror('Katla - Exception unexpected', msg)
        raise

if __name__ == '__main__':
    main()
else:
    raise Exception(f'not as module')