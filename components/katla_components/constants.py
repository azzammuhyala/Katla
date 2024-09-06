"""
Katla constants
"""

from time import sleep
from typing import Any, Literal, Optional
from .logs import Logs
from ..module.resource_path import resource_path, os

# versions
MAJOR   = 1  # ~.X.X
MINOR   = 2  # X.~.X
PATCH   = 2  # X.X.~
LABEL   = '' # LABEL VERSION [OPTIONAL]
VERSION = f"Katla {LABEL + (' ' if LABEL else '')}- {MAJOR}.{MINOR}.{PATCH}" # STRING VERSION
LICENSE = f"""
license and information
=======================

Katla - Kata game - pygame
(C) Copyright 2024 - 2026 [ Azzamuhyala ]
Version: {VERSION}

This application uses SDL pygame.

100% Using Python language. So, don't expect the FPS is high and stable. Lol
""".strip('\n')

RUNSYS = 'python.3.10+, $source' # information about the type of system running [OPTIONAL]

MAX_SCREEN_X     = 64000 # the maximum size also depends on the screen size
MAX_SCREEN_Y     = 64000
MAX_SOUND        = 100
MAX_MUSIC        = 100
MAX_WORD_LENGTH  = 9
MAX_CHANGE_GUESS = lambda IS_VALID_WORD : 10 if IS_VALID_WORD else 7
MAX_GEOMATRY     = 2.2
MAX_FPS          = 140

MIN_SCREEN_X     = 380
MIN_SCREEN_Y     = 380
MIN_SOUND        = 0
MIN_MUSIC        = 0
MIN_WORD_LENGTH  = 4
MIN_CHANGE_GUESS = 4
MIN_GEOMATRY     = 0.5
MIN_FPS          = 15

STEP_SOUND = 1
STEP_MUSIC = 1
STEP_FPS   = 5

DAILY_COINS      = 50
WIN_COINS_REWAND = lambda WORD_LENGTH : 2 if WORD_LENGTH == 9 else 1

PRICE_LETTER_HINT   = lambda WORD_LENGTH : 30 if WORD_LENGTH >= 8 else 35
PRICE_KEYBOARD_HINT = lambda WORD_LENGTH : 20 if WORD_LENGTH >= 8 else 25
PRICE_DEL_ENTRY     = lambda WORD_LENGTH : 15 if WORD_LENGTH >= 8 else 10

AUTO_SAVE_INTERVAL  = 15
POST_SETTINGS_DELAY = 0.5
RESET_DELAY         = 0.5

BACKSPACE = '\b'
ENTER     = '\n'
ALL_KEY   = (BACKSPACE, ENTER)

HELLO = "Hello World!"

Number       = int | float
Feedback     = list[dict[str, Literal['red', 'yellow', 'green']]]
KeyboardList = list[list[str]]
Path         = os.PathLike[str]
inf          = float('inf')
nan          = float('nan')

def mkdir_data(message: str, logs: Optional[Logs] = None) -> None:
    f = File()

    if not os.path.exists(f.DIR_DATA):
        if logs is not None:
            logs.log(message, 'warn')
            logs.log(f'cwdfolder "katla-data": {os.getcwd()}')

        os.mkdir(f.DIR_DATA)

def test_permissions(logs: Logs) -> tuple[dict[str, bool | None], Exception | None]:
    mkdir_data('katla-data not found when testing permissions', logs)

    f = File()

    testpath = f.DIR_DATA + '/test.txt'
    result = {
        'write': None,
        'read': None,
        'delete': None
    }

    try:
        with open(testpath, 'w') as testw:
            testw.write('Test')
            result['write'] = True

        sleep(.1)

        with open(testpath, 'r') as testr:
            testr.read()
            result['read'] = True

        os.remove(testpath)
        result['delete'] = True

    except Exception as e:
        return result, e

    return result, None

class Keyboard:

    __all__ = ['QWERTY', 'QWERTZ', 'AZERTY', 'COLEMAK', 'ABCDEF_1', 'ABCDEF_2', 'ABCDEF_3', 'ZYXWVU_1', 'ZYXWVU_2', 'ZYXWVU_3']

    QWERTY: KeyboardList = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        [BACKSPACE, "Z", "X", "C", "V", "B", "N", "M", ENTER]
    ]

    QWERTZ: KeyboardList = [
        ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        [BACKSPACE, "Y", "X", "C", "V", "B", "N", "M", ENTER]
    ]

    AZERTY: KeyboardList = [
        ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
        [BACKSPACE, "W", "X", "C", "V", "B", "N", ENTER]
    ]

    COLEMAK: KeyboardList = [
        ["Q", "W", "F", "P", "G", "J", "L", "U", "Y"],
        ["A", "R", "S", "T", "D", "H", "N", "E", "I", "O"],
        [BACKSPACE, "Z", "X", "C", "V", "B", "K", "M", ENTER]
    ]

    ABCDEF_1: KeyboardList = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        ["K", "L", "M", "N", "O", "P", "Q", "R", "S"],
        [BACKSPACE, "T", "U", "V", "W", "X", "Y", "Z", ENTER]
    ]

    ABCDEF_2: KeyboardList = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
        [BACKSPACE, "U", "V", "W", "X", "Y", "Z", ENTER]
    ]

    ABCDEF_3: KeyboardList = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
        ["J", "K", "L", "M", "N", "O", "P", "Q", "R", "S"],
        [BACKSPACE, "T", "U", "V", "W", "X", "Y", "Z", ENTER]
    ]

    ZYXWVU_1: KeyboardList = [
        ["Z", "Y", "X", "W", "V", "U", "T", "S", "R", "Q"],
        ["P", "O", "N", "M", "L", "K", "J", "I", "H"],
        [BACKSPACE, "G", "F", "E", "D", "C", "B", "A", ENTER]
    ]

    ZYXWVU_2: KeyboardList = [
        ["Z", "Y", "X", "W", "V", "U", "T", "S", "R", "Q"],
        ["P", "O", "N", "M", "L", "K", "J", "I", "H", "G"],
        [BACKSPACE, "F", "E", "D", "C", "B", "A", ENTER]
    ]

    ZYXWVU_3: KeyboardList = [
        ["Z", "Y", "X", "W", "V", "U", "T", "S", "R"],
        ["Q", "P", "O", "N", "M", "L", "K", "J", "I", "H"],
        [BACKSPACE, "G", "F", "E", "D", "C", "B", "A", ENTER]
    ]

class JsonData:
    DATA_LOST: dict[str, str] = [{
        "code": 404,
        "message": "json: data lost"
    }]

    DEFAULT_SETTINGS: dict[str, Any] = {
        "theme": "dark",
        "keyboard-layout": "QWERTY",
        "language-word": "idn",
        "language": "idn",
        "sound-volume": 25,
        "music-volume": 25,
        "change-guess": 6,
        "word-length": 5,
        "fps": 120,
        "geomatry": 1.0,
        "use-valid-word": True,
        "show-keyboard": True,
        "word-corrector": False,
        "screen-size": [640, 980]
    }

    DEFAULT_DATA_GAME: dict[str, Any] = {
        "joined-date": {
            "date": "00/00/00/01/01/0001",
            "edit-date": True,
        },
        "prize-claim-time": "00/00/00/01/01/0001",
        "played-time": "00/00/00/01/01/0001",
        "play-time-seconds": 0,
        "coins": 0,
        "prize-taken": 0,
        "hint": {
            "count": 0,
            "coins": 0
        },
        "have-played": 0,
        "losses": 0,
        "wins": {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0,
            "10": 0,
            "streak": 0,
            "max-streak": 0,
            "total": 0
        }
    }

class File:

    def __init__(self) -> None:
        self.LANGUAGES                 = resource_path('assets/json/language/languages.json')
        self.THEMES                    = resource_path('assets/json/theme/themes.json')
        self.WORDS                     = lambda file : resource_path('assets/json/word/' + file)
        self.WORDS_LIST                = resource_path('assets/json/word/words-list.json')
        self.DIR_DATA                  = 'katla-data'
        self.SETTINGS: Path            = self.DIR_DATA + '/settings.katla'
        self.GAME: Path                = self.DIR_DATA + '/game.katla'
        self.FONT_BAKSOSAPI_REGULAR    = resource_path('assets/fonts/bakso_sapi/regular.otf')
        self.FONT_ROBOTO_MEDIUM        = resource_path('assets/fonts/roboto/medium.ttf')
        self.FONT_ROBOTO_BOLD          = resource_path('assets/fonts/roboto/bold.ttf')
        self.FONT_ROBOTO_MONO_BOLD     = resource_path('assets/fonts/roboto/mono_bold.ttf')
        self.FONT_ROBOTO_MONO_REGULAR  = resource_path('assets/fonts/roboto/mono_regular.ttf')
        self.SOUND_MUSIC               = resource_path('assets/sounds/music/music-katla.mp3')
        self.SOUND_KEY                 = resource_path('assets/sounds/sound/key.mp3')
        self.SOUND_KEY_BACKSPACE_ENTER = resource_path('assets/sounds/sound/key-backspace-enter.mp3')
        self.SOUND_BUTTON_CLICK        = resource_path('assets/sounds/sound/button-click.mp3')
        self.SOUND_WIN                 = resource_path('assets/sounds/sound/win.mp3')
        self.SOUND_LOSE                = resource_path('assets/sounds/sound/lose.mp3')
        self.Images                    = lambda icon_color : _Images(icon_color)

class _Images:

    def __init__(self, icon_color: Literal['black', 'white']) -> None:
        self.ICON     = resource_path('assets/images/app icon/icon.png')
        self.ICO      = resource_path('assets/images/app icon/icon.ico')
        self.LOAD_GIF = resource_path('assets/images/gif/load.gif')
        self.WIN_GIF  = resource_path('assets/images/gif/win.gif')

        if icon_color == 'black':
            self.CLOSE         = resource_path('assets/images/icon/black/close.png')
            self.BACKSPACE     = resource_path('assets/images/icon/black/backspace.png')
            self.ENTER         = resource_path('assets/images/icon/black/enter.png')
            self.QUESTION_MARK = resource_path('assets/images/icon/black/question-mark.png')
            self.STATS         = resource_path('assets/images/icon/black/stats.png')
            self.RIGHT_ARROW   = resource_path('assets/images/icon/black/right-arrow.png')
            self.RESET         = resource_path('assets/images/icon/black/reset.png')
            self.SETTINGS      = resource_path('assets/images/icon/black/settings.png')
            self.COIN_BAG      = resource_path('assets/images/icon/black/coin-bag.png')
            self.LAMP          = resource_path('assets/images/icon/black/lamp.png')
            self.KEYBOARD      = resource_path('assets/images/icon/black/keyboard.png')
            self.HAMMER        = resource_path('assets/images/icon/black/hammer.png')
            self.CHECK         = resource_path('assets/images/icon/black/check.png')

        elif icon_color == 'white':
            self.CLOSE         = resource_path('assets/images/icon/white/close.png')
            self.BACKSPACE     = resource_path('assets/images/icon/white/backspace.png')
            self.ENTER         = resource_path('assets/images/icon/white/enter.png')
            self.QUESTION_MARK = resource_path('assets/images/icon/white/question-mark.png')
            self.STATS         = resource_path('assets/images/icon/white/stats.png')
            self.RIGHT_ARROW   = resource_path('assets/images/icon/white/right-arrow.png')
            self.RESET         = resource_path('assets/images/icon/white/reset.png')
            self.SETTINGS      = resource_path('assets/images/icon/white/settings.png')
            self.COIN_BAG      = resource_path('assets/images/icon/white/coin-bag.png')
            self.LAMP          = resource_path('assets/images/icon/white/lamp.png')
            self.KEYBOARD      = resource_path('assets/images/icon/white/keyboard.png')
            self.HAMMER        = resource_path('assets/images/icon/white/hammer.png')
            self.CHECK         = resource_path('assets/images/icon/white/check.png')

class _Math:

    def __init__(self) -> None:
        self.Rect = None

    def Rect_outline(self, rect, size_outline: Number):
        """ Formula : pygame.Rect(rect.left - size_outline, rect.top - size_outline, rect.width + size_outline * 2, rect.height + size_outline * 2) """
        if self.Rect is None:
            os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'HIDE'
            from pygame import Rect
            self.Rect = Rect

        return self.Rect(rect.left - size_outline, rect.top - size_outline, rect.width + size_outline * 2, rect.height + size_outline * 2)

    def get_center(self, width_surface: Number, width_object: Number) -> Number:
        """ Formula : (width_surface - width_object) / 2 """
        return (width_surface - width_object) / 2

    def get_pos_animation(self, pos_start: Number, pos_end: Number, time_end: Number, current_time: Number, start_time: Number) -> Number:
        """ Formula : pos_start + ( (pos_end - pos_start) / time_end ) * (current_time - start_time) """
        v = (pos_end - pos_start) / time_end
        return pos_start + v * (current_time - start_time)

math = _Math()

del _Math