"""
MARKDOWN DOCUMENTATION

# `pygameui.textwrap` / `pygametextwrap` module
Version: beta 1.0.0

pygame wraped text.


*next documentation will be created soon..*
"""


from .__private.private import (
    pygame,
    typing,
    prvt as _prvt
)
from .__private.const import (
    RealNumber as _RealNumber,
    WrappedList as _WrappedList,
    WrapFunc as _WrapFunc,
    PygameColorValue as _PygameColorValue
)


def wrap_mono(font: pygame.font.Font, word: str, wraplength: _RealNumber) -> _WrappedList:

    """
    Wraps a single word to fit within the specified width.

    Parameters:
        * `font`: font text
        * `word`: main text or word
        * `wraplength`: Length to be wrapped

    return -> `WrappedList`
    """

    _prvt.asserting(isinstance(font, pygame.font.Font), TypeError(f"font: must be pygame.font.Font not {_prvt.get_type(font)}"))
    _prvt.asserting(isinstance(wraplength, _RealNumber), TypeError(f"wraplength: must be RealNumber not {_prvt.get_type(wraplength)}"))

    word = str(word)

    if font.size(word)[0] <= wraplength:
        return [word]

    parts = []
    current_part = ''

    for char in word:
        if font.size(current_part + char)[0] <= wraplength:
            current_part += char
        else:
            parts.append(current_part)
            current_part = char

    if current_part:
        parts.append(current_part)

    return parts


def wrap_word(font: pygame.font.Font, text: str, wraplength: _RealNumber) -> _WrappedList:

    """
    Wraps a text of text to fit within the specified width.

    Parameters:
        * `font`: font text
        * `text`: main text or word
        * `wraplength`: Length to be wrapped

    return -> `WrappedList`
    """

    _prvt.asserting(isinstance(font, pygame.font.Font), TypeError(f"font: must be pygame.font.Font not {_prvt.get_type(font)}"))
    _prvt.asserting(isinstance(wraplength, _RealNumber), TypeError(f"wraplength: must be RealNumber not {_prvt.get_type(wraplength)}"))

    text = str(text)

    if text == '':
        return [text]

    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + ' ' + word if current_line else word

        if font.size(test_line)[0] <= wraplength:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)

            wrapped_words = wrap_mono(font, word, wraplength)

            for wrapped_word in wrapped_words[:-1]:
                lines.append(wrapped_word)

            current_line = wrapped_words[-1]

    if current_line:
        lines.append(current_line)

    return lines


def wrap_text(font: pygame.font.Font, text: str, wraplength: int, wrap_fn: _WrapFunc = 'word') -> list[str]:

    """
    Wraps text, supporting the newline character.

    Parameters:
        * `font`: font text
        * `text`: main text or word
        * `wraplength`: Length to be wrapped
        * `wrap_fn`: wrap function type

    return -> `WrappedList`
    """

    _prvt.asserting(isinstance(font, pygame.font.Font), TypeError(f"font: must be pygame.font.Font not {_prvt.get_type(font)}"))
    _prvt.asserting(isinstance(wraplength, _RealNumber), TypeError(f"wraplength: must be RealNumber not {_prvt.get_type(wraplength)}"))

    text = str(text)
    lines = text.split('\n')
    wrapped_lines = []

    for line in lines:

        match wrap_fn:

            case 'word':
                wrapped_lines.extend(wrap_word(font, line, wraplength))

            case 'mono':
                wrapped_lines.extend(wrap_mono(font, line, wraplength))

            case _:
                raise TypeError(f'wrap_fn: unknown wrap function -> {wrap_fn}')

    return wrapped_lines


def render_wrap(

        font: pygame.font.Font,
        text: str,
        wraplength: int,
        antialias: bool | typing.Literal[0, 1],
        color: _PygameColorValue,
        background: typing.Optional[_PygameColorValue] = None,
        wrap_fn: _WrapFunc = 'word',
        gap: int = 0,

    ) -> pygame.Surface:

    """
    Render wraps text returns the wrapped text surface and supporting the newline character.

    Parameters:
        * `font`: font text
        * `text`: main text or word
        * `wraplength`: Length to be wrapped
        * **kwargs render font method
        * `wrap_fn`: wrap function type
        * `gap`: text line distance

    return -> `pygame.Surface`
    """

    wrapped_lines = wrap_text(font, text, wraplength, wrap_fn)
    max_width = max(font.size(line)[0] for line in wrapped_lines)
    total_height = sum(font.size(line)[1] for line in wrapped_lines) + gap * (len(wrapped_lines) - 1)
    y_offset = 0

    if background == None:
        surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
    else:
        surface = pygame.Surface((max_width, total_height))
        surface.fill(background)

    for line in wrapped_lines:
        text_surface = font.render(line, antialias, color)
        surface.blit(text_surface, (0, y_offset))
        y_offset += font.size(line)[1] + gap

    return surface


__version__ = '1.0.0.beta'
__all__ = [
    'wrap_mono',
    'wrap_word',
    'wrap_text',
    'render_wrap'
]


del (
    _WrapFunc,
    _WrappedList,
    _PygameColorValue,
    typing
)