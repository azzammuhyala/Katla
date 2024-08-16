"""
MARKDOWN DOCUMENTATION

# `pygameui.vgif` / `pygamegif` module
Version: 1.0.0.beta

pygame gif surface.

Modules
-------
- `pillow` If you haven't installed it, use this command: `pip install pillow`


*next documentation will be created soon..*
"""


from .__private.private import (
    pygame,
    typing,
    prvt as _prvt
)
from .__private.const import (
    Path as _Path
)
from .__decorator.decorator import (
    ClassInterface
)
from PIL import (
    Image as _Image
)


class GIF(ClassInterface):

    """ GIF - Load a gif image and converting it to surface pygame """

    def __init__(self, gif_path: _Path, rect: pygame.Rect, frame_delay: int = 50) -> None:

        """
        Parameters:
            * `gif_path`: gift path
            * `rect`: rect gif
            * `frame_delay`: delay per frame
        """

        self.frame_delay = frame_delay

        self.__rect = rect
        self.__gif_path = gif_path
        self.__gif = _Image.open(self.gif_path)
        self.__frames: list[pygame.Surface] = []

        self.convert_gif()

        self.__last_update_time: int = pygame.time.get_ticks()
        self.__time_played: int | None = None
        self.__frame_index: int = 0

    @property
    def gif_path(self) -> _Path:
        return self.__gif_path

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @property
    def frame_delay(self) -> int:
        return self.__frame_delay
    
    @rect.setter
    def rect(self, rect: pygame.Rect) -> None:
        _prvt.asserting(isinstance(rect, pygame.Rect), TypeError(f"rect -> rect (setter): must be pygame.Rect not {_prvt.get_type(rect)}"))
        self.__rect = rect

    @frame_delay.setter
    def frame_delay(self, delay: int) -> None:
        _prvt.asserting(isinstance(delay, int), TypeError(f"frame_delay -> delay (setter): must be int not {_prvt.get_type(delay)}"))
        _prvt.asserting(delay >= 0, ValueError(f'frame_delay -> delay (setter): illegal below 0 -> {delay}'))
        self.__frame_delay = delay

    def copy(self, **kwargs) -> None:

        """
        Copy the GIF class.

        return -> `GIF(...)`
        """

        clonescroller = GIF(**(self.get_param() | kwargs))

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
            'gif_path': self.__gif_path,
            'rect': self.__rect,
            'frame_delay': self.__frame_delay
        }

    def get_private_attr(self, remove_underscore: bool = False) -> dict[str, object]:

        """
        Get private property.

        return -> `dict[str, object]`
        """

        attr_dict = {
            '__gif_path': self.__gif_path,
            '__last_update_time': self.__last_update_time,
            '__time_played': self.__time_played,
            '__frame_index': self.__frame_index
        }

        if remove_underscore:
            return {attr.lstrip('_'): value for attr, value in attr_dict}

        return attr_dict

    def get_frames(self) -> list[pygame.Surface]:

        """
        Get a list surfaces.

        return -> `list[pygame.Surface]`
        """

        return self.__frames

    def get_Image(self):

        """
        Get a gif Image class.

        return -> `Image`
        """

        return self.__gif

    def convert_gif(self) -> None:

        """
        Reads frame data to frame surface pygame.
        
        return -> `None`
        """

        self.__frames.clear()
        self.__frame_index = 0

        for frame in range(self.__gif.n_frames):
            self.__gif.seek(frame)
            frame_image = self.__gif.convert('RGBA')

            if self.rect.width <= 0 and self.rect.height <= 0:
                pass

            elif self.rect.width <= 0:
                frame_image = frame_image.resize((self.__gif.size[0], self.rect.height))

            elif self.rect.height <= 0:
                frame_image = frame_image.resize((self.rect.width, self.__gif.size[1]))

            else:
                frame_image = frame_image.resize((self.rect.width, self.rect.height))

            mode = frame_image.mode
            size = frame_image.size
            data = frame_image.tobytes()

            pygame_image = pygame.image.fromstring(data, size, mode)
            self.__frames.append(pygame_image)

    def reset_frame(self) -> None:

        """
        Reset the frame to initial settings.

        return -> `None`
        """

        self.__frame_index: int = 0
        self.__last_update_time: int = pygame.time.get_ticks()
        self.__time_played: int | None = None

    def draw_and_update(self, surface: typing.Optional[pygame.Surface]) -> pygame.Surface:

        """
        Draw or update the frame.

        return -> `pygame.Surface`
        """

        _prvt.asserting(isinstance(surface, pygame.Surface | None), TypeError('Objects are not pygame surface or (None for not draw)'))

        current_time = pygame.time.get_ticks()

        if self.__time_played is None:
            self.__time_played = current_time

        if current_time - self.__last_update_time > self.frame_delay:
            self.__frame_index = ((current_time - self.__time_played) // self.frame_delay) % len(self.__frames)
            self.__last_update_time = current_time

        frame = self.__frames[self.__frame_index]

        if surface is not None:
            surface.blit(frame, self.rect.topleft)

        return frame


__version__ = '1.0.0.beta'
__all__ = [
    'GIF'
]


del (
    _Path,
    ClassInterface,
    typing
)