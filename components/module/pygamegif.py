"""
GIF - pygame

req modules:
- pygame
- pillow

If you haven't installed it, use this command:
`pip install pygame pillow`
"""

import pygame
from os import PathLike as _PathLike
from warnings import warn as _warn
from PIL import Image as _Image

class GIF:

    """ GIF - Load a gif image and converting it to surface pygame """

    def __init__(self, gif_path: _PathLike[str], rect: pygame.Rect, frame_delay: int = 50) -> None:

        """
        param:
            - gif_path: gif to load
            - rect: pos and size gif
            - frame_delay: delay per frame (default: Literal[50])
        """

        self.gif_path: _PathLike[str] = gif_path
        self.rect: pygame.Rect = rect
        self.frame_delay: int = frame_delay

        self._validation()

        self.gif = _Image.open(self.gif_path)

        self._frames: list[pygame.Surface] = []

        self.convert_gif()

        self._last_update_time: int = pygame.time.get_ticks()
        self._time_played: int | None = None
        self._frame_index: int = 0

    def _validation(self) -> None:
        if isinstance(self.gif_path, str):
            if not self.gif_path.lower().endswith('.gif'):
                _warn("The gif file doesn't the '.gif' extension")

        assert isinstance(self.rect, pygame.Rect), 'rect: Objects are not pygame Rect'
        assert isinstance(self.frame_delay, int), 'frame_delay: Objects are not int'
        assert self.frame_delay >= 0, 'frame_delay: cannot be below 0'

    def convert_gif(self) -> None:

        """ Reads frame data to frame surface pygame """

        self._frames.clear()
        self._frame_index = 0

        for frame in range(self.gif.n_frames):
            self.gif.seek(frame)
            frame_image = self.gif.convert("RGBA")

            if self.rect.width <= 0 and self.rect.height <= 0:
                pass

            elif self.rect.width <= 0:
                frame_image = frame_image.resize((self.gif.size[0], self.rect.height))

            elif self.rect.height <= 0:
                frame_image = frame_image.resize((self.rect.width, self.gif.size[1]))

            else:
                frame_image = frame_image.resize((self.rect.width, self.rect.height))

            mode = frame_image.mode
            size = frame_image.size
            data = frame_image.tobytes()

            pygame_image = pygame.image.fromstring(data, size, mode)
            self._frames.append(pygame_image)

    def reset_frame(self) -> None:

        """ Reset the frame to initial settings. If you need it """

        self._frame_index: int = 0
        self._last_update_time: int = pygame.time.get_ticks()
        self._time_played: int | None = None

    def draw_and_update(self, surface: pygame.Surface | None) -> pygame.Surface:

        """
        Draw or update the frame.

        param:
            - surface: Draws the surface to the screen. If the value is None, isn't draw the image into surface

        returns:
            frame, pygame.Surface
        """

        assert isinstance(surface, pygame.Surface | None), 'Objects are not pygame surface or None (not draw)'
        self._validation()

        current_time = pygame.time.get_ticks()

        if self._time_played is None:
            self._time_played = current_time

        if current_time - self._last_update_time > self.frame_delay:
            self._frame_index = ((current_time - self._time_played) // self.frame_delay) % len(self._frames)
            self._last_update_time = current_time

        frame = self._frames[self._frame_index]

        if surface is not None:
            surface.blit(frame, self.rect.topleft)

        return frame