from .__private.private import (
    pygame,
    typing,
    prvt as _prvt
)
from .__private.const import (
    RealNumber as _RealNumber,
    WrappedList as _WrappedList,
    WrapFunc as _WrapFunc,
    WrapType as _WrapType,
    PygameColorValue as _PygameColorValue
)


def wrap_mono(font: pygame.font.Font, word: str, wraplength: _RealNumber) -> _WrappedList:

    """
    Wraps a single word to fit within the specified width.

    Parameters:
        :param `font`: font text.
        :param `word`: main text or word.
        :param `wraplength`: Length to be wrapped.

    Returns:
        `WrappedList`
    """

    _prvt.asserting(isinstance(font, pygame.font.Font), TypeError(f'font: must be pygame.font.Font not {_prvt.get_type(font)}'))
    _prvt.asserting(isinstance(wraplength, _RealNumber), TypeError(f'wraplength: must be RealNumber not {_prvt.get_type(wraplength)}'))
    _prvt.asserting(wraplength > 0, ValueError(f'wraplength: illegal below 0 -> {wraplength}'))

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
        :param `font`: font text.
        :param `text`: main text or word.
        :param `wraplength`: Length to be wrapped.

    Returns:
        `WrappedList`
    """

    _prvt.asserting(isinstance(font, pygame.font.Font), TypeError(f'font: must be pygame.font.Font not {_prvt.get_type(font)}'))
    _prvt.asserting(isinstance(wraplength, _RealNumber), TypeError(f'wraplength: must be RealNumber not {_prvt.get_type(wraplength)}'))
    _prvt.asserting(wraplength > 0, ValueError(f'wraplength: illegal below 0 -> {wraplength}'))

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
        :param `font`: font text.
        :param `text`: main text or word.
        :param `wraplength`: Length to be wrapped.
        :param `wrap_fn`: wrap function type.

    Returns:
        `WrappedList`
    """

    text = str(text)
    wrap_fn = str(wrap_fn).lower()
    lines = text.split('\n')
    wrapped_lines = []

    for line in lines:

        match wrap_fn:

            case 'word':
                wrapped_lines.extend(wrap_word(font, line, wraplength))

            case 'mono':
                wrapped_lines.extend(wrap_mono(font, line, wraplength))

            case _:
                raise TypeError(f'wrap_fn: unknown wrap function -> {repr(wrap_fn)}')

    return wrapped_lines


def render_wrap(

        font: pygame.font.Font,
        text: str,
        wraplength: int,
        antialias: bool | typing.Literal[0, 1],
        color: _PygameColorValue,
        background: typing.Optional[_PygameColorValue] = None,
        wrap_fn: _WrapFunc = 'word',
        wrap_type: _WrapType = 'left',
        lngap: int = 0,

    ) -> pygame.Surface:

    """
    Render wraps text returns the wrapped text surface and supporting the newline character.

    Parameters:
        :param `font`: font text.
        :param `text`: main text or word.
        :param `wraplength`: Length to be wrapped.
        :param **kwargs render font method.
        :param `wrap_fn`: wrap function type.
        :param `wrap_type`: text wrapping position. In the form of left, center, right, and fill (justify).
        :param `lngap`: text line distance.

    Returns:
        `pygame.Surface`
    """

    _prvt.asserting(isinstance(lngap, _RealNumber), TypeError(f'lngap: must be RealNumber not {_prvt.get_type(lngap)}'))

    wrap_type = str(wrap_type).lower()
    wrapped_lines = wrap_text(font, text, wraplength, wrap_fn)

    if wrap_type == 'fill':
        if str(text):
            max_width = wraplength
        else:
            max_width = 0
    else:
        max_width = max(font.size(line)[0] for line in wrapped_lines)
    total_height = sum(font.size(line)[1] for line in wrapped_lines) + lngap * (len(wrapped_lines) - 1)
    y_offset = 0

    if background is None:
        surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
    else:
        surface = pygame.Surface((max_width, total_height))
        surface.fill(background)

    for line in wrapped_lines:

        if wrap_type == 'fill':
            x_offset = 0
            words = line.split()
            total_words_width = sum(font.size(word)[0] for word in words)
            extra_space = wraplength - total_words_width

            if len(words) > 1:
                space_between_words = extra_space / (len(words) - 1)
            else:
                space_between_words = extra_space

            for word in words:
                word_surface = font.render(word, antialias, color)
                surface.blit(word_surface, (x_offset, y_offset))
                x_offset += word_surface.get_width() + space_between_words

        else:
            text_surface = font.render(line, antialias, color)
            text_width = text_surface.get_width()

            match wrap_type:

                case 'left':
                    surface.blit(text_surface, (0, y_offset))

                case 'center':
                    surface.blit(text_surface, ((max_width - text_width) / 2, y_offset))

                case 'right':
                    surface.blit(text_surface, ((max_width - text_width), y_offset))

                case _:
                    raise TypeError(f'wrap_type: unknown wrap type -> {repr(wrap_type)}')

        y_offset += font.size(line)[1] + lngap

    return surface


__all__ = [
    'wrap_mono',
    'wrap_word',
    'wrap_text',
    'render_wrap'
]


del (
    _WrapFunc,
    _WrapType,
    _WrappedList,
    _PygameColorValue,
    typing
)