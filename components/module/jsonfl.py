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
import typing as _typ
from warnings import warn as _warn
try:
    import fernet as _fernet
except ModuleNotFoundError:
    _warn('The `fernet` module is not installed. please install with the command `pip install fernet`')
    exit(-1)

JsonObj = dict | list | int | float | str | bool | None
Path = _os.PathLike[str]

class mode:
    def __init__(self, id) -> None:
        self.id = id

class Json:

    """
    Json class
    ----------
    - `file`: `str` -> Json file path
    - `default`: `JsonType` -> Default data (if get json decoder exception)
    - `indent`: `int | None` -> json file indentation/tabbing (default paramter is 4 spaces)
    - `encoding`: `str` -> File encoding (default "utf-8")
    """

    def __init__(self, file_path: Path, default: JsonObj = None, indent: int | None = 4, encoding: str = "utf-8") -> None:
        self.file_path = file_path
        self.default = default
        self.encoding = encoding
        self.new_data = None
        self.indent = indent
        self.isdefault = False
        self.showlog = True

        self.__validation()

    def __repr__(self) -> str:
        return f'Json(file_path={repr(self.file_path)}, default={repr(self.default)}, indent={repr(self.indent)}, encoding={repr(self.encoding)})'

    def __assert(self, condition: bool, raise_exception: Exception) -> None:
        if not bool(condition):
            raise raise_exception

    def __validation(self, data: JsonObj = None, key: bytes = b'', moderead: bytes | mode = b'') -> None:
        self.__assert(isinstance(data, JsonObj), TypeError(f'data: must be valid json type not {type(data).__name__}'))
        self.__assert(isinstance(key, bytes), TypeError(f'key: must be bytes not {type(key).__name__}'))
        self.__assert(isinstance(moderead, bytes | mode), TypeError(f'split_item: must be bytes or mode not {type(data).__name__}'))
        self.__assert(isinstance(self.file_path, str), TypeError(f'file: must be str not {type(self.file_path).__name__}'))
        self.__assert(isinstance(self.default, JsonObj), TypeError(f'default: must be dict or list or None (no default) not {type(self.default).__name__}'))
        self.__assert(isinstance(self.indent, int | None), TypeError(f'indent: must be int or None (no default) not {type(self.indent).__name__}'))

    def __write(self, data: JsonObj) -> None:
        with open(self.file_path, 'w', encoding=self.encoding) as w:

            if isinstance(data, JsonObj):
                json.dump(data, w, indent=self.indent)
            else:
                w.write('')

            self.new_data = data

    def copy(self):
        return Json(
            file_path = self.file_path,
            default = self.default,
            indent = self.indent,
            encoding = self.encoding
        )

    @property
    def file_exists(self) -> bool:
        return _os.path.exists(self.file_path)

    def load_write(self, new_data: JsonObj | mode = mode('read')) -> JsonObj:
        is_read = False

        if isinstance(new_data, mode):
            is_read = True

        if not is_read:
            self.__validation(new_data)

        try:
            if is_read:

                try:
                    with open(self.file_path, 'r', encoding=self.encoding) as fl:
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

    def encrypt_data(self, key: bytes, data: JsonObj | mode = mode('encrypt')) -> dict[_typ.Literal['ct-bytes'], bytes]:

        self.__validation(data, key)

        if isinstance(data, mode):
            data_str = self.get_json_dumps()
        else:
            data_str = json.dumps(data)

        cipher = _fernet.Fernet(key)
        data_bytes = data_str.encode()
        ct_bytes = cipher.encrypt(data_bytes)
        return {'ct-bytes': ct_bytes}

    def decrypt_data(self, key: bytes, moderead: bytes | mode = mode('jsonen')) -> str:

        self.__validation(key=key, moderead=moderead)

        if isinstance(moderead, mode):
            ct_bytes = self.load_write()['ct-bytes'].encode()

        elif isinstance(moderead, bytes):
            with open(self.file_path, 'rb') as data:
                ct_bytes = data.read()

        cipher = _fernet.Fernet(key)
        pt = cipher.decrypt(ct_bytes)
        return pt.decode()

    def encrypt_json(self, key: bytes, data: JsonObj | mode = mode('encrypt')) -> None:

        ct_bytes = self.encrypt_data(key, data)
        ct_bytes['ct-bytes'].decode()
        self.load_write(ct_bytes)

    def decrypt_json(self, key: bytes, moderead: bytes | mode = mode('jsonen')) -> JsonObj:

        try:
            return json.loads(self.decrypt_data(key, moderead))
        except json.decoder.JSONDecodeError:
            raise ValueError('Invalid json decoder. Cannot decoder the decrypt file.')

def generate_random_keys() -> bytes:
    return _fernet.Fernet.generate_key()