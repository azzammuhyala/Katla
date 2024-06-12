"""
# pygamebutton module
Version: 1.0.0 - Release.

pygame elements. Button and Range (new)

Explanations
------------
pygamebutton is a special tool module for displaying general button elements.
Pygame does not provide a button media element. However, the functions and
methods provided by the pygame module provide various ways to create this
button element. And this module is used as a button function that is
ready-made and ready to use

Functions or Classes provided:
```
<class name=SystemCursor(int)>
    <property> 
        * id
        * ARROW
        * CROSSHAIR
        * HAND
        * IBEAM
        * NO
        * SIZEALL
        * SIZENESW
        * SIZENS
        * SIZENWSE
        * SIZEWE
        * WAIT
        * WAITARROW
    </property>
    <method>
        * copy
        * set_cursor
        * get_cursor
        * get_set_cursor
    </method>
</class>

<class name=ButtonEvent>
    <property>
        * value
        * type
        # etc
    </property>
</class>

<class name=border_radius>
    <property>
        * radius
        * top_left_radius
        * top_right_radius
        * bottom_left_radius
        * bottom_right_radius
        * draw_rect_kwargs
    </property>
    <method>
        * get_param
    </method>
</class>

<class name=button_color>
    <property>
        * kwargs_color
        * inactive_color
        * active_color
        * hover_color
    </property>
</class>

<class name=Button>
    <property>
        * surface_screen
        * rect
        * text
        * font
        * antialias_text
        * image
        * outline_size
        * image_transform
        * get_rect_image_kwargs
        * get_rect_text_kwargs
        * text_color
        * color
        * outline_color
        * inactive_cursor
        * active_cursor
        * only_click
        * click_speed
        * borders
        * ishandlebyevent
        * button_event
    </property>
    <method>
        * copy
        * edit_param
        * get_param
        * handle_event
        * draw_and_update
        * draw_inactive
        * draw_hover
        * draw_active
    </method>
</class>

<class name=Range>
    <property>
        * surface_screen
        * thumb_size
        * rect_track
        * outline_size
        * thumb_color
        * track_color
        * track_fill_color
        * outline_color
        * inactive_cursor
        * active_cursor
        * active_cursor_outside
        * min_value
        * max_value
        * value
        * only_click
        * click_speed
        * borders_thumb
        * borders_track
        * borders_track_fill
        * ishandlebyevent
        * button_event
    </property>
    <method>
        * copy
        * edit_param
        * get_param
        * handle_event
        * draw_and_update
        * draw_inactive
        * draw_hover
        * draw_active
    </method>
</class>

<function name=operator_collidepoint_buttons>
<function name=SetAllCursorButtons>
```

Here is a example of a basic setup (opens the window, updates the screen, and handles events):
```
import pygame # import the pygame
import pygamebutton # import the pygamebutton

# pygame setup
pygame.init()
running = True
cursor = pygamebutton.SystemCursor() # gets all system cursor (optional)

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
rect_track = pygame.Rect((screen.get_width() - 400) / 2, 100, 400, 10)
# The size of the thumb range
thumb_size = (17, 17)
# initialization button (Do not initialization Buttons in the game loop because this will be affected by time, events, etc)
button1 = pygamebutton.Button(screen, rect_button1, text='BUTTON 1')
# if you want to copy an element, use the copy() method and fill it with new parameters if necessary
button2 = button1.copy(text='BUTTON 2', outline_size=5, rect=rect_button2, only_click='lrc', click_speed=250)
# input range parameters
range_button = pygamebutton.Range(screen, thumb_size=thumb_size, rect_track=rect_track, min_value=0, max_value=100, value=50)

# screen loop
while running:
    # events
    for event in pygame.event.get():
        # when the user clicks the X to close the screen (pygame)
        if event.type == pygame.QUIT:
            running = False
        # if you want to handle the input button via an event, do it using the handle_event(event) method
        button1.handle_event(event)
        button2.handle_event(event)
        # handle_event in the Range class is not recommended because the event cannot take input continuously after the first input is obtained
        # range_button.handle_event(event)
    # fill screen black
    screen.fill('black')
    # blit or draw and update the button
    button1.draw_and_update()
    button2.draw_and_update()
    range_button.draw_and_update()
    # if you want to control the cursor interaction on the button, do it using SetAllCursorButtons method
    # SetAllCursorButtons(*buttons, inactive_cursor=<Cursor | SystemCursor>, active_cursor=<Cursor | SystemCursor>)
    pygamebutton.SetAllCursorButtons(button1, button2, range_button, inactive_cursor=cursor.ARROW, active_cursor=cursor.HAND)

    text_range = showtext(f'Value Range: {range_button.button_event.range_value:.2f}')

    # get button event
    if button1.button_event.value:
        msg = 'Pressed BUTTON 1 -> ' + button1.button_event.value
        print(msg)
        text = showtext(msg)

    if button2.button_event.value:
        msg = 'Pressed BUTTON 2 -> ' + button2.button_event.value
        print(msg)
        text = showtext(msg)

    # show the range event text
    screen.blit(text_range, ((screen.get_width() - text_range.get_width()) / 2, 115))
    # show the button event text
    screen.blit(text, ((screen.get_width() - text.get_width()) / 2, 450))
    # flip() the display to put your work on screen
    pygame.display.flip()
    # Set the frame-rate speed to 60
    clock.tick(60)

# clean up pygame resources
pygame.quit()
```
Thank you to those of you who have read the documentation and code examples.
"""


import pygame


class _Private:

    """ _Private - private class """

    def __init__(self) -> None:

        """
        This class is private and contains methods contained in the button element
        """

        pass

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

    def get_mouse_pressed(self, only_click: tuple | str) -> tuple[bool, bool, bool]:

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


class SystemCursor(int):

    """ SystemCursor - cursor system type and set the cursor """

    def __init__(self, id: int | None = None) -> None:
        super().__init__()

        self.id = id
        self.ARROW: int = pygame.SYSTEM_CURSOR_ARROW
        self.CROSSHAIR: int = pygame.SYSTEM_CURSOR_CROSSHAIR
        self.HAND: int = pygame.SYSTEM_CURSOR_HAND
        self.IBEAM: int = pygame.SYSTEM_CURSOR_IBEAM
        self.NO: int = pygame.SYSTEM_CURSOR_NO
        self.SIZEALL: int = pygame.SYSTEM_CURSOR_SIZEALL
        self.SIZENESW: int = pygame.SYSTEM_CURSOR_SIZENESW
        self.SIZENS: int = pygame.SYSTEM_CURSOR_SIZENS
        self.SIZENWSE: int = pygame.SYSTEM_CURSOR_SIZENWSE
        self.SIZEWE: int = pygame.SYSTEM_CURSOR_SIZEWE
        self.WAIT: int = pygame.SYSTEM_CURSOR_WAIT
        self.WAITARROW: int = pygame.SYSTEM_CURSOR_WAITARROW

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
_BLUE       = (0,   0,   255)
_LIGHT_BLUE = (120, 120, 255)

# Private Initialization
_prvt = _Private()

# Union types
_RealNumber = int | float
_ArgsList = list | tuple
_ColorType = _ArgsList | str | pygame.Color
_CursorID = SystemCursor | pygame.Cursor | int


class ButtonEvent:

    """ ButtonEvent - The event of button function """

    def __init__(self, value: str, type: str) -> None:

        _prvt.asserting(isinstance(value, str), TypeError(f'value: must be str type not {_prvt.get_type(value)}'))

        self.value = value.lower()
        self.type = type
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
            self.range_value: float = None

        else:
            raise TypeError(f"type: unknown type '{type}'")

    def __repr__(self) -> str:
        return f'ButtonEvent(value="{self.value}", type="{self.type}")'

    def __str__(self) -> str:
        return self.value

    def __getitem__(self, index: int) -> str:
        _prvt.asserting(isinstance(index, int), TypeError(f'index: must be int type not {_prvt.get_type(index)}'))
        return self.value[index]

    def __eq__(self, order) -> bool:
        if isinstance(order, ButtonEvent):
            order = order.value
        return self.value == order

    def __ne__(self, order) -> bool:
        return not self.__eq__(order)

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

        self.kwargs_color: dict[str, object] = {
            'inactive_color': inactive_color,
            'active_color': active_color,
            'hover_color': hover_color
        }

        for key, value in self.kwargs_color.items():
            _prvt.asserting(isinstance(value, _ColorType | None), TypeError(f'{key}: must be ColorType or (None for default) color type not {_prvt.get_type(value)}'))

        self.inactive_color = inactive_color
        self.active_color = active_color
        self.hover_color = hover_color


class Button:

    """ Button - Push button class, creates a button function through the pygame screen and can set it with the parameters provided. """

    def __init__(

            self,
            surface_screen: pygame.Surface,
            rect: pygame.Rect = None,
            text: str = '',
            font: pygame.font.Font | None = None,
            antialias_text: bool = True,
            image: pygame.Surface | None = None,
            outline_size: _RealNumber | None = None,
            image_transform: _RealNumber | _ArgsList | None = None,
            get_rect_image_kwargs: dict | None = None,
            get_rect_text_kwargs: dict | None = None,
            text_color: button_color = button_color(_BLACK, _BLACK, _BLACK),
            color: button_color = button_color(_WHITE, _LIGHT_GRAY, _GRAY),
            outline_color: button_color = button_color(_GRAY, _WHITE, _LIGHT_GRAY),
            inactive_cursor: _CursorID | None = None,
            active_cursor: _CursorID | None = None,
            only_click: _ArgsList | str = 'l',
            click_speed: int = 50,
            borders: border_radius = border_radius()

        ) -> None:

        """
        param:
            * `surface_screen`: screen surface -> pygame.display.set_mode((x, y))
            * `rect`: rect button
            * `text`: text button
            * `font`: font text
            * `antialias_text`: param at -> font.render(text, antialias=<...>, ...)
            * `image`: image or icon on the button. (Use pygame.transform.scale(<Surface image source>, (rect button size))) to fit and fit the main button
            * `outline_size`: outline size of the button
            * `image_transform`: transform the size of the image surface. (If the type is numeric, then the size will be the size of the rect button with a margin of the numbers entered. If the type is tuple[number, number], then it will follow the scale of the contents of the tuple)
            * `get_rect_image_kwargs`: param at -> image.get_rect(<...>)
            * `get_rect_text_kwargs`: param at -> font.render.get_rect(<...>)
            * `text_color`: text color
            * `color`: button color
            * `outline_color`: outline color
            * `inactive_cursor`: change the cursor (un-hover)
            * `active_cursor`: change the cursor (hover)
            * `only_click`: click response ('r', 'c', 'l')
            * `click_speed`: click speed (ms)
            * `borders`: pygame.draw.rect borders. Use border_radius class
        """

        self.surface_screen = surface_screen
        self.rect = rect
        self.text = text
        self.font = font
        self.antialias_text = antialias_text
        self.image = image
        self.image_transform = image_transform
        self.get_rect_text_kwargs = get_rect_text_kwargs
        self.get_rect_image_kwargs = get_rect_image_kwargs
        self.outline_size = outline_size
        self.text_color = text_color
        self.color = color
        self.outline_color = outline_color
        self.inactive_cursor = inactive_cursor
        self.active_cursor = active_cursor
        self.only_click = only_click
        self.click_speed = click_speed
        self.borders = borders

        self.__last_click_time = 0
        self.__clicked_button = False
        self.__get_event = ButtonEvent('', 'Button')

        self.ishandlebyevent: bool = False
        self.button_event: ButtonEvent = ButtonEvent('', 'Button')

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

        if isinstance(self.outline_size, _RealNumber):
            pygame.draw.rect(self.surface_screen, self.outline_color.active_color, self.__rect_outline(), **self.borders.draw_rect_kwargs)
        pygame.draw.rect(self.surface_screen, self.color.active_color, self.rect, **self.borders.draw_rect_kwargs)

        text_surface = self.font.render(self.text, self.antialias_text, self.text_color.active_color)

        if self.get_rect_text_kwargs is None:
            text_rect = text_surface.get_rect(center=self.rect.center)
        elif isinstance(self.get_rect_text_kwargs, dict):
            text_rect = text_surface.get_rect(**self.get_rect_text_kwargs)
        else:
            raise TypeError(f'get_rect_text_kwargs: must be dict type not {_prvt.get_type(self.get_rect_text_kwargs)}')

        if self.image is not None:
            if self.get_rect_image_kwargs is None:
                self.surface_screen.blit(self.image, self.image.get_rect(center=self.rect.center))
            elif isinstance(self.get_rect_image_kwargs, dict):
                self.surface_screen.blit(self.image, self.image.get_rect(**self.get_rect_image_kwargs))
            else:
                raise TypeError(f'get_rect_text_kwargs: must be dict type not {_prvt.get_type(self.get_rect_text_kwargs)}')

        self.surface_screen.blit(text_surface, text_rect)

        if change_config:
            self.__clicked_button = False
            self.__last_click_time = current_time

    def __render_inactive_hover_button(self, ismousehover: bool) -> None:

        """
        Private method. Render the inactive or hover button.

        return -> `None`
        """

        if isinstance(self.outline_size, _RealNumber):
            pygame.draw.rect(self.surface_screen, (self.outline_color.hover_color if (self.outline_color.hover_color is not None) and ismousehover else self.outline_color.inactive_color), self.__rect_outline(), **self.borders.draw_rect_kwargs)
        pygame.draw.rect(self.surface_screen, (self.color.hover_color if (self.color.hover_color is not None) and ismousehover else self.color.inactive_color), self.rect, **self.borders.draw_rect_kwargs)

        text_surface = self.font.render(self.text, self.antialias_text, (self.text_color.hover_color if (self.text_color.hover_color is not None) and ismousehover else self.text_color.inactive_color))

        if self.get_rect_text_kwargs is None:
            text_rect = text_surface.get_rect(center=self.rect.center)
        elif isinstance(self.get_rect_text_kwargs, dict):
            text_rect = text_surface.get_rect(**self.get_rect_text_kwargs)
        else:
            raise TypeError(f'get_rect_text_kwargs: must be dict type not {_prvt.get_type(self.get_rect_text_kwargs)}')

        if self.image is not None:
            if self.get_rect_image_kwargs is None:
                self.surface_screen.blit(self.image, self.image.get_rect(center=self.rect.center))
            elif isinstance(self.get_rect_image_kwargs, dict):
                self.surface_screen.blit(self.image, self.image.get_rect(**self.get_rect_image_kwargs))
            else:
                raise TypeError(f'get_rect_text_kwargs: must be dict type not {_prvt.get_type(self.get_rect_text_kwargs)}')

        self.surface_screen.blit(text_surface, text_rect)

    def __set_and_validates(self, kwargs: dict | None = None) -> None:

        """
        Private method. Sets parameters and validates parameters.

        return -> `None`
        """

        self.text = str(self.text)

        if not isinstance(self.font, pygame.font.Font):
            self.font = pygame.font.SysFont('Arial', 15)

        _prvt.asserting(isinstance(self.color, button_color), TypeError(f'color: must be button_color type not {_prvt.get_type(self.color)}'))
        _prvt.asserting(isinstance(self.text_color, button_color), TypeError(f'text_color: must be button_color type not {_prvt.get_type(self.text_color)}'))
        _prvt.asserting(isinstance(self.outline_color, button_color), TypeError(f'outline_color: must be button_color type not {_prvt.get_type(self.text_color)}'))
        _prvt.asserting(isinstance(self.image_transform, _RealNumber | _ArgsList | None), TypeError(f'image_transform: must be RealNumber or ArgsList or (None for not being transformed) not {_prvt.get_type(self.image_transform)}'))
        _prvt.asserting(isinstance(self.borders, border_radius), TypeError(f'borders: must be border_radius type not {_prvt.get_type(self.borders)}'))
        _prvt.asserting(isinstance(self.click_speed, int), TypeError(f'click_speed: must be int type not {_prvt.get_type(self.click_speed)}'))
        _prvt.asserting(self.click_speed >= 0, ValueError(f'click_speed: illegal below 0 -> {self.click_speed}'))

        if kwargs is not None:
            _prvt.asserting(isinstance(kwargs, dict), TypeError(f'kwargs: must be dict type not {_prvt.get_type(kwargs)}'))
            rq_kw = self.get_param().keys()
            for kw in kwargs:
                _prvt.asserting(kw in rq_kw, TypeError(f"kwargs: got an unexpected keyword argument '{kw}'"))

        if isinstance(self.image_transform, _RealNumber | _ArgsList) and self.image is None:
            raise ValueError('image_transform: Cannot transform image because image parameters have not been provided')
        elif isinstance(self.image_transform, _RealNumber):
            self.image = pygame.transform.scale(self.image, (self.rect.width - self.image_transform, self.rect.height - self.image_transform)) if isinstance(self.rect, pygame.Rect) else self.image
        elif isinstance(self.image_transform, _ArgsList):
            self.image = pygame.transform.scale(self.image, self.image_transform)

    def copy(self, **kwargs):

        """
        Copy the Button class. Can be edited via keyword arguments.

        return -> `Button(...)`
        """

        clonebutton = Button(**self.get_param())
        clonebutton.edit_param(**kwargs)
        return clonebutton

    def edit_param(self, **kwargs) -> None:

        """
        Edit parameters via the key argument of this function. Can be edited via keyword arguments.

        return -> `None`
        """

        for attr, value in kwargs.items():
            setattr(self, attr, value)

        self.__set_and_validates(kwargs)

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        return -> `dict[str, object]`
        """

        return {
            'surface_screen': self.surface_screen,
            'rect': self.rect,
            'text': self.text,
            'font': self.font,
            'antialias_text': self.antialias_text,
            'image': self.image,
            'outline_size': self.outline_size,
            'image_transform': self.image_transform,
            'get_rect_image_kwargs': self.get_rect_image_kwargs,
            'get_rect_text_kwargs': self.get_rect_text_kwargs,
            'text_color': self.text_color,
            'color': self.color,
            'outline_color': self.outline_color,
            'inactive_cursor': self.inactive_cursor,
            'active_cursor': self.active_cursor,
            'only_click': self.only_click,
            'click_speed': self.click_speed,
            'borders': self.borders
        }

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

        _prvt.asserting(isinstance(self.rect, pygame.Rect), TypeError(f"rect: must be pygame.Rect type not {_prvt.get_type(self.rect)}"))

        current_time = pygame.time.get_ticks()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        get_pressed = _prvt.get_mouse_pressed(self.only_click)
        ismousehover = self.rect.collidepoint(mouse_x, mouse_y)

        render_active_button = lambda change_config=True : self.__render_active_button(current_time, change_config)
        render_inactive_hover_button = lambda : self.__render_inactive_hover_button(ismousehover)

        self.button_event.value = ''
        self.button_event.ismousehover = ismousehover
        self.button_event.isbuttoninactive = not ismousehover
        self.button_event.isbuttonhover = ismousehover
        self.button_event.isbuttonactive = False
        self.button_event.cursor_active = False
        self.button_event.cursor_inactive = False

        if self.active_cursor is not None and ismousehover:
            pygame.mouse.set_cursor(self.active_cursor)
            self.button_event.cursor_active = True
        elif self.inactive_cursor is not None:
            pygame.mouse.set_cursor(self.inactive_cursor)
            self.button_event.cursor_inactive = True

        if not ismousehover or not any(get_pressed) and not self.__clicked_button:
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
                return self.button_event

        elif ismousehover and self.ishandlebyevent:
            render_active_button(False)

            if self.__clicked_button and any(get_pressed):
                return self.button_event

            elif current_time - self.__last_click_time > self.click_speed and self.__get_event:
                render_active_button()
                self.button_event.value = self.__get_event.value
                self.button_event.isbuttonactive = True
                self.__get_event = ButtonEvent('', 'Button')
                return self.button_event

            else:
                render_inactive_hover_button()

        if not ismousehover and self.ishandlebyevent and not any(get_pressed):
            self.__clicked_button = False

        return self.button_event

    def draw_inactive(self) -> None:

        """
        Render the inactive button.

        return -> `None`
        """

        _prvt.asserting(isinstance(self.rect, pygame.Rect), TypeError(f"rect: must be pygame.Rect type not {_prvt.get_type(self.rect)}"))

        self.button_event = ButtonEvent('', 'Button')
        self.__clicked_button = False
        self.__render_inactive_hover_button(False)

    def draw_hover(self) -> None:

        """
        Render the hover button.

        return -> `None`
        """

        _prvt.asserting(isinstance(self.rect, pygame.Rect), TypeError(f"rect: must be pygame.Rect type not {_prvt.get_type(self.rect)}"))

        self.button_event = ButtonEvent('', 'Button')
        self.__clicked_button = False
        self.__render_inactive_hover_button(True)

    def draw_active(self) -> None:

        """
        Render the active button.

        return -> `None`
        """

        _prvt.asserting(isinstance(self.rect, pygame.Rect), TypeError(f"rect: must be pygame.Rect type not {_prvt.get_type(self.rect)}"))

        self.button_event = ButtonEvent('', 'Button')
        self.__clicked_button = False
        self.__render_active_button(0, False)


class Range:

    """ Button Range - Push button distance class, creates a button distance function (slider button) through the pygame screen and can set it with the provided. """

    def __init__(

        self,
        surface_screen: pygame.Surface,
        thumb_size: _ArgsList | None = None,
        rect_track: pygame.Rect = None,
        outline_size: _RealNumber | None = None,
        thumb_color: button_color = button_color(_WHITE, _GRAY, _LIGHT_GRAY),
        track_color: button_color = button_color(_GRAY, _WHITE, _GRAY),
        track_fill_color: button_color = button_color(_BLUE, _BLUE, _LIGHT_BLUE),
        outline_color: button_color = button_color(_GRAY, _WHITE, _LIGHT_GRAY),
        inactive_cursor: _CursorID | None = None,
        active_cursor: _CursorID | None = None,
        active_cursor_outside: bool = False,
        min_value: _RealNumber = 0,
        max_value: _RealNumber = 100,
        value: _RealNumber = 0,
        only_click: _ArgsList | str = 'l',
        click_speed: int = 50,
        borders_thumb: border_radius = border_radius(radius=100),
        borders_track: border_radius = border_radius(radius=50),
        borders_track_fill: border_radius = border_radius(radius=50),

    ) -> None:

        """
        param:
            * `surface_screen`: screen surface -> pygame.display.set_mode((x, y))
            * `thumb_size`: thumb size (width, height) or set the default to None to not show it
            * `rect_track`: rect track (as well a rect Button)
            * `outline_size`: outline size of the range track button
            * `thumb_color`: thumb color
            * `track_color`: track color
            * `track_fill_color`: track fill color
            * `outline_color`: outline color
            * `inactive_cursor`: change the cursor (un-hover)
            * `active_cursor`: change the cursor (hover)
            * `active_cursor_outside`: The active cursor will be active if it is in the track_rect area and also outside the track_rect area when dragging
            * `min_value`: minimum value output
            * `max_value`: maximum value output
            * `value`: value output / default value
            * `only_click`: click response ('r', 'c', 'l')
            * `click_speed`: click speed (ms)
            * `borders_thumb`: pygame.draw.rect thumb borders. Use border_radius class
            * `borders_track`: pygame.draw.rect track borders. Use border_radius class
            * `borders_track_fill`: pygame.draw.rect track borders. Use border_radius class
        """

        self.surface_screen = surface_screen
        self.thumb_size = thumb_size
        self.rect_track = rect_track
        self.outline_size = outline_size
        self.thumb_color = thumb_color
        self.track_color = track_color
        self.track_fill_color = track_fill_color
        self.outline_color = outline_color
        self.inactive_cursor = inactive_cursor
        self.active_cursor = active_cursor
        self.active_cursor_outside = active_cursor_outside
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.only_click = only_click
        self.click_speed = click_speed
        self.borders_thumb = borders_thumb
        self.borders_track = borders_track
        self.borders_track_fill = borders_track_fill

        self.__button_track: Button = Button(
            surface_screen = surface_screen,
            rect = rect_track,
            outline_size = outline_size,
            color = track_color,
            outline_color = outline_color,
            only_click = only_click,
            click_speed = click_speed,
            borders = borders_track
        )
        self.__button_thumb: Button = Button(
            surface_screen = surface_screen,
            color = thumb_color,
            borders = borders_thumb
        )
        self.__button_track_fill: Button = self.__button_track.copy(
            color = track_fill_color,
            borders = borders_track_fill
        )

        self.__clicked_button: bool = False
        self.__rect_thumb: pygame.Rect
        self.__rect_track_fill: pygame.Rect

        self.ishandlebyevent: bool = False
        self.button_event: ButtonEvent = ButtonEvent('', 'Range')
        self.button_event.range_value = self.value

        self.__set_and_validates()

    def __render_thumb_and_track_fill(self, type_draw: str) -> None:

        """
        Private method. Render the thumb and track fill.

        return -> `None`
        """

        if isinstance(self.thumb_size, _ArgsList):
            self.__button_thumb.edit_param(rect=self.__rect_thumb)
        self.__button_track_fill.edit_param(rect=self.__rect_track_fill)

        if type_draw == 'active':
            self.__button_track_fill.draw_active()
            if self.thumb_size is not None:
                self.__button_thumb.draw_active()

        elif type_draw == 'inactive':
            self.__button_track_fill.draw_inactive()
            if self.thumb_size is not None:
                self.__button_thumb.draw_inactive()

        elif type_draw == 'hover':
            self.__button_track_fill.draw_hover()
            if self.thumb_size is not None:
                self.__button_thumb.draw_hover()

    def __update(self, mouse_x: _RealNumber, get_pressed: _ArgsList | None) -> ButtonEvent:

        """
        Private method. Update the Range value.

        return -> `ButtonEvent`
        """

        if mouse_x > self.rect_track.right:
            relative_position = (self.rect_track.right - self.rect_track.left) / self.rect_track.width
        elif mouse_x < self.rect_track.left:
            relative_position = (self.rect_track.left - self.rect_track.left) / self.rect_track.width
        else:
            relative_position = (mouse_x - self.rect_track.left) / self.rect_track.width

        self.__rect_track_fill.width = relative_position * self.rect_track.width
        if self.thumb_size is not None:
            self.__rect_thumb.left = self.rect_track.left + self.__rect_track_fill.width - self.__rect_thumb.width / 2

        if isinstance(get_pressed, _ArgsList):
            if get_pressed[0]:
                self.button_event.value = 'l'
            elif get_pressed[1]:
                self.button_event.value = 'c'
            elif get_pressed[2]:
                self.button_event.value = 'r'
        else:
            self.button_event.value = self.__button_track.button_event.value

        self.button_event.range_value = self.value = self.min_value + (relative_position * (self.max_value - self.min_value))
        self.button_event.isdragging = True
        return self.button_event

    def __set_and_validates(self, kwargs: dict | None = None) -> None:

        """
        Private method. Sets parameters and validates parameters.

        return -> `None`
        """

        _prvt.asserting(isinstance(self.thumb_color, button_color), TypeError(f'thumb_color: must be button_color type not {_prvt.get_type(self.thumb_color)}'))
        _prvt.asserting(isinstance(self.track_color, button_color), TypeError(f'track_color: must be button_color type not {_prvt.get_type(self.track_color)}'))
        _prvt.asserting(isinstance(self.track_fill_color, button_color), TypeError(f'track_fill_color: must be button_color type not {_prvt.get_type(self.track_fill_color)}'))
        _prvt.asserting(isinstance(self.borders_thumb, border_radius), TypeError(f'borders_thumb: must be border_radius type not {_prvt.get_type(self.borders_thumb)}'))
        _prvt.asserting(isinstance(self.borders_track, border_radius), TypeError(f'borders_track: must be border_radius type not {_prvt.get_type(self.borders_track)}'))
        _prvt.asserting(isinstance(self.borders_track_fill, border_radius), TypeError(f'borders_track_fill: must be border_radius type not {_prvt.get_type(self.borders_track_fill)}'))
        _prvt.asserting(isinstance(self.click_speed, int), TypeError(f'click_speed: must be int type not {_prvt.get_type(self.click_speed)}'))
        _prvt.asserting(isinstance(self.min_value, _RealNumber), TypeError(f'min_value: must be RealNumber type not {_prvt.get_type(self.min_value)}'))
        _prvt.asserting(isinstance(self.max_value, _RealNumber), TypeError(f'max_value: must be RealNumber type not {_prvt.get_type(self.max_value)}'))
        _prvt.asserting(isinstance(self.value, _RealNumber), TypeError(f'value: must be RealNumber type not {_prvt.get_type(self.value)}'))
        _prvt.asserting(self.click_speed >= 0, ValueError(f'click_speed: illegal below 0 -> {self.click_speed}'))
        _prvt.asserting(self.min_value != self.max_value, ValueError(f'min_value, max_value: illegal min_value, max_value is same -> min_value: {self.min_value}, max_value: {self.max_value}'))
        _prvt.asserting(self.min_value < self.max_value, ValueError(f'min_value, max_value: illegal min_value is greater than max_value -> min_value: {self.min_value}, max_value: {self.max_value}'))
        _prvt.asserting(self.value > self.min_value or self.value < self.max_value, ValueError(f'value: illegal below min_value and above max_value -> {self.value}'))

        if kwargs is not None:
            _prvt.asserting(isinstance(kwargs, dict), TypeError(f'kwargs: must be dict type not {_prvt.get_type(kwargs)}'))
            rq_kw = self.get_param().keys()
            for kw in kwargs:
                _prvt.asserting(kw in rq_kw, TypeError(f"kwargs: got an unexpected keyword argument '{kw}'"))

        if isinstance(self.rect_track, pygame.Rect):
            track_fill_width = ((self.value - self.min_value) / (self.max_value - self.min_value)) * self.rect_track.width
            self.__rect_track_fill = pygame.Rect(self.rect_track.left, self.rect_track.top, track_fill_width, self.rect_track.height)

        if isinstance(self.thumb_size, _ArgsList):
            self.__rect_thumb = pygame.Rect(self.rect_track.left + self.__rect_track_fill.width - self.thumb_size[0] / 2, self.rect_track.top + (self.rect_track.height - self.thumb_size[1]) / 2, self.thumb_size[0], self.thumb_size[1])

    def copy(self, **kwargs):

        """
        Copy the Button class. Can be edited via keyword arguments.

        return -> `Range(...)`
        """

        clonerange = Range(**self.get_param())
        clonerange.edit_param(**kwargs)
        return clonerange

    def edit_param(self, **kwargs) -> None:

        """
        Edit parameters via the key argument of this function. Can be edited via keyword arguments.

        return -> `None`
        """

        for attr, value in kwargs.items():
            setattr(self, attr, value)

        self.__set_and_validates(kwargs)

        self.__button_track.edit_param(
            surface_screen = self.surface_screen,
            rect = self.rect_track,
            outline_size = self.outline_size,
            color = self.track_color,
            outline_color = self.outline_color,
            only_click = self.only_click,
            click_speed = self.click_speed,
            borders = self.borders_track
        )
        self.__button_thumb.edit_param(
            surface_screen = self.surface_screen,
            color = self.thumb_color,
            borders = self.borders_thumb
        )
        self.__button_track_fill = self.__button_track.copy(
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
            'thumb_size': self.thumb_size,
            'rect_track': self.rect_track,
            'outline_size': self.outline_size,
            'thumb_color': self.thumb_color,
            'track_color': self.track_color,
            'track_fill_color': self.track_fill_color,
            'outline_color': self.outline_color,
            'inactive_cursor': self.inactive_cursor,
            'active_cursor': self.active_cursor,
            'active_cursor_outside': self.active_cursor_outside,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'value': self.value,
            'only_click': self.only_click,
            'click_speed': self.click_speed,
            'borders_thumb': self.borders_thumb,
            'borders_track': self.borders_track,
            'borders_track_fill': self.borders_track_fill
        }

    def handle_event(self, event: pygame.event.Event) -> None:

        """
        Handling mouse input via pygame events.
        This function method is not recommended in the Range class.

        return -> `None`
        """

        self.ishandlebyevent = True

        self.__button_track.handle_event(event)

    def draw_and_update(self) -> ButtonEvent:

        """
        Draw and update Range button. Draw a range button and then update it according to the events obtained.

        return -> `ButtonEvent` or via `Range.button_event`
        """

        mouse_x, mouse_y = pygame.mouse.get_pos()
        get_pressed = _prvt.get_mouse_pressed(self.only_click)
        ismousehover = self.rect_track.collidepoint(mouse_x, mouse_y) or (self.__rect_thumb.collidepoint(mouse_x, mouse_y) if self.thumb_size is not None else None)

        self.button_event.value = ''
        self.button_event.ismousehover = ismousehover
        self.button_event.israngeinactive = not ismousehover
        self.button_event.israngehover = ismousehover
        self.button_event.israngeactive = False
        self.button_event.isdragging = False
        self.button_event.range_value = self.value
        self.button_event.cursor_active = False
        self.button_event.cursor_inactive = False

        if self.active_cursor is not None and (any([ismousehover, self.__clicked_button]) if self.active_cursor_outside else ismousehover):
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

        if self.ishandlebyevent and self.__button_track.button_event.value:
            return self.__update(mouse_x, None)

        if any(get_pressed) and not self.ishandlebyevent:
            if ismousehover:
                self.__clicked_button = True

            if self.__clicked_button:
                return self.__update(mouse_x, get_pressed)

        elif not self.ishandlebyevent:
            self.__clicked_button = False

    def draw_inactive(self) -> None:

        """
        Render the inactive button.

        return -> `None`
        """

        self.button_event = ButtonEvent('', 'Range')
        self.__clicked_button = False
        self.__button_track.draw_inactive()
        self.__render_thumb_and_track_fill('inactive')

    def draw_hover(self) -> None:

        """
        Render the hover button.

        return -> `None`
        """

        self.button_event = ButtonEvent('', 'Range')
        self.__clicked_button = False
        self.__button_track.draw_hover()
        self.__render_thumb_and_track_fill('hover')

    def draw_active(self) -> None:

        """
        Render the active button.

        return -> `None`
        """

        self.button_event = ButtonEvent('', 'Range')
        self.__clicked_button = False
        self.__button_track.draw_active()
        self.__render_thumb_and_track_fill('active')


def operator_collidepoint_buttons(*buttons: Button | Range, operator: str = 'or') -> bool:

    """
    get the collision point of each button and operate it in the form of OR or AND.

    return -> `bool`
    """

    func_operator = {
        'or': any,
        'and': all
    }
    mousehovers = []
    operator = operator.lower()

    _prvt.asserting(isinstance(operator, str), TypeError(f"operator: must be str type not {_prvt.get_type(operator)}"))
    _prvt.asserting(operator in func_operator.keys(), ValueError(f"operator: invalid operator '{operator}'"))

    for button in buttons:
        _prvt.asserting(isinstance(button, Button | Range), TypeError(f'*buttons: most be Button type not {_prvt.get_type(button)}'))
        mousehovers.append(button.button_event.ismousehover)

    return func_operator[operator](mousehovers)


def SetAllCursorButtons(

        *buttons: Button | Range,
        inactive_cursor: _CursorID | None = None,
        active_cursor: _CursorID | None = None,
        set_active_cursor_button: bool = True

    ) -> None:

    """
    Sets the cursor set_mode of the double or more button functions.

    return -> `None`
    """

    for button in buttons:

        _prvt.asserting(isinstance(button, Button | Range), TypeError(f'*buttons: most be Button or Range type not {_prvt.get_type(button)}'))

        if set_active_cursor_button:
            if isinstance(button, Range):
                button.active_cursor_outside = False

            button.active_cursor = active_cursor

        button.inactive_cursor = None

    if operator_collidepoint_buttons(*buttons) is False and inactive_cursor is not None:
        pygame.mouse.set_cursor(inactive_cursor)


__all__ = [
    'SystemCursor',
    'ButtonEvent',
    'border_radius',
    'button_color',
    'Button',
    'Range',
    'operator_collidepoint_buttons',
    'SetAllCursorButtons'
]


del _BLACK, _GRAY, _LIGHT_GRAY, _WHITE, _BLUE, _LIGHT_BLUE, _Private