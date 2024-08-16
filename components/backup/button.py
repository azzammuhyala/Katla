"""
MARKDOWN DOCUMENTATION

# `pygameui.button` / `pygamebutton` module
Version: 1.1.2

pygame elements. Button and Range.

Explanations
------------
pygamebutton is a special tool module for displaying general button elements.
Pygame does not provide a button media element. However, the functions and
methods provided by the pygame module provide various ways to create this
button elements. And this module is used as a buttons function that is
ready-made and ready to use.

Events
------
How to get input from pygame button? There are several ways to get button
input and execute it according to its function.

1. Method `ButtonEvent`

Each button class consists of the button_event attribute which is a class
object ButtonEvent. This class plays a role in getting events that occur on
the button such as mousehover, inactive, active, value when clicked, etc.
Every type buttons have different attributes.

How to use:

Create a variable to contain the button.
```py
button1_rect = pygame.Rect(25, 25, 50, 50)
button1 = pygamebutton.Button(
    screen,
    rect=button1_rect,
    id='button1' # The id function will be used in the second event method
)
```

Then create an event loop and call the draw_and_update method for interaction
knob.
```py
# loops game
while ...:
    for event in pygame.event.get():
        ... # your events
        button1.handle_event(event)

    button1.draw_and_update()
```

Check if the button is pressed or not.
```py
    if button1.button_event.value:
        # do something..
```

You can get the button event from the return of the draw_and_update method.
```py
    button1_event = button1.draw_and_update()

    if button1_event.value:
        # do something..
```

2. Method `pygame.Event`

This event method captures button events from the pygame event loop. Will
However, this feature requires an id parameter to be able to differentiate
between button and this method does not provide button event information.
overall.

How to use:

Create a variable to contain the button, enter the id type of the button.
```py
button1_rect = pygame.Rect(...)
button1 = pygamebutton.Button(
    ...
    id='button1' # enter the id
)
```

How to catch the events.
```py
# loops game
while ...:
    for event in pygame.event.get():
        ... # your events
        button1.handle_event(event)

        if event.type == pygamebutton.BUTTON_CLICK:
            if event.id == button1.id:
                # do something..
            ...

    button1.draw_and_update()
```

Properties of the event that can be obtained:
* value
* button_type
* id
* range_value (for Range button)

Information
-----------
This latest version allows you to edit properties directly like this without
using the `edit_param` method:
```py
button1.id = 'btn1'
```

The `edit_param` method is still available on the button. Just adjust it to
your needs:
```py
button1.edit_param(id='btn1')
```

For the latest version editing values from Range ​​still uses the `set_value`
method:
```py
myrange.set_value(25)
```
If you change it via properties it may cause minor errors or out of sync in
the Range display with the given value.

Examples
--------
Here is a example of a basic setup (opens the window, updates the screen, and
handles events):
```py
import pygame # import the pygame
import pygamebutton # import the pygamebutton

# pygame setup
pygame.init()
running = True
cursor = pygamebutton.SysCursor() # gets all system cursor (optional)

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

pygame.display.set_caption('Button Test')

font = pygame.font.SysFont('Monospace', 25, True)
showtext = lambda text : font.render(text, True, 'white')
text = showtext('Press one of the buttons')

# button rects
rect_button1 = pygame.Rect(100, (screen.get_height() - 100) / 2, 100, 100)
rect_button2 = pygame.Rect(screen.get_width() - 200, (screen.get_height() - 100) / 2, 100, 100)
# Range rects
rect_range = pygame.Rect((screen.get_width() - 400) / 2, 100, 400, 10)

# The size of the thumb range
thumb_size = (17, 17)

# initialization button (Do not initialization Buttons in the game loop because this will be affected by time, events, etc)
button1 = pygamebutton.Button(screen, rect_button1, id='button1', text='BUTTON 1')

# if you want to copy an element, use the copy() method and fill it with new parameters if necessary
button2 = button1.copy(id='button2', text='BUTTON 2', outline_size=5, rect=rect_button2, only_click='lrc', click_speed=250)

# input range parameters
range_button = pygamebutton.Range(screen, rect_range, id='range_button', thumb_size=thumb_size, min_value=0, max_value=100, value=50, step=1, range_value_output=int)

# manager (Optional) set events, draws, etc. in several buttons at once
manager = pygamebutton.Manager(button1, button2, range_button, inactive_cursor=cursor.ARROW, active_cursor=cursor.HAND)

# screen loop
while running:

    # events
    for event in pygame.event.get():
        # when the user clicks the X to close the screen (pygame)
        if event.type == pygame.QUIT:
            running = False

        # handle events of all buttons
        manager.handle_event(event)

        # event when one of the buttons is pressed
        if event.type == pygamebutton.BUTTON_CLICK:
            # your case
            print(f'button event property: id:{event.id}, ' +
                  f'button_type:{event.button_type}, ' +
                  f'value:{event.value}, ' + 
                  ("range_value: " + str(event.range_value) if event.button_type == 'Range' else "")
                )

    # fill screen black
    screen.fill('black')

    # blit or draw and update the button
    manager.draw_and_update()

    text_range = showtext(f'Value Range: {range_button.button_event.range_value}')

    # get button event
    if button1.button_event.value:
        msg = 'Pressed BUTTON 1 -> ' + button1.button_event.value
        print(msg)
        text = showtext(msg)

    elif button2.button_event.value:
        msg = 'Pressed BUTTON 2 -> ' + button2.button_event.value
        print(msg)
        text = showtext(msg)

    # show the range event text
    screen.blit(text_range, ((screen.get_width() - text_range.get_width()) / 2, 115))
    # show the button event text
    screen.blit(text, ((screen.get_width() - text.get_width()) / 2, 450))
    # flip() the display to put your work on screen
    pygame.display.flip()
    # Set the frame-rate speed to 60 (fps)
    clock.tick(60)

# clean up pygame resources
pygame.quit()
```

Thank you to those of you who have read the documentation and code examples.
"""


import pygame
import typing as _typing
from abc import (
    ABC as _ABC,
    abstractmethod as _abstract
)

# Literals
_ButtonEventValue = _typing.Literal['', 'r', 'c', 'l', 'rc', 'rl', 'cr', 'cl', 'lr', 'lc', 'rcl', 'rlc', 'crl', 'clr', 'lrc', 'lcr', 'sc', 'cs']
_Buttons = _typing.Literal['Button', 'Range']


class _Private:

    """ _Private - private class """

    def __init__(self) -> None:

        """
        This class is private and contains methods contained in the button element
        """

        self.init_rect = pygame.Rect(0, 0, 0, 0)

    def asserting(self, condition: bool, raise_exception: Exception) -> None:

        """
        Checks the condition if it is False then raises an exception.

        return -> `None`
        """

        if not bool(condition):
            raise raise_exception

    def get_type(self, obj: object) -> str:

        """
        Gets type object.

        return -> `str`
        """

        return type(obj).__name__

    def get_mouse_pressed(self, only_click: _ButtonEventValue) -> tuple[bool, bool, bool]:

        """
        Gets mouse presses corresponding to existing only_click.

        return -> `tuple[bool, bool, bool]` => (l, c, r)
        """

        isinonlyclick = lambda click: click in only_click 
        pressed = pygame.mouse.get_pressed()
        return (
            pressed[0] if isinonlyclick('l') else False,
            pressed[1] if isinonlyclick('c') else False,
            pressed[2] if isinonlyclick('r') else False
        )

    def is_partially_outside(self, main_rect: pygame.Rect, order_rect: pygame.Rect) -> bool:

        """
        Gets whether a rect is outside the main rect area completely.

        return -> `bool`
        """

        return not (
            main_rect.collidepoint(order_rect.left, order_rect.top) or
            main_rect.collidepoint(order_rect.right, order_rect.top) or
            main_rect.collidepoint(order_rect.left, order_rect.bottom) or
            main_rect.collidepoint(order_rect.right, order_rect.bottom) or
            order_rect.collidepoint(main_rect.left, main_rect.top) or
            order_rect.collidepoint(main_rect.right, main_rect.top) or
            order_rect.collidepoint(main_rect.left, main_rect.bottom) or
            order_rect.collidepoint(main_rect.right, main_rect.bottom)
        )


class SysCursor(int):

    """ SysCursor - cursor system type and set the cursor """

    ARROW: int = pygame.SYSTEM_CURSOR_ARROW
    CROSSHAIR: int = pygame.SYSTEM_CURSOR_CROSSHAIR
    HAND: int = pygame.SYSTEM_CURSOR_HAND
    IBEAM: int = pygame.SYSTEM_CURSOR_IBEAM
    NO: int = pygame.SYSTEM_CURSOR_NO
    SIZEALL: int = pygame.SYSTEM_CURSOR_SIZEALL
    SIZENESW: int = pygame.SYSTEM_CURSOR_SIZENESW
    SIZENS: int = pygame.SYSTEM_CURSOR_SIZENS
    SIZENWSE: int = pygame.SYSTEM_CURSOR_SIZENWSE
    SIZEWE: int = pygame.SYSTEM_CURSOR_SIZEWE
    WAIT: int = pygame.SYSTEM_CURSOR_WAIT
    WAITARROW: int = pygame.SYSTEM_CURSOR_WAITARROW

    def __init__(self, id: _typing.Optional[int] = None) -> None:
        super().__init__()

        self.id = id
        self.__set_cursor_id = self.ARROW

    def copy(self):
        return self.__class__(self)

    def set_cursor(self, id: int | pygame.Cursor | None) -> None:
        if id is None:
            id = self.id
        pygame.mouse.set_cursor(id)
        self.__set_cursor_id = id

    def get_cursor(self) -> pygame.Cursor:
        return pygame.mouse.get_cursor()

    def get_set_cursor(self) -> int:
        return self.__set_cursor_id


# Default Colors
_BLACK      = (0  , 0  , 0  )
_GRAY       = (127, 127, 127)
_LIGHT_GRAY = (190, 190, 190)
_WHITE      = (255, 255, 255)
_BLUE       = (0  ,   0, 255)
_LIGHT_BLUE = (120, 120, 255)

# Private Initialization
_prvt = _Private()

# Unions
_RealNumber = int | float
_ArgsList = list | tuple
_ButtonID = _typing.Optional[_typing.Any]
_ColorValue = _ArgsList | pygame.Color | int | str
_CursorValue = pygame.Cursor | int

# ID events
BUTTON_CLICK: int = pygame.USEREVENT + 1


class ButtonEvent:

    """ ButtonEvent - The event of button function """

    def __init__(self, value: _ButtonEventValue, type: _Buttons, id: _ButtonID = None) -> None:

        _prvt.asserting(isinstance(value, str), TypeError(f'value: must be str type not {_prvt.get_type(value)}'))
        _prvt.asserting(isinstance(type, str), TypeError(f'type: must be str type not {_prvt.get_type(type)}'))

        self.value: _ButtonEventValue = value.lower()
        self.type: _Buttons = type
        self.id: _ButtonID = id
        self.ismousehover: bool = None
        self.cursor_active: bool = None
        self.cursor_inactive: bool = None

        # Button
        if type == 'Button':
            self.isbuttoninactive: bool = None
            self.isbuttonhover: bool = None
            self.isbuttonactive: bool = None

        # Range
        elif type == 'Range':
            self.israngeinactive: bool = None
            self.israngehover: bool = None
            self.israngeactive: bool = None
            self.isdragging: bool = None
            self.range_value: _RealNumber = None

        else:
            raise TypeError(f"type: unknown type {repr(type)}")

    def _reset_property(self) -> None:
        self.__init__('', self.type, self.id)

    def _send_event(self) -> None:
        if self.type == 'Button':
            click_event = pygame.event.Event(BUTTON_CLICK, value=self.value, button_type=self.type, id=self.id)
        elif self.type == 'Range':
            click_event = pygame.event.Event(BUTTON_CLICK, value=self.value, button_type=self.type, id=self.id, range_value=self.range_value)

        pygame.event.post(click_event)

    def copy(self):
        return ButtonEvent(value=self.value, type=self.type, id=self.id)

    def __str__(self) -> str:
        return self.value

    def __getitem__(self, index: int) -> str:
        _prvt.asserting(isinstance(index, int), TypeError(f'index: must be int type not {_prvt.get_type(index)}'))
        return self.value[index]

    def __eq__(self, order) -> bool | None:
        if isinstance(order, ButtonEvent):
            return [self.value, self.type, self.id] == [order.value, order.type, order.id]
        elif isinstance(order, str):
            return self.value == order

        return None

    def __ne__(self, order) -> bool | None:
        eq = self.__eq__(order)
        return (not eq if eq is not None else None)

    def __len__(self) -> int:
        return len(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)


class border_radius:

    """ border_radius - Border radius type in pygame.draw.rect. Used for border styling purposes on elements that use this function """

    def __init__(

        self,
        radius: int = -1,
        top_left_radius: int = -1,
        top_right_radius: int = -1,
        bottom_left_radius: int = -1,
        bottom_right_radius: int = -1
 
    ) -> None:

        self.radius = radius
        self.top_left_radius = top_left_radius
        self.top_right_radius = top_right_radius
        self.bottom_left_radius = bottom_left_radius
        self.bottom_right_radius = bottom_right_radius

        for key, value in self.get_param().items():
            _prvt.asserting(isinstance(value, int), TypeError(f'{key}: must be int type not {_prvt.get_type(value)}'))

    def copy(self):
        return border_radius(**self.get_param())

    def get_param(self) -> dict[str, int]:
        return {
            'radius': self.radius,
            'top_left_radius': self.top_left_radius,
            'top_right_radius': self.top_right_radius,
            'bottom_left_radius': self.bottom_left_radius,
            'bottom_right_radius': self.bottom_right_radius
        }

    @property
    def draw_rect_kwargs(self) -> dict[str, int]:
        return {
            'border_radius': self.radius,
            'border_top_left_radius': self.top_left_radius,
            'border_top_right_radius': self.top_right_radius,
            'border_bottom_left_radius': self.bottom_left_radius,
            'border_bottom_right_radius': self.bottom_right_radius
        }


class button_color:

    """ button_color - The color of each button or range attribute. consisting of inactive, active, and hover """

    def __init__(

        self,
        inactive_color: _typing.Optional[_ColorValue] = None,
        active_color: _typing.Optional[_ColorValue] = None,
        hover_color: _typing.Optional[_ColorValue] = None,

    ) -> None:

        self.inactive_color = inactive_color
        self.active_color = active_color
        self.hover_color = hover_color

        for key, value in self.get_param().items():
            _prvt.asserting(isinstance(value, _ColorValue | None), TypeError(f'{key}: must be ColorType or (None for default) not {_prvt.get_type(value)}'))

    def copy(self):
        return button_color(**self.get_param())

    def get_param(self) -> dict[str, _ColorValue | None]:
        return {
            'inactive_color': self.inactive_color,
            'active_color': self.active_color,
            'hover_color': self.hover_color
        }


class _ButtonInterface(_ABC):

    """ _ButtonInterface - Button interface class. As a means of interface to the button class. """

    @_abstract
    @_typing.overload
    def __init__(self, surface_screen: pygame.Surface, rect: pygame.Rect, id: _ButtonID) -> None: ...
    @_abstract
    @_typing.overload
    def __init__(self) -> None: ...
    ...
    @_abstract
    def copy(self, **kwargs): ...
    @_abstract
    def edit_param(self, **kwargs) -> None: ...
    @_abstract
    def get_param(self) -> dict[str, object]: ...
    @_abstract
    def get_private_attr(self, remove_underscore: bool = False) -> dict[str, object]: ...
    @_abstract
    @_typing.overload
    def handle_event(self, event: pygame.event.Event) -> None: ...
    @_abstract
    @_typing.overload
    def handle_event(self, event: pygame.event.Event, handled_button: bool = False) -> None: ...
    @_abstract
    def draw_and_update(self) -> ButtonEvent: ...
    @_abstract
    def draw_inactive(self) -> None: ...
    @_abstract
    def draw_hover(self) -> None: ...
    @_abstract
    def draw_active(self) -> None: ...


class Button(_ButtonInterface):

    """ Button - Push button class, creates a button function through the pygame screen and can set it with the parameters provided. """

    def __init__(

            self,
            surface_screen: pygame.Surface,
            rect: pygame.Rect,
            id: _ButtonID = None,
            text: str = '',
            font: _typing.Optional[pygame.font.Font] = None,
            hide: bool = False,
            outline_size: _typing.Optional[_RealNumber] = None,
            antialias_text: bool | _typing.Literal[0, 1] = True,
            image: _typing.Optional[pygame.Surface] = None,
            image_scale: _typing.Optional[_RealNumber | _ArgsList] = None,
            get_rect_image_kwargs: _typing.Optional[dict] = None,
            get_rect_text_kwargs: _typing.Optional[dict] = None,
            color: button_color = button_color(_WHITE, _LIGHT_GRAY, _GRAY),
            text_color: button_color = button_color(_BLACK, _BLACK, _BLACK),
            outline_color: button_color = button_color(_GRAY, _WHITE, _LIGHT_GRAY),
            inactive_cursor: _typing.Optional[_CursorValue] = None,
            active_cursor: _typing.Optional[_CursorValue] = None,
            only_click: _ArgsList | _ButtonEventValue = 'l',
            click_speed: int = 50,
            borders: border_radius = border_radius()

        ) -> None:

        """
        param:
            * `surface_screen`: screen surface -> pygame.display.set_mode((x, y)) or pygame.Surface
            * `rect`: rect button
            * `id`: ID Button for events
            * `text`: text button
            * `font`: font text
            * `hide`: Hides the button but can still receive input. (Doesn't apply to text, image, outline (if not None value))
            * `outline_size`: outline size of the button
            * `antialias_text`: param at -> font.render(text, antialias=..., ...)
            * `image`: image or icon on the button. (Use pygame.transform.scale(<Surface image source>, (rect button size))) to fit and fit the main button
            * `image_scale`: transform / scaled the size of the image surface. (If the type is numeric, then the size will be the size of the rect button with a margin of the numbers entered. If the type is tuple[number, number], then it will follow the scale of the contents of the tuple)
            * `get_rect_image_kwargs`: param at -> image.get_rect(...)
            * `get_rect_text_kwargs`: param at -> font.render.get_rect(...)
            * `color`: button color
            * `text_color`: text color
            * `outline_color`: outline color
            * `inactive_cursor`: change the cursor (un-hover)
            * `active_cursor`: change the cursor (hover)
            * `only_click`: click response ('r', 'c', 'l')
            * `click_speed`: click speed (ms)
            * `borders`: pygame.draw.rect borders. Use border_radius class
        """

        self.button_event: ButtonEvent = ButtonEvent('', 'Button', id)
        self.ishandlebyevent: bool = False

        self.__font_default: bool = False
        self.__initialization: bool = True

        self.surface_screen = surface_screen
        self.rect = rect
        self.id = id
        self.text = text
        self.font = font
        self.hide = hide
        self.outline_size = outline_size
        self.antialias_text = antialias_text
        self.image = image
        self.image_scale = image_scale
        self.get_rect_text_kwargs = get_rect_text_kwargs
        self.get_rect_image_kwargs = get_rect_image_kwargs
        self.color = color
        self.text_color = text_color
        self.outline_color = outline_color
        self.inactive_cursor = inactive_cursor
        self.active_cursor = active_cursor
        self.only_click = only_click
        self.click_speed = click_speed
        self.borders = borders

        self._send_event: bool = True

        self.__last_click_time: int = 0
        self.__clicked_button: bool = False
        self.__button_outside: bool = False
        self.__get_event: ButtonEvent = ButtonEvent('', 'Button')

        self.__initialization = False

    def __render_active_button(self, current_time: int, change_config: bool) -> None:

        """
        Private method. Render the active button.
        
        return -> `None`
        """

        if not self.__button_outside:

            if isinstance(self.__outline_size, _RealNumber):
                pygame.draw.rect(
                    self.__surface_screen,
                    self.__outline_color.active_color,
                    pygame.Rect(
                        self.__rect.left - self.__outline_size,
                        self.__rect.top - self.__outline_size,
                        self.__rect.width + self.__outline_size * 2,
                        self.__rect.height + self.__outline_size * 2
                    ),
                    (
                        int(self.__outline_size) + 1)
                        if self.__outline_size - int(self.__outline_size) > 0.1 else
                        int(self.__outline_size
                    ),
                    **self.__borders.draw_rect_kwargs
                )

            if not self.__hide:
                pygame.draw.rect(self.__surface_screen, self.__color.active_color, self.__rect, **self.__borders.draw_rect_kwargs)

            if self.__image is not None:
                if self.__get_rect_image_kwargs is None:
                    self.__surface_screen.blit(self.__scaled_image, self.__scaled_image.get_rect(center=self.__rect.center))
                else:
                    self.__surface_screen.blit(self.__scaled_image, self.__scaled_image.get_rect(**self.__get_rect_image_kwargs))

            if self.__text:
                text_surface = self.__font.render(self.__text, self.__antialias_text, self.__text_color.active_color)

                if self.__get_rect_text_kwargs is None:
                    text_rect = text_surface.get_rect(center=self.__rect.center)
                else:
                    text_rect = text_surface.get_rect(**self.__get_rect_text_kwargs)

                self.__surface_screen.blit(text_surface, text_rect)

            if change_config:
                self.__clicked_button = False
                self.__last_click_time = current_time

    def __render_inactive_hover_button(self, ismousehover: bool) -> None:

        """
        Private method. Render the inactive or hover button.

        return -> `None`
        """

        if not self.__button_outside:

            if isinstance(self.__outline_size, _RealNumber):
                pygame.draw.rect(
                    self.__surface_screen,
                    (
                        self.__outline_color.hover_color
                        if (self.__outline_color.hover_color is not None) and ismousehover else
                        self.__outline_color.inactive_color
                    ),
                    pygame.Rect(
                        self.__rect.left - self.__outline_size,
                        self.__rect.top - self.__outline_size,
                        self.__rect.width + self.__outline_size * 2,
                        self.__rect.height + self.__outline_size * 2
                    ),
                    (
                        int(self.__outline_size) + 1)
                        if self.__outline_size - int(self.__outline_size) > 0.1 else
                        int(self.__outline_size
                    ),
                    **self.__borders.draw_rect_kwargs
                )

            if not self.__hide:
                pygame.draw.rect(
                    self.__surface_screen,
                    (
                        self.__color.hover_color
                        if (self.__color.hover_color is not None) and ismousehover else
                        self.__color.inactive_color
                    ), self.__rect, **self.__borders.draw_rect_kwargs
                )

            if self.__image is not None:
                if self.__get_rect_image_kwargs is None:
                    self.__surface_screen.blit(self.__scaled_image, self.__scaled_image.get_rect(center=self.__rect.center))
                else:
                    self.__surface_screen.blit(self.__scaled_image, self.__scaled_image.get_rect(**self.__get_rect_image_kwargs))

            if self.__text:
                text_surface = self.font.render(self.__text, self.__antialias_text, (self.__text_color.hover_color if (self.__text_color.hover_color is not None) and ismousehover else self.__text_color.inactive_color))

                if self.__get_rect_text_kwargs is None:
                    text_rect = text_surface.get_rect(center=self.rect.center)
                else:
                    text_rect = text_surface.get_rect(**self.__get_rect_text_kwargs)

                self.__surface_screen.blit(text_surface, text_rect)

    @property
    def surface_screen(self) -> pygame.Surface:
        return self.__surface_screen

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @property
    def id(self) -> _ButtonID:
        return self.__id

    @property
    def text(self) -> str:
        return self.__text

    @property
    def font(self) -> _typing.Optional[pygame.font.Font]:
        return self.__font

    @property
    def hide(self) -> bool:
        return self.__hide

    @property
    def outline_size(self) -> _typing.Optional[_RealNumber]:
        return self.__outline_size

    @property
    def antialias_text(self) -> bool | _typing.Literal[0, 1]:
        return self.__antialias_text

    @property
    def image(self) -> _typing.Optional[pygame.Surface]:
        return self.__image

    @property
    def image_scale(self) -> _typing.Optional[_RealNumber | _ArgsList]:
        return self.__image_scale

    @property
    def get_rect_text_kwargs(self) -> _typing.Optional[dict]:
        return self.__get_rect_text_kwargs

    @property
    def get_rect_image_kwargs(self) -> _typing.Optional[dict]:
        return self.__get_rect_image_kwargs

    @property
    def color(self) -> button_color:
        return self.__color

    @property
    def text_color(self) -> button_color:
        return self.__text_color

    @property
    def outline_color(self) -> button_color:
        return self.__outline_color

    @property
    def inactive_cursor(self) -> _typing.Optional[_CursorValue]:
        return self.__inactive_cursor

    @property
    def active_cursor(self) -> _typing.Optional[_CursorValue]:
        return self.__active_cursor

    @property
    def only_click(self) -> _ArgsList | _ButtonEventValue:
        return self.__only_click

    @property
    def click_speed(self) -> int:
        return self.__click_speed

    @property
    def borders(self) -> border_radius:
        return self.__borders

    @surface_screen.setter
    def surface_screen(self, surface: pygame.Surface) -> None:
        _prvt.asserting(isinstance(surface, pygame.Surface), TypeError(f"surface_screen -> surface (setter): must be pygame.Surface not {_prvt.get_type(surface)}"))
        self.__surface_screen = surface

    @rect.setter
    def rect(self, rect: pygame.Rect) -> None:
        _prvt.asserting(isinstance(rect, pygame.Rect), TypeError(f"rect -> rect (setter): must be pygame.Rect not {_prvt.get_type(rect)}"))
        self.__rect = rect
        if not self.__initialization:
            if isinstance(self.__image_scale, _RealNumber) and self.image:
                self.scale_image()

    @id.setter
    def id(self, id: _ButtonID) -> None:
        self.__id = id
        self.button_event.id = id

    @text.setter
    def text(self, text: str) -> None:
        self.__text = str(text)

    @font.setter
    def font(self, font: _typing.Optional[pygame.font.Font]) -> None:
        self.__font = font
        use_font = isinstance(font, pygame.font.Font)
        if not (use_font or self.__font_default):
            self.__font = pygame.font.SysFont('Arial', 15)
            self.__font_default = True
        elif use_font:
            self.__font_default = False

    @hide.setter
    def hide(self, hide: bool) -> None:
        self.__hide = bool(hide)

    @outline_size.setter
    def outline_size(self, size: _typing.Optional[_RealNumber]) -> None:
        _prvt.asserting(isinstance(size, _RealNumber | None), TypeError(f"outline_size -> size (setter): must be ArgsList or (None for no outline) not {_prvt.get_type(size)}"))
        self.__outline_size = size

    @antialias_text.setter
    def antialias_text(self, antialias: bool | _typing.Literal[0, 1]) -> None: 
        self.__antialias_text = antialias

    @image.setter
    def image(self, image: _typing.Optional[pygame.Surface]) -> None:
        _prvt.asserting(isinstance(image, pygame.Surface | None), TypeError(f"image -> image (setter): must be pygame.Surface or (None for no image)not {_prvt.get_type(image)}"))
        self.__image = image
        self.__scaled_image = image if isinstance(image, pygame.Surface) else None

    @image_scale.setter
    def image_scale(self, scale: _typing.Optional[_RealNumber | _ArgsList]) -> None:
        _prvt.asserting(isinstance(scale, _RealNumber | _ArgsList | None), TypeError(f'image_scale -> scale (setter): must be RealNumber or ArgsList or (None for not being scaled) not {_prvt.get_type(scale)}'))
        self.__image_scale = scale
        self.scale_image()

    @get_rect_text_kwargs.setter
    def get_rect_text_kwargs(self, kwargs: _typing.Optional[dict]) -> None:
        _prvt.asserting(isinstance(kwargs, dict | None), TypeError(f'get_rect_text_kwargs -> kwargs (setter): must be dict type or (None default: center) not {_prvt.get_type(kwargs)}'))
        self.__get_rect_text_kwargs = kwargs

    @get_rect_image_kwargs.setter
    def get_rect_image_kwargs(self, kwargs: _typing.Optional[dict]) -> None:
        _prvt.asserting(isinstance(kwargs, dict | None), TypeError(f'get_rect_image_kwargs -> kwargs (setter): must be dict type or (None default: center) not {_prvt.get_type(kwargs)}'))
        self.__get_rect_image_kwargs = kwargs

    @color.setter
    def color(self, color: button_color) -> None:
        _prvt.asserting(isinstance(color, button_color), TypeError(f'color -> color (setter): must be button_color not {_prvt.get_type(color)}'))
        self.__color = color

    @text_color.setter
    def text_color(self, color: button_color) -> None:
        _prvt.asserting(isinstance(color, button_color), TypeError(f'text_color -> color (setter): must be button_color not {_prvt.get_type(color)}'))
        self.__text_color = color

    @outline_color.setter
    def outline_color(self, color: button_color) -> None:
        _prvt.asserting(isinstance(color, button_color), TypeError(f'outline_color -> color (setter): must be button_color not {_prvt.get_type(color)}'))
        self.__outline_color = color

    @inactive_cursor.setter
    def inactive_cursor(self, cursor: _typing.Optional[_CursorValue]) -> None:
        self.__inactive_cursor = cursor

    @active_cursor.setter
    def active_cursor(self, cursor: _typing.Optional[_CursorValue]) -> None:
        self.__active_cursor = cursor

    @only_click.setter
    def only_click(self, click: _ArgsList | _ButtonEventValue) -> None:
        self.__only_click = click

    @click_speed.setter
    def click_speed(self, speed: int) -> None:
        _prvt.asserting(isinstance(speed, int), TypeError(f'click_speed -> speed (setter): must be int type not {_prvt.get_type(speed)}'))
        _prvt.asserting(speed >= 0, ValueError(f'click_speed -> speed (setter): illegal below 0 -> {speed}'))
        self.__click_speed = speed

    @borders.setter
    def borders(self, borders: border_radius) -> None:
        _prvt.asserting(isinstance(borders, border_radius), TypeError(f'borders -> borders (setter): must be border_radius not {_prvt.get_type(borders)}'))
        self.__borders = borders

    def copy(self, **kwargs):

        """
        Copy the Button class.

        return -> `Button(...)`
        """

        clonebutton = Button(**self.get_param())
        clonebutton.edit_param(**kwargs)

        return clonebutton

    def edit_param(self, **kwargs) -> None:

        """
        Edit parameters via the key argument of this function.

        return -> `None`
        """

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        return -> `dict[str, object]`
        """

        return {
            'surface_screen': self.__surface_screen,
            'rect': self.__rect,
            'id': self.__id,
            'text': self.__text,
            'font': self.__font,
            'hide': self.__hide,
            'outline_size': self.__outline_size,
            'antialias_text': self.__antialias_text,
            'image': self.__image,
            'image_scale': self.__image_scale,
            'get_rect_image_kwargs': self.__get_rect_image_kwargs,
            'get_rect_text_kwargs': self.__get_rect_text_kwargs,
            'color': self.__color,
            'text_color': self.__text_color,
            'outline_color': self.__outline_color,
            'inactive_cursor': self.__inactive_cursor,
            'active_cursor': self.__active_cursor,
            'only_click': self.__only_click,
            'click_speed': self.__click_speed,
            'borders': self.__borders
        }

    def get_private_attr(self, remove_underscore: bool = False) -> dict[str, object]:

        """
        Get private property.

        return -> `dict[str, object]`
        """

        attr_dict = {
            '__initialization': self.__initialization,
            '__last_click_time': self.__last_click_time,
            '__clicked_button': self.__clicked_button,
            '__button_outside': self.__button_outside,
            '__font_default': self.__font_default,
            '__get_event': self.__get_event.copy(),
            '__scaled_image': self.__scaled_image.copy() if self.__scaled_image else None
        }

        if not remove_underscore:
            return attr_dict
        return {attr.lstrip('_'): value for attr, value in attr_dict}

    def scale_image(self) -> None:

        """
        Set image size based on image_scale.

        return -> `None`
        """

        if isinstance(self.__image_scale, _RealNumber | _ArgsList) and self.__image is None:
            raise ValueError('scale_image -> image_scale (property): Cannot transform scale image because image parameters have not been provided')
        elif isinstance(self.__image_scale, _RealNumber):
            self.__scaled_image = pygame.transform.scale(self.__image, (self.__rect.width - self.__image_scale, self.__rect.height - self.__image_scale))
        elif isinstance(self.__image_scale, _ArgsList):
            self.__scaled_image = pygame.transform.scale(self.__image, self.__image_scale)

    def handle_event(self, event: pygame.event.Event) -> None:

        """
        Handling mouse input via pygame events.

        return -> `None`
        """

        _prvt.asserting(isinstance(event, pygame.event.Event), TypeError(f'event: must be event.Event type not {_prvt.get_type(event)}'))

        self.ishandlebyevent = True

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and 'l' in self.only_click:
                self.__get_event = ButtonEvent('l', 'Button')
                self.__clicked_button = True

            elif event.button == 2 and 'c' in self.only_click:
                self.__get_event = ButtonEvent('c', 'Button')
                self.__clicked_button = True

            elif event.button == 3 and 'r' in self.only_click:
                self.__get_event = ButtonEvent('r', 'Button')
                self.__clicked_button = True

    def draw_and_update(self) -> ButtonEvent:

        """
        Draw and update button. Draw a button and then update it according to the events obtained.

        return -> `ButtonEvent` or via `Button.button_event`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        ismousehover = self.__rect.collidepoint(mouse_x, mouse_y)

        self.button_event.value = ''
        self.button_event.ismousehover = ismousehover
        self.button_event.isbuttoninactive = not ismousehover
        self.button_event.isbuttonhover = ismousehover
        self.button_event.isbuttonactive = False
        self.button_event.cursor_active = False
        self.button_event.cursor_inactive = False

        if not self.__button_outside:
            current_time = pygame.time.get_ticks()
            get_pressed = _prvt.get_mouse_pressed(self.__only_click)
            any_pressed = (get_pressed[0] or get_pressed[1] or get_pressed[2])

            render_active_button = lambda change_config=True : self.__render_active_button(current_time, change_config)
            render_inactive_hover_button = lambda : self.__render_inactive_hover_button(ismousehover)

            if self.active_cursor is not None and ismousehover:
                pygame.mouse.set_cursor(self.active_cursor)
                self.button_event.cursor_active = True
            elif self.inactive_cursor is not None:
                pygame.mouse.set_cursor(self.inactive_cursor)
                self.button_event.cursor_inactive = True

            if not ismousehover or not any_pressed and not self.__clicked_button:
                render_inactive_hover_button()

            elif ismousehover and not self.ishandlebyevent:
                render_active_button(False)
                clicked = ''

                if get_pressed[0]:
                    clicked = 'l'
                elif get_pressed[1]:
                    clicked = 'c'
                elif get_pressed[2]:
                    clicked = 'r'

                if current_time - self.__last_click_time > self.click_speed and clicked:
                    render_active_button()
                    self.button_event.value = clicked
                    self.button_event.isbuttonactive = True
                    if self._send_event:
                        self.button_event._send_event()

                    return self.button_event

            elif ismousehover and self.ishandlebyevent:
                render_active_button(False)

                if self.__clicked_button and any_pressed:
                    return self.button_event

                elif current_time - self.__last_click_time > self.click_speed and self.__get_event:
                    render_active_button()
                    self.button_event.value = self.__get_event.value
                    self.button_event.isbuttonactive = True
                    self.__get_event._reset_property()
                    if self._send_event:
                        self.button_event._send_event()

                    return self.button_event

                else:
                    render_inactive_hover_button()

            if not ismousehover and self.ishandlebyevent and not any_pressed:
                self.__clicked_button = False

        return self.button_event

    def draw_inactive(self) -> None:

        """
        Render the inactive button.

        return -> `None`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__clicked_button = False
        self.__render_inactive_hover_button(False)
        self.button_event._reset_property()

    def draw_hover(self) -> None:

        """
        Render the hover button.

        return -> `None`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__clicked_button = False
        self.__render_inactive_hover_button(True)
        self.button_event._reset_property()

    def draw_active(self) -> None:

        """
        Render the active button.

        return -> `None`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__clicked_button = False
        self.__render_active_button(0, False)
        self.button_event._reset_property()

class Range(_ButtonInterface):

    """ Button Range - Push button distance class, creates a button distance function (slider button) through the pygame screen and can set it with the provided. """

    def __init__(

        self,
        surface_screen: pygame.Surface,
        rect: pygame.Rect,
        id: _ButtonID = None,
        thumb_size: _typing.Optional[_ArgsList] = None,
        outline_size: _typing.Optional[_RealNumber] = None,
        thumb_color: button_color = button_color(_WHITE, _GRAY, _LIGHT_GRAY),
        track_color: button_color = button_color(_GRAY, _WHITE, _GRAY),
        track_fill_color: button_color = button_color(_BLUE, _BLUE, _LIGHT_BLUE),
        outline_color: button_color = button_color(_GRAY, _WHITE, _LIGHT_GRAY),
        inactive_cursor: _typing.Optional[_CursorValue] = None,
        active_cursor: _typing.Optional[_CursorValue] = None,
        active_cursor_outside: bool = False,
        horizontal: bool = True,
        reversed: bool = False,
        reversed_scroller_mouse: bool = False,
        drag_scroller_mouse: bool = True,
        hide_thumb: bool = False,
        hide_track: bool = False,
        hide_track_fill: bool = False,
        min_value: _RealNumber = 0,
        max_value: _RealNumber = 100,
        value: _RealNumber = 0,
        step: _typing.Optional[_RealNumber] = 1,
        range_value_output: type[_RealNumber] = float,
        only_click: _ArgsList | _ButtonEventValue = 'l',
        click_speed: int = 50,
        borders_thumb: border_radius = border_radius(radius=100),
        borders_track: border_radius = border_radius(radius=50),
        borders_track_fill: border_radius = border_radius(radius=50),

    ) -> None:

        """
        param:
            * `surface_screen`: screen surface -> pygame.display.set_mode((x, y)) or pygame.Surface
            * `rect`: rect track (as well a rect Button)
            * `id`: ID Range for events
            * `thumb_size`: thumb size (width, height) or set the default to None to not show it
            * `outline_size`: outline size of the range track button
            * `thumb_color`: thumb color
            * `track_color`: track color
            * `track_fill_color`: track fill color
            * `outline_color`: outline color
            * `inactive_cursor`: change the cursor (un-hover)
            * `active_cursor`: change the cursor (hover)
            * `active_cursor_outside`: the active cursor will be active if it is in the track_rect area and also outside the track_rect area when dragging
            * `horizontal`: makes the drag move horizontally or vertically if the value is False. (width and height of the rect adjust)
            * `reversed`: reversed the drag in the opposite direction [(min -> max) => (max <- min)]
            * `reversed_scroller_mouse`: reverse drag on mouse scroll
            * `drag_scroller_mouse`: use the mouse scroll to drag the track (Requires handle_event method)
            * `hide_thumb`: hide thumb
            * `hide_track`: hide track
            * `hide_track_fill`: hide track fill
            * `min_value`: minimum value output
            * `max_value`: maximum value output
            * `value`: value output / default value
            * `step`: step value. None if there are no steps given
            * `range_value_output`: The type of numeric value output. In the form of int or float
            * `only_click`: click response ('r', 'c', 'l')
            * `click_speed`: click speed (ms)
            * `borders_thumb`: pygame.draw.rect thumb borders. Use border_radius class
            * `borders_track`: pygame.draw.rect track borders. Use border_radius class
            * `borders_track_fill`: pygame.draw.rect track borders. Use border_radius class
        """

        self.ishandlebyevent: bool = False
        self.button_event: ButtonEvent = ButtonEvent('', 'Range', id)

        self.__min_value = min_value
        self.__max_value = max_value
        self.__button_track: Button = Button(
            surface_screen = surface_screen,
            rect = rect,
            hide = hide_track,
            outline_size = outline_size,
            color = track_color,
            outline_color = outline_color,
            only_click = only_click,
            click_speed = click_speed,
            borders = borders_track
        )
        self.__button_thumb: Button = Button(
            surface_screen = surface_screen,
            rect = _prvt.init_rect,
            hide = hide_thumb,
            color = thumb_color,
            borders = borders_thumb
        )
        self.__button_track_fill: Button = self.__button_track.copy(
            hide = hide_track_fill,
            color = track_fill_color,
            borders = borders_track_fill
        )

        self.surface_screen = surface_screen
        self.rect = rect
        self.id = id
        self.thumb_size = thumb_size
        self.outline_size = outline_size
        self.thumb_color = thumb_color
        self.track_color = track_color
        self.track_fill_color = track_fill_color
        self.outline_color = outline_color
        self.inactive_cursor = inactive_cursor
        self.active_cursor = active_cursor
        self.active_cursor_outside = active_cursor_outside
        self.horizontal = horizontal
        self.reversed = reversed
        self.reversed_scroller_mouse = reversed_scroller_mouse
        self.drag_scroller_mouse = drag_scroller_mouse
        self.hide_thumb = hide_thumb
        self.hide_track = hide_track
        self.hide_track_fill = hide_track_fill
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.step = step
        self.range_value_output = range_value_output
        self.only_click = only_click
        self.click_speed = click_speed
        self.borders_thumb = borders_thumb
        self.borders_track = borders_track
        self.borders_track_fill = borders_track_fill

        self.button_event.range_value = self.__value
        self.__button_track._send_event = False
        self.__button_thumb._send_event = False
        self.__button_track_fill._send_event = False

        self.__clicked_button: bool = False
        self.__detected_scroller_mouse: bool = False
        self.__button_outside: bool = False
        self.__rect_thumb: pygame.Rect = _prvt.init_rect
        self.__rect_track_fill: pygame.Rect = _prvt.init_rect

        self.__set_track_and_thumb_positions()

    def __multiple_value(self, vtype: _typing.Literal['value', 'evalue'] = 'value', evalue = None, estep = None) -> None | _RealNumber:

        """
        Private method. Look for the closest multiple value.

        return -> (`None` => vtype='value') or (`RealNumber` => vtype='evalue')
        """

        if self.__step is not None:

            match vtype:

                case 'value':
                    rest = (self.__value - self.__min_value) % self.__step
                    if rest < self.__step / 2:
                        self.button_event.range_value = self.__value = self.range_value_output(self.__value - rest)
                    else:
                        self.button_event.range_value = self.__value = self.range_value_output(self.__value + (self.__step - rest))

                case 'evalue':
                    rest = evalue % estep
                    if rest < estep / 2:
                        return evalue - rest
                    else:
                        return evalue + (estep - rest)

    def __render_thumb_and_track_fill(self, type_draw: _typing.Literal['active', 'inactive', 'hover']) -> None:

        """
        Private method. Render the thumb and track fill.

        return -> `None`
        """

        if not self.__button_outside:

            if self.__use_thumb:
                self.__button_thumb.rect = self.__rect_thumb
            self.__button_track_fill.rect = self.__rect_track_fill

            match type_draw:

                case 'active':
                    self.__button_track_fill.draw_active()
                    if self.__use_thumb:
                        self.__button_thumb.draw_active()

                case 'inactive':
                    self.__button_track_fill.draw_inactive()
                    if self.__use_thumb:
                        self.__button_thumb.draw_inactive()

                case 'hover':
                    self.__button_track_fill.draw_hover()
                    if self.__use_thumb:
                        self.__button_thumb.draw_hover()

    def __set_track_and_thumb_positions(self) -> None:

        """
        Private method. Set the track fill size and thumb position.

        return -> `None`
        """

        self.__multiple_value()

        if self.__horizontal:
            if isinstance(self.__rect, pygame.Rect):
                track_fill_width = ((self.__value - self.__min_value) / (self.__max_value - self.__min_value)) * self.__rect.width
                self.__rect_track_fill = pygame.Rect(
                    self.__rect.left,
                    self.__rect.top,
                    track_fill_width,
                    self.__rect.height
                ) if not self.reversed else pygame.Rect(
                    self.__rect.right - track_fill_width,
                    self.__rect.top,
                    track_fill_width,
                    self.__rect.height
                )

            if self.__use_thumb:
                self.__rect_thumb = pygame.Rect(
                    self.__rect.left + self.__rect_track_fill.width - self.__thumb_size[0] / 2,
                    self.__rect.top + (self.__rect.height - self.__thumb_size[1]) / 2,
                    *self.__thumb_size
                ) if not self.reversed else pygame.Rect(
                    self.__rect_track_fill.left - self.__thumb_size[0] / 2,
                    self.__rect.top + (self.__rect.height - self.__thumb_size[1]) / 2,
                    *self.__thumb_size
                )

        else:
            if isinstance(self.__rect, pygame.Rect):
                track_fill_height = ((self.__value - self.__min_value) / (self.__max_value - self.__min_value)) * self.__rect.height
                self.__rect_track_fill = pygame.Rect(
                    self.__rect.left,
                    self.__rect.top,
                    self.__rect.width,
                    track_fill_height
                ) if not self.__reversed else pygame.Rect(
                    self.__rect.left,
                    self.__rect.bottom - track_fill_height,
                    self.__rect.width,
                    track_fill_height
                )

            if self.__use_thumb:
                self.__rect_thumb = pygame.Rect(
                    self.__rect.left + (self.__rect.width - self.__thumb_size[0]) / 2,
                    self.__rect.top + self.__rect_track_fill.height - self.__thumb_size[1] / 2,
                    *self.__thumb_size
                ) if not self.__reversed else pygame.Rect(
                    self.__rect.left + (self.__rect.width - self.__thumb_size[0]) / 2,
                    self.__rect_track_fill.top - self.__thumb_size[1] / 2,
                    *self.__thumb_size
                )

    def __update(self, mouse_pos: _ArgsList, get_pressed: _typing.Optional[_ArgsList]) -> ButtonEvent:

        """
        Private method. Update the Range value.

        return -> `ButtonEvent`
        """

        if self.__horizontal:
            if mouse_pos[0] > self.__rect.right:
                relative_position = (self.__rect.right - self.__rect.left) / self.__rect.width
            elif mouse_pos[0] < self.__rect.left:
                relative_position = (self.__rect.left - self.__rect.left) / self.__rect.width
            else:
                relative_position = (mouse_pos[0] - self.__rect.left) / self.__rect.width

            self.__rect_track_fill.width = relative_position * self.__rect.width
            if self.__step is not None:
                self.__rect_track_fill.width = self.__multiple_value('evalue', self.__rect_track_fill.width, self.__rect.width / (self.__max_value - self.__min_value))

            if self.__reversed:
                self.__rect_track_fill.width = self.__rect.width - self.__rect_track_fill.width
                self.__rect_track_fill.left = self.__rect.right - self.__rect_track_fill.width

            if self.__use_thumb:
                self.__rect_thumb.left = (
                    self.__rect.right - self.__rect_track_fill.width - self.__rect_thumb.width / 2
                    if self.__reversed else
                    self.__rect.left + self.__rect_track_fill.width - self.__rect_thumb.width / 2
                )

        else:
            if mouse_pos[1] > self.__rect.bottom:
                relative_position = (self.__rect.bottom - self.__rect.top) / self.__rect.height
            elif mouse_pos[1] < self.__rect.top:
                relative_position = (self.__rect.top - self.__rect.top) / self.__rect.height
            else:
                relative_position = (mouse_pos[1] - self.__rect.top) / self.__rect.height

            self.__rect_track_fill.height = relative_position * self.__rect.height
            if self.__step is not None:
                self.__rect_track_fill.height = self.__multiple_value('evalue', self.__rect_track_fill.height, self.__rect.height / (self.__max_value - self.__min_value))

            if self.__reversed:
                self.__rect_track_fill.height = self.__rect.height - self.__rect_track_fill.height
                self.__rect_track_fill.top = self.__rect.bottom - self.__rect_track_fill.height

            if self.__use_thumb:
                self.__rect_thumb.top = (
                    self.__rect.bottom - self.__rect_track_fill.height - self.__rect_thumb.height / 2
                    if self.__reversed else
                    self.__rect.top + self.__rect_track_fill.height - self.__rect_thumb.height / 2
                )

        self.button_event.range_value = self.value = self.range_value_output(
            self.__min_value + (relative_position * (self.__max_value - self.__min_value))
            if not self.__reversed else
            self.__max_value - (relative_position * (self.__max_value - self.__min_value))
        )

        self.__multiple_value()

        if isinstance(get_pressed, _ArgsList):
            if get_pressed[0]:
                self.button_event.value = 'l'
            elif get_pressed[1]:
                self.button_event.value = 'c'
            elif get_pressed[2]:
                self.button_event.value = 'r'
            self.button_event._send_event()

        else:
            self.button_event.value = self.__button_track.button_event.value

        self.button_event.isdragging = True

        return self.button_event

    @property
    def surface_screen(self) -> pygame.Surface:
        return self.__surface_screen

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @property
    def id(self) -> _ButtonID:
        return self.__id

    @property
    def thumb_size(self) -> _typing.Optional[_ArgsList]:
        return self.__thumb_size

    @property
    def outline_size(self) -> _typing.Optional[_RealNumber]:
        return self.__outline_size

    @property
    def thumb_color(self) -> button_color:
        return self.__thumb_color

    @property
    def track_color(self) -> button_color:
        return self.__track_color

    @property
    def track_fill_color(self) -> button_color:
        return self.__track_fill_color

    @property
    def outline_color(self) -> button_color:
        return self.__outline_color

    @property
    def inactive_cursor(self) -> _typing.Optional[_CursorValue]:
        return self.__inactive_cursor

    @property
    def active_cursor(self) -> _typing.Optional[_CursorValue]:
        return self.__active_cursor

    @property
    def active_cursor_outside(self) -> bool:
        return self.__active_cursor_outside

    @property
    def horizontal(self) -> bool:
        return self.__horizontal

    @property
    def reversed(self) -> bool:
        return self.__reversed

    @property
    def reversed_scroller_mouse(self) -> bool:
        return self.__reversed_scroller_mouse

    @property
    def drag_scroller_mouse(self) -> bool:
        return self.__drag_scroller_mouse

    @property
    def hide_thumb(self) -> bool:
        return self.__hide_thumb

    @property
    def hide_track(self) -> bool:
        return self.__hide_track

    @property
    def hide_track_fill(self) -> bool:
        return self.__hide_track_fill

    @property
    def min_value(self) -> _RealNumber:
        return self.__min_value

    @property
    def max_value(self) -> _RealNumber:
        return self.__max_value

    @property
    def value(self) -> _RealNumber:
        return self.__value

    @property
    def step(self) -> _typing.Optional[_RealNumber]:
        return self.__step

    @property
    def range_value_output(self) -> type[_RealNumber]:
        return self.__range_value_output

    @property
    def only_click(self) -> _ArgsList | _ButtonEventValue:
        return self.__only_click

    @property
    def click_speed(self) -> int:
        return self.__click_speed

    @property
    def borders_thumb(self) -> border_radius:
        return self.__borders_thumb

    @property
    def borders_track(self) -> border_radius:
        return self.__borders_track

    @property
    def borders_track_fill(self) -> border_radius:
        return self.__borders_track_fill
    
    @surface_screen.setter
    def surface_screen(self, surface: pygame.Surface) -> None:
        self.__surface_screen = surface
        self.__button_track.surface_screen = surface
        self.__button_thumb.surface_screen = surface
        self.__button_track_fill.surface_screen = surface

    @rect.setter
    def rect(self, rect: pygame.Rect) -> None:
        self.__rect = rect
        self.__button_track.rect = rect

    @id.setter
    def id(self, id: _ButtonID) -> None:
        self.__id = id
        self.button_event.id = id

    @thumb_size.setter
    def thumb_size(self, size: _typing.Optional[_ArgsList]) -> None:
        self.__use_thumb = isinstance(size, _ArgsList)
        self.__thumb_size = size
        if self.__use_thumb:
            self.__set_track_and_thumb_positions()

    @outline_size.setter
    def outline_size(self, size: _typing.Optional[_RealNumber]) -> None:
        self.__outline_size = size
        self.__button_track.outline_size = size

    @thumb_color.setter
    def thumb_color(self, color: button_color) -> None:
        self.__thumb_color = color
        self.__button_thumb.color = color

    @track_color.setter
    def track_color(self, color: button_color) -> None:
        self.__track_color = color
        self.__button_track.color = color

    @track_fill_color.setter
    def track_fill_color(self, color: button_color) -> None:
        self.__track_fill_color = color
        self.__button_track_fill.color = color

    @outline_color.setter
    def outline_color(self, color: button_color) -> None:
        self.__outline_color = color
        self.__button_track.outline_color = color

    @inactive_cursor.setter
    def inactive_cursor(self, cursor: _typing.Optional[_CursorValue]) -> None:
        self.__inactive_cursor = cursor

    @active_cursor.setter
    def active_cursor(self, cursor: _typing.Optional[_CursorValue]) -> None:
        self.__active_cursor = cursor

    @active_cursor_outside.setter
    def active_cursor_outside(self, boolean: bool) -> None:
        self.__active_cursor_outside = bool(boolean)

    @horizontal.setter
    def horizontal(self, boolean: bool) -> None:
        self.__horizontal = bool(boolean)

    @reversed.setter
    def reversed(self, reverse: bool) -> None:
        self.__reversed = bool(reverse)

    @reversed_scroller_mouse.setter
    def reversed_scroller_mouse(self, reverse: bool) -> None:
        self.__reversed_scroller_mouse = bool(reverse)

    @drag_scroller_mouse.setter
    def drag_scroller_mouse(self, boolean: bool) -> None:
        self.__drag_scroller_mouse = bool(boolean)

    @hide_thumb.setter
    def hide_thumb(self, hide: bool) -> None:
        self.__hide_thumb = bool(hide)
        self.__button_thumb.hide = hide

    @hide_track.setter
    def hide_track(self, hide: bool) -> None:
        self.__hide_track = bool(hide)
        self.__button_track.hide = hide

    @hide_track_fill.setter
    def hide_track_fill(self, hide: bool) -> None:
        self.__hide_track_fill = bool(hide)
        self.__button_track_fill.hide = hide

    @min_value.setter
    def min_value(self, value: _RealNumber) -> None:
        _prvt.asserting(isinstance(value, _RealNumber), TypeError(f'min_value -> value (setter): must be RealNumber type not {_prvt.get_type(value)}'))
        _prvt.asserting(self.__min_value != self.__max_value, ValueError(f'min_value, max_value: illegal min_value, max_value is same -> min_value: {self.__min_value}, max_value: {self.__max_value}'))
        _prvt.asserting(self.__min_value < self.__max_value, ValueError(f'min_value, max_value: illegal min_value is greater than max_value -> min_value: {self.__min_value}, max_value: {self.__max_value}'))
        self.__min_value = value

    @max_value.setter
    def max_value(self, value: _RealNumber) -> None:
        _prvt.asserting(isinstance(value, _RealNumber), TypeError(f'max_value -> value (setter): must be RealNumber type not {_prvt.get_type(value)}'))
        _prvt.asserting(self.__min_value != self.__max_value, ValueError(f'min_value, max_value: illegal min_value, max_value is same -> min_value: {self.__min_value}, max_value: {self.__max_value}'))
        _prvt.asserting(self.__min_value < self.__max_value, ValueError(f'min_value, max_value: illegal min_value is greater than max_value -> min_value: {self.__min_value}, max_value: {self.__max_value}'))
        self.__max_value = value

    @value.setter
    def value(self, value: _RealNumber) -> None:
        _prvt.asserting(isinstance(value, _RealNumber), TypeError(f'value -> value (setter): must be RealNumber type not {_prvt.get_type(value)}'))
        _prvt.asserting(self.__min_value <= value <= self.__max_value, ValueError(f'value -> value (setter): illegal below min_value and above max_value -> {value}'))
        self.__value = value

    @step.setter
    def step(self, value: _typing.Optional[_RealNumber]) -> None:
        _prvt.asserting(isinstance(value, _RealNumber | None), TypeError(f'step -> value (setter): must be RealNumber type or (None for no step) not {_prvt.get_type(value)}'))
        if value is not None:
            _prvt.asserting(isinstance(value, _RealNumber), TypeError(f'step -> value (setter): must be RealNumber type or (None for no step) not {_prvt.get_type(value)}'))
            _prvt.asserting(0 < value <= (self.max_value - self.min_value), ValueError(f'step -> value (setter): cannot exceed the total of min_value and max_value or below 1 -> {value}'))
        self.__step = value

    @range_value_output.setter
    def range_value_output(self, real_num_class_type: type[_RealNumber]) -> None:
        _prvt.asserting(isinstance(real_num_class_type, type), TypeError(f'range_value_output -> real_num_class_type (setter): must be class type object not {repr(real_num_class_type)} ~ {_prvt.get_type(real_num_class_type)}'))
        _prvt.asserting(real_num_class_type in (int, float), TypeError(f'range_value_output: must be (int or float) type not {real_num_class_type}'))
        self.__range_value_output = real_num_class_type

    @only_click.setter
    def only_click(self, click: _ArgsList | _ButtonEventValue) -> None:
        self.__only_click = click
        self.__button_track.only_click = click

    @click_speed.setter
    def click_speed(self, speed: int) -> None:
        self.__click_speed = speed
        self.__button_track.click_speed = speed

    @borders_thumb.setter
    def borders_thumb(self, borders: border_radius) -> None:
        self.__borders_thumb = borders
        self.__button_thumb.borders = borders

    @borders_track.setter
    def borders_track(self, borders: border_radius) -> None:
        self.__borders_track = borders
        self.__button_track.borders = borders

    @borders_track_fill.setter
    def borders_track_fill(self, borders: border_radius) -> None:
        self.__borders_track_fill = borders
        self.__button_track_fill.borders = borders

    def copy(self, **kwargs):

        """
        Copy the Range button class.

        return -> `Range(...)`
        """

        clonerange = Range(**self.get_param())
        clonerange.edit_param(**kwargs)

        return clonerange

    def edit_param(self, **kwargs) -> None:

        """
        Edit parameters via the key argument of this function.

        return -> `None`
        """

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        return -> `dict[str, object]`
        """

        return {
            'surface_screen': self.__surface_screen,
            'rect': self.__rect,
            'id': self.__id,
            'thumb_size': self.__thumb_size,
            'outline_size': self.__outline_size,
            'thumb_color': self.__thumb_color,
            'track_color': self.__track_color,
            'track_fill_color': self.__track_fill_color,
            'outline_color': self.__outline_color,
            'inactive_cursor': self.__inactive_cursor,
            'active_cursor': self.__active_cursor,
            'active_cursor_outside': self.__active_cursor_outside,
            'horizontal': self.__horizontal,
            'reversed': self.__reversed,
            'reversed_scroller_mouse': self.__reversed_scroller_mouse,
            'drag_scroller_mouse': self.__drag_scroller_mouse,
            'hide_thumb': self.__hide_thumb,
            'hide_track': self.__hide_track,
            'hide_track_fill': self.__hide_track_fill,
            'min_value': self.__min_value,
            'max_value': self.__max_value,
            'value': self.__value,
            'step': self.__step,
            'range_value_output': self.__range_value_output,
            'only_click': self.__only_click,
            'click_speed': self.__click_speed,
            'borders_thumb': self.__borders_thumb,
            'borders_track': self.__borders_track,
            'borders_track_fill': self.__borders_track_fill
        }

    def get_private_attr(self, remove_underscore: bool = False) -> dict[str, object]:

        """
        Get private property.

        return -> `dict[str, object]`
        """

        attr_dict = {
            '__button_track': self.__button_track.copy(),
            '__button_thumb': self.__button_thumb.copy(),
            '__button_track_fill': self.__button_track_fill.copy(),
            '__clicked_button': self.__clicked_button,
            '__detected_scroller_mouse': self.__detected_scroller_mouse,
            '__button_outside': self.__button_outside,
            '__use_thumb': self.__use_thumb,
            '__rect_thumb': self.__rect_thumb.copy(),
            '__rect_track_fill': self.__rect_track_fill.copy()
        }

        if not remove_underscore:
            return attr_dict
        else:
            return {attr.lstrip('_'): value for attr, value in attr_dict}

    def set_value(self, value: _RealNumber) -> None:

        """
        Set the value.

        return -> `None`
        """

        self.button_event.range_value = self.value = self.range_value_output(value)
        self.__set_track_and_thumb_positions()

    def handle_event(self, event: pygame.event.Event, handled_button: bool = False) -> None:

        """
        Handling mouse input via pygame events.

        return -> `None`
        """

        self.ishandlebyevent = True

        if handled_button:
            self.__button_track.handle_event(event)
        else:
            self.__button_track.ishandlebyevent = False

        if event.type == pygame.MOUSEBUTTONDOWN and self.drag_scroller_mouse:

            if event.button == (4 if not self.__reversed_scroller_mouse else 5) and self.button_event.ismousehover:
                self.__value += self.step

                if self.__value > self.__max_value:
                    self.__value = self.__max_value
                elif self.__value < self.__min_value:
                    self.__value = self.__min_value

                self.button_event.range_value = self.value = self.range_value_output(self.__value)
                self.button_event.value = 'sc'
                self.button_event.isdragging = True
                self.__detected_scroller_mouse = True
                self.__set_track_and_thumb_positions()
                self.button_event._send_event()

            elif event.button == (5 if not self.__reversed_scroller_mouse else 4) and self.button_event.ismousehover:
                self.__value -= self.step

                if self.__value > self.__max_value:
                    self.__value = self.__max_value
                elif self.__value < self.__min_value:
                    self.__value = self.__min_value

                self.button_event.range_value = self.value = self.range_value_output(self.__value)
                self.button_event.value = 'sc'
                self.button_event.isdragging = True
                self.__detected_scroller_mouse = True
                self.__set_track_and_thumb_positions()
                self.button_event._send_event()

    def draw_and_update(self) -> ButtonEvent:

        """
        Draw and update Range button. Draw a range button and then update it according to the events obtained.

        return -> `ButtonEvent` or via `Range.button_event`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)

        mouse_pos = pygame.mouse.get_pos()
        ismousehover = self.rect.collidepoint(*mouse_pos) or (self.__rect_thumb.collidepoint(*mouse_pos) if self.__use_thumb else None)

        self.button_event.value = ''
        self.button_event.ismousehover = ismousehover
        self.button_event.israngeinactive = not ismousehover
        self.button_event.israngehover = ismousehover
        self.button_event.israngeactive = False
        self.button_event.range_value = self.value = self.range_value_output(self.value)
        self.button_event.cursor_active = False
        self.button_event.cursor_inactive = False

        if not self.__button_outside:
            get_pressed = _prvt.get_mouse_pressed(self.__only_click)
            any_pressed = (get_pressed[0] or get_pressed[1] or get_pressed[2])

            if not self.__detected_scroller_mouse:
                self.button_event.isdragging = False

            if self.active_cursor is not None and ((ismousehover or self.__clicked_button) if self.__active_cursor_outside else ismousehover):
                pygame.mouse.set_cursor(self.__active_cursor)
                self.button_event.cursor_active = True
            elif self.inactive_cursor is not None:
                pygame.mouse.set_cursor(self.__inactive_cursor)
                self.button_event.cursor_inactive = True

            self.__button_track.draw_and_update()

            if ismousehover:
                self.__render_thumb_and_track_fill('hover')
            elif self.__button_track.button_event.isbuttonactive:
                self.__render_thumb_and_track_fill('active')
                self.button_event.israngeactive = True
            else:
                self.__render_thumb_and_track_fill('inactive')

            if self.__button_track.ishandlebyevent and self.__button_track.button_event.value:
                return self.__update(mouse_pos, None)

            if any_pressed and not self.__button_track.ishandlebyevent:
                if ismousehover:
                    self.__clicked_button = True

                if self.__clicked_button:
                    return self.__update(mouse_pos, get_pressed)

            elif not self.__button_track.ishandlebyevent:
                self.__clicked_button = False

            if self.__detected_scroller_mouse:
                self.__detected_scroller_mouse = False
        
        return self.button_event

    def draw_inactive(self) -> None:

        """
        Render the inactive button.

        return -> `None`
        """

        self.button_event._reset_property()
        self.button_event.range_value = self.value = self.range_value_output(self.value)
        self.__clicked_button = False
        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__button_track.draw_inactive()
        self.__render_thumb_and_track_fill('inactive')

    def draw_hover(self) -> None:

        """
        Render the hover button.

        return -> `None`
        """

        self.button_event._reset_property()
        self.button_event.range_value = self.value = self.range_value_output(self.value)
        self.__clicked_button = False
        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__button_track.draw_hover()
        self.__render_thumb_and_track_fill('hover')

    def draw_active(self) -> None:

        """
        Render the active button.

        return -> `None`
        """

        self.button_event._reset_property()
        self.button_event.range_value = self.value = self.range_value_output(self.value)
        self.__clicked_button = False
        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__button_track.draw_active()
        self.__render_thumb_and_track_fill('active')

# Type buttons
ButtonType = Button
RangeType = Range
ButtonsType = ButtonType | RangeType


def set_cursor_buttons(

        *buttons: ButtonsType,
        inactive_cursor: _typing.Optional[_CursorValue] = None,
        active_cursor: _typing.Optional[_CursorValue] = None,
        set_active_cursor_button: bool = True

    ) -> None:

    """
    Sets the cursor set_mode of the double or more button functions.

    param:
        * `*buttons`: button class (already initialized)
        * `inactive_cursor`: inactive cursor type
        * `active_cursor`: active cursor type
        * `set_active_cursor_button`: set the active type of cursor on each button

    return -> `None`
    """

    _prvt.asserting(buttons, ValueError('*buttons: requires at least one positional argument'))

    any_pressed = False

    for button in buttons:
        _prvt.asserting(isinstance(button, ButtonsType), TypeError(f'*buttons: most be Button or Range not {_prvt.get_type(button)}'))

        if set_active_cursor_button:
            if isinstance(button, RangeType):
                button.active_cursor_outside = False

            button.active_cursor = active_cursor

        button.inactive_cursor = None

        if button.button_event.ismousehover and not any_pressed:
            any_pressed = True

    if any_pressed is False and inactive_cursor is not None:
        pygame.mouse.set_cursor(inactive_cursor)


class Manager(_ButtonInterface):

    """ Manager - Handle multiple buttons on 1 screen at once. """

    def __init__(

            self,
            *buttons: ButtonsType,
            inactive_cursor: _typing.Optional[_CursorValue] = None,
            active_cursor: _typing.Optional[_CursorValue] = None,
            set_active_cursor_button: bool = True

        ) -> None:

        """
        param:
            * `*buttons`: Target buttons (already initialized)
            * **kw of set_cursor_buttons
        """

        _prvt.asserting(buttons, ValueError('*buttons: requires at least one positional argument'))

        for button in buttons:
            _prvt.asserting(isinstance(button, ButtonsType), TypeError(f'*buttons: most be Button or Range not {_prvt.get_type(button)}'))

        self.buttons = buttons
        self.inactive_cursor = inactive_cursor
        self.active_cursor = active_cursor
        self.set_active_cursor_button = set_active_cursor_button

    def __set_all_cursor_button(self) -> None:

        """
        Sets all the cursor on the button.

        return -> `None`
        """

        set_cursor_buttons(
            *self.buttons,
            inactive_cursor=self.inactive_cursor,
            active_cursor=self.active_cursor,
            set_active_cursor_button=self.set_active_cursor_button
        )

    def copy(self, *new_buttons: ButtonsType):

        """
        Copy the Manager class.
        Enter the button arguments to replace the new button.

        return -> `Manager(...)`
        """

        button_list = new_buttons or self.buttons
        return Manager(
            *button_list,
            inactive_cursor = self.inactive_cursor,
            active_cursor = self.active_cursor,
            set_active_cursor_button = self.set_active_cursor_button
        )

    def edit_param(self, id: _ButtonID, **kwargs) -> None:

        """
        Edit button parameters via the key argument of this function.
        Enter button id to edit specific parameters.

        return -> `None`
        """

        for button in self.buttons:
            if id == button.id:
                button.edit_param(**kwargs)

    def get_param(self, id: _ButtonID) -> list[dict[str, object]]:

        """
        Get class button parameters in the form dictionary type.
        Enter button id to edit specific parameters.

        return -> `list[dict[str, object]]`
        """

        buttons_param = []

        for button in self.buttons:
            if id == button.id:
                buttons_param.append(button.get_param())

        return buttons_param

    def get_private_attr(self, id: _ButtonID, remove_underscore: bool = False) -> list[dict[str, object]]:

        """
        Get buttons private property.
        Enter button id to edit specific parameters.

        return -> `list[dict[str, object]]`
        """

        buttons_param = []

        for button in self.buttons:
            if id == button.id:
                buttons_param.append(button.get_private_attr(remove_underscore))

        return buttons_param

    def handle_event(self, event: pygame.event.Event, range_handled_button: bool = False) -> None:

        """
        Handling mouse input via pygame events.

        return -> `None`
        """

        for button in self.buttons:

            if isinstance(button, RangeType):
                button.handle_event(event, range_handled_button)

            elif isinstance(button, ButtonsType):
                button.handle_event(event)

    def draw_and_update(self) -> None:

        """
        Draw, update, and set cursor buttons. Draw a button and then update it according to the events obtained.

        return -> `ButtonEvent` or via `Button.button_event`
        """

        self.__set_all_cursor_button()

        for button in self.buttons:
            button.draw_and_update()

    def draw_inactive(self) -> None:

        """
        Render the inactive buttons.

        return -> `None`
        """

        self.__set_all_cursor_button()

        for button in self.buttons:
            button.draw_inactive()

    def draw_hover(self) -> None:

        """
        Render the hover buttons.

        return -> `None`
        """

        self.__set_all_cursor_button()

        for button in self.buttons:
            button.draw_hover()

    def draw_active(self) -> None:

        """
        Render the active buttons.

        return -> `None`
        """

        self.__set_all_cursor_button()

        for button in self.buttons:
            button.draw_active()


__version__ = '1.1.2'
__all__ = [
    'BUTTON_CLICK',
    'SysCursor',
    'border_radius',
    'button_color',
    'Button',
    'Range',
    'set_cursor_buttons',
    'Manager'
]


del _BLACK, _GRAY, _LIGHT_GRAY, _WHITE, _BLUE, _LIGHT_BLUE, _Private, _ButtonInterface, _typing, _ABC, _abstract