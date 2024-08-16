"""
MARKDOWN DOCUMENTATION

# `pygameui.scroller` / `pygamescroller` module
Version: beta 1.0.0

pygame scrollers. Scroller, X and Y

Explanations
------------
pygamescroller is a special tool module for create a scroll element object.
Pygame does not have a medium to make elements move with user movement.
However, the functions and methods provided by the pygame module provide
various ways to create this scroller elements. And this module is used as a
scrollers function that is ready-made and ready to use.

Events
------
How to get input from pygame scroller? Here will be explained with several
methods that you can use.

1. Method `ElementEvent`

Each scroller class has a scroller_event attribute that functions to get all
events that occur on the scroller such as anchor offsets and others. Each
scroller has different properties.

How to use:

Create a variable to contain the scroller.
```py
scroller1 = scroller.Scroller(
    max_scrolled=(500, 500),
    clock=clock # optional
)
```

Then create an event loop and call the update method for interaction.
```py
# loops game
while ...:
    for event in pygame.event.get():
        ... # your events
        scroller1.handle_event(event)

    scroller1.update()
```

And now you get an event with attributes:
```py
scroller1.scroller_event # event
```
or
```py
    scevent = scroller1.update()
    scevent # event
```

2. Method `pygame.Event`

This event method continuously captures scroller events from the pygame event
loop. However, it requires an id parameter to distinguish between scrollers.

How to use:

Create a variable to contain the scroller, enter the id type of the scroller.
```py
scroller1 = scroller.Scroller(
    max_scrolled=(500, 500),
    id='scroller1', # enter the id
    clock=clock # optional
)
```

How to catch the events.
```py
# loops game
while ...:
    for event in pygame.event.get():
        ... # your events
        scroller1.handle_event(event)

        if event.type == scroller.SCROLLER:
            if event.id == scroller1.id:
                # do something..
            ...

    scroller1.update()
```

Examples
--------
Here is a example of a basic setup (opens the window, updates the screen, and
handles events):
```py
import pygame # import the pygame
from pygameui import scroller # import the pygame scroller

# pygame setup
pygame.init()

running = True
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

pygame.display.set_caption('Scroller Test')

# just a surface test, for example is a text
font = pygame.font.SysFont(None, 60)

testsurf = font.render('Hi!', True, 'white', 'magenta')
surfx = font.render('[]', True, 'red')
surfy = font.render('[]', True, 'blue')

sx, sy = screen.get_width(), screen.get_height()

# initialization the scrollers (Do not initialization Scrollers in the game loop because this will be affected by time, events, etc)
scroller1 = scroller.Scroller(
    max_scrolled=(sx - testsurf.get_width(), sy - testsurf.get_height()),
    clock=clock,
    reversed_keyboard=True
)
scroller2 = scroller.ScrollerX(
    min_max_scrolled=(0, sx - surfx.get_width()),
    y_pos=0,
    clock=clock,
    reversed_keyboard=True
)
scroller3 = scroller.ScrollerY(
    min_max_scrolled=(0, sy - surfy.get_height()),
    x_pos=sx - surfy.get_width(),
    clock=clock, 
    reversed_keyboard=True
)

# screen loop
while running:

    # events
    for event in pygame.event.get():
        # when the user clicks the X to close the screen (pygame)
        if event.type == pygame.QUIT:
            running = False

        # handle scroller events
        scroller1.handle_event(event)
        scroller2.handle_event(event)
        scroller3.handle_event(event)

        if event.type == scroller.SCROLLER:

            if event.element == 'Scroller':
                print(f'button event property: id:{event.id}, ' +
                    f'element:{event.element}, ' +
                    f'offset:{event.offset}, ' + 
                    f'offset_x:{event.offset_x}, ' +
                    f'offset_y:{event.offset_y}, ' +
                    f'ElementEvent:({event.element_event})'
                )
 
            if event.element == 'ScrollerX':
                print(f'button event property: id:{event.id}, ' +
                    f'element:{event.element}, ' +
                    f'offset:{event.offset}, ' + 
                    f'offset_x:{event.offset_x}, ' +
                    f'ElementEvent:({event.element_event})'
                )

            if event.element == 'ScrollerY':
                print(f'button event property: id:{event.id}, ' +
                    f'element:{event.element}, ' +
                    f'offset:{event.offset}, ' + 
                    f'offset_y:{event.offset_y}, ' +
                    f'ElementEvent:({event.element_event})'
                )

    # fill screen black
    screen.fill('black')
    # update the scrollers
    scroller1.update()
    scroller2.update()
    scroller3.update()
    # displays the image with scroller offset
    scroller1.apply(screen, testsurf)
    scroller2.apply(screen, surfx)
    scroller3.apply(screen, surfy)

    # flip() the display to put your work on screen
    pygame.display.flip()
    # Set the frame-rate speed to 60 (fps)
    clock.tick(60)

# clean up pygame resources
pygame.quit()
```

Thank you to those of you who have read the documentation and code examples.
"""


from .__private.private import (
    pygame,
    typing,
    prvt as _prvt
)
from .__private.const import (
    RealNumber as _RealNumber,
    ElementID as _ElementID,
    Direction as _Direction,
    ListDirection as _ListDirection
)
from .__private.event import (
    SCROLLER,
    ElementEvent
)
from .__decorator.decorator import (
    ClassInterface
)


class Scroller(ClassInterface):

    """ Scroller - Scroller class, to handle scrolling in Pygame applicationsto handle scrolling in Pygame applications """

    def __init__(

            self,
            max_scrolled: tuple[_RealNumber, _RealNumber],
            min_scrolled: tuple[_RealNumber, _RealNumber] = (0, 0),
            id: _ElementID = None,
            clock: typing.Optional[pygame.time.Clock] = None,
            momentum: float = 0.9,
            stop_threshold: int = 500,
            mouse_scroller_speed: typing.Optional[_RealNumber] = 25,
            keyboard_speed: typing.Optional[_RealNumber] = 15,
            mouse_scroller_to: _Direction = 'y',
            keyboard_to: _Direction = 'xy',
            reversed_mouse_scroller: bool = False,
            reversed_keyboard: bool = False

        ) -> None:

        """
        Parameters:
            * `max_scrolled`: maximum scroll values (x, y)
            * `min_scrolled`: minimum scroll values (x, y)
            * `clock`: pygame clock or set the default to None to initial new Clock
            * `momentum`: momentum factor for smooth scrolling
            * `stop_threshold`: threshold to stop scrolling
            * `mouse_scroller_speed`: speed for mouse scrolling
            * `keyboard_speed`: speed for keyboard scrolling
            * `mouse_scroller_to`: direction for mouse scrolling
            * `keyboard_to`: direction for keyboard scrolling
            * `reversed_mouse_scroller`: reversed the mouse scroller offset
            * `reversed_keyboard`: reversed the keyboard offset
        """

        self.scroller_event = ElementEvent('Scroller', id)

        self.max_scrolled = max_scrolled
        self.min_scrolled = min_scrolled
        self.id = id
        self.clock = clock
        self.momentum = momentum
        self.stop_threshold = stop_threshold
        self.mouse_scroller_speed = mouse_scroller_speed
        self.keyboard_speed = keyboard_speed
        self.mouse_scroller_to = mouse_scroller_to
        self.keyboard_to = keyboard_to
        self.reversed_mouse_scroller = reversed_mouse_scroller
        self.reversed_keyboard = reversed_keyboard

        self._send_event = True

        self.__offset_x = 0
        self.__offset_y = 0
        self.__scroll_speed_x = 0
        self.__scroll_speed_y = 0
        self.__last_mouse_pos = (0, 0)
        self.__stopped_time = 0
        self.__rscrolling = False
        self.__click_detected = False
        self.__initial_anchor_drag_state = False

        if self.clock is None:
            self.clock = pygame.time.Clock()

    @property
    def max_scrolled(self) -> tuple[_RealNumber, _RealNumber]:
        return self.__max_scrolled

    @property
    def min_scrolled(self) -> tuple[_RealNumber, _RealNumber]:
        return self.__min_scrolled

    @property
    def id(self) -> _ElementID:
        return self.__id

    @property
    def clock(self) -> typing.Optional[pygame.time.Clock]:
        return self.__clock

    @property
    def momentum(self) -> float:
        return self.__momentum

    @property
    def stop_threshold(self) -> int:
        return self.__stop_threshold

    @property
    def mouse_scroller_speed(self) -> typing.Optional[_RealNumber]:
        return self.__mouse_scroller_speed

    @property
    def keyboard_speed(self) -> typing.Optional[_RealNumber]:
        return self.__keyboard_speed

    @property
    def mouse_scroller_to(self) -> _Direction:
        return self.__mouse_scroller_to

    @property
    def keyboard_to(self) -> _Direction:
        return self.__keyboard_to

    @property
    def reversed_mouse_scroller(self) -> bool:
        return self.__reversed_mouse_scroller

    @property
    def reversed_keyboard(self) -> bool:
        return self.__reversed_keyboard

    @property
    def offset_x(self) -> _RealNumber:
        return self.__offset_x

    @property
    def offset_y(self) -> _RealNumber:
        return self.__offset_y

    @max_scrolled.setter
    def max_scrolled(self, tuple_scrolled: tuple[_RealNumber, _RealNumber]) -> None:
        _prvt.asserting(isinstance(tuple_scrolled, tuple), TypeError(f'max_scrolled -> tuple_scrolled (setter): must be tuple type not {_prvt.get_type(tuple_scrolled)}'))
        _prvt.asserting(len(tuple_scrolled) == 2, ValueError(f'max_scrolled -> tuple_scrolled (setter): tuple length must be 2 arguments not {len(tuple_scrolled)}'))
        _prvt.asserting(isinstance(tuple_scrolled[0], _RealNumber) and isinstance(tuple_scrolled[1], _RealNumber), TypeError('max_scrolled -> tuple_scrolled (setter): The 2 arguments must be a RealNumber'))
        self.__max_scrolled = tuple_scrolled

    @min_scrolled.setter
    def min_scrolled(self, tuple_scrolled: tuple[_RealNumber, _RealNumber]) -> None:
        _prvt.asserting(isinstance(tuple_scrolled, tuple), TypeError(f'min_scrolled -> tuple_scrolled (setter): must be tuple type not {_prvt.get_type(tuple_scrolled)}'))
        _prvt.asserting(len(tuple_scrolled) == 2, ValueError(f'min_scrolled -> tuple_scrolled (setter): tuple length must be 2 arguments not {len(tuple_scrolled)}'))
        _prvt.asserting(isinstance(tuple_scrolled[0], _RealNumber) and isinstance(tuple_scrolled[1], _RealNumber), TypeError('min_scrolled -> tuple_scrolled (setter): The 2 arguments must be a RealNumber'))
        self.__min_scrolled = tuple_scrolled

    @id.setter
    def id(self, id: _ElementID) -> None:
        self.__id = id
        self.scroller_event.id = id

    @clock.setter
    def clock(self, clock: pygame.time.Clock) -> None:
        _prvt.asserting(isinstance(clock, pygame.time.Clock), TypeError(f'clock -> clock (setter): must be pygame.Clock type not {_prvt.get_type(clock)}'))
        self.__clock = clock

    @momentum.setter
    def momentum(self, momentum: float) -> None:
        _prvt.asserting(isinstance(momentum, float), TypeError(f'momentum -> momentum (setter): must be float type not {_prvt.get_type(momentum)}'))
        self.__momentum = momentum

    @stop_threshold.setter
    def stop_threshold(self, threshold: int) -> None:
        _prvt.asserting(isinstance(threshold, int), TypeError(f'stop_threshold -> threshold (setter): must be int type not {_prvt.get_type(threshold)}'))
        self.__stop_threshold = threshold

    @mouse_scroller_speed.setter
    def mouse_scroller_speed(self, speed: typing.Optional[_RealNumber]) -> None:
        _prvt.asserting(isinstance(speed, _RealNumber | None), TypeError(f'mouse_scroller_speed -> speed (setter): must be RealNumber or (None for no mouse scroller) type not {_prvt.get_type(speed)}'))
        self.__mouse_scroller_speed = speed

    @keyboard_speed.setter
    def keyboard_speed(self, speed: typing.Optional[_RealNumber]) -> None:
        _prvt.asserting(isinstance(speed, _RealNumber | None), TypeError(f'keyboard_speed -> speed (setter): must be RealNumber or (None for no mouse scroller) type not {_prvt.get_type(speed)}'))
        self.__keyboard_speed = speed

    @mouse_scroller_to.setter
    def mouse_scroller_to(self, direction: _Direction) -> None:
        _prvt.asserting(direction in _ListDirection, ValueError(f'mouse_scroller_to -> direction (setter): must be valid direction type not {repr(direction)}'))
        self.__mouse_scroller_to = direction

    @keyboard_to.setter
    def keyboard_to(self, direction: _Direction) -> None:
        _prvt.asserting(direction in _ListDirection, ValueError(f'keyboard_to -> direction (setter): must be valid direction type not {repr(direction)}'))
        self.__keyboard_to = direction

    @reversed_mouse_scroller.setter
    def reversed_mouse_scroller(self, reverse: bool) -> None:
        self.__reversed_mouse_scroller = bool(reverse)

    @reversed_keyboard.setter
    def reversed_keyboard(self, reverse: bool) -> None:
        self.__reversed_keyboard = bool(reverse)

    @offset_x.setter
    def offset_x(self, offset: _RealNumber) -> None:
        _prvt.asserting(isinstance(offset, _RealNumber), TypeError(f'offset_x -> offset (setter): must be RealNumber type not {_prvt.get_type(offset)}'))
        self.__offset_x = offset

    @offset_y.setter
    def offset_y(self, offset: _RealNumber) -> None:
        _prvt.asserting(isinstance(offset, _RealNumber), TypeError(f'offset_y -> offset (setter): must be RealNumber type not {_prvt.get_type(offset)}'))
        self.__offset_y = offset

    def copy(self, **kwargs) -> None:

        """
        Copy the Scroller class.

        return -> `Scroller(...)`
        """

        clonescroller = Scroller(**(self.get_param() | kwargs))

        return clonescroller

    def edit_param(self, **kwargs) -> None:

        """
        Edit parameters via the key argument of this function.

        return -> `None`
        """

        param = self.get_param()

        for attr, value in kwargs.items():
            _prvt.asserting(attr in param, TypeError(f"edit_param: **kwargs: got an unexpected keyword argument '{attr}'"))
            setattr(self, attr, value)

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        return -> `dict[str, object]`
        """

        return {
            'max_scrolled': self.__max_scrolled,
            'min_scrolled': self.__min_scrolled,
            'id': self.__id,
            'clock': self.__clock,
            'momentum': self.__momentum,
            'stop_threshold': self.__stop_threshold,
            'mouse_scroller_speed': self.__mouse_scroller_speed,
            'keyboard_speed': self.__keyboard_speed,
            'mouse_scroller_to': self.__mouse_scroller_to,
            'keyboard_to': self.__keyboard_to
        }
    
    def get_private_attr(self, remove_underscore: bool = False) -> dict[str, object]:

        """
        Get private property.

        return -> `dict[str, object]`
        """

        attr_dict = {
            '__scroll_speed_x': self.__scroll_speed_x,
            '__scroll_speed_y': self.__scroll_speed_y,
            '__last_mouse_pos': self.__last_mouse_pos,
            '__stopped_time': self.__stopped_time,
            '__rscrolling': self.__rscrolling,
            '__click_detected': self.__click_detected,
            '__initial_anchor_drag_state': self.__initial_anchor_drag_state
        }

        if remove_underscore:
            return {attr.lstrip('_'): value for attr, value in attr_dict}

        return attr_dict

    def handle_event(self, event: pygame.event.Event) -> None:

        """
        Handling mouse input via pygame events.

        return -> `None`
        """

        _prvt.asserting(isinstance(event, pygame.event.Event), TypeError(f'event: must be event.Event type not {_prvt.get_type(event)}'))

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                self.scroller_event.isdragging = True
                # it will work perfectly on Windows platform, or any other (idk in other platform)
                # but it doesn't work perfectly on pydroid3 because it might be another issue.. so i use real time method to fix it
                # using `pygame.mouse.get_pressed()[0]` - Left mouse

                # self.__initial_anchor_drag_state = self.scroller_event.isanchordrag'

                self.__last_mouse_pos = pygame.mouse.get_pos()
                self.__scroll_speed_x = 0
                self.__scroll_speed_y = 0
                self.__stopped_time = 0

            elif event.button == (5 if self.__reversed_mouse_scroller else 4) and self.mouse_scroller_speed is not None and not self.scroller_event.isanchormousescroller:
                self.scroller_event.isscrolling = True

                match self.__mouse_scroller_to:

                    case 'y':
                        self.__offset_y += self.__mouse_scroller_speed
                    case 'x':
                        self.__offset_x += self.__mouse_scroller_speed
                    case 'xy':
                        self.__offset_x += self.__mouse_scroller_speed
                        self.__offset_y += self.__mouse_scroller_speed

            elif event.button == (4 if self.__reversed_mouse_scroller else 5) and self.mouse_scroller_speed is not None and not self.scroller_event.isanchormousescroller:
                self.scroller_event.isscrolling = True

                match self.__mouse_scroller_to:

                    case 'y':
                        self.__offset_y -= self.__mouse_scroller_speed
                    case 'x':
                        self.__offset_x -= self.__mouse_scroller_speed
                    case 'xy':
                        self.__offset_x -= self.__mouse_scroller_speed
                        self.__offset_y -= self.__mouse_scroller_speed

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.scroller_event.isdragging = False
                if self.__stopped_time >= self.stop_threshold:
                    self.__scroll_speed_x = 0
                    self.__scroll_speed_y = 0

    def update(

            self,
            anchor: bool = False,
            anchor_drag: bool = False,
            anchor_mouse_scroller: bool = False,
            anchor_keyboard: bool = False

        ) -> ElementEvent:

        """
        Update the scroller.

        return -> `ElementEvent`
        """

        self.scroller_event.isanchor = anchor
        self.scroller_event.isanchordrag = anchor_drag
        self.scroller_event.isanchormousescroller = anchor_mouse_scroller
        self.scroller_event.isanchorkeyboard = anchor_keyboard

        if self.scroller_event.isanchor:
            self.scroller_event.isanchordrag = True
            self.scroller_event.isanchormousescroller = True
            self.scroller_event.isanchorkeyboard = True

        # this is a best way to fix that bug
        press_l = pygame.mouse.get_pressed()[0]

        if press_l and not self.__click_detected:
            self.__initial_anchor_drag_state = self.scroller_event.isanchordrag
            self.__click_detected = True
        elif not press_l and self.__click_detected:
            self.__click_detected = False

        if self.scroller_event.isanchordrag and self.__initial_anchor_drag_state:
            self.scroller_event.isdragging = False

        if self.scroller_event.isdragging:
            mouse_pos = pygame.mouse.get_pos()
            dx, dy = mouse_pos[0] - self.__last_mouse_pos[0], mouse_pos[1] - self.__last_mouse_pos[1]
            self.__scroll_speed_x = dx
            self.__scroll_speed_y = dy
            self.__last_mouse_pos = mouse_pos

            if dx == 0 and dy == 0:
                self.__stopped_time += self.clock.get_time()
            else:
                self.__stopped_time = 0

        else:
            self.__scroll_speed_x *= self.__momentum
            self.__scroll_speed_y *= self.__momentum

            if abs(self.__scroll_speed_x) < 0.1:
                self.__scroll_speed_x = 0
            if abs(self.__scroll_speed_y) < 0.1:
                self.__scroll_speed_y = 0

        if self.__keyboard_speed is not None and not self.scroller_event.isanchorkeyboard:

            keyboard_keys = pygame.key.get_pressed()
            self.scroller_event.iskeyscrolling = False

            if 'x' in self.__keyboard_to:

                if keyboard_keys[pygame.K_LEFT]:
                    self.__offset_x = (self.__offset_x - self.__keyboard_speed) if self.__reversed_keyboard else (self.__offset_x + self.__keyboard_speed)
                    self.scroller_event.iskeyscrolling = True
                elif keyboard_keys[pygame.K_RIGHT]:
                    self.__offset_x = (self.__offset_x + self.__keyboard_speed) if self.__reversed_keyboard else (self.__offset_x - self.__keyboard_speed)
                    self.scroller_event.iskeyscrolling = True

            if 'y' in self.__keyboard_to:

                if keyboard_keys[pygame.K_UP]:
                    self.__offset_y = (self.__offset_y - self.__keyboard_speed) if self.__reversed_keyboard else (self.__offset_y + self.__keyboard_speed)
                    self.scroller_event.iskeyscrolling = True
                elif keyboard_keys[pygame.K_DOWN]:
                    self.__offset_y = (self.__offset_y + self.__keyboard_speed) if self.__reversed_keyboard else (self.__offset_y - self.__keyboard_speed)
                    self.scroller_event.iskeyscrolling = True

        self.__offset_x += self.__scroll_speed_x
        self.__offset_y += self.__scroll_speed_y

        if self.__rscrolling:
            self.__rscrolling = False
            self.scroller_event.isscrolling = False
        elif self.scroller_event.isscrolling:
            self.__rscrolling = True

        if self.__max_scrolled[0] < self.__offset_x:
            self.__offset_x = self.__max_scrolled[0]
        elif self.__min_scrolled[0] > self.__offset_x:
            self.__offset_x = self.__min_scrolled[0]

        if self.__max_scrolled[1] < self.__offset_y:
            self.__offset_y = self.__max_scrolled[1]
        elif self.__min_scrolled[1] > self.__offset_y:
            self.__offset_y = self.__min_scrolled[1]

        self.scroller_event.offset = (self.__offset_x, self.__offset_y)

        if self._send_event:
            self.scroller_event.offset_x = self.__offset_x
            self.scroller_event.offset_y = self.__offset_y
            self.scroller_event._send_event()

        return self.scroller_event

    def get_offset(self) -> tuple[_RealNumber, _RealNumber]:

        """
        Get current offset values.

        return -> `tuple[RealNumber, RealNumber]`
        """

        return (self.__offset_x, self.__offset_y)

    def apply(self, screen_surface: pygame.Surface, surface: pygame.Surface) -> None:

        """
        Applies the offset to a surface and blits it onto the screen surface.

        return -> `None`
        """

        screen_surface.blit(surface, self.scroller_event.offset)


class ScrollerX(Scroller):

    """ ScrollerX - Scroller horizontal class, to handle horizontal scrolling in Pygame applications. """

    def __init__(

            self,
            min_max_scrolled: tuple[_RealNumber, _RealNumber],
            y_pos: _RealNumber,
            id: _ElementID = None,
            clock: typing.Optional[pygame.time.Clock] = None,
            momentum: float = 0.9,
            stop_threshold: int = 500,
            mouse_scroller_speed: typing.Optional[_RealNumber] = 25,
            keyboard_speed: typing.Optional[_RealNumber] = 15,
            reversed_mouse_scroller: bool = False,
            reversed_keyboard: bool = False

        ) -> None:

        """
        Parameters:
            * `min_max_scrolled`: minimum and maximum scroll values (x direction)
            * `y_pos`: fixed y position
            * `clock`: pygame clock or set the default to None to initial new Clock
            * `momentum`: momentum factor for smooth scrolling
            * `stop_threshold`: threshold to stop scrolling
            * `mouse_scroller_speed`: speed for mouse scrolling
            * `keyboard_speed`: speed for keyboard scrolling
            * `reversed_mouse_scroller`: reversed the mouse scroller offset
            * `reversed_keyboard`: reversed the keyboard offset
        """

        self.__min_max_scrolled = min_max_scrolled
        self.__y_pos = y_pos

        super().__init__(
            (self.min_max_scrolled[1], y_pos),
            (self.min_max_scrolled[0], y_pos),
            id,
            clock,
            momentum,
            stop_threshold,
            mouse_scroller_speed,
            keyboard_speed,
            'x',
            'x',
            reversed_mouse_scroller,
            reversed_keyboard
        )

        self.scroller_event = ElementEvent('ScrollerX', id)
        self._send_event = False

    @property
    def y_pos(self) -> _RealNumber:
        return self.__y_pos

    @property
    def min_max_scrolled(self) -> tuple[_RealNumber, _RealNumber]:
        return self.__min_max_scrolled

    @y_pos.setter
    def y_pos(self, value: _RealNumber) -> None:
        self.max_scrolled = (self.__min_max_scrolled[1], value)
        self.min_scrolled = (self.__min_max_scrolled[0], value)
        self.__y_pos = value

    @min_max_scrolled.setter
    def min_max_scrolled(self, value: tuple[_RealNumber, _RealNumber]) -> None:
        self.max_scrolled = (value[1], self.__y_pos)
        self.min_scrolled = (value[0], self.__y_pos)
        self.__min_max_scrolled = value

    def copy(self, **kwargs):

        """
        Copy the ScrollerX class.

        return -> `ScrollerX(...)`
        """

        clonescrollerx = ScrollerX(**(self.get_param() | kwargs))

        return clonescrollerx
    
    def edit_param(self, **kwargs) -> None:

        """
        Edit parameters via the key argument of this function.

        return -> `None`
        """

        param = self.get_param()

        for attr, value in kwargs.items():
            _prvt.asserting(attr in param, TypeError(f"edit_param: **kwargs: got an unexpected keyword argument '{attr}'"))
            setattr(self, attr, value)

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        return -> `dict[str, object]`
        """

        return {
            'min_max_scrolled': self.__min_max_scrolled,
            'y_pos': self.__y_pos,
            'clock': self.__clock,
            'momentum': self.__momentum,
            'stop_threshold': self.__stop_threshold,
            'mouse_scroller_speed': self.__mouse_scroller_speed,
            'keyboard_speed': self.__keyboard_speed
        }
    
    def update(

            self,
            anchor: bool = False,
            anchor_drag: bool = False,
            anchor_mouse_scroller: bool = False,
            anchor_keyboard: bool = False

        ) -> ElementEvent:

        scroller_event = super().update(anchor, anchor_drag, anchor_mouse_scroller, anchor_keyboard)

        self.scroller_event.offset_x = self.offset_x
        self.scroller_event.y_pos = self.__y_pos
        self.scroller_event._send_event()

        return scroller_event


class ScrollerY(Scroller):

    """ScrollerY - A class to handle vertical scrolling in Pygame applications."""

    def __init__(

            self,
            min_max_scrolled: tuple[_RealNumber, _RealNumber],
            x_pos: _RealNumber,
            id: _ElementID = None,
            clock: typing.Optional[pygame.time.Clock] = None,
            momentum: float = 0.9,
            stop_threshold: int = 500,
            mouse_scroller_speed: typing.Optional[_RealNumber] = 25,
            keyboard_speed: typing.Optional[_RealNumber]= 15,
            reversed_mouse_scroller: bool = False,
            reversed_keyboard: bool = False

        ) -> None:

        """
        Parameters:
            * `min_max_scrolled`: minimum and maximum scroll values (y direction)
            * `x_pos`: fixed x position
            * `clock`: pygame clock or set the default to None to initial new Clock
            * `momentum`: momentum factor for smooth scrolling
            * `stop_threshold`: threshold to stop scrolling
            * `mouse_scroller_speed`: speed for mouse scrolling
            * `keyboard_speed`: speed for keyboard scrolling
            * `reversed_mouse_scroller`: reversed the mouse scroller offset
            * `reversed_keyboard`: reversed the keyboard offset
        """

        self.__min_max_scrolled = min_max_scrolled
        self.__x_pos = x_pos

        super().__init__(
            (x_pos, self.min_max_scrolled[1]),
            (x_pos, self.min_max_scrolled[0]),
            id,
            clock,
            momentum,
            stop_threshold,
            mouse_scroller_speed,
            keyboard_speed,
            'y',
            'y',
            reversed_mouse_scroller,
            reversed_keyboard
        )

        self.scroller_event = ElementEvent('ScrollerY', id)
        self._send_event = False

    @property
    def x_pos(self) -> _RealNumber:
        return self.__x_pos

    @property
    def min_max_scrolled(self) -> tuple[_RealNumber, _RealNumber]:
        return self.__min_max_scrolled

    @x_pos.setter
    def x_pos(self, value: _RealNumber) -> None:
        self.max_scrolled = (value, self.min_max_scrolled[1])
        self.min_scrolled = (value, self.min_max_scrolled[0])
        self.__x_pos = value
    
    @min_max_scrolled.setter
    def min_max_scrolled(self, value: tuple[_RealNumber, _RealNumber]) -> None:
        self.max_scrolled = (self.__x_pos, value[1])
        self.min_scrolled = (self.__x_pos, value[0])
        self.__min_max_scrolled = value

    def copy(self, **kwargs):

        """
        Copy the ScrollerY class.

        return -> `ScrollerY(...)`
        """

        clonescrollerx = ScrollerY(**(self.get_param() | kwargs))

        return clonescrollerx

    def edit_param(self, **kwargs) -> None:

        """
        Edit parameters via the key argument of this function.

        return -> `None`
        """

        param = self.get_param()

        for attr, value in kwargs.items():
            _prvt.asserting(attr in param, TypeError(f"edit_param: **kwargs: got an unexpected keyword argument '{attr}'"))
            setattr(self, attr, value)

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        return -> `dict[str, object]`
        """

        return {
            'min_max_scrolled': self.__min_max_scrolled,
            'x_pos': self.__x_pos,
            'clock': self.__clock,
            'momentum': self.__momentum,
            'stop_threshold': self.__stop_threshold,
            'mouse_scroller_speed': self.__mouse_scroller_speed,
            'keyboard_speed': self.__keyboard_speed
        }

    def update(

            self,
            anchor: bool = False,
            anchor_drag: bool = False,
            anchor_mouse_scroller: bool = False,
            anchor_keyboard: bool = False

        ) -> ElementEvent:

        scroller_event = super().update(anchor, anchor_drag, anchor_mouse_scroller, anchor_keyboard)

        self.scroller_event.offset_y = self.offset_y
        self.scroller_event.x_pos = self.__x_pos
        self.scroller_event._send_event()

        return scroller_event


# Type buttons
ScrollerType = Scroller
ScrollerXType = ScrollerX
ScrollerYType = ScrollerY
ScrollersType = ScrollerType | ScrollerXType | ScrollerYType


__version__ = '1.0.0.beta'
__all__ = [
    'SCROLLER'
    'Scroller',
    'ScrollerX',
    'ScrollerY'
]


del (
    _ElementID,
    _Direction,
    ClassInterface,
    typing
)