import random

_Key = int | float | str | bytes | bytearray
class DecoderError(Exception): ...

class DenXOR:

    def __init__(self, key: _Key) -> None:
        self.key = key

        if not isinstance(key, _Key):
            raise TypeError('The only supported key types are: int, float, str, bytes, and bytearray.')

    def generate_key(self, data_length: int) -> bytes:
        if not isinstance(data_length, int):
            raise TypeError('The only supported data_length type are int')

        random.seed(self.key)
        key = bytes([random.randint(0, 255) for _ in range(data_length)])
        random.seed(None)
        return key

    def xor_bytes(self, key: bytes, data: bytes | str) -> bytes:
        if not isinstance(data, str | bytes):
            raise TypeError('The only supported data types are: str, and bytes')
        if not isinstance(key, bytes):
            raise TypeError('The only supported key type are bytes on self.generate_key')
        if isinstance(data, str):
            data = data.encode()

        return bytes(a ^ b for a, b in zip(data, key))

    def dencrypt(self, data: bytes | str) -> bytes:
        key = self.generate_key(len(data))
        return self.xor_bytes(key, data)

class KatlaEncryptor:

    def __init__(self, key: _Key = b'object.Katla?key=%20NULL?!#ssLo1') -> None:
        self.__den = DenXOR(key)
        self.__char = {
            'A': b'\x12', 'B': b'.', 'C': b'\xcc', 'D': b'\xd1', 'E': b'\x01', 'F': b'\x8f', 'G': b'\x03', 'H': b'\x24', 'I': b'\x3b', 'J': b'\x0a', 'K': b'\x9c', 'L': b'\xff', 'M': b'\xfc', 'N': b'\x4a', 'O': b'\x1d', 'P': b'\x8e', 'Q': b'\x8a', 'R': b'<', 'S': b'\x55', 'T': b'R', 'U': b'\xcb', 'V': b'\xaa', 'W': b'\xa1', 'X': b'\x99', 'Y': b'\xfa', 'Z': b':',
            'a': b'\x2c', 'b': b'\x31', 'c': b'\xac', 'd': b'\xcf', 'e': b'\x38', 'f': b'\x8b', 'g': b'\x77', 'h': b'\x65', 'i': b'\x48', 'j': b'\xdd', 'k': b'\xdc', 'l': b'\x1b', 'm': b'\x41', 'n': b'\x3e', 'o': b'\x3f', 'p': b'\x90', 'q': b'\x23', 'r': b'\x1c', 's': b']', 't': b'*', 'u': b'\xca', 'v': b'\x4d', 'w': b'q', 'x': b'\x34', 'y': b'\x5f', 'z': b'\x02',
            '0': b'\x4c', '1': b'\x4b', '2': b'\x81', '3': b'(', '4': b'\x85', '5': b'\x09', '6': b'\x37', '7': b'\x7c', '8': b'\x7f', '9': b'~',
            '~': b'\xc0', '`': b'\x05', '!': b'\x44', '@': b'\x70', '#': b'\x97', '$': b'\x10', '%': b'\xf1', '^': b'\xb4', '&': b'\x83', '*': b'\xb2', '(': b'\xd5', ')': b'\x9e', '-': b'2', '_': b'\x9a', '=': b'\x2b', '+': b'\x57', '[': b'\x63', '{': b'\a', ']': b'\x43', '}': b'\x86', '\\': b'!', '|': b'\x13', ';': b'\x5c', ':': b'\x08', "'": b'\x25', '"': b'\x15', ',': b'\13', '<': b'\f', '.': b'\x0d', '>': b'\x5b', '/': b'\x2f', '?': b'\x6a', ' ': b'\x39', '\t': b'\x91', '\n': b'\x94'
        }

    def encrypt(self, source_string: str) -> bytes:
        if not isinstance(source_string, str):
            raise TypeError('source_string must be str')

        encrypted_bytes = b''

        for char in source_string:
            try:
                encrypted_bytes += self.__char[char]
            except KeyError:
                raise DecoderError(f"{repr(char)} character is not supported")
        return self.__den.dencrypt(encrypted_bytes)

    def decrypt(self, source_bytes: bytes) -> str:
        if not isinstance(source_bytes, bytes):
            raise TypeError('source_bytes must be bytes')

        decrypted_string = ''
        reversed_char_map = {value: key for key, value in self.__char.items()}

        for byte in self.__den.dencrypt(source_bytes):
            try:
                decrypted_string += reversed_char_map[bytes([byte])]
            except KeyError:
                raise DecoderError("Corrupted bytes")
        return decrypted_string