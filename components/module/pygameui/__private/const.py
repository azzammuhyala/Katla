import pygame as __pygame
import typing as __typing
import os as __os


# Default Colors
BLACK      = (0  , 0  , 0  )
GRAY       = (127, 127, 127)
LIGHT_GRAY = (190, 190, 190)
WHITE      = (255, 255, 255)
BLUE       = (0  ,   0, 255)
LIGHT_BLUE = (120, 120, 255)


# Unions
Path = __os.PathLike[str]
RealNumber = int | float
ArgsList = list | tuple
ElementID = __typing.Optional[__typing.Any]
ColorValue = ArgsList | __pygame.Color | int | str
CursorValue = __pygame.Cursor | int
RGBAOutput = tuple[int, int, int, int]
PygameColorValue = __pygame.Color | int | str | tuple[int, int, int] | RGBAOutput | __typing.Sequence[int]


# Union of textwrap
WrappedList = list[str]


# Literals
ModElementEvent = __typing.Literal[
    'Button',
    'Range',
    'Scroller',
    'ScrollerX',
    'ScrollerY',
    'GIF'
]

# Literal of button
ButtonEventClick = __typing.Literal['', 'r', 'c', 'l', 'rc', 'rl', 'cr', 'cl', 'lr', 'lc', 'rcl', 'rlc', 'crl', 'clr', 'lrc', 'lcr', 'sc', 'cs']
Buttons = __typing.Literal['Button', 'Range']

# Literal of scroller
Direction = __typing.Literal['x', 'y', 'xy']
Scrollers = __typing.Literal['Scroller', 'ScrollerX', 'ScrollerY']
# List
ListDirection = ['x', 'y', 'xy']

# Literal of textwrap
WrapFunc = __typing.Literal['word', 'mono']
WrapType = __typing.Literal['left', 'center', 'right', 'fill']


ModsElementEvent = {
    'button': ['Button', 'Range'],
    'scroller': ['Scroller', 'ScrollerX', 'ScrollerY'],
    'vgif': ['GIF']
}