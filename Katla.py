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
from random import choice
from threading import Thread
from tkinter import messagebox
from string import ascii_uppercase
from platform import python_version
from datetime import datetime, timedelta
from pyuac import isUserAdmin, runAsAdmin
from components.module.corrector import Correction
from components.module.format_number import NumberFormat
from components.module.pygameui.vgif import GIF
from components.module.pygameui.scroller import ScrollerY
from components.module.pygameui.textwrap import wrap_text, render_wrap
from components.module.pygameui.button import button_color, Button, Range, set_cursor_buttons
from components.katla_components import constants as const
from components.katla_components.logs import Logs
from components.katla_components.popup import Popup, Notification
from components.katla_components.json_validator import Languages, Themes, WordsValidator, SettingsValidator, GameDataValidator

logs = Logs()

logs.log(f"pygame {pygame.ver} (SDL {'.'.join(map(str, pygame.get_sdl_version()))}, Python {python_version()})")
logs.log(f"running system - RUNSYS: {const.RUNSYS}")

class Katla:

    """
    # Katla - pygame - Python 3

    Supported software - Perangkat lunak yang didukung:
    - Android: pydroid3 -> Python [VERSION] 3.10+
    - Windows, ...etc: Python [VERSION] 3.10+
    """

    __version__       = (const.MAJOR, const.MINOR, const.PATCH)
    __label_version__ = const.VERSION
    __license__       = const.LICENSE

    def __init__(self) -> None:
        logs.log('-- Katla logs --')

        const.os.environ['SDL_VIDEO_CENTERED'] = '1'

        logs.log('Initialization pygame init, and font.init')
        pygame.init()
        pygame.font.init()

        logs.log('Initialization files, languages, themes, and katla data')
        self.file                = const.File()
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
        self.word_corrector : bool  = self.settings['word-corrector']

        logs.log(f'loaded themes and icon')
        self.themes = self.validator_themes.load(self.theme)

        images = self.file.Images(self.themes['icon-color'])

        self.image_icon = pygame.image.load(images.ICON)

        pygame.display.set_icon(self.image_icon)
        pygame.display.set_caption('Katla - Loading...')

        logs.log(f'Initialization words, with id: {self.language_word}')
        self.validator_word_dictionary = WordsValidator(self.language_word)

        logs.log('Load and validation words and load languages')
        self.word_dictionary = self.validator_word_dictionary.load_and_validation()
        self.languages       = self.validator_languages      .load(self.language)

        logs.log('Load attributes')
        self.keyboards                : dict[str, const.KeyboardList] = {key: getattr(const.Keyboard, key) for key in const.Keyboard.__all__}
        self.keyboard_feedback        : dict[str, str]                = {char: 'not-inputed' for line in self.keyboards[self.keyboard_layout] for char in line}
        self.running                  : bool                          = True
        self.isshow_Settings          : bool                          = False
        self.isshow_Logs              : bool                          = False
        self.detected_time_cheat      : bool                          = False
        self.init_mixer               : bool                          = False
        self.search_correct           : str | None                    = None
        self.file_game_corrupt        : bool                          = self.validator_game_data.file_corrupt
        self.coins                    : const.Number                  = self.game_data['coins']
        self.last_play_time_seconds   : int                           = self.game_data['play-time-seconds']
        self.guess_count              : int                           = self.change_guess
        self.notification_initial_y   : float                         = 130 * self.geomatry
        self.play_lose_or_win         : int                           = 0
        self.last_win_line            : int                           = 0
        self.last_geomatry            : float                         = 0.0
        self.words_list               : list[str]                     = [word.upper()  for word in self.word_dictionary[f'length-{self.word_length}']]
        self.correct_char_tile        : list[str]                     = ['not-inputed' for _ in range(self.word_length)]
        self.correct_char_keyboard    : list[str]                     = []
        self.notifications_layer      : list[str]                     = []
        self.hint_tile                : list[str]                     = []
        self.hint_keyboard            : list[str]                     = []
        self.feedback_history         : list[const.Feedback]          = []
        self.feedback_history_keyboard: list[const.Feedback]          = []
        self.input_history            : list[list[str]]               = [[]]
        self.input_point              : list[int, int]                = [0, 0]
        self.isshow_popup_warn        : list[bool, bool, bool]        = [False, False, False]
        self.selected_word            : str                           = 'LARON'# choice(self.words_list)
        self.last_word_input          : str                           = ''

        self.corrector = Correction(self.words_list, 0.6)

        self.num_format = NumberFormat(
            config_exponents = self.languages['exponents-number'],
            decimal_places   = 2,
            rounded          = False,
            reach            = (3, 'thousand')
        )

        logs.log('Set the screen')
        self.display_info = pygame.display.Info()

        self.minsize_screen = (const.MIN_SCREEN_X, const.MIN_SCREEN_Y)
        self.maxsize_screen = (min(self.display_info.current_w - 75, const.MAX_SCREEN_X), min(self.display_info.current_h - 50, const.MAX_SCREEN_Y))

        init_screen = self.settings['screen-size']

        if init_screen == 'FULL':
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        elif init_screen[0] < const.MIN_SCREEN_X or init_screen[1] < const.MIN_SCREEN_Y:
            self.screen = pygame.display.set_mode(self.minsize_screen, pygame.RESIZABLE)

        elif init_screen[0] > self.maxsize_screen[0] or init_screen[1] > self.maxsize_screen[1]:
            init_screen[0] = self.maxsize_screen[0] if init_screen[0] > self.maxsize_screen[0] else init_screen[0]
            init_screen[1] = self.maxsize_screen[1] if init_screen[1] > self.maxsize_screen[1] else init_screen[1]
            self.screen = pygame.display.set_mode(init_screen, pygame.RESIZABLE)

        else:
            self.screen = pygame.display.set_mode(init_screen, pygame.RESIZABLE)

        self.fullscreen_attr = {
            'full':      init_screen == 'FULL',
            'last-size': list(self.screen.get_size() if init_screen != 'FULL' else self.maxsize_screen)
        }

        logs.log(f'Screen sized: (W={self.screen.get_width()}, H={self.screen.get_height()})')

        size_confetti           = 500 * self.geomatry
        self.init_rect          = pygame.Rect(0, 0, 0, 0)
        self.boardRect_keyboard = self.init_rect
        self.confetti_rect      = pygame.Rect(const.math.get_center(self.screen.get_width(), size_confetti), self.screen.get_height() - size_confetti, size_confetti, size_confetti)

        self.fullscreen_attr          : dict[const.Literal['full', 'last-size'], const.Any]
        self.gif_win                  : GIF
        self.sound_music              : pygame.mixer.Sound
        self.sound_key                : pygame.mixer.Sound
        self.sound_key_backspace_enter: pygame.mixer.Sound
        self.sound_button_click       : pygame.mixer.Sound
        self.sound_win                : pygame.mixer.Sound
        self.sound_lose               : pygame.mixer.Sound
        self.popup                    : Popup
        self.notifications            : dict[const.Literal[
            'NotInDictionary',
            'NotEnoughLength',
            'TileIsEmpty',
            'AllKeyboardHintsProvided',
            'AllTileHintsProvided',
            'StreakEnded',
            'Win',
            'Lose',
            'Reset',
            'Unfullscreen'
        ], Notification]

        def load_assets() -> None:
            try:
                logs.log('Initialization pygame mixer.init')
                pygame.mixer.init()
                self.init_mixer = True
            except Exception as e:
                logs.log(f'pygame mixer error: {e}', 'error')
                logs.log('Initialization pygame mixer.init failed. Sounds cannot be loaded and played', 'warn')
                self.init_mixer = False

            logs.log('Load gif')
            self.gif_win = GIF(gif_path=images.WIN_GIF, rect=self.confetti_rect, frame_delay=25)

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
            self.font_tile         = pygame.font.Font(self.file.FONT_BAKSOSAPI_REGULAR, int(self.size_tile))
            self.font_textbar      = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(20 * self.geomatry))
            self.font_keyboard     = pygame.font.Font(self.file.FONT_BAKSOSAPI_REGULAR, int(35 * self.geomatry))
            self.font_katla        = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,       int(40 * self.geomatry))
            self.font_notification = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(30 * self.geomatry))
            self.font_coins        = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(35 * self.geomatry))

            logs.log('Initialization Button')
            self.buttonKeyboard = Button(
                surface_screen = self.screen,
                rect           = self.init_rect,
                text_color     = self.single_color_button(self.themes['keyboard']['text']),
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

            logs.log('Initialization Popup and Notifications')
            self.popup         = Popup(self)
            self.notifications = {
                'NotInDictionary':          Notification(self, 'NotInDictionary'),
                'NotEnoughLength':          Notification(self, 'NotEnoughLength'),
                'TileIsEmpty':              Notification(self, 'TileIsEmpty'),
                'AllKeyboardHintsProvided': Notification(self, 'AllKeyboardHintsProvided'),
                'AllTileHintsProvided':     Notification(self, 'AllTileHintsProvided'),
                'StreakEnded':              Notification(self, 'StreakEnded'),
                'Win':                      Notification(self, 'Win'),
                'Lose':                     Notification(self, 'Lose'),
                'Reset':                    Notification(self, 'Reset'),
                'Unfullscreen':             Notification(self, 'Unfullscreen')
            }

        sizeload = 50 * self.geomatry
        sizeicon = 100 * self.geomatry

        icon = pygame.transform.scale(self.image_icon, (sizeicon, sizeicon))

        thread_load = Thread(target=load_assets)

        gif_loading = GIF(
            gif_path = images.LOAD_GIF,
            rect = pygame.Rect(
                const.math.get_center(self.screen.get_width(), sizeload),
                self.screen.get_height() - 80 * self.geomatry,
                sizeload,
                sizeload
            ),
            frame_delay = 100
        )

        self.clock = pygame.time.Clock()

        self.scroller_tile     = ScrollerY((0, 0), 0, clock=self.clock)
        self.scroller_logs     = self.scroller_tile.copy()
        self.scroller_settings = self.scroller_tile.copy()

        self.scroller_tile.offset_y = 130 * self.geomatry

        try:
            logs.log('Thread and loading screen starting')
            thread_load.start()

            runloading = True

            while runloading:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        runloading   = False
                        self.running = False

                        thread_load.join(.01)

                    self.handle_screen_resize(event, show_notif=False)

                if not thread_load.is_alive() and runloading:
                    runloading = False

                sizescreen = self.screen.get_size()

                gif_loading.rect = pygame.Rect(const.math.get_center(sizescreen[0], sizeload), sizescreen[1] - 80 * self.geomatry, sizeload, sizeload)

                self.screen.fill(self.themes['screen'])

                self.screen.blit(icon, (const.math.get_center(sizescreen[0], sizeicon), const.math.get_center(sizescreen[1], sizeicon)))

                gif_loading.draw_and_update(self.screen)

                pygame.display.flip()

                self.clock.tick(self.fps)

            if self.detect_time_manipulation():
                logs.log('Detected suspicion of cheating: Current time with larger game data time.', 'warn')
                self.detected_time_cheat = True

            if self.game_data['joined-date']['edit-date']:
                self.game_data['joined-date']['date']      = self.get_datetime()
                self.game_data['joined-date']['edit-date'] = False
                self.save_game()

            self.new_streak()
            self.set_volume()

            self.threadgif = Thread(target=self.gif_win.convert_gif)

            self.last_time_save_game      = self.get_tick()
            self.last_time_reset          = self.get_tick()
            self.last_time_close_settings = self.get_tick()

            pygame.display.set_caption('Katla')

            logs.log('Game was ready')

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

        self.words_list         = [word.upper()  for word in self.word_dictionary[f'length-{self.word_length}']]
        self.correct_char_tile  = ['not-inputed' for _ in range(self.word_length)]
        self.input_point        = [0, 0]
        self.input_history      = [[]]
        self.search_correct     = None
        self.guess_count        = self.change_guess
        self.selected_word      = choice(self.words_list)
        self.corrector.database = self.words_list

        self.update_correct_tile()
        self.update_keyboard_feedback()

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
            if color == 'not-inputed' and char in self.hint_keyboard:
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
                        if feedback[j][char] in ("green", "yellow") and guess_char_frequency[char] > 0:
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
        timedelta_days0 = timedelta(0)
        timedelta_days1 = timedelta(1)

        last_time_int = list(map(int, self.game_data['prize-claim-time'].split('/')))

        last_claim_datetime = datetime(last_time_int[5], last_time_int[4], last_time_int[3], last_time_int[0], last_time_int[1], last_time_int[2])
        time_difference     = datetime.now() - last_claim_datetime
        countdown           = timedelta_days1 - time_difference if time_difference < timedelta_days1 else timedelta_days0

        return True if countdown == timedelta_days0 else f"{countdown.seconds // 3600:02}:{(countdown.seconds % 3600) // 60:02}:{(countdown.seconds % 3600) % 60:02}"

    def get_tick(self) -> float:
        return pygame.time.get_ticks() / 1000

    def get_datetime(self) -> str:
        return datetime.now().strftime(r'%H/%M/%S/%d/%m/%Y')

    def detect_time_manipulation(self, use_date: const.Literal['prize-claim-time', 'played-time', 'joined-date'] = 'prize-claim-time') -> bool:
        datestr = self.game_data[use_date]

        if use_date == 'joined-date':
            datestr = self.game_data['joined-date']['date']

        last_time_int = list(map(int, datestr.split('/')))

        last_claim_datetime = datetime(last_time_int[5], last_time_int[4], last_time_int[3], last_time_int[0], last_time_int[1], last_time_int[2])
        current_time        = datetime.now()
        time_difference     = current_time - last_claim_datetime

        return time_difference.total_seconds() < 0

    def single_color_button(self, color) -> button_color:
        return button_color(*[color for _ in range(3)])

    def new_streak(self) -> None:
        last_time_int = list(map(int, self.game_data['played-time'].split('/')))

        last_claim_datetime = datetime(last_time_int[5], last_time_int[4], last_time_int[3], last_time_int[0], last_time_int[1], last_time_int[2])
        time_difference     = datetime.now() - last_claim_datetime

        if time_difference > timedelta(1):
            self.game_data['wins']['streak'] = 0
            self.game_data['played-time']    = self.get_datetime()
            self.notifications['StreakEnded'].start()

    def set_volume(self) -> None:
        if self.init_mixer:
            musicvol = self.music_volume / 100
            soundvol = self.sound_volume / 100

            self.sound_music              .set_volume(musicvol)
            self.sound_key                .set_volume(soundvol)
            self.sound_key_backspace_enter.set_volume(soundvol)
            self.sound_button_click       .set_volume(soundvol)
            self.sound_win                .set_volume(soundvol)
            self.sound_lose               .set_volume(soundvol)

    def save_game(self, win: bool = False, line: str = '', lose: bool = False, prize_taken: bool = False, hint_coins_price: int | bool = False) -> None:
        self.update_keyboard_feedback()
        self.new_streak()

        self.game_data['play-time-seconds'] = self.last_play_time_seconds + int(self.get_tick())
        self.game_data['coins']             = self.coins

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

        if self.detect_time_manipulation():
            self.detected_time_cheat = True

        self.last_time_save_game = self.get_tick()

        if not self.detected_time_cheat:
            self.validator_game_data.encrypt_data(self.game_data)
        else:
            logs.log('Cannot save data. Please close the application and reopen it', 'warn')

    def save_game_periodically(self) -> None:
        if self.last_time_save_game + const.AUTO_SAVE_INTERVAL < self.get_tick():
            self.save_game()

    def input_event(self, event: pygame.event.Event) -> tuple[const.Literal['key', 'shortcut'], str] | tuple[None, None]:
        if event.type == pygame.KEYDOWN:

            match event.key:

                case pygame.K_a:         return 'key',      'A'
                case pygame.K_b:         return 'key',      'B'
                case pygame.K_c:         return 'key',      'C'
                case pygame.K_d:         return 'key',      'D'
                case pygame.K_e:         return 'key',      'E'
                case pygame.K_f:         return 'key',      'F'
                case pygame.K_g:         return 'key',      'G'
                case pygame.K_h:         return 'key',      'H'
                case pygame.K_i:         return 'key',      'I'
                case pygame.K_j:         return 'key',      'J'
                case pygame.K_k:         return 'key',      'K'
                case pygame.K_l:         return 'key',      'L'
                case pygame.K_m:         return 'key',      'M'
                case pygame.K_n:         return 'key',      'N'
                case pygame.K_o:         return 'key',      'O'
                case pygame.K_p:         return 'key',      'P'
                case pygame.K_q:         return 'key',      'Q'
                case pygame.K_r:         return 'key',      'R'
                case pygame.K_s:         return 'key',      'S'
                case pygame.K_t:         return 'key',      'T'
                case pygame.K_u:         return 'key',      'U'
                case pygame.K_v:         return 'key',      'V'
                case pygame.K_w:         return 'key',      'W'
                case pygame.K_x:         return 'key',      'X'
                case pygame.K_y:         return 'key',      'Y'
                case pygame.K_z:         return 'key',      'Z'
                case pygame.K_BACKSPACE: return 'key',      const.BACKSPACE
                case pygame.K_RETURN:    return 'key',      const.ENTER
                case pygame.K_1:         return 'shortcut', '1'
                case pygame.K_2:         return 'shortcut', '2'
                case pygame.K_3:         return 'shortcut', '3'
                case pygame.K_4:         return 'shortcut', '4'
                case pygame.K_5:         return 'shortcut', '5'
                case pygame.K_6:         return 'shortcut', '6'
                case pygame.K_7:         return 'shortcut', '7'
                case pygame.K_8:         return 'shortcut', '8'
                case pygame.K_9:         return 'shortcut', '9'
                case pygame.K_0:         return 'shortcut', '0'

        return None, None

    def handle_screen_resize(self, event: pygame.event.Event, show_notif: bool = True) -> None:
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
                    if show_notif:
                        self.notifications['Unfullscreen'].start()

                else:
                    self.screen                       = pygame.display.set_mode(self.minsize_screen, pygame.RESIZABLE)
                    self.settings['screen-size']      = list(self.minsize_screen)
                    self.fullscreen_attr['last-size'] = self.settings['screen-size']
                    self.validator_settings.encrypt_data(self.settings)

        elif event.type == pygame.VIDEORESIZE and not self.fullscreen_attr['full']:
            x, y        = event.size
            self.screen = pygame.display.set_mode((max(const.MIN_SCREEN_X, x), max(const.MIN_SCREEN_Y, y)), pygame.RESIZABLE)
            screen_size = list(self.screen.get_size())

            if screen_size[0] > self.maxsize_screen[0]:
                screen_size[0] = self.maxsize_screen[0]
            if screen_size[1] > self.maxsize_screen[1]:
                screen_size[1] = self.maxsize_screen[1]

            self.settings['screen-size']      = screen_size
            self.fullscreen_attr['last-size'] = screen_size
            self.validator_settings.encrypt_data(self.settings)

    def handle_sound(self, stype: const.Literal['backsound', 'key', 'key-bn', 'click', 'win', 'lose'], do: const.Literal['play', 'stop']) -> None:

        def playstop(sound: pygame.mixer.Sound) -> None:
            if do == 'play':
                if stype == 'backsound':
                    sound.play(-1)
                else:
                    sound.play()
            elif do == 'stop':
                sound.stop()

        if self.init_mixer:

            match stype:

                case 'backsound':
                    playstop(self.sound_music)

                case 'key':
                    playstop(self.sound_key)

                case 'key-bn':
                    playstop(self.sound_key_backspace_enter)

                case 'click':
                    playstop(self.sound_button_click)

                case 'win':
                    playstop(self.sound_win)

                case 'lose':
                    playstop(self.sound_lose)

    def handle_input(self, char: str) -> None:
        ln     = self.input_point[1]
        len_ln = len(self.input_history[ln])

        self.showKeyboard(char, True)
        pygame.display.flip()
        pygame.time.delay(30)

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

                    if guess_word in self.corrector.database:
                        self.corrector.database.remove(guess_word)

                    self.input_point[0]  = 0
                    self.input_point[1] += 1
                    self.guess_count    -= 1
                    self.update_keyboard_feedback()

                else:
                    if self.word_corrector:
                        list_correct = self.corrector.get_list_correct(guess_word)
                        self.search_correct = ''
                        if list_correct:
                            self.search_correct = choice(list_correct)

                    self.last_word_input = guess_word

                    self.notifications['NotInDictionary'].start()

                if guess_word == self.selected_word:
                    line                  = ln + 1
                    self.coins           += const.WIN_COINS_REWAND(self.word_length)
                    self.last_win_line    = line
                    self.last_word_input  = guess_word

                    self.notifications['Win'].start()
                    self.save_game(win=True, line=str(line))

                elif self.guess_count <= 0:
                    self.last_word_input = guess_word

                    self.notifications['Lose'].start()
                    self.save_game(lose=True)

            else:
                self.notifications['NotEnoughLength'].start()

        elif char in ascii_uppercase:
            self.handle_sound('key', 'play')

            if len_ln < self.word_length:
                self.input_history[ln].append(char)

                if self.input_point[0] < self.word_length - 1:
                    self.input_point[0] += 1

        self.update_correct_tile()

    def handle_popup(self, shortcut_key: str | None, can_inputed: bool) -> None:
        if self.file_game_corrupt and not self.isshow_popup_warn[0]:
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

        if self.buttonHowToPlay.button_event.click or shortcut_key == '1':
            self.handle_sound('click', 'play')
            self.popup.edit_param(type='how-to-play')
            self.popup()

        elif self.buttonStats.button_event.click or shortcut_key == '2':
            self.handle_sound('click', 'play')
            self.popup.edit_param(type='stats')
            self.popup()

        elif self.buttonDailyCoins.button_event.click or shortcut_key == '7':

            def take_coins() -> None:
                if self.get_daily_countdown() is True:
                    self.coins                        += const.DAILY_COINS
                    self.game_data['prize-claim-time'] = self.get_datetime()
                    self.save_game(prize_taken=True)

            self.handle_sound('click', 'play')
            self.popup.edit_param(type='daily-coins', take_coins_function=take_coins)
            self.popup()

        elif shortcut_key == '6':
            self.handle_sound('click', 'play')
            self.showLogs()

        elif (self.buttonAutoWrite.button_event.click or shortcut_key == '3') and can_inputed:
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

        elif (self.buttonLetterHint.button_event.click or shortcut_key == '8') and can_inputed:
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

                        letter = self.selected_word[len(self.hint_tile) if len(self.hint_tile) < self.word_length - 1 else -1]

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
                        self.notifications['AllTileHintsProvided'].start()

        elif (self.buttonKeyboardHint.button_event.click or shortcut_key == '9') and self.show_keyboard and can_inputed:
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
                        self.notifications['AllKeyboardHintsProvided'].start()

        elif (self.buttonDeletedEntry.button_event.click or shortcut_key == '0') and can_inputed:
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
                    self.input_history    .pop(-2)
                    self.input_history[-1].clear()
                    self.feedback_history .pop()

                    self.guess_count    += 1
                    self.input_point[0]  = 0
                    self.input_point[1] -= 1

                    self.coins -= COINS_PRICE
                    self.save_game(hint_coins_price=COINS_PRICE)

            elif isbuy == 'buy' and self.input_point[1] <= 0:
                self.notifications['TileIsEmpty'].start()

        elif (self.buttonReset.button_event.click or shortcut_key == '4') and self.last_time_reset + const.RESET_DELAY <= self.get_tick() and can_inputed:
            self.handle_sound('click', 'play')
            self.reset()
            self.notifications['Reset'].start()

        elif (self.buttonSettings.button_event.click or shortcut_key == '5') and can_inputed:
            self.handle_sound('click', 'play')
            self.showSettings()
            self.last_time_close_settings = self.get_tick()

    def handle_notification(self) -> None:
        LANG = self.languages['notification']

        notifNotInDictionary          = self.notifications['NotInDictionary']
        notifNotEnoughLength          = self.notifications['NotEnoughLength']
        notifTileIsEmpty              = self.notifications['TileIsEmpty']
        notifAllKeyboardHintsProvided = self.notifications['AllKeyboardHintsProvided']
        notifAllTileHintsProvided     = self.notifications['AllTileHintsProvided']
        notifStreakEnded              = self.notifications['StreakEnded']
        notifWin                      = self.notifications['Win']
        notifLose                     = self.notifications['Lose']
        notifReset                    = self.notifications['Reset']
        notifUnfullscreen             = self.notifications['Unfullscreen']

        if notifWin.is_visible:
            notifWin.text = LANG['win']

            size                    = 500 * self.geomatry
            sizescreen              = self.screen.get_size()
            self.confetti_rect.left = const.math.get_center(sizescreen[0], size)
            self.confetti_rect.top  = sizescreen[1] - size

            if self.play_lose_or_win != 2:
                self.play_lose_or_win = 1
            if self.play_lose_or_win == 1:
                self.handle_sound('win', 'play')
                self.gif_win.reset_frame()
                self.play_lose_or_win = 2

            self.gif_win.draw_and_update(self.screen)

            notifWin()
            return

        elif notifLose.is_visible:
            notifLose.text = LANG['lose'].replace('<WORD>', self.selected_word, 1)

            if self.play_lose_or_win != 2:
                self.play_lose_or_win = 1
            if self.play_lose_or_win == 1:
                self.handle_sound('lose', 'play')
                self.play_lose_or_win = 2

            notifLose()
            return

        if not self.notifications_layer:
            self.notification_initial_y = 130 * self.geomatry

            notifNotInDictionary         .position_finalized = False
            notifNotEnoughLength         .position_finalized = False
            notifTileIsEmpty             .position_finalized = False
            notifAllKeyboardHintsProvided.position_finalized = False
            notifAllTileHintsProvided    .position_finalized = False
            notifStreakEnded             .position_finalized = False
            notifWin                     .position_finalized = False
            notifLose                    .position_finalized = False
            notifReset                   .position_finalized = False
            notifUnfullscreen            .position_finalized = False

        for notif_layer in self.notifications_layer:

            match notif_layer:

                case 'NotInDictionary':
                    if self.search_correct and self.word_corrector:
                        notifNotInDictionary.text = (
                            LANG['not-in-dictionary-corrector']
                                .replace('<WORD>',           self.last_word_input, 1)
                                .replace('<WORD-CORRECTOR>', self.search_correct,  1)
                        )
                    else:
                        notifNotInDictionary.text = LANG['not-in-dictionary'].replace('<WORD>', self.last_word_input, 1)
                    notifNotInDictionary()

                case 'NotEnoughLength':
                    notifNotEnoughLength.text = LANG['less-letter-length']
                    notifNotEnoughLength()

                case 'AllTileHintsProvided':
                    notifAllTileHintsProvided.text = LANG['tile-hint-provided']
                    notifAllTileHintsProvided()

                case 'AllKeyboardHintsProvided':
                    notifAllKeyboardHintsProvided.text = LANG['keyboard-hint-provided']
                    notifAllKeyboardHintsProvided()

                case 'TileIsEmpty':
                    notifTileIsEmpty.text = LANG['tile-empty']
                    notifTileIsEmpty()

                case 'StreakEnded':
                    notifStreakEnded.text = LANG['streak-ended']
                    notifStreakEnded()

                case 'Reset':
                    notifReset.text = LANG['reset']
                    notifReset()

                case 'Unfullscreen':
                    notifUnfullscreen.text = LANG['unfullscreen']
                    notifUnfullscreen()

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
        LANG = self.languages['text-bar']

        sizescreen = self.screen.get_size()
        text       = self.font_textbar.render(
            '{} | {} | {} | {}'.format(
                self.__label_version__,
                LANG['word']               .replace('<WORD-ID>',    self.language_word.upper(), 1),
                LANG['valid-word']['label'].replace('<VALID-WORD>', LANG['valid-word'][str(self.use_valid_word).lower()], 1),
                LANG['fps']                .replace('<FPS>',        self.num_format.parse(self.clock.get_fps()), 1)
            ), True, self.themes['bar-menu']['text'], self.themes['bar-menu']['background']
        )

        text.set_alpha(200)

        textwidth, textheight = text.get_width(), text.get_height()

        self.screen.blit(text, (
            const.math.get_center(sizescreen[0], textwidth),
            sizescreen[1] - textheight - const.math.get_center(sizescreen[1] - self.boardRect_keyboard.bottom, textheight)
        ))

    def showKeyboard(self, letter_typing: const.Optional[str] = None, justshow: bool = False, letter_hovered: const.Optional[str] = None) -> tuple[bool, str | None, bool]:
        sizescreen     = self.screen.get_size()
        margin         = 10 * self.geomatry
        marginlr       = 40 * self.geomatry
        buttonSize     = (50 * self.geomatry, 70 * self.geomatry)
        inputDetected  = (False, None, False)
        max_buttonkey  = ((10 * buttonSize[0] + margin * 9), (3 * buttonSize[1] + margin * 2))
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
            mousePos      = pygame.mouse.get_pos()

            backspace_and_enter_left_pos = {
                const.BACKSPACE: marginlr / 2,
                const.ENTER    : self.boardRect_keyboard.width - marginlr / 2 - (buttonSize[0] + buttonSize[0] / 2 + margin / 2)
            }

            pygame.draw.rect(self.screen, self.themes['keyboard']['background'], self.boardRect_keyboard)

            for row, line in enumerate(keyboards):
                for col, letter in enumerate(line):

                    keyboards_row_length = len(keyboards[row])

                    keyRect = pygame.Rect(
                        self.boardRect_keyboard.left + (const.math.get_center(self.boardRect_keyboard.width,  (keyboards_row_length * buttonSize[0] + margin * (keyboards_row_length - 1))) + (col * (buttonSize[0] + margin)) if letter not in const.ALL_KEY else backspace_and_enter_left_pos[letter]),
                        self.boardRect_keyboard.top  +  const.math.get_center(self.boardRect_keyboard.height, max_buttonkey[1]) + (row * (buttonSize[1] + margin)),
                        buttonSize[0] + buttonSize[0] / 2 + margin / 2 if letter in const.ALL_KEY else buttonSize[0],
                        buttonSize[1]
                    )

                    color       = self.keyboard_feedback[letter.upper()]
                    isMouseOver = keyRect.collidepoint(mousePos)
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
                        self.buttonKeyboard       .draw_and_update()

                        if letter == letter_hovered:
                            inputDetected = (False, None, self.buttonKeyboard.button_event.ismousehover)

                        if self.buttonKeyboard.button_event.click:
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
        wscreen = self.screen.get_width()

        self.margin_tile = 10 * self.geomatry
        self.size_tile   = 80 * self.geomatry

        if self.word_length * self.size_tile + self.margin_tile * (self.word_length - 1) > wscreen - self.margin_tile * 2:
            self.size_tile = (wscreen - self.margin_tile) / self.word_length - self.margin_tile

        if self.last_size_tile != self.size_tile:
            self.font_tile      = pygame.font.Font(self.file.FONT_BAKSOSAPI_REGULAR, int(self.size_tile))
            self.last_size_tile = self.size_tile

        for row in range(self.change_guess):
            for col in range(self.word_length):

                letter      = None
                color       = 'not-inputed'
                pointed     = [col, row] == self.input_point
                blinked     = int(self.get_tick() * 2) % 2 == 0
                tile_active = not (justshow or self.notifications['Win'].is_visible or self.notifications['Lose'].is_visible)

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
                    self.scroller_tile.offset_y + (row * (self.size_tile + self.margin_tile)),
                    self.size_tile,
                    self.size_tile
                )

                if tile_point_preview:
                    outline_color = self.themes['tile']['box']['outline']['point-active' if pointed else 'point-inactive']
                    tile_color    = self.themes['tile']['box']['pointed' if pointed and color == 'not-inputed' else color]
                else:
                    outline_color = self.themes['tile']['box']['outline']['point-active' if pointed and tile_active and blinked else 'point-inactive']
                    tile_color    = self.themes['tile']['box']['pointed' if pointed and tile_active and color == 'not-inputed' else color]

                pygame.draw.rect(self.screen, outline_color, const.math.Rect_outline(tile_rect, 4 * self.geomatry))
                pygame.draw.rect(self.screen, tile_color,    tile_rect)

                if letter is not None:
                    showLetter = self.font_tile.render(letter, True, self.themes['tile']['text'])
                    self.screen.blit(showLetter, showLetter.get_rect(center=tile_rect.center))

    def showBarMenu(self, justshow: bool = False) -> None:
        wscreen = self.screen.get_width()

        barTop_rect    = pygame.Rect(const.math.get_center(wscreen, (wscreen - 10 * self.geomatry)), 5 * self.geomatry,                      wscreen - 10 * self.geomatry, 60 * self.geomatry)
        barBottom_rect = pygame.Rect(barTop_rect.left,                                               barTop_rect.bottom + 5 * self.geomatry, barTop_rect.width,            50 * self.geomatry)

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

        self.buttonHowToPlay   .rect = button_howToPlay_rect
        self.buttonDailyCoins  .rect = button_bag_coin_rect
        self.buttonStats       .rect = button_stats_rect
        self.buttonAutoWrite   .rect = button_auto_write_rect
        self.buttonReset       .rect = button_reset_rect
        self.buttonSettings    .rect = button_settings_rect
        self.buttonLetterHint  .rect = button_lamp_rect
        self.buttonKeyboardHint.rect = button_keyboard_rect
        self.buttonDeletedEntry.rect = button_hammer_rect

        if self.last_geomatry != self.geomatry:
            self.buttonHowToPlay   .image_scale = 2.5 * self.geomatry
            self.buttonDailyCoins  .image_scale = self.buttonHowToPlay.image_scale
            self.buttonStats       .image_scale = self.buttonHowToPlay.image_scale
            self.buttonAutoWrite   .image_scale = self.buttonHowToPlay.image_scale
            self.buttonReset       .image_scale = self.buttonHowToPlay.image_scale
            self.buttonSettings    .image_scale = self.buttonHowToPlay.image_scale
            self.buttonLetterHint  .image_scale = self.buttonHowToPlay.image_scale
            self.buttonDeletedEntry.image_scale = self.buttonHowToPlay.image_scale

            if self.show_keyboard:
                self.buttonKeyboardHint.image_scale = self.buttonHowToPlay.image_scale

        pygame.draw.rect(self.screen, self.themes['bar-menu']['background'], barTop_rect)
        pygame.draw.rect(self.screen, self.themes['bar-menu']['background'], barBottom_rect)

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
            pygame.draw.circle(self.screen, self.themes['bar-menu']['indicator'], (button_bag_coin_rect.right, button_bag_coin_rect.top), radius=7 * self.geomatry)

        showKatla = self.font_katla.render(f'KATLA #{self.word_length}',      True, self.themes['bar-menu']['text'])
        showCoins = self.font_coins.render(self.num_format.parse(self.coins), True, self.themes['bar-menu']['text'])

        showKatla_rect = showKatla.get_rect(center=barTop_rect.center)

        if button_stats_rect.right < showKatla_rect.left and button_auto_write_rect.left > showKatla_rect.right:
            self.screen.blit(showKatla, showKatla_rect)

        self.screen.blit(showCoins, (button_bag_coin_rect.right + 20 * self.geomatry, button_bag_coin_rect.top + const.math.get_center(button_bag_coin_rect.height, showCoins.get_height())))

    def showFreezeKatla(self, tile_point_preview: bool = False) -> None:
        self.scroller_tile.min_max_scrolled = (-((self.size_tile + self.margin_tile) * (self.change_guess - 1) - self.margin_tile / 2), self.screen.get_height() - (self.size_tile + self.margin_tile / 2))

        self.scroller_tile.update(anchor=True)

        self.screen.fill(self.themes['screen'])

        self.showTile    (justshow=True, tile_point_preview=tile_point_preview)
        self.showBarMenu (justshow=True)
        self.showKeyboard(justshow=True)
        self.showTextBar ()

        self.handle_notification()

        self.save_game_periodically()

    def showLogs(self) -> None:
        self.isshow_Logs = True

        LANG = self.languages['logs']

        close_button = Button(
            surface_screen  = self.screen,
            rect            = self.init_rect,
            image           = self.image_close,
            outline_size    = 4 * self.geomatry,
            color           = button_color(
                self.themes['logs']['button']['inactive'],
                self.themes['logs']['button']['active'],
                self.themes['logs']['button']['hover']
            ),
            outline_color   = self.single_color_button(self.themes['logs']['button']['outline']),
            inactive_cursor = pygame.SYSTEM_CURSOR_ARROW,
            active_cursor   = pygame.SYSTEM_CURSOR_HAND,
            only_click      = 'l'
        )

        font_log  = pygame.font.Font(self.file.FONT_ROBOTO_MONO_REGULAR, int(15 * self.geomatry))
        font_warn = pygame.font.Font(self.file.FONT_ROBOTO_MONO_BOLD,    int(20 * self.geomatry))

        height_font = font_log.size(const.HELLO)[1]

        warnings         = 0
        errors           = 0
        last_size_screen = (0, 0)
        wraped_text      = []
        last_message     = []

        while self.isshow_Logs:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running         = False
                    self.isshow_Logs     = False
                    self.isshow_Settings = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isshow_Logs = False

                self.handle_screen_resize(event)

                self.scroller_logs.handle_event(event)

                close_button.handle_event(event)

            screen_size = self.screen.get_size()

            close_rect         = pygame.Rect(screen_size[0] - 70 * self.geomatry, screen_size[1] - 70 * self.geomatry, 50 * self.geomatry, 50 * self.geomatry)
            background_surface = pygame.Surface(screen_size)

            background_surface.fill(self.themes['logs']['background'])
            background_surface.set_alpha(150)

            close_button.edit_param(rect=close_rect, image_scale=5 * self.geomatry)

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

                    match line_type:

                        case 'warn':
                            warnings += 1
                        case 'error':
                            errors += 1

                    text_wrap = wrap_text(font_log, stringinfo, screen_size[0] - 10 * self.geomatry, 'mono')

                    for line_wrap in text_wrap:
                        wraped_text.append({'line': line_wrap, 'type': line_type})

                last_size_screen = screen_size

            log_summary_text = font_warn.render("{}: {} | {}: {} | {}, {}: {}, {}".format(
                    LANG['warnings'],
                    self.num_format.parse(warnings),
                    LANG['errors'],
                    self.num_format.parse(errors),
                    LANG['total'],
                    LANG['lines'],
                    self.num_format.parse(len(logs.messages)),
                    self.num_format.parse(len(wraped_text))
                ), True, self.themes['logs']['text']['label-color'], self.themes['logs']['text']['label-background']
            )

            self.scroller_logs.min_max_scrolled = (-max(len(wraped_text) * height_font + close_rect.width + 10 * self.geomatry - self.screen.get_height(), 0), 0)

            visible_start = int(abs(self.scroller_logs.offset_y) // height_font)
            visible_end   = int(visible_start + (screen_size[1] // height_font))

            self.scroller_logs.update(anchor_drag=close_button.button_event.ismousehover)

            self.screen.blit(background_surface, (0, 0))

            for i in range(visible_start, min(visible_end + 1, len(wraped_text))):
                ln     = wraped_text[i]
                text   = ln['line']
                typeln = ln['type']

                surface_text = font_log.render(text, True, self.themes['logs']['text'][typeln])

                self.screen.blit(surface_text, (
                    5 * self.geomatry,
                    (self.scroller_logs.offset_y + i * surface_text.get_height()) + 5 * self.geomatry
                ))

            close_button.draw_and_update()

            self.screen.blit(log_summary_text, (5 * self.geomatry, screen_size[1] - (5 * self.geomatry) - log_summary_text.get_height()))

            if close_button.button_event.click:
                self.handle_sound('click', 'play')
                self.isshow_Logs = False

            pygame.display.flip()

            self.clock.tick(self.fps)

    def showSettings(self) -> None:
        self.isshow_Settings = True

        LANG = self.languages['settings']

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
        word_corrector  = self.settings['word-corrector']

        languages_id_list       = self.validator_languages      .get_lang_id ()
        theme_id_list           = self.validator_themes         .get_theme_id()
        languages_word_id_list  = self.validator_word_dictionary.get_lang_id ()
        language_name_list      = self.validator_languages      .get_lang_name()
        language_word_name_list = self.validator_word_dictionary.get_lang_name()

        index_lang_word       = languages_word_id_list.index(language_word)
        index_lang            = languages_id_list     .index(language)
        index_theme           = theme_id_list         .index(theme)
        index_keyboard_layout = const.Keyboard.__all__.index(keyboard_layout)

        last_configuration  = [index_theme, index_keyboard_layout, sound_volume, music_volume, change_guess, word_length, fps, geomatry, index_lang, index_lang_word, use_valid_word, show_keyboard, word_corrector]
        first_configuration = last_configuration.copy()

        background_rect      = self.init_rect.copy()
        navbar_rect          = self.init_rect.copy()
        last_background_rect = self.init_rect.copy()

        font_title       = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,      int(35 * self.geomatry))
        font_license     = pygame.font.Font(self.file.FONT_ROBOTO_MONO_BOLD, int(15 * self.geomatry))
        label_group_font = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,      int(32 * self.geomatry))
        label_font       = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(25 * self.geomatry))
        nav_font         = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(35 * self.geomatry))
        font1            = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,    int(30 * self.geomatry))

        surface_title = font_title.render(LANG['title'], True, self.themes['settings']['text'])

        buttonClose = Button(
            surface_screen = self.screen,
            rect           = self.init_rect,
            hide           = True,
            image          = self.image_close,
            image_scale    = 0,
            click_speed    = 0
        )
        buttonLang = Button(
            surface_screen = self.screen,
            rect           = self.init_rect,
            font           = label_font,
            outline_size   = 4 * self.geomatry,
            text_color     = self.single_color_button(self.themes['settings']['text']),
            color          = button_color(
                self.themes['settings']['button']['set']['inactive'],
                self.themes['settings']['button']['set']['active'],
                self.themes['settings']['button']['set']['hover']
            ),
            outline_color  = self.single_color_button(self.themes['settings']['outline']),
            only_click     = 'rl',
            click_speed    = 500
        )
        buttonLangWord        = buttonLang      .copy()
        buttonOxfordWord      = buttonLang      .copy(only_click='l', click_speed=50)
        buttonCorrector       = buttonOxfordWord.copy()
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

        words_len    = len(self.words_list)
        wrap_license = pygame.Surface((0, 0))

        def update_wrap_license() -> None:
            nonlocal wrap_license
            wrap_license = render_wrap(font_license, self.__license__, background_rect.width - 10 * self.geomatry, True, self.themes['settings']['text'])

        def label(label_text: str, type: const.Literal['group', 'label'], index: const.Number) -> None:
            match type:

                case 'group':
                    surface_text = label_group_font.render(label_text, True, self.themes['settings']['text'])

                case 'label':
                    surface_text = label_font.render(label_text, True, self.themes['settings']['text'])

            self.screen.blit(surface_text, (background_rect.left + 10 * self.geomatry, index))

        def button_edit(button_edit_param: Button, button_get_param: Button, kw: dict | None = None) -> None:
            button_edit_param.edit_param(**((button_get_param.get_param() | kw) if kw is not None else button_get_param.get_param()))

        def button_edit_switch(button_edit_param: Button, var: bool) -> None:
            color = self.themes['settings']['button']['switch'][str(var).lower()]

            button_edit_param.edit_param(
                color = button_color(
                    color['inactive'],
                    color['active'],
                    color['hover']
                ),
                **({
                    'image': self.image_check,
                    'image_scale': 5 * self.geomatry
                } if var else {
                    'image': None,
                    'image_scale': None
                })
            )

        def ternary(condination: bool, expression1: const.Any, expression2: const.Any) -> const.Any:
            return expression1 if bool(condination) else expression2

        nfgeomatry = NumberFormat(self.languages['exponents-number'], decimal_places=1, rounded=False, anchor_decimal_places=True, reach=(3, 'thousand'))

        if not self.init_mixer:
            rangeSound.alpha_transparency = 140
            rangeMusic.alpha_transparency = 140

        while self.isshow_Settings:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                    self.isshow_Settings = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isshow_Settings = False

                self.handle_screen_resize(event)

                self.scroller_settings.handle_event(event)

                buttonClose               .handle_event(event)
                buttonLang                .handle_event(event)
                buttonLangWord            .handle_event(event)
                buttonCorrector           .handle_event(event)
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

            self.scroller_settings.min_max_scrolled = (-max(1250 * self.geomatry + wrap_license.get_height() - self.screen.get_height(), 0), 0)

            mouse_pos  = pygame.mouse.get_pos()
            sizescreen = self.screen.get_size()

            self.scroller_settings.update(anchor_drag=(
                not background_rect       .collidepoint(mouse_pos)   or
                navbar_rect               .collidepoint(mouse_pos)   or
                rangeSound                .button_event.israngehover or
                rangeMusic                .button_event.israngehover or
                buttonLang                .button_event.ismousehover or
                buttonLangWord            .button_event.ismousehover or
                buttonOxfordWord          .button_event.ismousehover or
                buttonCorrector           .button_event.ismousehover or
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

            g40  = 40 * self.geomatry
            g50  = 50 * self.geomatry
            g150 = 150 * self.geomatry
            g250 = 250 * self.geomatry

            br45  = background_rect.right - 45 * self.geomatry
            br95  = background_rect.right - 95 * self.geomatry
            br145 = background_rect.right - 145 * self.geomatry
            br155 = background_rect.right - 155 * self.geomatry
            br205 = background_rect.right - 205 * self.geomatry
            br255 = background_rect.right - 255 * self.geomatry
            br305 = background_rect.right - 305 * self.geomatry
            br355 = background_rect.right - 355 * self.geomatry

            background_rect        = pygame.Rect(const.math.get_center(sizescreen[0], sizescreen[0] - 100 * self.geomatry), 0,                                        sizescreen[0] - 100 * self.geomatry, sizescreen[1])
            buttonClose.rect       = pygame.Rect(background_rect.right - g50,                                               background_rect.top + 10 * self.geomatry, g40,                                 g40)
            navbar_rect            = pygame.Rect(background_rect.left,                                                      background_rect.top,                      background_rect.width,               buttonClose.rect.bottom + 10 * self.geomatry)
            mainBackground_rect    = const.math.Rect_outline(background_rect, 10 * self.geomatry)
            mainBackground_surface = pygame.Surface((mainBackground_rect.width, mainBackground_rect.height))
            background_surface     = pygame.Surface((background_rect.width,     mainBackground_rect.height))

            buttonLang                .rect = pygame.Rect(br255, self.scroller_settings.offset_y + navbar_rect.bottom + 60 * self.geomatry,   g250, g50)
            buttonLangWord            .rect = pygame.Rect(br255, self.scroller_settings.offset_y + navbar_rect.bottom + 120 * self.geomatry,  g250, g50)
            buttonOxfordWord          .rect = pygame.Rect(br45,  self.scroller_settings.offset_y + navbar_rect.bottom + 435 * self.geomatry,  g40,  g40)
            buttonCorrector           .rect = pygame.Rect(br45,  self.scroller_settings.offset_y + navbar_rect.bottom + 485 * self.geomatry,  g40,  g40)
            buttonWordLen             .rect = pygame.Rect(br45,  self.scroller_settings.offset_y + navbar_rect.bottom + 535 * self.geomatry,  g40,  g40)
            buttonChangeGuess         .rect = pygame.Rect(br45,  self.scroller_settings.offset_y + navbar_rect.bottom + 585 * self.geomatry,  g40,  g40)
            buttonShowKeyboard        .rect = pygame.Rect(br45,  self.scroller_settings.offset_y + navbar_rect.bottom + 715 * self.geomatry,  g40,  g40)
            buttonTypeKeyboard        .rect = pygame.Rect(br155, self.scroller_settings.offset_y + navbar_rect.bottom + 765 * self.geomatry,  g150, g50)
            buttonTheme               .rect = pygame.Rect(br155, self.scroller_settings.offset_y + navbar_rect.bottom + 825 * self.geomatry,  g150, g50)
            buttonGeomatry            .rect = pygame.Rect(br155, self.scroller_settings.offset_y + navbar_rect.bottom + 965 * self.geomatry,  g150, g50)
            buttonFps                 .rect = pygame.Rect(br155, self.scroller_settings.offset_y + navbar_rect.bottom + 1025 * self.geomatry, g150, g50)
            buttonLogs                .rect = pygame.Rect(br255, self.scroller_settings.offset_y + navbar_rect.bottom + 1085 * self.geomatry, g250, g50)
            buttonNav_lang['l']       .rect = pygame.Rect(br355, self.scroller_settings.offset_y + navbar_rect.bottom + 65 * self.geomatry,   g40,  g40)
            buttonNav_lang['r']       .rect = pygame.Rect(br305, self.scroller_settings.offset_y + navbar_rect.bottom + 65 * self.geomatry,   g40,  g40)
            buttonNav_langword['l']   .rect = pygame.Rect(br355, self.scroller_settings.offset_y + navbar_rect.bottom + 125 * self.geomatry,  g40,  g40)
            buttonNav_langword['r']   .rect = pygame.Rect(br305, self.scroller_settings.offset_y + navbar_rect.bottom + 125 * self.geomatry,  g40,  g40)
            buttonNav_wordlen['l']    .rect = pygame.Rect(br145, self.scroller_settings.offset_y + navbar_rect.bottom + 535 * self.geomatry,  g40,  g40)
            buttonNav_wordlen['r']    .rect = pygame.Rect(br95,  self.scroller_settings.offset_y + navbar_rect.bottom + 535 * self.geomatry,  g40,  g40)
            buttonNav_changeguess['l'].rect = pygame.Rect(br145, self.scroller_settings.offset_y + navbar_rect.bottom + 585 * self.geomatry,  g40,  g40)
            buttonNav_changeguess['r'].rect = pygame.Rect(br95,  self.scroller_settings.offset_y + navbar_rect.bottom + 585 * self.geomatry,  g40,  g40)
            buttonNav_typekeyb['l']   .rect = pygame.Rect(br255, self.scroller_settings.offset_y + navbar_rect.bottom + 770 * self.geomatry,  g40,  g40)
            buttonNav_typekeyb['r']   .rect = pygame.Rect(br205, self.scroller_settings.offset_y + navbar_rect.bottom + 770 * self.geomatry,  g40,  g40)
            buttonNav_theme['l']      .rect = pygame.Rect(br255, self.scroller_settings.offset_y + navbar_rect.bottom + 830 * self.geomatry,  g40,  g40)
            buttonNav_theme['r']      .rect = pygame.Rect(br205, self.scroller_settings.offset_y + navbar_rect.bottom + 830 * self.geomatry,  g40,  g40)
            buttonNav_geomarty['l']   .rect = pygame.Rect(br255, self.scroller_settings.offset_y + navbar_rect.bottom + 970 * self.geomatry,  g40,  g40)
            buttonNav_geomarty['r']   .rect = pygame.Rect(br205, self.scroller_settings.offset_y + navbar_rect.bottom + 970 * self.geomatry,  g40,  g40)
            buttonNav_fps['l']        .rect = pygame.Rect(br255, self.scroller_settings.offset_y + navbar_rect.bottom + 1030 * self.geomatry, g40,  g40)
            buttonNav_fps['r']        .rect = pygame.Rect(br205, self.scroller_settings.offset_y + navbar_rect.bottom + 1030 * self.geomatry, g40,  g40)
            rangeSound                .rect = pygame.Rect(background_rect.right - 315 * self.geomatry, self.scroller_settings.offset_y + navbar_rect.bottom + 270 * self.geomatry,  300 * self.geomatry,   14 * self.geomatry)
            rangeMusic                .rect = pygame.Rect(rangeSound.rect.left,                        self.scroller_settings.offset_y + navbar_rect.bottom + 320 * self.geomatry,  rangeSound.rect.width, rangeSound.rect.height)

            buttonLang        .text = language_name_list[index_lang]
            buttonLangWord    .text = language_word_name_list[index_lang_word]
            buttonWordLen     .text = word_length
            buttonChangeGuess .text = change_guess
            buttonTheme       .text = LANG['display']['buttons-label']['app-theme'][theme]
            buttonTypeKeyboard.text = keyboard_layout
            buttonGeomatry    .text = nfgeomatry.parse(geomatry / 10) + 'x'
            buttonFps         .text = fps
            buttonLogs        .text = LANG['additional-settings']['label']['logs']['button-label']

            if self.init_mixer:
                rangeSound.thumb_size = (20 * self.geomatry, 20 * self.geomatry)
                rangeMusic.thumb_size = rangeSound.thumb_size

            button_edit_switch(buttonOxfordWord,   use_valid_word)
            button_edit_switch(buttonCorrector,    word_corrector)
            button_edit_switch(buttonShowKeyboard, show_keyboard)

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
                buttonCorrector,
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

            sepLine = (const.math.get_center(sizescreen[0], background_rect.width - 30 * self.geomatry), background_rect.width - 30 * self.geomatry, 4 * self.geomatry)

            pygame.draw.rect(self.screen, self.themes['settings']['outline'], (sepLine[0], self.scroller_settings.offset_y + navbar_rect.bottom + 185 * self.geomatry,  sepLine[1], sepLine[2]))
            pygame.draw.rect(self.screen, self.themes['settings']['outline'], (sepLine[0], self.scroller_settings.offset_y + navbar_rect.bottom + 365 * self.geomatry,  sepLine[1], sepLine[2]))
            pygame.draw.rect(self.screen, self.themes['settings']['outline'], (sepLine[0], self.scroller_settings.offset_y + navbar_rect.bottom + 640 * self.geomatry,  sepLine[1], sepLine[2]))
            pygame.draw.rect(self.screen, self.themes['settings']['outline'], (sepLine[0], self.scroller_settings.offset_y + navbar_rect.bottom + 890 * self.geomatry,  sepLine[1], sepLine[2]))
            pygame.draw.rect(self.screen, self.themes['settings']['outline'], (sepLine[0], self.scroller_settings.offset_y + navbar_rect.bottom + 1150 * self.geomatry, sepLine[1], sepLine[2]))

            if not navbar_rect.collidepoint(mouse_pos):
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
                buttonCorrector           .draw_and_update()
                buttonWordLen             .draw_and_update()
                buttonChangeGuess         .draw_and_update()
                buttonTheme               .draw_and_update()
                buttonShowKeyboard        .draw_and_update()
                buttonGeomatry            .draw_and_update()
                buttonFps                 .draw_and_update()
                buttonLogs                .draw_and_update()

                if show_keyboard:
                    buttonTypeKeyboard.alpha_transparency = 255

                    buttonTypeKeyboard     .draw_and_update()
                    buttonNav_typekeyb['l'].draw_and_update()
                    buttonNav_typekeyb['r'].draw_and_update()
                else:
                    buttonTypeKeyboard.alpha_transparency = 140

                    buttonTypeKeyboard.draw_inactive()

                if self.init_mixer and not self.scroller_settings.scroller_event.isdragging:
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
                buttonCorrector           .draw_inactive()
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

            label(LANG['languages']['title'],                            'group', self.scroller_settings.offset_y + navbar_rect.bottom + 10 * self.geomatry)
            label(LANG['languages']['label']['app-language'],            'label', self.scroller_settings.offset_y + navbar_rect.bottom + 70 * self.geomatry)
            label(LANG['languages']['label']['word-language'],           'label', self.scroller_settings.offset_y + navbar_rect.bottom + 130 * self.geomatry)

            label(LANG['sounds']['title'],                               'group', self.scroller_settings.offset_y + navbar_rect.bottom + 210 * self.geomatry)
            label(LANG['sounds']['label']['sound'],                      'label', self.scroller_settings.offset_y + navbar_rect.bottom + 262.5 * self.geomatry)
            label(LANG['sounds']['label']['music'],                      'label', self.scroller_settings.offset_y + navbar_rect.bottom + 312.5 * self.geomatry)

            label(LANG['game-rules']['title'],                           'group', self.scroller_settings.offset_y + navbar_rect.bottom + 390 * self.geomatry)
            label(LANG['game-rules']['label']['only-in-dictionary'],     'label', self.scroller_settings.offset_y + navbar_rect.bottom + 440 * self.geomatry)
            label(LANG['game-rules']['label']['word-correction'],        'label', self.scroller_settings.offset_y + navbar_rect.bottom + 490 * self.geomatry)
            label(LANG['game-rules']['label']['word-length']
                .replace('<WORDS-LENGTH>',
                    self.num_format.parse(words_len), 1),                'label', self.scroller_settings.offset_y + navbar_rect.bottom + 540 * self.geomatry)
            label(LANG['game-rules']['label']['change-guess'],           'label', self.scroller_settings.offset_y + navbar_rect.bottom + 590 * self.geomatry)

            label(LANG['display']['title'],                              'group', self.scroller_settings.offset_y + navbar_rect.bottom + 665 * self.geomatry)
            label(LANG['display']['label']['show-keyboard'],             'label', self.scroller_settings.offset_y + navbar_rect.bottom + 720 * self.geomatry)
            label(LANG['display']['label']['keyboard-layout'],           'label', self.scroller_settings.offset_y + navbar_rect.bottom + 775 * self.geomatry)
            label(LANG['display']['label']['app-theme'],                 'label', self.scroller_settings.offset_y + navbar_rect.bottom + 835 * self.geomatry)

            label(LANG['additional-settings']['title'],                  'group', self.scroller_settings.offset_y + navbar_rect.bottom + 915 * self.geomatry)
            label(LANG['additional-settings']['label']['geomatry'],      'label', self.scroller_settings.offset_y + navbar_rect.bottom + 975 * self.geomatry)
            label(LANG['additional-settings']['label']['fps'],           'label', self.scroller_settings.offset_y + navbar_rect.bottom + 1035 * self.geomatry)
            label(LANG['additional-settings']['label']['logs']['label'], 'label', self.scroller_settings.offset_y + navbar_rect.bottom + 1095 * self.geomatry)

            self.screen.blit(wrap_license, (background_rect.left + 5, self.scroller_settings.offset_y + 1240 * self.geomatry))

            pygame.draw.rect(self.screen, self.themes['settings']['navbar'], navbar_rect)

            buttonClose.draw_and_update()

            self.screen.blit(surface_title, surface_title.get_rect(center=navbar_rect.center))

            if rangeSound.button_event.click:
                sound_volume = rangeSound.button_event.range_value
            if rangeMusic.button_event.click:
                music_volume = rangeMusic.button_event.range_value

            if (clk := buttonLang.button_event.click) or buttonNav_lang['l'].button_event.click or buttonNav_lang['r'].button_event.click:
                self.handle_sound('click', 'play')
                index_lang = (index_lang + ternary(clk == 'l' or buttonNav_lang['r'].button_event.click, 1, -1)) % len(languages_id_list)

            elif (clk := buttonLangWord.button_event.click) or buttonNav_langword['l'].button_event.click or buttonNav_langword['r'].button_event.click:
                self.handle_sound('click', 'play')
                index_lang_word = (index_lang_word + ternary(clk == 'l' or buttonNav_langword['r'].button_event.click, 1, -1)) % len(languages_word_id_list)

            elif buttonOxfordWord.button_event.click:
                self.handle_sound('click', 'play')
                use_valid_word = not use_valid_word

            elif buttonCorrector.button_event.click:
                self.handle_sound('click', 'play')
                word_corrector = not word_corrector

            elif (clk := buttonWordLen.button_event.click) or buttonNav_wordlen['l'].button_event.click or buttonNav_wordlen['r'].button_event.click:
                self.handle_sound('click', 'play')
                word_length += ternary(clk == 'l' or buttonNav_wordlen['r'].button_event.click, 1, -1)

            elif (clk := buttonChangeGuess.button_event.click) or buttonNav_changeguess['l'].button_event.click or buttonNav_changeguess['r'].button_event.click:
                self.handle_sound('click', 'play')
                change_guess += ternary(clk == 'l' or buttonNav_changeguess['r'].button_event.click, 1, -1)

            elif buttonShowKeyboard.button_event.click:
                self.handle_sound('click', 'play')
                show_keyboard = not show_keyboard
                if show_keyboard:
                    self.buttonKeyboardHint.image_scale = self.buttonHowToPlay.image_scale

            elif (clk := buttonTypeKeyboard.button_event.click) or buttonNav_typekeyb['l'].button_event.click or buttonNav_typekeyb['r'].button_event.click:
                self.handle_sound('click', 'play')
                index_keyboard_layout = (index_keyboard_layout + ternary(clk == 'l' or buttonNav_typekeyb['r'].button_event.click, 1, -1)) % len(const.Keyboard.__all__)

            elif (clk := buttonTheme.button_event.click) or buttonNav_theme['l'].button_event.click or buttonNav_theme['r'].button_event.click:
                self.handle_sound('click', 'play')
                index_theme = (index_theme + ternary(clk == 'l' or buttonNav_theme['r'].button_event.click, 1, -1)) % len(theme_id_list)

            elif (clk := buttonFps.button_event.click) or buttonNav_fps['l'].button_event.click or buttonNav_fps['r'].button_event.click:
                self.handle_sound('click', 'play')
                fps += ternary(clk == 'l' or buttonNav_fps['r'].button_event.click, const.STEP_FPS, -const.STEP_FPS)

            elif (clk := buttonGeomatry.button_event.click) or buttonNav_geomarty['l'].button_event.click or buttonNav_geomarty['r'].button_event.click:
                self.handle_sound('click', 'play')
                geomatry += ternary(clk == 'l' or buttonNav_geomarty['r'].button_event.click, 1, -1)

            if buttonClose.button_event.click:
                self.handle_sound('click', 'play')
                self.isshow_Settings = False

            elif buttonLogs.button_event.click:
                self.handle_sound('click', 'play')
                self.showLogs()

            if last_background_rect.width != background_rect.width:
                update_wrap_license()
                last_background_rect = background_rect.copy()

            if last_configuration != [index_theme, index_keyboard_layout, sound_volume, music_volume, change_guess, word_length, fps, geomatry, index_lang, index_lang_word, use_valid_word, show_keyboard, word_corrector]:

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
                self.settings['word-corrector']  = self.word_corrector  = word_corrector

                self.set_volume()

                if [last_configuration[0], last_configuration[7], last_configuration[8]] != [index_theme, geomatry, index_lang]:
                    self.languages = self.validator_languages.load(self.language)
                    self.themes    = self.validator_themes   .load(self.theme)

                    LANG = self.languages['settings']

                    self.num_format = NumberFormat(self.languages['exponents-number'], decimal_places=2, rounded=False, reach=(3, 'thousand'))
                    nfgeomatry      = NumberFormat(self.languages['exponents-number'], decimal_places=1, rounded=False, anchor_decimal_places=True, reach=(3, 'thousand'))

                    self.font_textbar      = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(20 * self.geomatry))
                    self.font_keyboard     = pygame.font.Font(self.file.FONT_BAKSOSAPI_REGULAR, int(35 * self.geomatry))
                    self.font_katla        = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,       int(40 * self.geomatry))
                    self.font_coins        = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(35 * self.geomatry))
                    self.font_notification = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(30 * self.geomatry))
                    font_license           = pygame.font.Font(self.file.FONT_ROBOTO_MONO_BOLD,  int(15 * self.geomatry))
                    label_group_font       = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,       int(32 * self.geomatry))
                    label_font             = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(25 * self.geomatry))
                    nav_font               = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(35 * self.geomatry))
                    font_title             = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,       int(35 * self.geomatry))
                    font1                  = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(30 * self.geomatry))

                    images = self.file.Images(self.themes['icon-color'])

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

                    buttonClose.edit_param(image=self.image_close)
                    buttonLang .edit_param(
                        font          = label_font,
                        outline_size  = 4 * self.geomatry,
                        text_color    = self.single_color_button(self.themes['settings']['text']),
                        color         = button_color(
                            self.themes['settings']['button']['set']['inactive'],
                            self.themes['settings']['button']['set']['active'],
                            self.themes['settings']['button']['set']['hover']
                        ),
                        outline_color = self.single_color_button(self.themes['settings']['outline']),
                        click_speed   = 500
                    )
                    button_edit(buttonOxfordWord,           buttonLang, {'text': '', 'only_click': 'l', 'click_speed': 100})
                    button_edit(buttonCorrector,            buttonOxfordWord)
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

                    update_wrap_license()

                    surface_title = font_title.render(LANG['title'], True, self.themes['settings']['text'])
                    self.buttonKeyboard = Button(
                        surface_screen = self.screen,
                        rect           = self.buttonKeyboard.rect,
                        text_color     = self.single_color_button(self.themes['keyboard']['text']),
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

                    self.popup.refresh()
                    for notif in self.notifications:
                        self.notifications[notif].refresh()

                    self.buttonHowToPlay   .image_scale = 2.5 * self.geomatry
                    self.buttonDailyCoins  .image_scale = self.buttonHowToPlay.image_scale
                    self.buttonStats       .image_scale = self.buttonHowToPlay.image_scale
                    self.buttonAutoWrite   .image_scale = self.buttonHowToPlay.image_scale
                    self.buttonReset       .image_scale = self.buttonHowToPlay.image_scale
                    self.buttonSettings    .image_scale = self.buttonHowToPlay.image_scale
                    self.buttonLetterHint  .image_scale = self.buttonHowToPlay.image_scale
                    self.buttonDeletedEntry.image_scale = self.buttonHowToPlay.image_scale

                    if self.show_keyboard:
                        self.buttonKeyboardHint.image_scale = self.buttonHowToPlay.image_scale

                if last_configuration[9] != index_lang_word:
                    self.validator_word_dictionary = WordsValidator(language_word)
                    self.word_dictionary           = self.validator_word_dictionary.load_and_validation()

                if [change_guess, word_length, index_lang_word, use_valid_word, word_corrector] != [last_configuration[4], last_configuration[5], last_configuration[9], last_configuration[10], last_configuration[12]]:
                    self.reset()
                    words_len = len(self.words_list)

                last_configuration = [index_theme, index_keyboard_layout, sound_volume, music_volume, change_guess, word_length, fps, geomatry, index_lang, index_lang_word, use_valid_word, show_keyboard, word_corrector]

            pygame.display.flip()

            self.clock.tick(self.fps)

        if first_configuration != last_configuration:
            self.validator_settings.encrypt_data(self.settings)

    def Appmainloop(self) -> None:
        last_time_backspace = self.get_tick()

        pressed_backspace = False
        hold_backspace    = False
        pressed_key       = False
        mouse_up          = False
        in_keyboard_rect  = True
        last_letter       = None

        self.handle_sound('backsound', 'play')

        while self.running:

            keyboard_letter = None
            shortcut_key    = None
            can_inputed     = not (
                self.notifications['Win'].is_visible or
                self.notifications['Lose'].is_visible or
                self.last_time_close_settings + const.POST_SETTINGS_DELAY > self.get_tick()
            )

            sizescreen = self.screen.get_size  ()
            mouse_pos  = pygame.mouse.get_pos  ()
            getkeys    = pygame.key.get_pressed()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        in_keyboard_rect = self.boardRect_keyboard.collidepoint(mouse_pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_up = True

                self.handle_screen_resize(event)

                self.scroller_tile.handle_event(event)

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

            barTop_rect = pygame.Rect(
                const.math.get_center(sizescreen[0], sizescreen[0] - 10 * self.geomatry),
                5 * self.geomatry,
                sizescreen[0] - 10 * self.geomatry,
                115 * self.geomatry
            )

            self.scroller_tile.min_max_scrolled = (-((self.size_tile + self.margin_tile) * (self.change_guess - 1) - self.margin_tile / 2), sizescreen[1] - (self.size_tile + self.margin_tile / 2))

            self.scroller_tile.update(anchor_drag=(self.boardRect_keyboard.collidepoint(mouse_pos) if self.show_keyboard else False) or barTop_rect.collidepoint(mouse_pos))

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

            self.save_game_periodically()

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

                    if get_k_backspace:
                        self.handle_input(const.BACKSPACE)
                    elif in_keyboard_rect:
                        self.handle_input(const.BACKSPACE)

                    continue

            else:
                pressed_backspace = False

            if click_detected and not pressed_key and can_inputed:
                last_letter = keyboard_visual_letter
                pressed_key = True

            elif not click_detected and pressed_key and can_inputed:
                if letter_hovered and in_keyboard_rect and not hold_backspace:
                    self.handle_input(last_letter)

                last_letter = None
                pressed_key = False

            elif keyboard_letter and can_inputed:
                self.handle_input(keyboard_letter)

            elif hold_backspace and not pressed_backspace:
                hold_backspace = False

            if mouse_up:
                in_keyboard_rect = True
                mouse_up         = False

        self.save_game()
        pygame.quit()

MAIN_RETURNS = const.Literal[-2, -1, 0, 1]

def main() -> MAIN_RETURNS:
    try:

        logs.log('Test permission')

        test_output = const.test_permissions(logs)

        if test_output[1] is not None:
            logs.log(f'Test completed with errors -> {type(test_output[1]).__name__}', 'error')
            raise test_output[1]

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
                    return 0

            except Exception as e:
                msgdenied = f'Failed to run Katla as administrator. Please try again later. {e}'

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
    print('ExitCode: ' + (f'\033[33m{exitcode}\033[0m' if exitcode != 0 else '0'))