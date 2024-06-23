"""
AnimatedGIF - pygame

req modules:
- pygame
- pillow

`pip install pygame pillow`
"""

import pygame
from os import PathLike
from PIL import Image

class AnimatedGIF:

    def __init__(self, gif_path: PathLike[str], rect: pygame.Rect, frame_delay: int = 100) -> None:
        self.gif_path: PathLike[str] = gif_path
        self.rect: pygame.Rect = rect
        self.frame_delay: int = frame_delay
        self._frames: list[pygame.surface.Surface] = []

        self._validation()

        self.gif = Image.open(self.gif_path)

        self.convert_gif()

        self._frame_index: int = 0
        self._last_update_time: int = pygame.time.get_ticks()

    def _validation(self) -> None:
        assert isinstance(self.rect, pygame.Rect), 'rect: Objects are not pygame Rect'
        assert isinstance(self.frame_delay, int), 'frame_delay: Objects are not int'
        assert self.frame_delay > 0, 'frame_delay: cannot be below 0'

    def convert_gif(self) -> None:
        self._frames = []
        original_size = self.gif.size

        for frame in range(self.gif.n_frames):
            self.gif.seek(frame)
            frame_image = self.gif.convert("RGBA")

            if self.rect.width <= 0 and self.rect.height <= 0:
                pass

            elif self.rect.width <= 0:
                frame_image = frame_image.resize((original_size[0], self.rect.height))

            elif self.rect.height <= 0:
                frame_image = frame_image.resize((self.rect.width, original_size[1]))

            else:
                frame_image = frame_image.resize((self.rect.width, self.rect.height))

            mode = frame_image.mode
            size = frame_image.size
            data = frame_image.tobytes()

            pygame_image = pygame.image.fromstring(data, size, mode)
            self._frames.append(pygame_image)

    def reset_frame(self) -> None:
        self._frame_index: int = 0
        self._last_update_time: int = pygame.time.get_ticks()

    def draw_and_update(self, surface: pygame.surface.Surface | None) -> pygame.surface.Surface:
        assert isinstance(surface, pygame.surface.Surface | None), 'Objects are not pygame surface or None (not draw)'
        self._validation()

        current_time = pygame.time.get_ticks()

        if current_time - self._last_update_time > self.frame_delay:
            self._frame_index = (self._frame_index + 1) % len(self._frames)
            self._last_update_time = current_time

        frame = self._frames[self._frame_index]

        if surface is not None:
            surface.blit(frame, self.rect.topleft)

        return frame