"""
Katla JSON Validator.

classes:
- Languages
- WordsValidator
- SettingsValidator
- GameDataValidator
"""

from string import ascii_lowercase, ascii_uppercase
from random import shuffle
from ..module.jsonfl import Json, json, _fernet, JsonObj
from .katla_crypt import KatlaEncryptor
from .constants import (
    MIN_SCREEN_X, MIN_SCREEN_Y, MIN_SOUND, MIN_MUSIC, MIN_CHANGE_GUESS, MIN_WORD_LENGTH, MIN_FPS, MIN_GEOMATRY,
    MAX_SCREEN_X, MAX_SCREEN_Y, MAX_SOUND, MAX_MUSIC, MAX_CHANGE_GUESS, MAX_WORD_LENGTH, MAX_FPS, MAX_GEOMATRY,
    STEP_FPS,
    Keyboard, File, Logs, JsonData, mkdir_data
)

_file = File()
_logs = Logs()

class Languages:

    def __init__(self) -> None:
        self.json = Json(_file.LANGUAGES, JsonData.DATA_LOST)
        self.datajson = self.json.load_write()

    def get_lang_id(self) -> list[str]:
        result = []
        for item_spec in self.datajson:
            result.append(item_spec['id'])
        return result

    def get_lang_name(self) -> list[str]:
        result = []
        for item_spec in self.datajson:
            result.append(item_spec['name'])
        return result

    def load(self, lang_id: str) -> dict[str, JsonObj]:
        if lang_id not in self.get_lang_id():
            raise IndexError('lang_id not found:', lang_id)

        for item_spec in self.datajson:
            if item_spec['id'] == lang_id:
                return item_spec

class Themes:

    def __init__(self) -> None:
        self.json = Json(_file.THEMES, JsonData.DATA_LOST)
        self.datajson = self.json.load_write()

    def get_theme_id(self) -> list[str]:
        result = []
        for item_theme in self.datajson:
            result.append(item_theme['id'])
        return result

    def load(self, theme_id: str) -> dict[str, JsonObj]:
        if theme_id not in self.get_theme_id():
            raise IndexError('theme_id not found:', theme_id)

        for item_theme in self.datajson:
            if item_theme['id'] == theme_id:
                return item_theme

class WordsValidator:

    def __init__(self, lang_id: str) -> None:
        self.spec_langs = Json(_file.WORDS_LIST, JsonData.DATA_LOST).load_write()

        if lang_id not in self.get_lang_id():
            raise IndexError('lang_id not found:', lang_id)

        for item_spec in self.spec_langs:
            if item_spec['id'] == lang_id:
                self.spec = item_spec

        self.json = Json(_file.WORDS(self.spec['path']), JsonData.DATA_LOST, indent=None)
        self.datajson = self.json.load_write()

    def get_lang_id(self) -> list[str]:
        result = []
        for item_spec in self.spec_langs:
            result.append(item_spec['id'])
        return result

    def get_lang_name(self) -> list[str]:
        result = []
        for item_spec in self.spec_langs:
            result.append(item_spec['name'])
        return result

    def make_lower(self) -> None:
        for length_word, words_list in self.datajson.items():
            for i, word in enumerate(words_list):
                self.datajson[length_word][i] = word.lower()

    def make_upper(self) -> None:
        for length_word, words_list in self.datajson.items():
            for i, word in enumerate(words_list):
                self.datajson[length_word][i] = word.upper()

    def words_according_to_length(self) -> None:
        for length_word, words_list in self.datajson.items():
            length = int(length_word[7:])
            for i, word in enumerate(words_list):
                if len(word) != length:
                    del self.datajson[length_word][i]

    def words_according_to_letters(self) -> None:
        for length_word, words_list in self.datajson.items():
            for i, word in enumerate(words_list):
                for char in word:
                    if char not in ascii_lowercase+ascii_uppercase:
                        del self.datajson[length_word][i]
                        break

    def set_words(self) -> None:
        for length_word, words_list in self.datajson.items():
            self.datajson[length_word] = list(set(words_list))

    def strip_words(self, char: str = ' ') -> None:
        for length_word, words_list in self.datajson.items():
            for i, word in enumerate(words_list):
                self.datajson[length_word][i] = word.strip(char)

    def shuffle_words(self) -> None:
        for length_word in self.datajson.keys():
            shuffle(self.datajson[length_word])

    def sorted_words(self) -> None:
        for length_word, words_list in self.datajson.items():
            self.datajson[length_word] = sorted(words_list)

    def load_and_validation(self, readonly: bool = True) -> dict[str, list[str]]:
        if not bool(readonly):
            self.strip_words()
            self.make_lower()
            self.words_according_to_length()
            self.words_according_to_letters()
            self.set_words()
            self.sorted_words()
            return self.json.load_write(self.datajson)
        else:
            return self.datajson

class SettingsValidator:

    def __init__(self, logs: Logs | None = None) -> None:
        self.key = b'OMv5ELkug3vciuGQwnk-GuQEabAx47DVeWWeIBQPqus='
        self.file_corrupt = False
        self.words_validator = WordsValidator('idn')
        self.languages_validator = Languages()
        self.themes_validator = Themes()
        self.katla_crypt = KatlaEncryptor(self.key)
        if logs is None:
            self.logs = _logs
        else:
            self.logs = logs
        self.md = lambda : mkdir_data(f'file "{_file.DIR_DATA}/settings.katla" doesn\'t exists', self.logs)
        self.md()

    def encrypt_data(self, data) -> None:
        self.md()
        fernet = _fernet.Fernet(self.key)
        json_string = json.dumps(data)
        encrypted_data = fernet.encrypt(json_string.encode())
        try:
            with open(_file.SETTINGS, 'wb') as f:
                f.write(self.katla_crypt.encrypt(encrypted_data.decode()))
        except Exception as e:
            self.logs.log(f'settings data - write: Cannot save data: {type(e).__name__}: {e}', 'error')
        self.file_corrupt = False

    def decrypt_data(self) -> dict[str, JsonObj]:
        try:
            with open(_file.SETTINGS, 'rb') as f:
                decrypted_data = self.katla_crypt.decrypt(f.read())
            fernet = _fernet.Fernet(self.key)
            decrypted_json = fernet.decrypt(decrypted_data.encode())
            return json.loads(decrypted_json.decode())
        except Exception as e:
            self.logs.log(f'settings data: {type(e).__name__}: {e}', 'error')
            self.set_default()
            return self.file_data

    def set_default(self, reason: str | None = None) -> None:
        self.encrypt_data(JsonData.DEFAULT_SETTINGS)
        self.logs.log(f"Set settings as default{'. Reason: {}'.format(reason) if reason is not None else ''}", 'warn')
        self.file_data = JsonData.DEFAULT_SETTINGS
        self.file_corrupt = True

    def load_and_validation(self) -> dict[str, JsonObj]:
        use_valid_word = None
        self.file_data = self.decrypt_data()
        list_req_settings = {
            "theme": self.themes_validator.get_theme_id(),
            "keyboard-layout": Keyboard.__all__,
            "language-word": self.words_validator.get_lang_id(),
            "language": self.languages_validator.get_lang_id(),
            "sound-volume": [MIN_SOUND, MAX_SOUND],
            "music-volume": [MIN_MUSIC, MAX_MUSIC],
            "change-guess": [MIN_CHANGE_GUESS, MAX_CHANGE_GUESS(True)],
            "word-length": [MIN_WORD_LENGTH, MAX_WORD_LENGTH],
            "fps": [MIN_FPS, MAX_FPS],
            "geomatry": [MIN_GEOMATRY, MAX_GEOMATRY],
            "use-valid-word": bool,
            "show-keyboard": bool,
            "word-correction": bool,
            "screen-size": [[MIN_SCREEN_X, MAX_SCREEN_X], [MIN_SCREEN_Y, MAX_SCREEN_Y]]
        }

        if not isinstance(self.file_data, dict):
            self.set_default('Not dictionary or object')

        elif JsonData.DEFAULT_SETTINGS.keys() - self.file_data.keys():
            self.set_default('Unbalanced key')

        else:
            for key, value in self.file_data.items():

                if key in ['theme', 'keyboard-layout', 'language-word', 'language']:
                    if value not in list_req_settings[key]:
                        self.set_default(f'{key}: Invalid value')
                        break

                elif key in ['sound-volume', 'music-volume', 'change-guess', 'word-length', 'fps', 'geomatry']:
                    if not isinstance(value, int):
                        if not (key == 'geomatry' and isinstance(value, float)):
                            if key == 'geomatry':
                                self.set_default('geomatry: Not float')
                            else:
                                self.set_default(f'{key}: Not int')
                            break

                    elif value < list_req_settings[key][0]:
                        self.set_default(f'{key}: Value is smaller than standard')
                        break

                    elif value > list_req_settings[key][1]:
                        self.set_default(f'{key}: Value is greater than standard')
                        break

                    elif key == 'fps' and value % STEP_FPS != 0:
                        self.set_default('fps: Value is not a multiple of 5')
                        break

                elif key in ['use-valid-word', 'show-keyboard', 'word-correction']:
                    if not isinstance(value, bool):
                        self.set_default('use-valid-word: Not bool')
                        break
                    else:
                        use_valid_word = value

                elif key == 'screen-size':
                    if not isinstance(value, list):
                        if value != 'FULL':
                            self.set_default('screen-size: Not list or str Literal["FULL"]')
                        break

                    elif len(value) != 2:
                        self.set_default('screen-size: List length is not appropriate')
                        break

                    for size in value:
                        if not isinstance(size, int):
                            self.set_default('screen-size: Not int')
                            break

                    if value[0] < list_req_settings[key][0][0]:
                        self.set_default('screen-size index: [0]: Value is smaller than standard')
                        break

                    elif value[0] > list_req_settings[key][0][1]:
                        self.set_default('screen-size index: [0]: Value is greater than standard')
                        break

                    elif value[1] < list_req_settings[key][1][0]:
                        self.set_default('screen-size index: [1]: Value is smaller than standard')
                        break

                    elif value[1] > list_req_settings[key][1][1]:
                        self.set_default('screen-size index: [1]: Value is greater than standard')
                        break

        if isinstance(use_valid_word, bool) and self.file_data['change-guess'] > ( cg := MAX_CHANGE_GUESS(use_valid_word)):
            self.file_data['change-guess'] = cg

        return self.file_data

class GameDataValidator:

    def __init__(self, logs: Logs | None = None) -> None:
        self.key = b'6B4qF6oZ64V4_Z7sdCNKErkF_eT1A_qTP8HQMAbu2Uw='
        self.file_corrupt = False
        self.katla_crypt = KatlaEncryptor(self.key)
        if logs is None:
            self.logs = _logs
        else:
            self.logs = logs
        self.md = lambda : mkdir_data(f'file "{_file.DIR_DATA}/game.katla" doesn\'t exists', logs)
        self.md()

    def encrypt_data(self, data) -> None:
        self.md()
        fernet = _fernet.Fernet(self.key)
        json_string = json.dumps(data)
        encrypted_data = fernet.encrypt(json_string.encode())
        try:
            with open(_file.GAME, 'wb') as f:
                f.write(self.katla_crypt.encrypt(encrypted_data.decode()))
        except Exception as e:
            self.logs.log(f'game data - write: Cannot save data: {type(e).__name__}: {e}', 'error')
        self.file_corrupt = False

    def decrypt_data(self) -> dict[str, JsonObj]:
        try:
            with open(_file.GAME, 'rb') as f:
                decrypted_data = self.katla_crypt.decrypt(f.read())
            fernet = _fernet.Fernet(self.key)
            decrypted_json = fernet.decrypt(decrypted_data.encode())
            return json.loads(decrypted_json.decode())
        except Exception as e:
            self.logs.log(f'game data: {type(e).__name__}: {e}', 'error')
            self.set_default()
            return self.file_data

    def set_default(self, reason: str | None = None) -> None:
        self.encrypt_data(JsonData.DEFAULT_DATA_GAME)
        self.logs.log(f"Set game data as default{'. Reason: {}'.format(reason) if reason is not None else ''}", 'warn')
        self.file_data = JsonData.DEFAULT_DATA_GAME
        self.file_corrupt = True

    def load_and_validation(self) -> dict[str, JsonObj]:
        self.file_data = self.decrypt_data()

        if not isinstance(self.file_data, dict):
            self.set_default('Not dictionary or object')

        elif JsonData.DEFAULT_DATA_GAME.keys() - self.file_data.keys():
            self.set_default('Unbalanced key')

        else:
            for key, value in self.file_data.items():

                if key == 'coins':
                    if not isinstance(value, int):
                        self.set_default('coins: Not an int value')
                        break

                elif key in ['prize-claim-time', 'played-time']:
                    if not isinstance(value, str):
                        self.set_default(f'{key}: Not str')
                        break

                    date_split = value.split('/')

                    if len(date_split) != 6:
                        self.set_default(f"{key}: Time format doesn't match")
                        break
                    else:
                        for date in date_split:
                            if not date.isdigit():
                                self.set_default(f'{key}: One of them is not a number')
                                break

                elif key in ['joined-date', 'hint', 'wins']:
                    if not isinstance(value, dict):
                        self.set_default(f'{key}: Not dictionary or object')
                        break

                    elif self.file_data[key].keys() - JsonData.DEFAULT_DATA_GAME[key].keys():
                        self.set_default(f'{key}: Unbalanced key')
                        break

                    if key == 'joined-date':
                        if not isinstance(self.file_data['joined-date']['date'], str):
                            self.set_default(f'{key}: Not str')
                            break
                        if not isinstance(self.file_data['joined-date']['edit-date'], bool):
                            self.set_default(f'{key}: Not bool')
                            break

                        date_split = self.file_data['joined-date']['date'].split('/')

                        if len(date_split) != 6:
                            self.set_default(f"{key}: Time format doesn't match")
                            break
                        else:
                            for date in date_split:
                                if not date.isdigit():
                                    self.set_default(f'{key}: One of them is not a number')
                                    break

                    else:
                        for value_hint in self.file_data[key].values():

                            if not isinstance(value_hint, int):
                                self.set_default(f'{key}: Not int')
                                break

                elif key in ('prize-taken', 'have-played', 'losses', 'play-time-seconds'):
                    if not isinstance(value, int):
                        self.set_default(f'{key}: Not int')
                        break

        return self.file_data