import pygame
from .constants import Any, Number, Literal

class ScrollerY:

    def __init__(self, katla, min_max_scrolled: tuple[Number, Number], reversed: tuple[bool, bool, bool] = (False, False, False)) -> None:
        self.katla = katla
        self.min_max_scrolled = min_max_scrolled
        self.reversed = reversed
        self.direction = 0
        self.last_mouse_y_pos = 0
        self.scrolled = False
        self.move: Literal['+', '-'] | None = None
        self.time_momentum = self.katla.get_time()
        self.time_unscroll = self.katla.get_time()

    def reset(self) -> None:
        self.scrolled = False
        self.move = None
        self.time_momentum = self.katla.get_time()
        self.time_unscroll = self.katla.get_time()

    def _reverse(self, a: Any, b: Any, index: int) -> Any:
        return a if self.reversed[index] else b

    def edit_param(self, **kw) -> None:
        for attr, value in kw.items():
            setattr(self, attr, value)

    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == self._reverse(4, 5, 0):
                self.direction += 30 * self.katla.geomatry
                self.reset()

            elif event.button == self._reverse(5, 4, 0):
                self.direction -= 30 * self.katla.geomatry
                self.reset()

    def update(self, anchor: bool = False) -> None:

        isclickscreen = pygame.mouse.get_pressed()[0]
        getkeys       = pygame.key.get_pressed()
        mouse_y       = pygame.mouse.get_pos()[1] // 10
        speedkey      = 10 * self.katla.geomatry

        if getkeys[pygame.K_UP]:
            self.direction += self._reverse(speedkey, -speedkey, 1)
            self.reset()

        elif getkeys[pygame.K_DOWN]:
            self.direction += self._reverse(-speedkey, speedkey, 1)
            self.reset()

        gettime  = self.katla.get_time()
        momentum = 30 * self.katla.geomatry

        if mouse_y > self.last_mouse_y_pos and isclickscreen and not anchor:
            self.direction     += self._reverse(momentum, -momentum, 2)
            self.move           = self._reverse('+', '-', 2)
            self.scrolled       = True
            self.momentum       = momentum
            self.time_momentum  = gettime
            self.time_unscroll  = gettime

        elif mouse_y < self.last_mouse_y_pos and isclickscreen and not anchor:
            self.direction     += self._reverse(-momentum, momentum, 2)
            self.move           = self._reverse('-', '+', 2)
            self.scrolled       = True
            self.momentum       = momentum
            self.time_momentum  = gettime
            self.time_unscroll  = gettime

        if self.scrolled:
            if self.momentum < 0 or (isclickscreen and self.time_unscroll + 0.1 < gettime):
                self.reset()

            if self.move == '+' and self.time_momentum + 0.025 < gettime and not isclickscreen:
                self.direction    += self.momentum
                self.momentum     -= 1 * self.katla.geomatry
                self.time_momentum = gettime

            elif self.move == '-' and self.time_momentum + 0.025 < gettime and not isclickscreen:
                self.direction    -= self.momentum
                self.momentum     -= 1 * self.katla.geomatry
                self.time_momentum = gettime

        self.last_mouse_y_pos = mouse_y

        if self.direction < self.min_max_scrolled[0]:
            self.direction = self.min_max_scrolled[0]
        elif self.direction > self.min_max_scrolled[1]:
            self.direction = self.min_max_scrolled[1]