"""
Katla constants
"""

from time import sleep
from warnings import warn
from math import isnan, isinf
from typing import Any, Literal
from .resource_path import resource_path, os

MAJOR = 1
MINOR = 1
PATCH = 5
LABEL = 'BETA'
VERSION = f"Katla {LABEL + (' ' if LABEL else '')}- {MAJOR}.{MINOR}.{PATCH}"
LICENSE = f"""license and information
=======================

Katla - Kata game - pygame
(C) Copyright 2024 - 2026 [ Azzamuhyala ]
Version: {VERSION}

This application uses SDL pygame.

100% Using Python language. So, don't expect the FPS is high and stable. Lol"""

Number = int | float
Feedback = list[dict[str, str]]
KeyboardList = list[list[str]]
Path = os.PathLike[str]
inf = float('inf')
nan = float('nan')

def mkdir_data(message: str) -> None:
    f = File()
    if not os.path.exists(f.PATH_DATA):
        warn(message)
        os.mkdir(f.PATH_DATA)

def test_read_write_delete() -> tuple[dict[str, bool | None], Exception | None]:
    mkdir_data('katla-data not found when testing permissions')

    f = File()
    testpath = f.PATH_DATA + '/test.txt'
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

class LiteralConst:
    all_keyboard = ['QWERTY', 'QWERTZ', 'AZERTY', 'COLEMAK', 'ABCDEF_1', 'ABCDEF_2', 'ABCDEF_3', 'ZYXWVU_1', 'ZYXWVU_2', 'ZYXWVU_3']
    all_theme    = ['dark', 'dark-gray', 'light', 'solid']

    literal_keyboard = Literal['QWERTY', 'QWERTZ', 'AZERTY', 'COLEMAK', 'ABCDEF_1', 'ABCDEF_2', 'ABCDEF_3', 'ZYXWVU_1', 'ZYXWVU_2', 'ZYXWVU_3']
    literal_theme    = Literal['dark', 'dark-gray', 'light', 'solid']

class Keyboard:

    __all__ = LiteralConst.all_keyboard

    QWERTY: KeyboardList = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["\b", "Z", "X", "C", "V", "B", "N", "M", "\n"]
    ]
    QWERTZ: KeyboardList = [
        ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["\b", "Y", "X", "C", "V", "B", "N", "M", "\n"]
    ]
    AZERTY: KeyboardList = [
        ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
        ["\b", "W", "X", "C", "V", "B", "N", "\n"]
    ]
    COLEMAK: KeyboardList = [
        ["Q", "W", "F", "P", "G", "J", "L", "U", "Y"],
        ["A", "R", "S", "T", "D", "H", "N", "E", "I", "O"],
        ["\b", "Z", "X", "C", "V", "B", "K", "M", "\n"]
    ]
    ABCDEF_1: KeyboardList = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        ["K", "L", "M", "N", "O", "P", "Q", "R", "S"],
        ["\b", "T", "U", "V", "W", "X", "Y", "Z", "\n"]
    ]
    ABCDEF_2: KeyboardList = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
        ["\b", "U", "V", "W", "X", "Y", "Z", "\n"]
    ]
    ABCDEF_3: KeyboardList = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
        ["J", "K", "L", "M", "N", "O", "P", "Q", "R", "S"],
        ["\b", "T", "U", "V", "W", "X", "Y", "Z", "\n"]
    ]
    ZYXWVU_1: KeyboardList = [
        ["Z", "Y", "X", "W", "V", "U", "T", "S", "R", "Q"],
        ["P", "O", "N", "M", "L", "K", "J", "I", "H"],
        ["\b", "G", "F", "E", "D", "C", "B", "A", "\n"]
    ]
    ZYXWVU_2: KeyboardList = [
        ["Z", "Y", "X", "W", "V", "U", "T", "S", "R", "Q"],
        ["P", "O", "N", "M", "L", "K", "J", "I", "H", "G"],
        ["\b", "F", "E", "D", "C", "B", "A", "\n"]
    ]
    ZYXWVU_3: KeyboardList = [
        ["Z", "Y", "X", "W", "V", "U", "T", "S", "R"],
        ["Q", "P", "O", "N", "M", "L", "K", "J", "I", "H"],
        ["\b", "G", "F", "E", "D", "C", "B", "A", "\n"]
    ]

class JsonData:
    LOST_DICTIONARY: dict[str, str] = {"error-message": "lost dictionary"}
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
        "screen-size": [640, 980]
    }
    DEFAULT_DATA_GAME: dict[str, Any] = {
        "coins": 0,
        "prize-claim-time": "00/00/00/01/01/0001",
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
        self.PATH_LANGUAGES = resource_path('assets/json/languages/katla-languages.json')
        self.PATH_WORDS = lambda file : resource_path('assets/json/words/' + file)
        self.PATH_WORDS_LIST = resource_path('assets/json/words/words-list.json')
        self.PATH_DATA = 'katla-data'
        self.DATA_SETTINGS: Path = self.PATH_DATA + '/settings.katla'
        self.DATA_GAME: Path = self.PATH_DATA + '/game.katla'
        self.FONT_ROBOTO_MEDIUM = resource_path('assets/fonts/roboto-Medium.ttf')
        self.FONT_ROBOTO_BOLD = resource_path('assets/fonts/roboto-Bold.ttf')
        self.FONT_ROBOTO_MONO_BOLD = resource_path('assets/fonts/roboto-Mono_Bold.ttf')
        self.SOUND_MUSIC = resource_path('assets/sounds/music-katla.mp3')
        self.SOUND_KEY = resource_path('assets/sounds/key.mp3')
        self.SOUND_KEY_BACKSPACE_ENTER = resource_path('assets/sounds/key-backspace-enter.mp3')
        self.SOUND_BUTTON_CLICK = resource_path('assets/sounds/button-click.mp3')
        self.SOUND_WIN = resource_path('assets/sounds/win.mp3')
        self.SOUND_LOSE = resource_path('assets/sounds/lose.mp3')
        self.Images = lambda theme : _Images(theme)

class Color:

    def __init__(self, theme: LiteralConst.literal_theme) -> None:
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (127, 127, 127)

        if theme == 'dark':
            self.screen = (14, 20, 33)

            self.barMenu = {
                'background': (10, 28, 46),
                'indicator': (175, 15, 1),
                'text': self.WHITE
            }

            self.keyboard = {
                'background': (10, 28, 46),
                'button': {
                    'not-inputed': {
                        'inactive': (17, 22, 33),
                        'active': (23, 31, 46),
                        'hover': (32, 43, 64)
                    },
                    'green': {
                        'inactive': (61, 153, 61),
                        'active': (61, 123, 61),
                        'hover': (61, 183, 61)
                    },
                    'yellow': {
                        'inactive': (153, 138, 61),
                        'active': (123, 108, 61),
                        'hover': (183, 168, 61)
                    },
                    'red': {
                        'inactive': (153, 61, 61),
                        'active': (123, 61, 61),
                        'hover': (183, 61, 61)
                    },
                    'outline': {
                        'inactive': (59, 59, 87),
                        'active': (109, 184, 227)
                    }
                },
                'text': self.WHITE
            }

            self.boxEntryTile = {
                'box': {
                    'not-inputed': (17, 22, 33),
                    'green': (61, 153, 61),
                    'yellow': (153, 138, 61),
                    'red': (153, 61, 61),
                    'outline': {
                        'point-inactive': (59, 59, 87),
                        'point-active': (109, 184, 227)
                    }
                },
                'text': self.WHITE
            }

            self.notification = {
                'default': {
                    'background': (17, 22, 33),
                    'outline': (59, 59, 87),
                    'text': self.WHITE
                },
                'win': {
                    'background': (61, 153, 61),
                    'outline': (61, 103, 61),
                    'text': self.WHITE
                },
                'lose': {
                    'background': (153, 61, 61),
                    'outline': (103, 61, 61),
                    'text': self.WHITE
                }
            }

            self.popup = {
                'background': (17, 22, 33),
                'shadow': self.BLACK,
                'outline': (59, 59, 87),
                'button': {
                    'close': (17, 22, 33),
                    'buy': {
                        'inactive': (12, 20, 59),
                        'active': (16, 25, 74),
                        'hover': (17, 28, 87)
                    },
                },
                'text': self.WHITE
            }

            self.settings = {
                'background': (17, 22, 33),
                'outline': (59, 59, 87),
                'navbar': (10, 28, 46),
                'button': {
                    'close': (10, 28, 46),
                    'set': {
                        'inactive': (32, 44, 66),
                        'active': (23, 31, 46),
                        'hover': (45, 63, 94)
                    },
                    'switch': {
                        'true': {
                            'inactive': (61, 153, 61),
                            'active': (61, 123, 61),
                            'hover': (61, 183, 61)
                        },
                        'false': {
                            'inactive': (153, 61, 61),
                            'active': (123, 61, 61),
                            'hover': (183, 61, 61)
                        }
                    }
                },
                'range': {
                    'thumb': {
                        'inactive': (212, 212, 212),
                        'active': (224, 225, 231),
                        'hover': self.WHITE
                    },
                    'track': {
                        'inactive': (32, 44, 66),
                        'active': (23, 31, 46),
                        'hover': (45, 63, 94)
                    },
                    'track-fill': {
                        'inactive': (23, 133, 48),
                        'active': (26, 74, 37),
                        'hover': (28, 163, 59)
                    }
                },
                'text': self.WHITE
            }

        elif theme == 'dark-gray':
            self.screen = (30, 30, 30)

            self.barMenu = {
                'background': (60, 60, 60),
                'indicator': (120, 2, 2),
                'text': self.WHITE
            }

            self.keyboard = {
                'background': (26, 24, 24),
                'button': {
                    'not-inputed': {
                        'inactive': (69, 69, 71),
                        'active': (60, 59, 63),
                        'hover': (78, 80, 79)
                    },
                    'green': {
                        'inactive': (21, 128, 61),
                        'active': (61, 123, 61),
                        'hover': (61, 183, 61)
                    },
                    'yellow': {
                        'inactive': (202, 138, 4),
                        'active': (123, 108, 61),
                        'hover': (183, 168, 61)
                    },
                    'red': {
                        'inactive': (50, 50, 54),
                        'active': (40, 41, 43),
                        'hover': (59, 60, 61)
                    },
                    'outline': {
                        'inactive': (51, 51, 51),
                        'active': (163, 162, 162)
                    }
                },
                'text': self.WHITE
            }

            self.boxEntryTile = {
                'box': {
                    'not-inputed': (69, 69, 71),
                    'green': (21, 128, 61),
                    'yellow': (202, 138, 4),
                    'red': (50, 50, 54),
                    'outline': {
                        'point-inactive': (51, 51, 51),
                        'point-active': (183, 182, 182)
                    }
                },
                'text': self.WHITE
            }

            self.notification = {
                'default': {
                    'background': (69, 69, 71),
                    'outline': (51, 51, 51),
                    'text': self.WHITE
                },
                'win': {
                    'background': (21, 128, 61),
                    'outline': (15, 110, 51),
                    'text': self.WHITE
                },
                'lose': {
                    'background': (50, 50, 54),
                    'outline': (44, 56, 70),
                    'text': self.WHITE
                }
            }

            self.popup = {
                'background': (30, 30, 30),
                'shadow': self.BLACK,
                'outline': (51, 51, 51),
                'button': {
                    'close': (30, 30, 30),
                    'buy': {
                        'inactive': (19, 20, 23),
                        'active': (12, 14, 15),
                        'hover': (27, 29, 30)
                    },
                },
                'text': self.WHITE
            }

            self.settings = {
                'background': (30, 30, 30),
                'outline': (66, 63, 62),
                'navbar': (60, 60, 60),
                'button': {
                    'close': (60, 60, 60),
                    'set': {
                        'inactive': (19, 20, 23),
                        'active': (12, 14, 15),
                        'hover': (27, 29, 30)
                    },
                    'switch': {
                        'true': {
                            'inactive': (21, 128, 61),
                            'active': (61, 123, 61),
                            'hover': (61, 183, 61)
                        },
                        'false': {
                            'inactive': (50, 50, 54),
                            'active': (40, 41, 43),
                            'hover': (59, 60, 61)
                        }
                    }
                },
                'range': {
                    'thumb': {
                        'inactive': (212, 212, 212),
                        'active': (224, 225, 231),
                        'hover': self.WHITE
                    },
                    'track': {
                        'inactive': (19, 20, 23),
                        'active': (12, 14, 15),
                        'hover': (27, 29, 30)
                    },
                    'track-fill': {
                        'inactive': (202, 138, 4),
                        'active': (123, 108, 61),
                        'hover': (183, 168, 61)
                    }
                },
                'text': self.WHITE
            }

        elif theme == 'light':

            self.screen = (232, 232, 232)

            self.barMenu = {
                'background': (218, 222, 235),
                'indicator': (175, 15, 1),
                'text': self.BLACK
            }

            self.keyboard = {
                'background': (218, 222, 235),
                'button': {
                    'not-inputed': {
                        'inactive': (209, 213, 219),
                        'active': (210, 211, 219),
                        'hover': (239, 246, 249)
                    },
                    'green': {
                        'inactive': (61, 153, 61),
                        'active': (61, 123, 61),
                        'hover': (61, 183, 61)
                    },
                    'yellow': {
                        'inactive': (153, 138, 61),
                        'active': (123, 108, 61),
                        'hover': (183, 168, 61)
                    },
                    'red': {
                        'inactive': (153, 61, 61),
                        'active': (123, 61, 61),
                        'hover': (183, 61, 61)
                    },
                    'outline': {
                        'inactive': (148, 141, 168),
                        'active': (214, 178, 92)
                    }
                },
                'text': self.BLACK
            }

            self.boxEntryTile = {
                'box': {
                    'not-inputed': (209, 213, 219),
                    'green': (61, 153, 61),
                    'yellow': (153, 138, 61),
                    'red': (153, 61, 61),
                    'outline': {
                        'point-inactive': (148, 141, 168),
                        'point-active': (214, 178, 92)
                    }
                },
                'text': self.BLACK
            }

            self.notification = {
                'default': {
                    'background': (218, 222, 235),
                    'outline': (148, 141, 168),
                    'text': self.BLACK
                },
                'win': {
                    'background': (41, 206, 41),
                    'outline': (61, 103, 61),
                    'text': self.BLACK
                },
                'lose': {
                    'background': (206, 41, 41),
                    'outline': (103, 61, 61),
                    'text': self.BLACK
                }
            }

            self.popup = {
                'background': (209, 213, 219),
                'shadow': self.BLACK,
                'outline': (148, 141, 168),
                'button': {
                    'close': (209, 213, 219),
                    'buy': {
                        'inactive': (204, 208, 255),
                        'active': (193, 198, 255),
                        'hover': (221, 224, 255)
                    },
                },
                'text': self.BLACK
            }

            self.settings = {
                'background': (209, 213, 219),
                'outline': (148, 141, 168),
                'navbar': (218, 222, 235),
                'button': {
                    'close': (218, 222, 235),
                    'set': {
                        'inactive': (204, 208, 255),
                        'active': (193, 198, 255),
                        'hover': (221, 224, 255)
                    },
                    'switch': {
                        'true': {
                            'inactive': (61, 153, 61),
                            'active': (61, 123, 61),
                            'hover': (61, 183, 61)
                        },
                        'false': {
                            'inactive': (153, 61, 61),
                            'active': (123, 61, 61),
                            'hover': (183, 61, 61)
                        }
                    }
                },
                'range': {
                    'thumb': {
                        'inactive': (104, 100, 117),
                        'active': (71, 69, 77),
                        'hover': (141, 138, 150)
                    },
                    'track': {
                        'inactive': (204, 208, 255),
                        'active': (193, 198, 255),
                        'hover': (221, 224, 255)
                    },
                    'track-fill': {
                        'inactive': (23, 133, 48),
                        'active': (26, 74, 37),
                        'hover': (28, 163, 59)
                    }
                },
                'text': self.BLACK
            }

        elif theme == 'solid':
            R = (255, 0, 0)
            G = (0, 255, 0)
            B = (0, 0, 255)
            C = (0, 255, 255)
            O = (255, 127, 0)
            Y = (255, 255, 0)
            M = (255, 0, 255)

            self.screen = self.GRAY

            self.barMenu = {
                'background': self.BLACK,
                'indicator': R,
                'text': self.WHITE
            }

            self.keyboard = {
                'background': self.BLACK,
                'button': {
                    'not-inputed': {
                        'inactive': self.GRAY,
                        'active': self.GRAY,
                        'hover': self.GRAY
                    },
                    'green': {
                        'inactive': G,
                        'active': G,
                        'hover': G
                    },
                    'yellow': {
                        'inactive': Y,
                        'active': Y,
                        'hover': Y
                    },
                    'red': {
                        'inactive': R,
                        'active': R,
                        'hover': R
                    },
                    'outline': {
                        'inactive': M,
                        'active': O
                    }
                },
                'text': self.WHITE
            }

            self.boxEntryTile = {
                'box': {
                    'not-inputed': self.GRAY,
                    'green': G,
                    'yellow': Y,
                    'red': R,
                    'outline': {
                        'point-inactive': M,
                        'point-active': O
                    }
                },
                'text': self.BLACK
            }

            self.notification = {
                'default': {
                    'background': self.GRAY,
                    'outline': M,
                    'text': self.BLACK
                },
                'win': {
                    'background': G,
                    'outline': Y,
                    'text': self.BLACK
                },
                'lose': {
                    'background': R,
                    'outline': Y,
                    'text': self.BLACK
                }
            }

            self.popup = {
                'background': self.GRAY,
                'shadow': self.BLACK,
                'outline': M,
                'button': {
                    'close': self.GRAY,
                    'buy': {
                        'inactive': B,
                        'active': B,
                        'hover': B
                    },
                },
                'text': self.BLACK
            }

            self.settings = {
                'background': self.GRAY,
                'outline': Y,
                'navbar': self.BLACK,
                'button': {
                    'close': self.BLACK,
                    'set': {
                        'inactive': B,
                        'active': B,
                        'hover': B
                    },
                    'switch': {
                        'true': {
                            'inactive': G,
                            'active': G,
                            'hover': G
                        },
                        'false': {
                            'inactive': R,
                            'active': R,
                            'hover': R
                        }
                    }
                },
                'range': {
                    'thumb': {
                        'inactive': self.WHITE,
                        'active': self.WHITE,
                        'hover': self.WHITE
                    },
                    'track': {
                        'inactive': M,
                        'active': M,
                        'hover': M
                    },
                    'track-fill': {
                        'inactive': C,
                        'active': C,
                        'hover': C
                    }
                },
                'text': self.WHITE
            }

class _Images:

    def __init__(self, theme: LiteralConst.literal_theme) -> None:
        self.ICON = resource_path('assets/images/icon.png')
        self.ICO = resource_path('assets/images/icon.ico')
        self.WINS_GIF = resource_path('assets/images/wins-gif.gif')

        if theme in ['light']:
            # BLACK IMAGES
            self.CLOSE = resource_path('assets/images/close-black.png')
            self.BACKSPACE = resource_path('assets/images/backspace-black.png')
            self.ENTER = resource_path('assets/images/enter-black.png')
            self.QUESTION_MARK = resource_path('assets/images/question-mark-black.png')
            self.STATS = resource_path('assets/images/stats-black.png')
            self.RIGHT_ARROW = resource_path('assets/images/right-arrow-black.png')
            self.RESET = resource_path('assets/images/reset-black.png')
            self.SETTINGS = resource_path('assets/images/settings-black.png')
            self.COIN_BAG = resource_path('assets/images/coin-bag-black.png')
            self.LAMP = resource_path('assets/images/lamp-black.png')
            self.KEYBOARD = resource_path('assets/images/keyboard-black.png')
            self.HAMMER = resource_path('assets/images/hammer-black.png')
            self.CHECK = resource_path('assets/images/check-black.png')

        elif theme in ['dark', 'dark-gray', 'solid']:
            # WHITE IMAGES
            self.CLOSE = resource_path('assets/images/close-white.png')
            self.BACKSPACE = resource_path('assets/images/backspace-white.png')
            self.ENTER = resource_path('assets/images/enter-white.png')
            self.QUESTION_MARK = resource_path('assets/images/question-mark-white.png')
            self.STATS = resource_path('assets/images/stats-white.png')
            self.RIGHT_ARROW = resource_path('assets/images/right-arrow-white.png')
            self.RESET = resource_path('assets/images/reset-white.png')
            self.SETTINGS = resource_path('assets/images/settings-white.png')
            self.COIN_BAG = resource_path('assets/images/coin-bag-white.png')
            self.LAMP = resource_path('assets/images/lamp-white.png')
            self.KEYBOARD = resource_path('assets/images/keyboard-white.png')
            self.HAMMER = resource_path('assets/images/hammer-white.png')
            self.CHECK = resource_path('assets/images/check-white.png')

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

    def isnan(self, number: Number) -> bool:
        return isnan(number)

    def isinf(self, number: Number) -> bool:
        return isinf(number)

    def get_center(self, width_surface: Number, width_object: Number) -> Number:
        """ Formula : (width_surface - width_object) / 2 """
        return (width_surface - width_object) / 2

    def get_pos_animation(self, pos_start: Number, pos_end: Number, time_end: Number, current_time: Number, start_time: Number) -> Number:
        """ Formula : pos_start + ( (pos_end - pos_start) / (time_end - time_start) ) * (current_time - start_time) """
        v = (pos_end - pos_start) / time_end
        return pos_start + v * (current_time - start_time)

math = _Math()

del _Math