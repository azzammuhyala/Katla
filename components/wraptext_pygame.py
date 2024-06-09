"""
Wraped text for pygame
"""

import pygame

def wrap(font: pygame.font.Font, text: str, wraplength: int) -> list[str]:

    """ pygame word wrap (not supported on line character "\\n") """

    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + ' ' + word if current_line != '' else word

        if font.size(test_line)[0] < wraplength:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines

def wrap_text(font: pygame.font.Font, text: str, wraplength: int) -> list[str]:

    """ pygame word wrap (suppored line character "\\n") """

    subline = []
    for line in text.split('\n'):
        subline.extend(wrap(font, line, wraplength))

    return subline