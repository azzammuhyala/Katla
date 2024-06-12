"""
Wraped text for pygame
"""

import pygame

def wrap_word(font: pygame.font.Font, word: str, wraplength: int) -> list[str]:

    """ Wraps a single word to fit within the specified width. """

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

def wrap_line(font: pygame.font.Font, line: str, wraplength: int) -> list[str]:

    """ Wraps a line of text to fit within the specified width. """

    if line == '':
        return [line]

    words = line.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + ' ' + word if current_line else word

        if font.size(test_line)[0] <= wraplength:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            wrapped_words = wrap_word(font, word, wraplength)
            for wrapped_word in wrapped_words[:-1]:
                lines.append(wrapped_word)
            current_line = wrapped_words[-1]

    if current_line:
        lines.append(current_line)

    return lines

def wrap_text(font: pygame.font.Font, text: str, wraplength: int) -> list[str]:

    """ Wraps text, supporting the newline character. """

    lines = text.split('\n')
    wrapped_lines = []

    for line in lines:
        wrapped_lines.extend(wrap_line(font, line, wraplength))

    return wrapped_lines