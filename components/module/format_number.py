from re import sub as _sub
from math import (isinf as _isinf, isnan as _isnan)

RealNumber = int | float

class exponents:
    exponents_en_us = {
        "decimal": ".",
        "separator": ",",
        "scientific": "E+",
        "thousand": "K",
        "million": "M",
        "billion": "B",
        "trillion": "T",
        "quadrillion": "Q",
        "quintillion": "Qn",
        "sextillion": "Sx",
        "septillion": "Sp",
        "octillion": "Oc",
        "nonillion": "Nn"
    }
    exponents_id = {
        "decimal": ",",
        "separator": ".",
        "scientific": "E+",
        "thousand": "Rb",
        "million": "Jt",
        "billion": "M",
        "trillion": "T",
        "quadrillion": "Kd",
        "quintillion": "Kn",
        "sextillion": "St",
        "septillion": "Sp",
        "octillion": "Ok",
        "nonillion": "Nn"
    }

class NumberFormat:

    def __init__(self, config_exponents: dict[str, str] = exponents.exponents_en_us, decimal_places: int = 1, use_exponent: bool = True, rounded: bool = True, anchor_decimal_places: bool = False) -> None:
        self.config_exponents = config_exponents
        tenpow = lambda x : 10 ** x
        self.exponents_mapping = {
            'thousand': tenpow(3),
            'million': tenpow(6),
            'billion': tenpow(9),
            'trillion': tenpow(12),
            'quadrillion': tenpow(15),
            'quintillion': tenpow(18),
            'sextillion': tenpow(21),
            'septillion': tenpow(24),
            'octillion': tenpow(27),
            'nonillion': tenpow(30)
        }
        self.decimal_separator = self.config_exponents['decimal']
        self.thousands_separator = self.config_exponents['separator']
        self.scientific_seperator = self.config_exponents['scientific']
        self.decimal_places = decimal_places
        self._const_decimal_places = decimal_places
        self.use_exponent = use_exponent
        self.rounded = rounded
        self.anchor_decimal_places = anchor_decimal_places

    def __validation(self, number) -> None:
        nametype = lambda x : type(x).__name__
        if not isinstance(number, RealNumber):
            raise TypeError('type error at number -> ' + nametype(number))
        elif not isinstance(self.decimal_places, int):
            raise TypeError('type error at NumberParse.decimal_places -> ' + nametype(self.decimal_places))
        elif self.decimal_places < 0:
            raise ValueError('value error at NumberParse.decimal_places -> ' + str(self.decimal_places))

    def rounded_number(self, number: RealNumber) -> str:
        self.__validation(number)

        if self.rounded:
            return f"{number:.{self.decimal_places}f}".replace('.', self.decimal_separator)

        parts = str(float(number)).split('.')
        interger_part = parts[0]

        if self.decimal_places > 0:
            decimal_part = self.decimal_separator + parts[1][:self.decimal_places]
        else:
            decimal_part = ''

        return interger_part + decimal_part

    def parse_precision(self, number: RealNumber) -> str:
        formatted_number = self.rounded_number(number)
        parts = formatted_number.split(self.decimal_separator)
        integer_part = parts[0]

        if self.decimal_places > 0:
            decimal_part = self.decimal_separator + parts[1]
        else:
            decimal_part = ''

        integer_part_with_separator = _sub(r'(?<=\d)(?=(\d{3})+$)', self.thousands_separator, integer_part)

        return integer_part_with_separator + decimal_part

    def parse_scientific(self, number: RealNumber) -> str:
        self.__validation(number)

        return (
            f"{number:.{self.decimal_places}e}"
                .replace('.', self.decimal_separator)
                .replace('e+', self.scientific_seperator)
        )

    def _parse_exponent(self, number: RealNumber, exponent_key: str) -> str:
        if self.use_exponent:
            return ('-' if number < 0 else '') + self.parse_precision(abs(number) / self.exponents_mapping[exponent_key]) + ' ' + self.config_exponents[exponent_key]
        return self.parse_precision(number)

    def parse(self, number: RealNumber) -> str:
        self.__validation(number)
        abs_number = abs(number)
        self.decimal_places = self._const_decimal_places

        if abs_number < self.exponents_mapping['thousand']:
            if not self.anchor_decimal_places:
                self.decimal_places = 0
            return self.parse_precision(number)
        elif self.exponents_mapping['thousand'] <= abs_number < self.exponents_mapping['million']:
            return self._parse_exponent(number, 'thousand')
        elif self.exponents_mapping['million'] <= abs_number < self.exponents_mapping['billion']:
            return self._parse_exponent(number, 'million')
        elif self.exponents_mapping['billion'] <= abs_number < self.exponents_mapping['trillion']:
            return self._parse_exponent(number, 'billion')
        elif self.exponents_mapping['trillion'] <= abs_number < self.exponents_mapping['quadrillion']:
            return self._parse_exponent(number, 'trillion')
        elif self.exponents_mapping['quadrillion'] <= abs_number < self.exponents_mapping['quintillion']:
            return self._parse_exponent(number, 'quadrillion')
        elif self.exponents_mapping['quintillion'] <= abs_number < self.exponents_mapping['sextillion']:
            return self._parse_exponent(number, 'quintillion')
        elif self.exponents_mapping['sextillion'] <= abs_number < self.exponents_mapping['septillion']:
            return self._parse_exponent(number, 'sextillion')
        elif self.exponents_mapping['septillion'] <= abs_number < self.exponents_mapping['octillion']:
            return self._parse_exponent(number, 'octillion')
        elif self.exponents_mapping['octillion'] <= abs_number < self.exponents_mapping['nonillion']:
            return self._parse_exponent(number, 'octillion')
        elif self.exponents_mapping['nonillion'] <= abs_number < self.exponents_mapping['nonillion'] * 1000:
            return self._parse_exponent(number, 'nonillion')
        elif _isinf(number) or _isnan(number):
            return number
        else:
            return self.parse_scientific(number)