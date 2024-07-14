"""
# pygamebutton module
Version: 1.1.0

pygame elements. Button and Range.

Explanations
------------
pygamebutton is a special tool module for displaying general button elements.
Pygame does not provide a button media element. However, the functions and
methods provided by the pygame module provide various ways to create this
button element. And this module is used as a button function that is
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
```
button1_rect = pygame.Rect(25, 25, 50, 50)
button1 = pygamebutton.Button(
    screen,
    rect=button1_rect,
    id='button1' # The id function will be used in the second event method
)
```

Then create an event loop and call the draw_and_update method for interaction
knob.
```
# loops game
while ...:
    for event in pygame.event.get():
        ... # your events
        button1.handle_event(event)

    button1.draw_and_update()
```

Check if the button is pressed or not.
```
    if button1.button_event.value:
        # do something..
```

You can get the button event from the return of the draw_and_update method.
```
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
```
button1_rect = pygame.Rect(...)
button1 = pygamebutton.Button(
    ...
    id='button1' # enter the id
)
```

How to catch the events.
```
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

Prohibition
-----------
Never change properties directly like this:
```
button1.id = 'btn1'
```

do:
```
button1.edit_param(id='btn1')
```

*Set value on Range:
```
myrange.set_value(25)
```

Because it can cause bugs and errors if you edit parameters manually, use the
edit_param method to edit parameters.

Examples
--------
Here is a example of a basic setup (opens the window, updates the screen, and
handles events):
```
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
from abc import (ABC as _ABC, abstractmethod as _abstract)

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

    def __init__(self, id: int | None = None) -> None:
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
_ColorType = _ArgsList | str | pygame.Color
_CursorID = pygame.Cursor | int

# ID events
BUTTON_CLICK = pygame.USEREVENT + 1


class ButtonEvent:

    """ ButtonEvent - The event of button function """

    def __init__(self, value: _ButtonEventValue, type: _Buttons, id: _typing.Any = None) -> None:

        _prvt.asserting(isinstance(value, str), TypeError(f'value: must be str type not {_prvt.get_type(value)}'))
        _prvt.asserting(isinstance(type, str), TypeError(f'type: must be str type not {_prvt.get_type(type)}'))

        self.value: _ButtonEventValue = value.lower()
        self.type: _Buttons = type
        self.id: _typing.Any = id
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

    def reset_property(self) -> None:
        self.__init__('', self.type, self.id)

    def send_event(self) -> None:
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
        inactive_color: _ColorType | None = None,
        active_color: _ColorType | None = None,
        hover_color: _ColorType | None = None,

    ) -> None:

        self.inactive_color = inactive_color
        self.active_color = active_color
        self.hover_color = hover_color

        for key, value in self.get_param().items():
            _prvt.asserting(isinstance(value, _ColorType | None), TypeError(f'{key}: must be ColorType or (None for default) not {_prvt.get_type(value)}'))

    def copy(self):
        return button_color(**self.get_param())

    def get_param(self) -> dict[str, _ColorType | None]:
        return {
            'inactive_color': self.inactive_color,
            'active_color': self.active_color,
            'hover_color': self.hover_color
        }


class _ButtonInterface(_ABC):

    """ _ButtonInterface - Button interface class. As a means of interface to the button class. """

    @_abstract
    @_typing.overload
    def __init__(self, surface_screen: pygame.Surface, rect: pygame.Rect, id: _typing.Any) -> None: ...
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
            id: _typing.Any = None,
            text: str = '',
            font: pygame.font.Font | None = None,
            hide: bool = False,
            outline_size: _RealNumber | None = None,
            antialias_text: bool = True,
            image: pygame.Surface | None = None,
            image_transform: _RealNumber | _ArgsList | None = None,
            get_rect_image_kwargs: dict | None = None,
            get_rect_text_kwargs: dict | None = None,
            color: button_color = button_color(_WHITE, _LIGHT_GRAY, _GRAY),
            text_color: button_color = button_color(_BLACK, _BLACK, _BLACK),
            outline_color: button_color = button_color(_GRAY, _WHITE, _LIGHT_GRAY),
            inactive_cursor: _CursorID | None = None,
            active_cursor: _CursorID | None = None,
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
            * `hide`: Hides the button but can still receive input. (Doesn't apply to text, and image)
            * `outline_size`: outline size of the button
            * `antialias_text`: param at -> font.render(text, antialias=..., ...)
            * `image`: image or icon on the button. (Use pygame.transform.scale(<Surface image source>, (rect button size))) to fit and fit the main button
            * `image_transform`: transform the size of the image surface. (If the type is numeric, then the size will be the size of the rect button with a margin of the numbers entered. If the type is tuple[number, number], then it will follow the scale of the contents of the tuple)
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

        self.surface_screen = surface_screen
        self.rect = rect
        self.id = id
        self.text = text
        self.font = font
        self.hide = hide
        self.outline_size = outline_size
        self.antialias_text = antialias_text
        self.image = image
        self.image_transform = image_transform
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
        self.__transform_image: pygame.Surface = self.image.copy() if isinstance(self.image, pygame.Surface) else None

        self.ishandlebyevent: bool = False
        self.button_event: ButtonEvent = ButtonEvent('', 'Button', id)

        self.__set_and_validates()

    def __rect_outline(self) -> pygame.Rect:

        """
        Private method. Gets the outline rect.

        return -> `pygame.Rect`
        """

        return pygame.Rect(self.rect.left - self.outline_size, self.rect.top - self.outline_size, self.rect.width + self.outline_size * 2, self.rect.height + self.outline_size * 2)

    def __render_active_button(self, current_time: int, change_config: bool) -> None:

        """
        Private method. Render the active button.
        
        return -> `None`
        """

        if not self.__button_outside:

            if not self.hide:
                if isinstance(self.outline_size, _RealNumber):
                    pygame.draw.rect(self.surface_screen, self.outline_color.active_color, self.__rect_outline(), **self.borders.draw_rect_kwargs)

                pygame.draw.rect(self.surface_screen, self.color.active_color, self.rect, **self.borders.draw_rect_kwargs)

            if self.image is not None:
                if self.get_rect_image_kwargs is None:
                    self.surface_screen.blit(self.__transform_image, self.__transform_image.get_rect(center=self.rect.center))
                else:
                    self.surface_screen.blit(self.__transform_image, self.__transform_image.get_rect(**self.get_rect_image_kwargs))

            if self.text:
                text_surface = self.font.render(self.text, self.antialias_text, self.text_color.active_color)

                if self.get_rect_text_kwargs is None:
                    text_rect = text_surface.get_rect(center=self.rect.center)
                else:
                    text_rect = text_surface.get_rect(**self.get_rect_text_kwargs)

                self.surface_screen.blit(text_surface, text_rect)

            if change_config:
                self.__clicked_button = False
                self.__last_click_time = current_time

    def __render_inactive_hover_button(self, ismousehover: bool) -> None:

        """
        Private method. Render the inactive or hover button.

        return -> `None`
        """

        if not self.__button_outside:

            if not self.hide:
                if isinstance(self.outline_size, _RealNumber):
                    pygame.draw.rect(self.surface_screen, (self.outline_color.hover_color if (self.outline_color.hover_color is not None) and ismousehover else self.outline_color.inactive_color), self.__rect_outline(), **self.borders.draw_rect_kwargs)

                pygame.draw.rect(self.surface_screen, (self.color.hover_color if (self.color.hover_color is not None) and ismousehover else self.color.inactive_color), self.rect, **self.borders.draw_rect_kwargs)

            if self.image is not None:
                if self.get_rect_image_kwargs is None:
                    self.surface_screen.blit(self.__transform_image, self.__transform_image.get_rect(center=self.rect.center))
                else:
                    self.surface_screen.blit(self.__transform_image, self.__transform_image.get_rect(**self.get_rect_image_kwargs))

            if self.text:
                text_surface = self.font.render(self.text, self.antialias_text, (self.text_color.hover_color if (self.text_color.hover_color is not None) and ismousehover else self.text_color.inactive_color))

                if self.get_rect_text_kwargs is None:
                    text_rect = text_surface.get_rect(center=self.rect.center)
                else:
                    text_rect = text_surface.get_rect(**self.get_rect_text_kwargs)

                self.surface_screen.blit(text_surface, text_rect)

    def __set_and_validates(self, kwargs: dict | None = None) -> None:

        """
        Private method. Sets parameters and validates parameters.

        return -> `None`
        """

        self.text = str(self.text)

        if not isinstance(self.font, pygame.font.Font):
            self.font = pygame.font.SysFont('Arial', 15)

        _prvt.asserting(isinstance(self.surface_screen, pygame.Surface), TypeError(f"surface_screen: must be pygame.Surface not {_prvt.get_type(self.surface_screen)}"))
        _prvt.asserting(isinstance(self.rect, pygame.Rect), TypeError(f"rect: must be pygame.Rect not {_prvt.get_type(self.rect)}"))
        _prvt.asserting(isinstance(self.outline_size, _RealNumber | None), TypeError(f"outline_size: must be ArgsList or (None for no outline) not {_prvt.get_type(self.outline_size)}"))
        _prvt.asserting(isinstance(self.image, pygame.Surface | None), TypeError(f"image: must be pygame.Surface or (None for no image)not {_prvt.get_type(self.image)}"))
        _prvt.asserting(isinstance(self.image_transform, _RealNumber | _ArgsList | None), TypeError(f'image_transform: must be RealNumber or ArgsList or (None for not being transformed) not {_prvt.get_type(self.image_transform)}'))
        _prvt.asserting(isinstance(self.get_rect_text_kwargs, dict | None), TypeError(f'get_rect_text_kwargs: must be dict type or (None default: center) not {_prvt.get_type(self.get_rect_text_kwargs)}'))
        _prvt.asserting(isinstance(self.get_rect_image_kwargs, dict | None), TypeError(f'get_rect_image_kwargs: must be dict type or (None default: center) not {_prvt.get_type(self.get_rect_image_kwargs)}'))
        _prvt.asserting(isinstance(self.color, button_color), TypeError(f'color: must be button_color not {_prvt.get_type(self.color)}'))
        _prvt.asserting(isinstance(self.text_color, button_color), TypeError(f'text_color: must be button_color not {_prvt.get_type(self.text_color)}'))
        _prvt.asserting(isinstance(self.outline_color, button_color), TypeError(f'outline_color: must be button_color not {_prvt.get_type(self.text_color)}'))
        _prvt.asserting(isinstance(self.click_speed, int), TypeError(f'click_speed: must be int type not {_prvt.get_type(self.click_speed)}'))
        _prvt.asserting(isinstance(self.borders, border_radius), TypeError(f'borders: must be border_radius not {_prvt.get_type(self.borders)}'))
        _prvt.asserting(self.click_speed >= 0, ValueError(f'click_speed: illegal below 0 -> {self.click_speed}'))

        if kwargs is not None:
            rq_key = self.get_param().keys()

            for key in kwargs:
                _prvt.asserting(key in rq_key, TypeError(f"kwargs: got an unexpected keyword argument '{key}'"))

        if isinstance(self.image_transform, _RealNumber | _ArgsList) and self.image is None:
            raise ValueError('image_transform: Cannot transform image because image parameters have not been provided')
        elif isinstance(self.image_transform, _RealNumber):
            self.__transform_image = pygame.transform.scale(self.image, (self.rect.width - self.image_transform, self.rect.height - self.image_transform))
        elif isinstance(self.image_transform, _ArgsList):
            self.__transform_image = pygame.transform.scale(self.image, self.image_transform)

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

        self.__set_and_validates(kwargs)

        self.button_event.id = self.id

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        return -> `dict[str, object]`
        """

        return {
            'surface_screen': self.surface_screen,
            'rect': self.rect,
            'id': self.id,
            'text': self.text,
            'font': self.font,
            'hide': self.hide,
            'outline_size': self.outline_size,
            'antialias_text': self.antialias_text,
            'image': self.image,
            'image_transform': self.image_transform,
            'get_rect_image_kwargs': self.get_rect_image_kwargs,
            'get_rect_text_kwargs': self.get_rect_text_kwargs,
            'color': self.color,
            'text_color': self.text_color,
            'outline_color': self.outline_color,
            'inactive_cursor': self.inactive_cursor,
            'active_cursor': self.active_cursor,
            'only_click': self.only_click,
            'click_speed': self.click_speed,
            'borders': self.borders
        }

    def get_private_attr(self, remove_underscore: bool = False) -> dict[str, object]:

        """
        Get private property.

        return -> `dict[str, object]`
        """

        attr_dict = {
            '__last_click_time': self.__last_click_time,
            '__clicked_button': self.__clicked_button,
            '__button_outside': self.__button_outside,
            '__get_event': self.__get_event.copy(),
            '__transform_image': self.__transform_image.copy()
        }

        if not remove_underscore:
            return attr_dict
        else:
            return {attr.lstrip('_'): value for attr, value in attr_dict}

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

        self.__button_outside = _prvt.is_partially_outside(self.surface_screen.get_rect(), self.rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        ismousehover = self.rect.collidepoint(mouse_x, mouse_y)

        self.button_event.value = ''
        self.button_event.ismousehover = ismousehover
        self.button_event.isbuttoninactive = not ismousehover
        self.button_event.isbuttonhover = ismousehover
        self.button_event.isbuttonactive = False
        self.button_event.cursor_active = False
        self.button_event.cursor_inactive = False

        if not self.__button_outside:
            current_time = pygame.time.get_ticks()
            get_pressed = _prvt.get_mouse_pressed(self.only_click)
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
                        self.button_event.send_event()

                    return self.button_event

            elif ismousehover and self.ishandlebyevent:
                render_active_button(False)

                if self.__clicked_button and any_pressed:
                    return self.button_event

                elif current_time - self.__last_click_time > self.click_speed and self.__get_event:
                    render_active_button()
                    self.button_event.value = self.__get_event.value
                    self.button_event.isbuttonactive = True
                    self.__get_event.reset_property()
                    if self._send_event:
                        self.button_event.send_event()

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

        self.__button_outside = _prvt.is_partially_outside(self.surface_screen.get_rect(), self.rect)
        self.__clicked_button = False
        self.__render_inactive_hover_button(False)
        self.button_event.reset_property()

    def draw_hover(self) -> None:

        """
        Render the hover button.

        return -> `None`
        """

        self.__button_outside = _prvt.is_partially_outside(self.surface_screen.get_rect(), self.rect)
        self.__clicked_button = False
        self.__render_inactive_hover_button(True)
        self.button_event.reset_property()

    def draw_active(self) -> None:

        """
        Render the active button.

        return -> `None`
        """

        self.__button_outside = _prvt.is_partially_outside(self.surface_screen.get_rect(), self.rect)
        self.__clicked_button = False
        self.__render_active_button(0, False)
        self.button_event.reset_property()


class Range(_ButtonInterface):

    """ Button Range - Push button distance class, creates a button distance function (slider button) through the pygame screen and can set it with the provided. """

    def __init__(

        self,
        surface_screen: pygame.Surface,
        rect: pygame.Rect,
        id: _typing.Any = None,
        thumb_size: _ArgsList | None = None,
        outline_size: _RealNumber | None = None,
        thumb_color: button_color = button_color(_WHITE, _GRAY, _LIGHT_GRAY),
        track_color: button_color = button_color(_GRAY, _WHITE, _GRAY),
        track_fill_color: button_color = button_color(_BLUE, _BLUE, _LIGHT_BLUE),
        outline_color: button_color = button_color(_GRAY, _WHITE, _LIGHT_GRAY),
        inactive_cursor: _CursorID | None = None,
        active_cursor: _CursorID | None = None,
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
        step: _RealNumber | None = 1,
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

        self.__button_track._send_event = False
        self.__button_thumb._send_event = False
        self.__button_track_fill._send_event = False

        self.__clicked_button: bool = False
        self.__detected_scroller_mouse: bool = False
        self.__button_outside: bool = False
        self.__use_thumb: bool = isinstance(self.thumb_size, _ArgsList)
        self.__rect_thumb: pygame.Rect = _prvt.init_rect
        self.__rect_track_fill: pygame.Rect = _prvt.init_rect

        self.ishandlebyevent: bool = False
        self.button_event: ButtonEvent = ButtonEvent('', 'Range', id)
        self.button_event.range_value = self.value

        self.__set_and_validates()

    def __multiple_value(self, vtype: _typing.Literal['value', 'evalue'] = 'value', evalue = None, estep = None) -> None | _RealNumber:

        """
        Private method. Look for the closest multiple value.

        return -> (`None` => vtype='value') or (`RealNumber` => vtype='evalue')
        """

        if self.step is not None:

            if vtype == 'value':
                rest = (self.value - self.min_value) % self.step
                if rest < self.step / 2:
                    self.button_event.range_value = self.value = self.range_value_output(self.value - rest)
                else:
                    self.button_event.range_value = self.value = self.range_value_output(self.value + (self.step - rest))

            elif vtype == 'evalue':
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

            if type_draw == 'active':
                self.__button_track_fill.draw_active()
                if self.__use_thumb:
                    self.__button_thumb.draw_active()

            elif type_draw == 'inactive':
                self.__button_track_fill.draw_inactive()
                if self.__use_thumb:
                    self.__button_thumb.draw_inactive()

            elif type_draw == 'hover':
                self.__button_track_fill.draw_hover()
                if self.__use_thumb:
                    self.__button_thumb.draw_hover()

    def __set_track_and_thumb_positions(self) -> None:

        """
        Private method. Set the track fill size and thumb position.

        return -> `None`
        """

        self.__multiple_value()

        if self.horizontal:
            if isinstance(self.rect, pygame.Rect):
                track_fill_width = ((self.value - self.min_value) / (self.max_value - self.min_value)) * self.rect.width
                self.__rect_track_fill = (
                    pygame.Rect(self.rect.left, self.rect.top, track_fill_width, self.rect.height)
                    if not self.reversed else
                    pygame.Rect(self.rect.right - track_fill_width, self.rect.top, track_fill_width, self.rect.height)
                )

            if self.__use_thumb:
                self.__rect_thumb = (
                    pygame.Rect(self.rect.left + self.__rect_track_fill.width - self.thumb_size[0] / 2, self.rect.top + (self.rect.height - self.thumb_size[1]) / 2, self.thumb_size[0], self.thumb_size[1])
                    if not self.reversed else
                    pygame.Rect(self.__rect_track_fill.left - self.thumb_size[0] / 2, self.rect.top + (self.rect.height - self.thumb_size[1]) / 2, self.thumb_size[0], self.thumb_size[1])
                )

        else:
            if isinstance(self.rect, pygame.Rect):
                track_fill_height = ((self.value - self.min_value) / (self.max_value - self.min_value)) * self.rect.height
                self.__rect_track_fill = (
                    pygame.Rect(self.rect.left, self.rect.top, self.rect.width, track_fill_height)
                    if not self.reversed else
                    pygame.Rect(self.rect.left, self.rect.bottom - track_fill_height, self.rect.width, track_fill_height)
                )

            if self.__use_thumb:
                self.__rect_thumb = (
                    pygame.Rect(self.rect.left + (self.rect.width - self.thumb_size[0]) / 2, self.rect.top + self.__rect_track_fill.height - self.thumb_size[1] / 2, self.thumb_size[0], self.thumb_size[1])
                    if not self.reversed else
                    pygame.Rect(self.rect.left + (self.rect.width - self.thumb_size[0]) / 2, self.__rect_track_fill.top - self.thumb_size[1] / 2, self.thumb_size[0], self.thumb_size[1])
                )

    def __update(self, mouse_pos: _ArgsList, get_pressed: _ArgsList | None) -> ButtonEvent:

        """
        Private method. Update the Range value.

        return -> `ButtonEvent`
        """

        if self.horizontal:
            if mouse_pos[0] > self.rect.right:
                relative_position = (self.rect.right - self.rect.left) / self.rect.width
            elif mouse_pos[0] < self.rect.left:
                relative_position = (self.rect.left - self.rect.left) / self.rect.width
            else:
                relative_position = (mouse_pos[0] - self.rect.left) / self.rect.width

            self.__rect_track_fill.width = relative_position * self.rect.width
            if self.step is not None:
                self.__rect_track_fill.width = self.__multiple_value('evalue', self.__rect_track_fill.width, self.rect.width / (self.max_value - self.min_value))

            if self.reversed:
                self.__rect_track_fill.width = self.rect.width - self.__rect_track_fill.width
                self.__rect_track_fill.left = self.rect.right - self.__rect_track_fill.width

            if self.__use_thumb:
                self.__rect_thumb.left = (
                    self.rect.right - self.__rect_track_fill.width - self.__rect_thumb.width / 2
                    if self.reversed else
                    self.rect.left + self.__rect_track_fill.width - self.__rect_thumb.width / 2
                )

        else:
            if mouse_pos[1] > self.rect.bottom:
                relative_position = (self.rect.bottom - self.rect.top) / self.rect.height
            elif mouse_pos[1] < self.rect.top:
                relative_position = (self.rect.top - self.rect.top) / self.rect.height
            else:
                relative_position = (mouse_pos[1] - self.rect.top) / self.rect.height

            self.__rect_track_fill.height = relative_position * self.rect.height
            if self.step is not None:
                self.__rect_track_fill.height = self.__multiple_value('evalue', self.__rect_track_fill.height, self.rect.height / (self.max_value - self.min_value))

            if self.reversed:
                self.__rect_track_fill.height = self.rect.height - self.__rect_track_fill.height
                self.__rect_track_fill.top = self.rect.bottom - self.__rect_track_fill.height

            if self.__use_thumb:
                self.__rect_thumb.top = (
                    self.rect.bottom - self.__rect_track_fill.height - self.__rect_thumb.height / 2
                    if self.reversed else
                    self.rect.top + self.__rect_track_fill.height - self.__rect_thumb.height / 2
                )

        self.button_event.range_value = self.value = self.range_value_output(
            self.min_value + (relative_position * (self.max_value - self.min_value))
            if not self.reversed else
            self.max_value - (relative_position * (self.max_value - self.min_value))
        )

        self.__multiple_value()

        if isinstance(get_pressed, _ArgsList):
            if get_pressed[0]:
                self.button_event.value = 'l'
            elif get_pressed[1]:
                self.button_event.value = 'c'
            elif get_pressed[2]:
                self.button_event.value = 'r'
            self.button_event.send_event()

        else:
            self.button_event.value = self.__button_track.button_event.value

        self.button_event.isdragging = True

        return self.button_event

    def __set_and_validates(self, kwargs: dict | None = None) -> None:

        """
        Private method. Sets parameters and validates parameters.

        return -> `None`
        """

        _prvt.asserting(isinstance(self.surface_screen, pygame.Surface), TypeError(f"surface_screen: must be pygame.Surface not {_prvt.get_type(self.surface_screen)}"))
        _prvt.asserting(isinstance(self.rect, pygame.Rect), TypeError(f"rect: must be pygame.Rect not {_prvt.get_type(self.rect)}"))
        _prvt.asserting(isinstance(self.outline_size, _RealNumber | None), TypeError(f"outline_size: must be ArgsList or (None for no outline) not {_prvt.get_type(self.outline_size)}"))
        _prvt.asserting(isinstance(self.thumb_color, button_color), TypeError(f'thumb_color: must be button_color not {_prvt.get_type(self.thumb_color)}'))
        _prvt.asserting(isinstance(self.track_color, button_color), TypeError(f'track_color: must be button_color not {_prvt.get_type(self.track_color)}'))
        _prvt.asserting(isinstance(self.track_fill_color, button_color), TypeError(f'track_fill_color: must be button_color not {_prvt.get_type(self.track_fill_color)}'))
        _prvt.asserting(isinstance(self.min_value, _RealNumber), TypeError(f'min_value: must be RealNumber type not {_prvt.get_type(self.min_value)}'))
        _prvt.asserting(isinstance(self.max_value, _RealNumber), TypeError(f'max_value: must be RealNumber type not {_prvt.get_type(self.max_value)}'))
        _prvt.asserting(isinstance(self.value, _RealNumber), TypeError(f'value: must be RealNumber type not {_prvt.get_type(self.value)}'))
        _prvt.asserting(isinstance(self.step, _RealNumber | None), TypeError(f'step: must be RealNumber type not {_prvt.get_type(self.step)}'))
        _prvt.asserting(isinstance(self.click_speed, int), TypeError(f'click_speed: must be int type not {_prvt.get_type(self.click_speed)}'))
        _prvt.asserting(isinstance(self.range_value_output, type), TypeError(f'range_value_output: must be class type object not {repr(self.range_value_output)} -> {_prvt.get_type(self.range_value_output)}'))
        _prvt.asserting(isinstance(self.borders_thumb, border_radius), TypeError(f'borders_thumb: must be border_radius not {_prvt.get_type(self.borders_thumb)}'))
        _prvt.asserting(isinstance(self.borders_track, border_radius), TypeError(f'borders_track: must be border_radius not {_prvt.get_type(self.borders_track)}'))
        _prvt.asserting(isinstance(self.borders_track_fill, border_radius), TypeError(f'borders_track_fill: must be border_radius not {_prvt.get_type(self.borders_track_fill)}'))
        _prvt.asserting(self.range_value_output in (int, float), TypeError(f'range_value_output: must be (int or float) type not {self.range_value_output}'))
        _prvt.asserting(self.min_value != self.max_value, ValueError(f'min_value, max_value: illegal min_value, max_value is same -> min_value: {self.min_value}, max_value: {self.max_value}'))
        _prvt.asserting(self.min_value < self.max_value, ValueError(f'min_value, max_value: illegal min_value is greater than max_value -> min_value: {self.min_value}, max_value: {self.max_value}'))
        _prvt.asserting(self.min_value <= self.value <= self.max_value, ValueError(f'value: illegal below min_value and above max_value -> {self.value}'))
        _prvt.asserting(self.click_speed >= 0, ValueError(f'click_speed: illegal below 0 -> {self.click_speed}'))

        if self.step is not None:
            _prvt.asserting(isinstance(self.step, _RealNumber), TypeError(f'step: must be RealNumber type or (None for no step) not {_prvt.get_type(self.step)}'))
            _prvt.asserting(0 < self.step <= (self.max_value - self.min_value), ValueError(f'step: cannot exceed the total of min_value and max_value or below 1 -> {self.step}'))

        if kwargs is not None:
            rq_key = self.get_param().keys()
            for key in kwargs:
                _prvt.asserting(key in rq_key, TypeError(f"kwargs: got an unexpected keyword argument '{key}'"))

        self.__set_track_and_thumb_positions()

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

        self.__set_and_validates(kwargs)

        self.button_event.id = self.id
        self.__use_thumb = isinstance(self.thumb_size, _ArgsList)
        if 'value' in kwargs:
            self.set_value(kwargs['value'])

        self.__button_track.edit_param(
            surface_screen = self.surface_screen,
            hide = self.hide_track,
            rect = self.rect,
            outline_size = self.outline_size,
            color = self.track_color,
            outline_color = self.outline_color,
            only_click = self.only_click,
            click_speed = self.click_speed,
            borders = self.borders_track
        )
        self.__button_thumb.edit_param(
            surface_screen = self.surface_screen,
            hide = self.hide_thumb,
            color = self.thumb_color,
            borders = self.borders_thumb
        )
        self.__button_track_fill = self.__button_track.copy(
            hide = self.hide_track_fill,
            color = self.track_fill_color,
            borders = self.borders_track_fill
        )

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        return -> `dict[str, object]`
        """

        return {
            'surface_screen': self.surface_screen,
            'rect': self.rect,
            'id': self.id,
            'thumb_size': self.thumb_size,
            'outline_size': self.outline_size,
            'thumb_color': self.thumb_color,
            'track_color': self.track_color,
            'track_fill_color': self.track_fill_color,
            'outline_color': self.outline_color,
            'inactive_cursor': self.inactive_cursor,
            'active_cursor': self.active_cursor,
            'active_cursor_outside': self.active_cursor_outside,
            'horizontal': self.horizontal,
            'reversed': self.reversed,
            'reversed_scroller_mouse': self.reversed_scroller_mouse,
            'drag_scroller_mouse': self.drag_scroller_mouse,
            'hide_thumb': self.hide_thumb,
            'hide_track': self.hide_track,
            'hide_track_fill': self.hide_track_fill,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'value': self.value,
            'step': self.step,
            'range_value_output': self.range_value_output,
            'only_click': self.only_click,
            'click_speed': self.click_speed,
            'borders_thumb': self.borders_thumb,
            'borders_track': self.borders_track,
            'borders_track_fill': self.borders_track_fill
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
        self.__set_and_validates()

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

            if event.button == (4 if not self.reversed_scroller_mouse else 5) and self.button_event.ismousehover:
                self.value += self.step

                if self.value > self.max_value:
                    self.value = self.max_value
                elif self.value < self.min_value:
                    self.value = self.min_value

                self.button_event.range_value = self.value = self.range_value_output(self.value)
                self.button_event.value = 'sc'
                self.button_event.isdragging = True
                self.__detected_scroller_mouse = True
                self.__set_track_and_thumb_positions()
                self.button_event.send_event()

            elif event.button == (5 if not self.reversed_scroller_mouse else 4) and self.button_event.ismousehover:
                self.value -= self.step

                if self.value > self.max_value:
                    self.value = self.max_value
                elif self.value < self.min_value:
                    self.value = self.min_value

                self.button_event.range_value = self.value = self.range_value_output(self.value)
                self.button_event.value = 'sc'
                self.button_event.isdragging = True
                self.__detected_scroller_mouse = True
                self.__set_track_and_thumb_positions()
                self.button_event.send_event()

    def draw_and_update(self) -> ButtonEvent:

        """
        Draw and update Range button. Draw a range button and then update it according to the events obtained.

        return -> `ButtonEvent` or via `Range.button_event`
        """

        self.__button_outside = _prvt.is_partially_outside(self.surface_screen.get_rect(), self.rect)

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
            get_pressed = _prvt.get_mouse_pressed(self.only_click)
            any_pressed = (get_pressed[0] or get_pressed[1] or get_pressed[2])

            if not self.__detected_scroller_mouse:
                self.button_event.isdragging = False

            if self.active_cursor is not None and ((ismousehover or self.__clicked_button) if self.active_cursor_outside else ismousehover):
                pygame.mouse.set_cursor(self.active_cursor)
                self.button_event.cursor_active = True
            elif self.inactive_cursor is not None:
                pygame.mouse.set_cursor(self.inactive_cursor)
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

        self.button_event.reset_property()
        self.button_event.range_value = self.value = self.range_value_output(self.value)
        self.__clicked_button = False
        self.__button_outside = _prvt.is_partially_outside(self.surface_screen.get_rect(), self.rect)
        self.__button_track.draw_inactive()
        self.__render_thumb_and_track_fill('inactive')

    def draw_hover(self) -> None:

        """
        Render the hover button.

        return -> `None`
        """

        self.button_event.reset_property()
        self.button_event.range_value = self.value = self.range_value_output(self.value)
        self.__clicked_button = False
        self.__button_outside = _prvt.is_partially_outside(self.surface_screen.get_rect(), self.rect)
        self.__button_track.draw_hover()
        self.__render_thumb_and_track_fill('hover')

    def draw_active(self) -> None:

        """
        Render the active button.

        return -> `None`
        """

        self.button_event.reset_property()
        self.button_event.range_value = self.value = self.range_value_output(self.value)
        self.__clicked_button = False
        self.__button_outside = _prvt.is_partially_outside(self.surface_screen.get_rect(), self.rect)
        self.__button_track.draw_active()
        self.__render_thumb_and_track_fill('active')

# Type buttons
ButtonType = Button
RangeType = Range
ButtonsType = ButtonType | RangeType


def set_cursor_buttons(

        *buttons: ButtonsType,
        inactive_cursor: _CursorID | None = None,
        active_cursor: _CursorID | None = None,
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
            inactive_cursor: _CursorID | None = None,
            active_cursor: _CursorID | None = None,
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

    def edit_param(self, id: _typing.Any, **kwargs) -> None:

        """
        Edit button parameters via the key argument of this function.
        Enter button id to edit specific parameters.

        return -> `None`
        """

        for button in self.buttons:
            if id == button.id:
                button.edit_param(**kwargs)

    def get_param(self, id: _typing.Any) -> list[dict[str, object]]:

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

    def get_private_attr(self, id: _typing.Any, remove_underscore: bool = False) -> list[dict[str, object]]:

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

        set_cursor_buttons(*self.buttons, inactive_cursor=self.inactive_cursor, active_cursor=self.active_cursor, set_active_cursor_button=self.set_active_cursor_button)

        for button in self.buttons:
            button.draw_and_update()

    def draw_inactive(self) -> None:

        """
        Render the inactive buttons.

        return -> `None`
        """

        set_cursor_buttons(*self.buttons, inactive_cursor=self.inactive_cursor, active_cursor=self.active_cursor, set_active_cursor_button=self.set_active_cursor_button)

        for button in self.buttons:
            button.draw_inactive()

    def draw_hover(self) -> None:

        """
        Render the hover buttons.

        return -> `None`
        """

        set_cursor_buttons(*self.buttons, inactive_cursor=self.inactive_cursor, active_cursor=self.active_cursor, set_active_cursor_button=self.set_active_cursor_button)

        for button in self.buttons:
            button.draw_hover()

    def draw_active(self) -> None:

        """
        Render the active buttons.

        return -> `None`
        """

        set_cursor_buttons(*self.buttons, inactive_cursor=self.inactive_cursor, active_cursor=self.active_cursor, set_active_cursor_button=self.set_active_cursor_button)

        for button in self.buttons:
            button.draw_active()


__version__ = '1.1.0'
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