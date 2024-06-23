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
from warnings import warn
from .katla_crypt import KatlaEncryptor
from .constants import File, JsonData, LiteralConst, Any, isinf, mkdir_data
from ..module.jsonfl import Json, json, _fernet

_file = File()

class Languages:

    def __init__(self) -> None:
        self.json = Json(_file.PATH_LANGUAGES, JsonData.LOST_DICTIONARY)
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

    def load(self, lang_id: str) -> dict[str, Any]:
        if lang_id not in self.get_lang_id():
            raise IndexError('lang_id not found:', lang_id)

        for item_spec in self.datajson:
            if item_spec['id'] == lang_id:
                return item_spec

class WordsValidator:

    def __init__(self, lang_id: str) -> None:
        self.spec_langs = Json(_file.PATH_WORDS_LIST, JsonData.LOST_DICTIONARY).load_write()

        if lang_id not in self.get_lang_id():
            raise IndexError('lang_id not found:', lang_id)

        for item_spec in self.spec_langs:
            if item_spec['id'] == lang_id:
                self.spec = item_spec

        self.json = Json(_file.PATH_WORDS(self.spec['path']), JsonData.LOST_DICTIONARY, indent=None)
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

    def shuffle_words(self) -> None:
        for length_word in self.datajson.keys():
            shuffle(self.datajson[length_word])

    def sorted_words(self) -> None:
        for length_word, words_list in self.datajson.items():
            self.datajson[length_word] = sorted(words_list)

    def load_and_validation(self, readonly: bool = True) -> dict[str, list[str]]:
        if not bool(readonly):
            self.words_according_to_length()
            self.words_according_to_letters()
            self.set_words()
            self.make_lower()
            self.sorted_words()
            return self.json.load_write(self.datajson)
        else:
            return self.json.load_write()

class SettingsValidator:

    def __init__(self) -> None:
        self.__key = b'OMv5ELkug3vciuGQwnk-GuQEabAx47DVeWWeIBQPqus='
        self.file_corrupt = False
        self.words_validator = WordsValidator('idn')
        self.languages_validator = Languages()
        self.katla_crypt = KatlaEncryptor()
        self.md = lambda : mkdir_data(f'file "{_file.PATH_DATA}/settings.katla" doesn\'t exists')
        self.md()

    def encrypt_data(self, data) -> None:
        self.md()
        fernet = _fernet.Fernet(self.__key)
        json_string = json.dumps(data)
        encrypted_data = fernet.encrypt(json_string.encode())
        with open(_file.DATA_SETTINGS, 'wb') as f:
            f.write(self.katla_crypt.encrypt(encrypted_data.decode()))
        self.file_corrupt = False

    def decrypt_data(self) -> dict[str, Any]:
        try:
            with open(_file.DATA_SETTINGS, 'rb') as f:
                decrypted_data = self.katla_crypt.decrypt(f.read())
            fernet = _fernet.Fernet(self.__key)
            decrypted_json = fernet.decrypt(decrypted_data.encode())
            return json.loads(decrypted_json.decode())
        except Exception as e:
            warn(f"{type(e).__name__}: {e}")
            self.set_default()
            return self.file_data

    def set_default(self) -> None:
        self.encrypt_data(JsonData.DEFAULT_SETTINGS)
        self.file_data = JsonData.DEFAULT_SETTINGS
        self.file_corrupt = True

    def load_and_validation(self) -> dict[str, Any]:
        self.file_data = self.decrypt_data()
        list_req_settings = {
            "theme": LiteralConst.all_theme,
            "keyboard-layout": LiteralConst.all_keyboard,
            "language-word": self.words_validator.get_lang_id(),
            "language": self.languages_validator.get_lang_id(),
            "sound-volume": [0, 100],
            "music-volume": [0, 100],
            "change-guess": [4, 10],
            "word-length": [4, 9],
            "fps": [10, 120],
            "geomatry": [0.9, 2.2],
            "use-valid-word": bool,
            "screen-size": [[550, 64000], [700, 64000]]
        }

        if not isinstance(self.file_data, dict):
            self.set_default()

        elif JsonData.DEFAULT_SETTINGS.keys() - self.file_data.keys():
            self.set_default()

        else:
            for key, value in self.file_data.items():

                if key in ['theme', 'keyboard-layout', 'language-word', 'language']:
                    if value not in list_req_settings[key]:
                        self.set_default()
                        break

                elif key in ['sound-volume', 'music-volume', 'change-guess', 'word-length', 'fps', 'geomatry']:
                    if not isinstance(value, int):
                        if not (key == 'geomatry' and isinstance(value, float)):
                            self.set_default()
                            break

                    elif value < list_req_settings[key][0]:
                        self.set_default()
                        break

                    elif value > list_req_settings[key][1]:
                        self.set_default()
                        break

                elif key == 'use-valid-word':
                    if not isinstance(value, bool):
                        self.set_default()
                        break

                elif key == 'screen-size':
                    if not isinstance(value, list):
                        if value != 'FULL':
                            self.set_default()
                        break

                    elif len(value) != 2:
                        self.set_default()
                        break

                    for size in value:
                        if not isinstance(size, int):
                            self.set_default()
                            break

                    if value[0] < list_req_settings[key][0][0]:
                        self.set_default()
                        break

                    elif value[0] > list_req_settings[key][0][1]:
                        self.set_default()
                        break

                    elif value[1] < list_req_settings[key][1][0]:
                        self.set_default()
                        break

                    elif value[1] > list_req_settings[key][1][1]:
                        self.set_default()
                        break

        return self.file_data

class GameDataValidator:

    def __init__(self) -> None:
        self.__key = b'6B4qF6oZ64V4_Z7sdCNKErkF_eT1A_qTP8HQMAbu2Uw='
        self.file_corrupt = False
        self.katla_crypt = KatlaEncryptor()
        self.md = lambda : mkdir_data(f'file "{_file.PATH_DATA}/game.katla" doesn\'t exists')
        self.md()

    def encrypt_data(self, data) -> None:
        self.md()
        fernet = _fernet.Fernet(self.__key)
        json_string = json.dumps(data)
        encrypted_data = fernet.encrypt(json_string.encode())
        with open(_file.DATA_GAME, 'wb') as f:
            f.write(self.katla_crypt.encrypt(encrypted_data.decode()))
        self.file_corrupt = False

    def decrypt_data(self) -> dict[str, Any]:
        try:
            with open(_file.DATA_GAME, 'rb') as f:
                decrypted_data = self.katla_crypt.decrypt(f.read())
            fernet = _fernet.Fernet(self.__key)
            decrypted_json = fernet.decrypt(decrypted_data.encode())
            return json.loads(decrypted_json.decode())
        except Exception as e:
            warn(f"{type(e).__name__}: {e}")
            self.set_default()
            return self.file_data

    def set_default(self) -> None:
        self.encrypt_data(JsonData.DEFAULT_DATA_GAME)
        self.file_data = JsonData.DEFAULT_DATA_GAME
        self.file_corrupt = True

    def load_and_validation(self) -> dict[str, Any]:
        self.file_data = self.decrypt_data()

        if not isinstance(self.file_data, dict):
            self.set_default()

        elif JsonData.DEFAULT_DATA_GAME.keys() - self.file_data.keys():
            self.set_default()

        else:
            for key, value in self.file_data.items():

                if key == 'coins':
                    if not isinstance(value, int):
                        if not isinf(value):
                            self.set_default()
                            break

                elif key == 'prize-claim-time':
                    if not isinstance(value, str):
                        self.set_default()
                        break

                    date_split = value.split('/')

                    if len(date_split) != 6:
                        self.set_default()
                        break
                    else:
                        for date in date_split:
                            if not date.isdigit():
                                self.set_default()
                                break

                elif key in ['hint', 'wins']:
                    if not isinstance(value, dict):
                        self.set_default()
                        break

                    elif self.file_data[key].keys() - JsonData.DEFAULT_DATA_GAME[key].keys():
                        self.set_default()
                        break

                    for value_hint in self.file_data[key].values():
                        if not isinstance(value_hint, int):
                            self.set_default()
                            break

                elif key in ['prize-taken', 'have-played', 'losses']:
                    if not isinstance(value, int):
                        self.set_default()
                        break

        return self.file_data