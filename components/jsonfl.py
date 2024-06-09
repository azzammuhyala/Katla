"""
Json File Module.

Requirements module:
```
fernet
```

Features:

- Writing, Reading JSON files (catching json decoder error exceptions)
- Encrypt, Decrypt JSON files
"""

import json
import os as _os
from typing import Union as _Union
from warnings import warn as _warn
try:
    import fernet as _fernet
except ModuleNotFoundError:
    _warn('The `fernet` module is not installed. please install with the command `pip install fernet`')
    exit(-1)

JsonType = _Union[dict, list, tuple, int, float, str, bool, None]

class read: ...
class encrypt: ...
class jsonen: ...

class Json:

    """
    Json class
    ----------

    - `file`: `str` -> Json file path
    - `default`: `JsonType` -> Default data (if get json decoder exception)
    - `indent`: `int | None` -> json file indentation/tabbing (default paramter is 4 spaces)
    """

    def __init__(self, file_path: str, default: JsonType = None, indent: int | None = 4) -> None:
        self.file_path = file_path
        self.default = default
        self.new_data = None
        self.indent = indent
        self.isdefault = False
        self.showlog = True

        self.__validation()

    def __repr__(self) -> str:
        encode_esc = lambda string : str(string).encode("unicode_escape").decode("utf-8")
        return f'Json(file_path="{encode_esc(self.file_path)}", default={encode_esc(self.default)}, indent={self.indent})'

    def __assert(self, condition: bool, raise_exception: Exception) -> None:
        if not bool(condition):
            raise raise_exception

    def __validation(self, data: JsonType = None, key: bytes = b'', moderead=b'') -> None:
        self.__assert(isinstance(data, JsonType), TypeError(f'data: must be valid json type not {type(data).__name__}'))
        self.__assert(isinstance(key, bytes), TypeError(f'key: must be bytes not {type(key).__name__}'))
        self.__assert(isinstance(moderead, _Union[bytes, jsonen]), TypeError(f'split_item: must be bytes or jsonen not {type(data).__name__}'))
        self.__assert(isinstance(self.file_path, str), TypeError(f'file: must be str not {type(self.file_path).__name__}'))
        self.__assert(isinstance(self.default, JsonType), TypeError(f'default: must be dict or list or None (no default) not {type(self.default).__name__}'))
        self.__assert(isinstance(self.indent, _Union[int, None]), TypeError(f'indent: must be int or None (no default) not {type(self.indent).__name__}'))

    def __write(self, data: JsonType = None) -> None:
        with open(self.file_path, 'w', encoding='utf8') as w:
            if isinstance(data, JsonType):
                json.dump(data, w, indent=self.indent)
            else:
                w.write('')
            self.new_data = data

    def copy(self):
        return Json(
            file_path = self.file_path,
            default = self.default,
            indent = self.indent
        )

    @property
    def file_exists(self) -> bool:
        return _os.path.exists(self.file_path)

    def load_write(self, new_data: _Union[JsonType, read] = read()) -> JsonType:
        is_read = isinstance(new_data, read)

        if not is_read:
            self.__validation(new_data)

        try:
            if is_read:

                try:
                    with open(self.file_path, 'r', encoding='utf8') as fl:
                        return json.load(fl)

                except json.decoder.JSONDecodeError:
                    self.__write(self.default)
                    self.isdefault = True
                    return self.default if is_read else self.new_data

            else:
                self.__write(new_data)
                return new_data

        except FileNotFoundError:
            self.__write(self.default)
            self.isdefault = True
            return self.default

        except PermissionError:
            if self.showlog:
                _warn("JSON file access denied by system. Please don't open too often and write files too fast")
            return self.default if is_read else self.new_data

    def get_json_dumps(self) -> str:
        return json.dumps(self.load_write())

    def encrypt_data(self, key: bytes, data: _Union[JsonType, encrypt] = encrypt()) -> dict[str, bytes]:

        self.__validation(data, key)

        if isinstance(data, encrypt):
            data_str = self.get_json_dumps()
        else:
            data_str = json.dumps(data)

        data_bytes = data_str.encode()
        cipher = _fernet.Fernet(key)
        ct_bytes = cipher.encrypt(data_bytes)
        return {'ct-bytes': ct_bytes}

    def decrypt_data(self, key: bytes, moderead: _Union[jsonen, bytes] = jsonen()) -> str:

        self.__validation(key=key, moderead=moderead)

        if isinstance(moderead, jsonen):
            ct_bytes = self.load_write()['ct-bytes'].encode()
        elif isinstance(moderead, bytes):
            with open(self.file_path, 'rb') as data:
                ct_bytes = data.read()

        cipher = _fernet.Fernet(key)
        pt = cipher.decrypt(ct_bytes)
        return pt.decode()

    def encrypt_json(self, key: bytes, data: _Union[JsonType, encrypt] = encrypt()) -> None:

        ct_bytes = self.encrypt_data(key, data)
        ct_bytes['ct-bytes'].decode()
        self.load_write(ct_bytes)

    def decrypt_json(self, key: bytes, moderead: _Union[bytes, jsonen] = jsonen()) -> JsonType:

        try:
            return json.loads(self.decrypt_data(key, moderead))
        except json.decoder.JSONDecodeError:
            raise ValueError('Invalid json decoder. Cannot decoder the decrypt file.')

def generate_random_keys() -> bytes:
    return _fernet.Fernet.generate_key()