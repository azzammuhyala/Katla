
# This module is in the development process

import pygame

RealNumber = int | float

class ScrollerY:

    def __init__(
            
        self,
        max_scroll: RealNumber | None = None,
        min_scroll: RealNumber | None = None,
        scroll_step: RealNumber = 1

        ) -> None:

        self.max_scroll = max_scroll
        self.min_scroll = min_scroll
        self.scroll_step = scroll_step

        self.pos = 0
        self._last_mouse_y_pos = 0
        self._scroll_momentum_attr = {
            'scrolled': False,
            'move': None,
            'momentum': 0,
            'time-momentum': pygame.time.get_ticks(),
            'time-unscroll': pygame.time.get_ticks()
        }

    def _reset_momentum(self) -> None:
        self._scroll_momentum_attr = {
            'scrolled': False,
            'move': None,
            'momentum': 0,
            'time-momentum': pygame.time.get_ticks(),
            'time-unscroll': pygame.time.get_ticks()
        }

    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.pos += self.scroll_step
                self._reset_momentum()
            elif event.button == 5:
                self.pos -= self.scroll_step
                self._reset_momentum()

    def update(self) -> None:
        mouse_pos         = pygame.mouse.get_pos()
        isclickscreen     = pygame.mouse.get_pressed()[0]
        gettime           = pygame.time.get_ticks()
        getkeys           = pygame.key.get_pressed()
        mouse_direction_y = mouse_pos[1]

        if getkeys[pygame.K_UP]:
            self.pos += self.scroll_step
            self._reset_momentum()
        elif getkeys[pygame.K_DOWN]:
            self.pos -= self.scroll_step
            self._reset_momentum()

        if mouse_direction_y > self._last_mouse_y_pos and isclickscreen:
            self.pos += self.scroll_step
            self._scroll_momentum_attr['scrolled'] = True
            self._scroll_momentum_attr['move'] = '+'
            self._scroll_momentum_attr['momentum'] = self.scroll_step
            self._scroll_momentum_attr['time-momentum'] = gettime
            self._scroll_momentum_attr['time-unscroll'] = gettime

        elif mouse_direction_y < self._last_mouse_y_pos and isclickscreen:
            self.pos -= self.scroll_step
            self._scroll_momentum_attr['scrolled'] = True
            self._scroll_momentum_attr['move'] = '-'
            self._scroll_momentum_attr['momentum'] = self.scroll_step
            self._scroll_momentum_attr['time-momentum'] = gettime
            self._scroll_momentum_attr['time-unscroll'] = gettime

        if self._scroll_momentum_attr['scrolled']:
            if self._scroll_momentum_attr['momentum'] < 0 or (isclickscreen and self._scroll_momentum_attr['time-unscroll'] + 10 < gettime):
                self._reset_momentum()

            if self._scroll_momentum_attr['move'] == '+' and self._scroll_momentum_attr['time-momentum'] + 25 < gettime and not isclickscreen:
                self.pos += self._scroll_momentum_attr['momentum']
                self._scroll_momentum_attr['momentum']     -= 1
                self._scroll_momentum_attr['time-momentum'] = gettime

            elif self._scroll_momentum_attr['move'] == '-' and self._scroll_momentum_attr['time-momentum'] + 25 < gettime and not isclickscreen:
                self.pos -= self._scroll_momentum_attr['momentum']
                self._scroll_momentum_attr['momentum']      -= 1
                self._scroll_momentum_attr['time-momentum'] = gettime

        self._last_mouse_y_pos = mouse_direction_y

        if self.pos < self.min_scroll:
            self.pos = self.min_scroll
        elif self.pos > self.max_scroll:
            self.pos = self.max_scroll

if __name__ == '__main__':

    def test():

        pygame.init()

        screen = pygame.display.set_mode((700, 700))
        font = pygame.font.SysFont(None, 30)
        clock = pygame.time.Clock()
        scroller = ScrollerY(screen.get_height() - font.size('jg - Test')[1], 0, 20)
        running = True

        pygame.display.set_caption('Test Scrolling')

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                scroller.event(event)

            scroller.update()

            txt = font.render('Hello World!', True, 'white')

            screen.fill('black')

            screen.blit(txt, ((screen.get_width() - txt.get_width()) / 2, scroller.pos))

            pygame.display.flip()

            clock.tick(120)

        pygame.quit()
        quit()

    test()
    del test