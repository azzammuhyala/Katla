from .__private.private import (
    pygame,
    typing,
    prvt as _prvt
)
from .__private.const import (
    BLACK,
    GRAY,
    LIGHT_GRAY,
    WHITE,
    BLUE,
    LIGHT_BLUE,
    RealNumber as _RealNumber,
    ArgsList as _ArgsList,
    ElementID as _ElementID,
    ColorValue as _ColorValue,
    CursorValue as _CursorValue,
    ButtonEventClick as _ButtonEventClick,
)
from .__private.event import (
    BUTTON_CLICK,
    ElementEvent
)
from .__private.decorator import (
    ButtonInterface
)


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

    def copy(self) -> 'border_radius':
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
        inactive_color: typing.Optional[_ColorValue] = None,
        active_color: typing.Optional[_ColorValue] = None,
        hover_color: typing.Optional[_ColorValue] = None,

    ) -> None:

        self.inactive_color = inactive_color
        self.active_color = active_color
        self.hover_color = hover_color

        for key, value in self.get_param().items():
            _prvt.asserting(isinstance(value, _ColorValue | None), TypeError(f'{key}: must be ColorType or (None for default) not {_prvt.get_type(value)}'))

    def copy(self) -> 'button_color':
        return button_color(**self.get_param())

    def get_param(self) -> dict[str, _ColorValue | None]:
        return {
            'inactive_color': self.inactive_color,
            'active_color': self.active_color,
            'hover_color': self.hover_color
        }


class Button(ButtonInterface):

    """ Button - Push button class, creates a button function through the pygame screen and can set it with the parameters provided. """

    def __init__(

            self,
            surface_screen: pygame.Surface,
            rect: pygame.Rect,
            id: _ElementID = None,
            text: str = '',
            font: typing.Optional[pygame.font.Font] = None,
            hide: bool = False,
            alpha_transparency: int = 255,
            all_click: bool = True,
            outline_size: typing.Optional[_RealNumber] = None,
            antialias_text: bool | typing.Literal[0, 1] = True,
            image: typing.Optional[pygame.Surface] = None,
            image_scale: typing.Optional[_RealNumber | _ArgsList] = None,
            get_rect_image_kwargs: typing.Optional[dict] = None,
            get_rect_text_kwargs: typing.Optional[dict] = None,
            color: button_color = button_color(WHITE, LIGHT_GRAY, GRAY),
            text_color: button_color = button_color(BLACK, BLACK, BLACK),
            outline_color: button_color = button_color(GRAY, WHITE, LIGHT_GRAY),
            inactive_cursor: typing.Optional[_CursorValue] = None,
            active_cursor: typing.Optional[_CursorValue] = None,
            only_click: _ButtonEventClick = 'l',
            click_speed: int = 50,
            borders: border_radius = border_radius()

        ) -> None:

        """
        Parameters:
            :param `surface_screen`: screen surface, `pygame.display.set_mode((x, y))` or `pygame.Surface`.
            :param `rect`: rect button.
            :param `id`: ID Button for events.
            :param `text`: text button.
            :param `font`: font text.
            :param `hide`: hides the button but can still receive input. (Doesn't apply to text, image, outline (if not None value)).
            :param `alpha_transparency`: change alpha transparency.
            :param `all_click`: loads all clicks that occur. (Works for without event handle).
            :param `outline_size`: outline size of the button.
            :param `antialias_text`: param at `font.render(text, antialias=..., ...)`.
            :param `image`: image or icon on the button.
            :param `image_scale`: scaled the size of the image surface. (If the type is numeric, then the size will be the size of the rect button with a margin of the numbers entered. If the type is tuple[number, number], then it will follow the scale of the contents of the tuple).
            :param `get_rect_image_kwargs`: param `image.get_rect(...)`.
            :param `get_rect_text_kwargs`: param at `font.render.get_rect(...)`.
            :param `color`: button color.
            :param `text_color`: text color.
            :param `outline_color`: outline color.
            :param `inactive_cursor`: change the cursor (un-hover).
            :param `active_cursor`: change the cursor (hover).
            :param `only_click`: click response 'r' or 'c' or 'l'.
            :param `click_speed`: click speed (ms).
            :param `borders`: pygame.draw.rect borders. Use border_radius class.
        """

        self.button_event: ElementEvent = ElementEvent('Button', id)
        self.ishandlebyevent: bool = False

        self.__initialization: bool = True
        self.__font_default: bool = False

        self.surface_screen = surface_screen
        self.rect = rect
        self.id = id
        self.text = text
        self.font = font
        self.hide = hide
        self.alpha_transparency = alpha_transparency
        self.all_click = all_click
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
        self.__initial_click_state: str = ''

        self.__initialization = False

    def __copy__(self) -> 'Button':

        """
        Copy the Button class. (No kwargs). 

        Returns:
            `Button`
        """

        return self.copy()

    def __render_active_button(self, current_time: int, change_config: bool) -> None:

        """
        Private method. Render the active button.

        Parameters:
            :param `current_time`: change Button.__last_click_time to the current time.
            :param `change_config`: change the configuration.

        Returns:
            `None`
        """

        if not self.__button_outside:

            if isinstance(self.__outline_size, _RealNumber):
                outline_size = int(self.__outline_size)
                _prvt.draw_srect(
                    self.__surface_screen,
                    self.__outline_color.active_color,
                    (
                        self.__rect.left - self.__outline_size,
                        self.__rect.top - self.__outline_size,
                        self.__rect.width + self.__outline_size * 2,
                        self.__rect.height + self.__outline_size * 2
                    ),
                    self.__alpha_transparency,
                    (outline_size + 1) if self.__outline_size - outline_size > 0.1 else outline_size,
                    **self.__borders.draw_rect_kwargs
                )

            if not self.__hide:
                _prvt.draw_srect(self.__surface_screen, self.__color.active_color, self.__rect, self.__alpha_transparency, **self.__borders.draw_rect_kwargs)

            if self.__image is not None:
                self.__scaled_image.set_alpha(self.__alpha_transparency)
                if self.__get_rect_image_kwargs is None:
                    self.__surface_screen.blit(self.__scaled_image, self.__scaled_image.get_rect(center=self.__rect.center))
                else:
                    self.__surface_screen.blit(self.__scaled_image, self.__scaled_image.get_rect(**self.__get_rect_image_kwargs))

            if self.__text:
                text_surface = self.__font.render(self.__text, self.__antialias_text, self.__text_color.active_color)
                text_surface.set_alpha(self.__alpha_transparency)

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

        Parameters:
            :param `ismousehover`: get mouse hovered.

        Returns:
            `None`
        """

        if not self.__button_outside:

            if isinstance(self.__outline_size, _RealNumber):
                outline_size = int(self.__outline_size)
                _prvt.draw_srect(
                    self.__surface_screen,
                    self.__outline_color.hover_color if (self.__outline_color.hover_color is not None) and ismousehover else self.__outline_color.inactive_color,
                    (
                        self.__rect.left - self.__outline_size,
                        self.__rect.top - self.__outline_size,
                        self.__rect.width + self.__outline_size * 2,
                        self.__rect.height + self.__outline_size * 2
                    ),
                    self.__alpha_transparency,
                    (outline_size + 1) if self.__outline_size - outline_size > 0.1 else outline_size,
                    **self.__borders.draw_rect_kwargs
                )

            if not self.__hide:
                _prvt.draw_srect(
                    self.__surface_screen,
                    self.__color.hover_color if (self.__color.hover_color is not None) and ismousehover else self.__color.inactive_color,
                    self.__rect,
                    self.__alpha_transparency,
                    **self.__borders.draw_rect_kwargs
                )

            if self.__image is not None:
                self.__scaled_image.set_alpha(self.__alpha_transparency)
                if self.__get_rect_image_kwargs is None:
                    self.__surface_screen.blit(self.__scaled_image, self.__scaled_image.get_rect(center=self.__rect.center))
                else:
                    self.__surface_screen.blit(self.__scaled_image, self.__scaled_image.get_rect(**self.__get_rect_image_kwargs))

            if self.__text:
                text_surface = self.font.render(self.__text, self.__antialias_text, (self.__text_color.hover_color if (self.__text_color.hover_color is not None) and ismousehover else self.__text_color.inactive_color))
                text_surface.set_alpha(self.__alpha_transparency)

                if self.__get_rect_text_kwargs is None:
                    text_rect = text_surface.get_rect(center=self.rect.center)
                else:
                    text_rect = text_surface.get_rect(**self.__get_rect_text_kwargs)

                self.__surface_screen.blit(text_surface, text_rect)

    def __send_event(self) -> None:

        """
        Private method. Send the button event.

        Returns:
            `None`
        """

        if self._send_event:
            self.button_event._send_event()

    @property
    def surface_screen(self) -> pygame.Surface:
        return self.__surface_screen

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @property
    def id(self) -> _ElementID:
        return self.__id

    @property
    def text(self) -> str:
        return self.__text

    @property
    def font(self) -> typing.Optional[pygame.font.Font]:
        return self.__font

    @property
    def hide(self) -> bool:
        return self.__hide

    @property
    def alpha_transparency(self) -> int:
        return self.__alpha_transparency

    @property
    def all_click(self) -> bool:
        return self.__all_click

    @property
    def outline_size(self) -> typing.Optional[_RealNumber]:
        return self.__outline_size

    @property
    def antialias_text(self) -> bool | typing.Literal[0, 1]:
        return self.__antialias_text

    @property
    def image(self) -> typing.Optional[pygame.Surface]:
        return self.__image

    @property
    def image_scale(self) -> typing.Optional[_RealNumber | _ArgsList]:
        return self.__image_scale

    @property
    def get_rect_text_kwargs(self) -> typing.Optional[dict]:
        return self.__get_rect_text_kwargs

    @property
    def get_rect_image_kwargs(self) -> typing.Optional[dict]:
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
    def inactive_cursor(self) -> typing.Optional[_CursorValue]:
        return self.__inactive_cursor

    @property
    def active_cursor(self) -> typing.Optional[_CursorValue]:
        return self.__active_cursor

    @property
    def only_click(self) -> _ButtonEventClick:
        return self.__only_click

    @property
    def click_speed(self) -> int:
        return self.__click_speed

    @property
    def borders(self) -> border_radius:
        return self.__borders

    @surface_screen.setter
    def surface_screen(self, surface: pygame.Surface) -> None:
        _prvt.asserting(isinstance(surface, pygame.Surface), TypeError(f'surface_screen -> surface (setter): must be pygame.Surface not {_prvt.get_type(surface)}'))
        self.__surface_screen = surface

    @rect.setter
    def rect(self, rect: pygame.Rect) -> None:
        _prvt.asserting(isinstance(rect, pygame.Rect), TypeError(f'rect -> rect (setter): must be pygame.Rect not {_prvt.get_type(rect)}'))
        self.__rect = rect
        if not self.__initialization:
            if isinstance(self.__image_scale, _RealNumber) and self.image:
                self.scale_image()

    @id.setter
    def id(self, id: _ElementID) -> None:
        self.__id = id
        self.button_event.id = id

    @text.setter
    def text(self, text: str) -> None:
        self.__text = str(text)

    @font.setter
    def font(self, font: typing.Optional[pygame.font.Font]) -> None:
        self.__font = font
        use_font = isinstance(font, pygame.font.Font)
        if not (use_font or self.__font_default):
            self.__font = pygame.font.SysFont(None, 20)
            self.__font_default = True
        elif use_font:
            self.__font_default = False

    @hide.setter
    def hide(self, hide: bool) -> None:
        self.__hide = bool(hide)

    @alpha_transparency.setter
    def alpha_transparency(self, alpha: int) -> None:
        _prvt.asserting(isinstance(alpha, int), TypeError(f'alpha_transparency -> alpha (setter): must be int not {_prvt.get_type(alpha)}'))
        _prvt.asserting(0 <= alpha <= 255, ValueError(f'alpha_transparency -> alpha (setter): illegal below 0 and above 255 -> {alpha}'))
        self.__alpha_transparency = alpha

    @all_click.setter
    def all_click(self, boolean: bool) -> None:
        self.__all_click = bool(boolean)

    @outline_size.setter
    def outline_size(self, size: typing.Optional[_RealNumber]) -> None:
        _prvt.asserting(isinstance(size, _RealNumber | None), TypeError(f'outline_size -> size (setter): must be ArgsList or (None for no outline) not {_prvt.get_type(size)}'))
        self.__outline_size = size

    @antialias_text.setter
    def antialias_text(self, antialias: bool | typing.Literal[0, 1]) -> None: 
        self.__antialias_text = antialias

    @image.setter
    def image(self, image: typing.Optional[pygame.Surface]) -> None:
        _prvt.asserting(isinstance(image, pygame.Surface | None), TypeError(f'image -> image (setter): must be pygame.Surface or (None for no image) not {_prvt.get_type(image)}'))
        self.__image = image
        self.__scaled_image = image if isinstance(image, pygame.Surface) else None

    @image_scale.setter
    def image_scale(self, scale: typing.Optional[_RealNumber | _ArgsList]) -> None:
        _prvt.asserting(isinstance(scale, _RealNumber | _ArgsList | None), TypeError(f'image_scale -> scale (setter): must be RealNumber or ArgsList or (None for not being scaled) not {_prvt.get_type(scale)}'))
        self.__image_scale = scale
        self.scale_image()

    @get_rect_text_kwargs.setter
    def get_rect_text_kwargs(self, kwargs: typing.Optional[dict]) -> None:
        _prvt.asserting(isinstance(kwargs, dict | None), TypeError(f'get_rect_text_kwargs -> kwargs (setter): must be dict type or (None default: center) not {_prvt.get_type(kwargs)}'))
        self.__get_rect_text_kwargs = kwargs

    @get_rect_image_kwargs.setter
    def get_rect_image_kwargs(self, kwargs: typing.Optional[dict]) -> None:
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
    def inactive_cursor(self, cursor: typing.Optional[_CursorValue]) -> None:
        self.__inactive_cursor = cursor

    @active_cursor.setter
    def active_cursor(self, cursor: typing.Optional[_CursorValue]) -> None:
        self.__active_cursor = cursor

    @only_click.setter
    def only_click(self, click: _ButtonEventClick) -> None:
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

    def copy(self, **kwargs) -> 'Button':

        """
        Copy the Button class.

        Parameters:
            kwargs: in the form of a Button init parameters.

        Returns:
            `Button`
        """

        return Button(**(self.get_param() | kwargs))

    def edit_param(self, **kwargs) -> None:

        """
        Edit parameters via the key argument of this function.

        Parameters:
            kwargs: in the form of an init parameters for the button to be edited.

        Returns:
            `None`
        """

        param = self.get_param()

        for attr, value in kwargs.items():
            _prvt.asserting(attr in param, TypeError(f"edit_param: **kwargs: got an unexpected keyword argument '{attr}'"))
            setattr(self, attr, value)

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        Returns:
            `dict[str, object]`
        """

        return {
            'surface_screen': self.__surface_screen,
            'rect': self.__rect,
            'id': self.__id,
            'text': self.__text,
            'font': self.__font,
            'hide': self.__hide,
            'alpha_transparency': self.__alpha_transparency,
            'all_click': self.__all_click,
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

    def scale_image(self) -> None:

        """
        Set image size based on image_scale.

        Returns:
            `None`
        """

        if isinstance(self.__image_scale, _RealNumber | _ArgsList) and self.__image is None:
            raise ValueError('scale_image -> image_scale (property): Cannot transform scale image because image parameters have not been provided')
        elif isinstance(self.__image_scale, _RealNumber):
            self.__scaled_image = pygame.transform.scale(self.__image, (self.__rect.width - self.__image_scale, self.__rect.height - self.__image_scale))
        elif isinstance(self.__image_scale, _ArgsList):
            self.__scaled_image = pygame.transform.scale(self.__image, self.__image_scale)

    def handle_event(self, event: pygame.event.Event) -> None:

        """
        Handling input via pygame events.

        Parameters:
            :param `event`: events that occur in the pygame event loop.

        Returns:
            `None`
        """

        _prvt.asserting(isinstance(event, pygame.event.Event), TypeError(f'event: must be event.Event type not {_prvt.get_type(event)}'))

        self.ishandlebyevent = True

        if event.type == pygame.MOUSEBUTTONDOWN:

            ismousehover = self.__rect.collidepoint(pygame.mouse.get_pos())
            self.__initial_click_state = ''
            self.__clicked_button = False

            if event.button == 1 and ismousehover and 'l' in self.only_click:
                self.__initial_click_state = 'l'
                self.__clicked_button = True

            elif event.button == 2 and ismousehover and 'c' in self.only_click:
                self.__initial_click_state = 'c'
                self.__clicked_button = True

            elif event.button == 3 and ismousehover and 'r' in self.only_click:
                self.__initial_click_state = 'r'
                self.__clicked_button = True

    def draw_and_update(self) -> ElementEvent:

        """
        Draw and update button. Draw a button and then update it according to the events obtained.

        Returns:
            `ElementEvent` or via `Button.button_event`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)

        ismousehover = self.__rect.collidepoint(pygame.mouse.get_pos())

        self.button_event.click = ''
        self.button_event.ismousehover = ismousehover
        self.button_event.isbuttoninactive = not ismousehover
        self.button_event.isbuttonhover = ismousehover
        self.button_event.isbuttonactive = False
        self.button_event.cursor_active = False
        self.button_event.cursor_inactive = False

        if not self.__button_outside:
            current_time = pygame.time.get_ticks()
            get_pressed = _prvt.button_get_mouse_pressed(self.__only_click)
            any_pressed = (get_pressed[0] or get_pressed[1] or get_pressed[2])

            if self.active_cursor is not None and ismousehover:
                pygame.mouse.set_cursor(self.active_cursor)
                self.button_event.cursor_active = True
            elif self.inactive_cursor is not None:
                pygame.mouse.set_cursor(self.inactive_cursor)
                self.button_event.cursor_inactive = True

            if not ismousehover or not any_pressed and not self.__clicked_button:
                self.__render_inactive_hover_button(ismousehover)

            elif ismousehover and not self.ishandlebyevent:
                self.__render_active_button(current_time, False)

                if current_time - self.__last_click_time > self.click_speed and any_pressed:
                    clicked = ''

                    if self.__all_click:
                        if get_pressed[0]:
                            clicked += 'l'
                        if get_pressed[1]:
                            clicked += 'c'
                        if get_pressed[2]:
                            clicked += 'r'

                    else:
                        if get_pressed[0]:
                            clicked = 'l'
                        elif get_pressed[1]:
                            clicked = 'c'
                        elif get_pressed[2]:
                            clicked = 'r'

                    self.__render_active_button(current_time, True)
                    self.button_event.click = clicked
                    self.button_event.isbuttonactive = True
                    self.__send_event()

                    return self.button_event

            elif ismousehover and self.ishandlebyevent:
                self.__render_active_button(current_time, False)

                if self.__clicked_button and any_pressed:
                    return self.button_event

                elif current_time - self.__last_click_time > self.click_speed and self.__initial_click_state:
                    self.__render_active_button(current_time, True)
                    self.button_event.click = self.__initial_click_state
                    self.button_event.isbuttonactive = True
                    self.__send_event()

                    return self.button_event

                else:
                    self.__render_inactive_hover_button(ismousehover)

            if not ismousehover and self.ishandlebyevent and not any_pressed:
                self.__clicked_button = False

        return self.button_event

    def draw_inactive(self) -> None:

        """
        Render the inactive button.

        Returns:
            `None`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__clicked_button = False
        self.__render_inactive_hover_button(False)
        self.button_event._reset_property()

    def draw_hover(self) -> None:

        """
        Render the hover button.

        Returns:
            `None`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__clicked_button = False
        self.__render_inactive_hover_button(True)
        self.button_event._reset_property()

    def draw_active(self) -> None:

        """
        Render the active button.

        Returns:
            `None`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__clicked_button = False
        self.__render_active_button(0, False)
        self.button_event._reset_property()


class Range(ButtonInterface):

    """ Button Range - Push button distance class, creates a button distance function (slider button) through the pygame screen and can set it with the provided. """

    def __init__(

        self,
        surface_screen: pygame.Surface,
        rect: pygame.Rect,
        id: _ElementID = None,
        thumb_size: typing.Optional[_ArgsList] = None,
        outline_size: typing.Optional[_RealNumber] = None,
        thumb_color: button_color = button_color(WHITE, GRAY, LIGHT_GRAY),
        track_color: button_color = button_color(GRAY, WHITE, GRAY),
        track_fill_color: button_color = button_color(BLUE, BLUE, LIGHT_BLUE),
        outline_color: button_color = button_color(GRAY, WHITE, LIGHT_GRAY),
        inactive_cursor: typing.Optional[_CursorValue] = None,
        active_cursor: typing.Optional[_CursorValue] = None,
        active_cursor_outside: bool = False,
        horizontal: bool = True,
        reversed: bool = False,
        reversed_scroller_mouse: bool = False,
        drag_scroller_mouse: bool = True,
        hide_thumb: bool = False,
        hide_track: bool = False,
        hide_track_fill: bool = False,
        alpha_transparency: int = 255,
        all_click: bool = True,
        min_value: _RealNumber = 0,
        max_value: _RealNumber = 100,
        value: _RealNumber = 0,
        step: typing.Optional[_RealNumber] = 1,
        range_value_output: type[_RealNumber] = float,
        only_click: _ArgsList | _ButtonEventClick = 'l',
        click_speed: int = 50,
        borders_thumb: border_radius = border_radius(radius=100),
        borders_track: border_radius = border_radius(radius=50),
        borders_track_fill: border_radius = border_radius(radius=50),

    ) -> None:

        """
        Parameters:
            :param `surface_screen`: screen surface, `pygame.display.set_mode((x, y))` or `pygame.Surface`.
            :param `rect`: rect track (as well a rect Button).
            :param `id`: ID Range for events.
            :param `thumb_size`: thumb size (width, height) or set the default to None to not show it.
            :param `outline_size`: outline size of the range track button.
            :param `thumb_color`: thumb color.
            :param `track_color`: track color.
            :param `track_fill_color`: track fill color.
            :param `outline_color`: outline color.
            :param `inactive_cursor`: change the cursor (un-hover).
            :param `active_cursor`: change the cursor (hover).
            :param `active_cursor_outside`: the active cursor will be active if it is in the track_rect area and also outside the track_rect area when dragging.
            :param `horizontal`: makes the drag move horizontally or vertically if the value is False. (width and height of the rect adjust).
            :param `reversed`: reversed the drag in the opposite direction [(min -> max) => (max <- min)].
            :param `reversed_scroller_mouse`: reverse drag on mouse scroll.
            :param `drag_scroller_mouse`: use the mouse scroll to drag the track (Requires handle_event method).
            :param `hide_thumb`: hide thumb.
            :param `hide_track`: hide track.
            :param `hide_track_fill`: hide track fill.
            :param `alpha_transparency`: change alpha transparency.
            :param `all_click`: loads all clicks that occur. (Valid for without event handle).
            :param `min_value`: minimum value output.
            :param `max_value`: maximum value output.
            :param `value`: value output / default value.
            :param `step`: step value. None if there are no steps given.
            :param `range_value_output`: The type of numeric value output. In the form of int or float.
            :param `only_click`: click response 'r' or 'c' or 'l'.
            :param `click_speed`: click speed (ms).
            :param `borders_thumb`: pygame.draw.rect thumb borders. Use border_radius class.
            :param `borders_track`: pygame.draw.rect track borders. Use border_radius class.
            :param `borders_track_fill`: pygame.draw.rect track borders. Use border_radius class.
        """

        self.ishandlebyevent: bool = False
        self.button_event: ElementEvent = ElementEvent('Range', id)

        self.__initialization: bool = True
        self.__min_value = min_value
        self.__max_value = max_value

        self.__button_track: Button = Button(
            surface_screen = surface_screen,
            rect = rect,
            hide = hide_track,
            alpha_transparency = alpha_transparency,
            all_click = all_click,
            outline_size = outline_size,
            color = track_color,
            outline_color = outline_color,
            only_click = only_click,
            click_speed = click_speed,
            borders = borders_track
        )
        self.__button_thumb: Button = Button(
            surface_screen = surface_screen,
            rect = _prvt.init_rect.copy(),
            hide = hide_thumb,
            alpha_transparency = alpha_transparency,
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
        self.alpha_transparency = alpha_transparency
        self.all_click = all_click
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

        self.thumb_size = thumb_size

        self.button_event.rect_thumb = _prvt.init_rect.copy()
        self.button_event.rect_track_fill = _prvt.init_rect.copy()
        self.button_event.range_value = self.__value

        self.__button_track._send_event = False
        self.__button_thumb._send_event = False
        self.__button_track_fill._send_event = False

        self.__clicked_button: bool = False
        self.__detected_scroller_mouse: bool = False
        self.__button_outside: bool = False

        self.__initialization = False

        self.__set_track_and_thumb_positions()

    def __copy__(self) -> 'Range':

        """
        Copy the Range button class. (No kwargs).

        Returns:
            `Range`
        """

        return self.copy()

    def __multiple_value(self, vtype: typing.Literal['value', 'evalue'] = 'value', value = None, step = None) -> None | _RealNumber:

        """
        Private method. Look for the closest multiple value.

        Parameters:
            :param `vtype`: edited value type.
            :param `evalue`: value.
            :param `estep`: step.

        Returns:
            (`None` if `vtype=='value'`) or (`RealNumber` if `vtype=='evalue'`)
        """

        if self.__step is not None:

            match vtype:

                case 'value':
                    rest = (self.__value - self.__min_value) % self.__step
                    if rest < self.__step / 2:
                        self.button_event.range_value = self.__value = self.__range_value_output(self.__value - rest)
                    else:
                        self.button_event.range_value = self.__value = self.__range_value_output(self.__value + (self.__step - rest))

                case 'evalue':
                    rest = value % step
                    if rest < step / 2:
                        return value - rest
                    else:
                        return value + (step - rest)

    def __render_thumb_and_track_fill(self, type_draw: typing.Literal['active', 'inactive', 'hover']) -> None:

        """
        Private method. Render the thumb and track fill.

        Parameters:
            :param `type_draw`: the type of button to be rendered.

        Returns:
            `None`
        """

        if not self.__button_outside:

            if self.__use_thumb:
                self.__button_thumb.rect = self.button_event.rect_thumb
            self.__button_track_fill.rect = self.button_event.rect_track_fill

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

        Returns:
            `None`
        """

        self.__multiple_value()

        if self.__horizontal:
            if isinstance(self.__rect, pygame.Rect):
                track_fill_width = ((self.__value - self.__min_value) / (self.__max_value - self.__min_value)) * self.__rect.width
                self.button_event.rect_track_fill = pygame.Rect(
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
                self.button_event.rect_thumb = pygame.Rect(
                    self.__rect.left + self.button_event.rect_track_fill.width - self.__thumb_size[0] / 2,
                    self.__rect.top + (self.__rect.height - self.__thumb_size[1]) / 2,
                    *self.__thumb_size
                ) if not self.reversed else pygame.Rect(
                    self.button_event.rect_track_fill.left - self.__thumb_size[0] / 2,
                    self.__rect.top + (self.__rect.height - self.__thumb_size[1]) / 2,
                    *self.__thumb_size
                )

        else:
            if isinstance(self.__rect, pygame.Rect):
                track_fill_height = ((self.__value - self.__min_value) / (self.__max_value - self.__min_value)) * self.__rect.height
                self.button_event.rect_track_fill = pygame.Rect(
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
                self.button_event.rect_thumb = pygame.Rect(
                    self.__rect.left + (self.__rect.width - self.__thumb_size[0]) / 2,
                    self.__rect.top + self.button_event.rect_track_fill.height - self.__thumb_size[1] / 2,
                    *self.__thumb_size
                ) if not self.__reversed else pygame.Rect(
                    self.__rect.left + (self.__rect.width - self.__thumb_size[0]) / 2,
                    self.button_event.rect_track_fill.top - self.__thumb_size[1] / 2,
                    *self.__thumb_size
                )

    def __update(self, mouse_pos: _ArgsList, get_pressed: typing.Optional[_ArgsList]) -> ElementEvent:

        """
        Private method. Update the Range value.

        Parameters:
            :param `mouse_pos`: mouse position.
            :param `get_pressed`: mouse pressed.

        Returns:
            `ElementEvent`
        """

        if self.__horizontal:
            if mouse_pos[0] > self.__rect.right:
                relative_position = (self.__rect.right - self.__rect.left) / self.__rect.width
            elif mouse_pos[0] < self.__rect.left:
                relative_position = (self.__rect.left - self.__rect.left) / self.__rect.width
            else:
                relative_position = (mouse_pos[0] - self.__rect.left) / self.__rect.width

            self.button_event.rect_track_fill.width = relative_position * self.__rect.width
            if self.__step is not None:
                self.button_event.rect_track_fill.width = self.__multiple_value('evalue', self.button_event.rect_track_fill.width, self.__rect.width / (self.__max_value - self.__min_value))

            if self.__reversed:
                self.button_event.rect_track_fill.width = self.__rect.width - self.button_event.rect_track_fill.width
                self.button_event.rect_track_fill.left = self.__rect.right - self.button_event.rect_track_fill.width

            if self.__use_thumb:
                self.button_event.rect_thumb.left = (
                    self.__rect.right - self.button_event.rect_track_fill.width - self.button_event.rect_thumb.width / 2
                    if self.__reversed else
                    self.__rect.left + self.button_event.rect_track_fill.width - self.button_event.rect_thumb.width / 2
                )

        else:
            if mouse_pos[1] > self.__rect.bottom:
                relative_position = (self.__rect.bottom - self.__rect.top) / self.__rect.height
            elif mouse_pos[1] < self.__rect.top:
                relative_position = (self.__rect.top - self.__rect.top) / self.__rect.height
            else:
                relative_position = (mouse_pos[1] - self.__rect.top) / self.__rect.height

            self.button_event.rect_track_fill.height = relative_position * self.__rect.height
            if self.__step is not None:
                self.button_event.rect_track_fill.height = self.__multiple_value('evalue', self.button_event.rect_track_fill.height, self.__rect.height / (self.__max_value - self.__min_value))

            if self.__reversed:
                self.button_event.rect_track_fill.height = self.__rect.height - self.button_event.rect_track_fill.height
                self.button_event.rect_track_fill.top = self.__rect.bottom - self.button_event.rect_track_fill.height

            if self.__use_thumb:
                self.button_event.rect_thumb.top = (
                    self.__rect.bottom - self.button_event.rect_track_fill.height - self.button_event.rect_thumb.height / 2
                    if self.__reversed else
                    self.__rect.top + self.button_event.rect_track_fill.height - self.button_event.rect_thumb.height / 2
                )

        self.button_event.range_value = self.value = self.range_value_output(
            self.__min_value + (relative_position * (self.__max_value - self.__min_value))
            if not self.__reversed else
            self.__max_value - (relative_position * (self.__max_value - self.__min_value))
        )

        self.__multiple_value()

        if isinstance(get_pressed, _ArgsList):
            self.button_event.click = ''

            if self.__all_click:
                if get_pressed[0]:
                    self.button_event.click += 'l'
                if get_pressed[1]:
                    self.button_event.click += 'c'
                if get_pressed[2]:
                    self.button_event.click += 'r'

            else:
                if get_pressed[0]:
                    self.button_event.click = 'l'
                elif get_pressed[1]:
                    self.button_event.click = 'c'
                elif get_pressed[2]:
                    self.button_event.click = 'r'

            self.button_event._send_event()

        else:
            self.button_event.click = self.__button_track.button_event.click

        self.button_event.isdragging = True

        return self.button_event

    @property
    def surface_screen(self) -> pygame.Surface:
        return self.__surface_screen

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @property
    def id(self) -> _ElementID:
        return self.__id

    @property
    def thumb_size(self) -> typing.Optional[_ArgsList]:
        return self.__thumb_size

    @property
    def outline_size(self) -> typing.Optional[_RealNumber]:
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
    def inactive_cursor(self) -> typing.Optional[_CursorValue]:
        return self.__inactive_cursor

    @property
    def active_cursor(self) -> typing.Optional[_CursorValue]:
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
    def alpha_transparency(self) -> int:
        return self.__alpha_transparency
    
    @property
    def all_click(self) -> bool:
        return self.__all_click

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
    def step(self) -> typing.Optional[_RealNumber]:
        return self.__step

    @property
    def range_value_output(self) -> type[_RealNumber]:
        return self.__range_value_output

    @property
    def only_click(self) -> _ArgsList | _ButtonEventClick:
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
        if not self.__initialization:
            self.__set_track_and_thumb_positions()

    @id.setter
    def id(self, id: _ElementID) -> None:
        self.__id = id
        self.button_event.id = id

    @thumb_size.setter
    def thumb_size(self, size: typing.Optional[_ArgsList]) -> None:
        self.__use_thumb = isinstance(size, _ArgsList)
        self.__thumb_size = size
        if self.__use_thumb:
            _prvt.asserting(len(size) == 2, ValueError(f'thumb_size -> size (setter): ArgsList length must be 2 arguments not {len(size)}'))
            _prvt.asserting(isinstance(size[0], _RealNumber) and isinstance(size[1], _RealNumber), TypeError('thumb_size -> size (setter): The 2 arguments must be a RealNumber'))
            self.__set_track_and_thumb_positions()

    @outline_size.setter
    def outline_size(self, size: typing.Optional[_RealNumber]) -> None:
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
    def inactive_cursor(self, cursor: typing.Optional[_CursorValue]) -> None:
        self.__inactive_cursor = cursor

    @active_cursor.setter
    def active_cursor(self, cursor: typing.Optional[_CursorValue]) -> None:
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

    @alpha_transparency.setter
    def alpha_transparency(self, alpha: int) -> None:
        self.__alpha_transparency = alpha
        self.__button_track.alpha_transparency = alpha
        self.__button_thumb.alpha_transparency = alpha
        self.__button_track_fill.alpha_transparency = alpha

    @all_click.setter
    def all_click(self, boolean: bool) -> None:
        self.__all_click = bool(boolean)
        self.__button_track.all_click = boolean

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
    def step(self, value: typing.Optional[_RealNumber]) -> None:
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
    def only_click(self, click: _ArgsList | _ButtonEventClick) -> None:
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

    def copy(self, **kwargs) -> 'Range':

        """
        Copy the Range button class.

        Parameters:
            kwargs: in the form of a Range button init parameters.

        Returns:
            `Range`
        """

        return Range(**(self.get_param() | kwargs))

    def edit_param(self, **kwargs) -> None:

        """
        Edit parameters via the key argument of this function.

        Parameters:
            kwargs: in the form of an init parameters for the Range button to be edited.        

        Returns:
            `None`
        """

        param = self.get_param()

        for attr, value in kwargs.items():
            _prvt.asserting(attr in param, TypeError(f"edit_param: **kwargs: got an unexpected keyword argument '{attr}'"))
            setattr(self, attr, value)

    def get_param(self) -> dict[str, object]:

        """
        Get class parameters in the form dictionary type.

        Returns:
            `dict[str, object]`
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
            'alpha_transparency': self.__alpha_transparency,
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

    def set_value(self, value: _RealNumber) -> None:

        """
        Set the value.

        Parameters:
            :param `value`: the new range value to be changed.

        Returns:
            `None`
        """

        self.button_event.range_value = self.value = self.range_value_output(value)
        self.__set_track_and_thumb_positions()

    def handle_event(self, event: pygame.event.Event, handled_button: bool = False) -> None:

        """
        Handling input via pygame events.

        Parameters:
            :param `event`: events that occur in the pygame event loop.

        Returns:
            `None`
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
                self.button_event.click = 'sc'
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
                self.button_event.click = 'sc'
                self.button_event.isdragging = True
                self.__detected_scroller_mouse = True
                self.__set_track_and_thumb_positions()
                self.button_event._send_event()

    def draw_and_update(self) -> ElementEvent:

        """
        Draw and update Range button. Draw a range button and then update it according to the events obtained.

        Returns:
            `ElementEvent` or via `Range.button_event`
        """

        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)

        mouse_pos = pygame.mouse.get_pos()
        ismousehover = self.rect.collidepoint(*mouse_pos) or (self.button_event.rect_thumb.collidepoint(*mouse_pos) if self.__use_thumb else None)

        self.button_event.click = ''
        self.button_event.ismousehover = ismousehover
        self.button_event.israngeinactive = not ismousehover
        self.button_event.israngehover = ismousehover
        self.button_event.israngeactive = False
        self.button_event.range_value = self.value = self.range_value_output(self.value)
        self.button_event.cursor_active = False
        self.button_event.cursor_inactive = False

        if not self.__button_outside:
            get_pressed = _prvt.button_get_mouse_pressed(self.__only_click)
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

            if self.__button_track.ishandlebyevent and self.__button_track.button_event.click:
                return self.__update(mouse_pos, None)

            if any_pressed and not self.__button_track.ishandlebyevent:
                if ismousehover:
                    self.__clicked_button = True

                if self.__clicked_button:
                    self.__render_thumb_and_track_fill('active')
                    return self.__update(mouse_pos, get_pressed)

            elif not self.__button_track.ishandlebyevent:
                self.__clicked_button = False

            if self.__detected_scroller_mouse:
                self.__detected_scroller_mouse = False

        return self.button_event

    def draw_inactive(self) -> None:

        """
        Render the inactive range button.

        Returns:
            `None`
        """

        rect_thumb = self.button_event.rect_thumb
        rect_track_fill = self.button_event.rect_track_fill

        self.button_event._reset_property()

        self.button_event.rect_thumb = rect_thumb
        self.button_event.rect_track_fill = rect_track_fill
        self.button_event.range_value = self.value = self.range_value_output(self.value)

        self.__clicked_button = False
        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__button_track.draw_inactive()
        self.__render_thumb_and_track_fill('inactive')

    def draw_hover(self) -> None:

        """
        Render the hover range button.

        Returns:
            `None`
        """

        rect_thumb = self.button_event.rect_thumb
        rect_track_fill = self.button_event.rect_track_fill

        self.button_event._reset_property()

        self.button_event.rect_thumb = rect_thumb
        self.button_event.rect_track_fill = rect_track_fill
        self.button_event.range_value = self.value = self.range_value_output(self.value)

        self.__clicked_button = False
        self.__button_outside = _prvt.is_partially_outside(self.__surface_screen.get_rect(), self.__rect)
        self.__button_track.draw_hover()
        self.__render_thumb_and_track_fill('hover')

    def draw_active(self) -> None:

        """
        Render the active range button.

        Returns:
            `None`
        """

        rect_thumb = self.button_event.rect_thumb
        rect_track_fill = self.button_event.rect_track_fill

        self.button_event._reset_property()

        self.button_event.rect_thumb = rect_thumb
        self.button_event.rect_track_fill = rect_track_fill
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
        inactive_cursor: typing.Optional[_CursorValue] = None,
        active_cursor: typing.Optional[_CursorValue] = None,
        set_active_cursor_button: bool = True

    ) -> None:

    """
    Sets the cursor set_mode of the double or more button functions.

    Parameters:
        :param `buttons`: button class (already initialized).
        :param `inactive_cursor`: inactive cursor type.
        :param `active_cursor`: active cursor type.
        :param `set_active_cursor_button`: set the active type of cursor on each button.

    Returns:
        `None`
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


class Manager(ButtonInterface):

    """ Manager - Handle multiple buttons on 1 screen at once. """

    def __init__(

            self,
            *buttons: ButtonsType,
            inactive_cursor: typing.Optional[_CursorValue] = None,
            active_cursor: typing.Optional[_CursorValue] = None,
            set_active_cursor_button: bool = True

        ) -> None:

        """
        Parameters:
            :param `buttons`: Target buttons (already initialized).
            :param `inactive_cursor`: inactive cursor type.
            :param `active_cursor`: active cursor type.
            :param `set_active_cursor_button`: set the active type of cursor on each button.
        """

        _prvt.asserting(buttons, ValueError('*buttons: requires at least one positional argument'))

        for button in buttons:
            _prvt.asserting(isinstance(button, ButtonsType), TypeError(f'*buttons: most be Button or Range not {_prvt.get_type(button)}'))

        self.buttons = buttons
        self.inactive_cursor = inactive_cursor
        self.active_cursor = active_cursor
        self.set_active_cursor_button = set_active_cursor_button

    def __copy__(self) -> 'Manager':

        """
        Copy the Manager class. (No kwargs).

        Returns:
            `Manager`
        """

        return self.copy()

    def __set_all_cursor_button(self) -> None:

        """
        Private method. Sets all the cursor on the button.

        Returns:
            `None`
        """

        set_cursor_buttons(
            *self.buttons,
            inactive_cursor=self.inactive_cursor,
            active_cursor=self.active_cursor,
            set_active_cursor_button=self.set_active_cursor_button
        )

    def copy(self, *new_buttons: ButtonsType) -> 'Manager':

        """
        Copy the Manager class.

        Parameters:
            :param `new_buttons`: Load new buttons manager.

        Returns:
            `Manager`
        """

        button_list = list(self.buttons)
        button_list.extend(new_buttons)

        return Manager(
            *button_list,
            inactive_cursor = self.inactive_cursor,
            active_cursor = self.active_cursor,
            set_active_cursor_button = self.set_active_cursor_button
        )

    def edit_param(self, id: _ElementID, **kwargs) -> None:

        """
        Edit button parameters via the key argument of this function.

        Parameters:
            :param `id`: id for edit specific parameters button.
            kwargs: parameters to edited.

        Returns:
            `None`
        """

        for button in self.buttons:
            if id == button.id:
                button.edit_param(**kwargs)

    def get_param(self, id: _ElementID) -> list[dict[str, object]]:

        """
        Get class button parameters in the form dictionary type.

        Parameters:
            :param `id`: id to get specific parameters.

        Returns:
            `list[dict[str, object]]`
        """

        buttons_param = []

        for button in self.buttons:
            if id == button.id:
                buttons_param.append(button.get_param())

        return buttons_param
    
    def get_button(self, id: _ElementID) -> ButtonsType:

        """
        Get the button.

        Parameters:
            :param `id`: id to get the button target.

        Returns:
            `ButtonsType`
        """

        for button in self.buttons:
            if id == button.id:
                return button

        raise ValueError(f'id: id with {repr(id)} not found')

    def handle_event(self, event: pygame.event.Event, range_handled_button: bool = False) -> None:

        """
        Handling input via pygame events.

        Parameters:
            :param `event`: events that occur in the pygame event loop.

        Returns:
            `None`
        """

        for button in self.buttons:

            if isinstance(button, RangeType):
                button.handle_event(event, range_handled_button)

            elif isinstance(button, ButtonType):
                button.handle_event(event)

    def draw_and_update(self) -> None:

        """
        Draw, update, and set cursor buttons. Draw a button and then update it according to the events obtained.

        Returns:
            `None`
        """

        self.__set_all_cursor_button()

        for button in self.buttons:
            button.draw_and_update()

    def draw_inactive(self) -> None:

        """
        Render the inactive buttons.

        Returns:
            `None`
        """

        self.__set_all_cursor_button()

        for button in self.buttons:
            button.draw_inactive()

    def draw_hover(self) -> None:

        """
        Render the hover buttons.

        Returns:
            `None`
        """

        self.__set_all_cursor_button()

        for button in self.buttons:
            button.draw_hover()

    def draw_active(self) -> None:

        """
        Render the active buttons.

        Returns:
            `None`
        """

        self.__set_all_cursor_button()

        for button in self.buttons:
            button.draw_active()


__all__ = [
    'BUTTON_CLICK',
    'border_radius',
    'button_color',
    'Button',
    'Range',
    'set_cursor_buttons',
    'Manager'
]


del (
    BLACK,
    GRAY,
    LIGHT_GRAY,
    WHITE,
    BLUE,
    LIGHT_BLUE,
    _ElementID,
    _CursorValue,
    _ButtonEventClick,
    ButtonInterface,
    typing
)