"""
Katla Popup components
"""

import pygame
from . import constants as const
from ..module.pygameui.button import button_color, Button, set_cursor_buttons
from ..module.pygameui.textwrap import wrap_text
from ..module.format_number import NumberFormat

class Popup:

    def __init__(self, katla) -> None:

        self.katla = katla
        self.type = None
        self.kw = None

        self.buttonClose = Button(
            surface_screen  = self.katla.screen,
            rect            = self.katla.init_rect,
            hide            = True,
            image           = self.katla.image_close,
            image_scale     = 0,
            active_cursor   = pygame.SYSTEM_CURSOR_HAND,
            inactive_cursor = pygame.SYSTEM_CURSOR_ARROW,
            click_speed     = 0
        )
        self.buttonAction = Button(
            surface_screen = self.katla.screen,
            rect           = self.katla.init_rect,
            outline_size   = 5 * self.katla.geomatry,
            text_color     = button_color(*[self.katla.themes['popup']['text'] for _ in range(3)]),
            color          = button_color(
                self.katla.themes['popup']['button']['buy']['inactive'],
                self.katla.themes['popup']['button']['buy']['active'],
                self.katla.themes['popup']['button']['buy']['hover']
            ),
            outline_color  = button_color(*[self.katla.themes['popup']['outline'] for _ in range(3)]),
            click_speed    = 0
        )

        self.file = const.File()

        self.font_action             = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(35 * self.katla.geomatry))
        self.font_how_to_play_text   = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(19 * self.katla.geomatry))
        self.font_how_to_play_tile   = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(60 * self.katla.geomatry))
        self.font_stats_stat_text    = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(26 * self.katla.geomatry))
        self.font_title              = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,   int(27 * self.katla.geomatry))
        self.font_stats_distribution = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM, int(25 * self.katla.geomatry))
        self.font_message            = self.katla.font_notification
        self.font_daily_countdown    = self.katla.font_notification
        self.font_daily_take         = self.katla.font_notification

        self.percent_format      = NumberFormat(self.katla.languages['exponents-number'], anchor_decimal_places=True, reach=(3, 'thousand'))
        self.hours_format        = NumberFormat(self.katla.languages['exponents-number'], decimal_places=2, anchor_decimal_places=True, rounded=False, reach=(3, 'thousand'))
        self.last_game_data      = self.katla.game_data.copy()
        self.timeanimation       = self.katla.get_tick()
        self.start_time          = self.katla.get_tick()
        self.move_up_time        = self.timeanimation
        self.move_down_time      = self.start_time + 0.25
        self.index               = 0
        self.list_wrapped_text   = []
        self.clicked_ok          = False
        self.isbuy               = False
        self.isclosed            = False
        self.is_animation_up_end = False
        self.is_animation        = False

    def __call__(self) -> str | bool | None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.start_time          = self.katla.get_tick()
        self.move_up_time        = self.timeanimation
        self.move_down_time      = self.start_time + 0.25
        self.list_wrapped_text   = []
        self.clicked_ok          = False
        self.isbuy               = False
        self.isclosed            = False
        self.is_animation_up_end = False
        self.is_animation        = False

        posY = {
            'start': {
                'hint': -610 * self.katla.geomatry,
                'info': -610 * self.katla.geomatry,
                'daily-coins': -610 * self.katla.geomatry,
                'how-to-play': -680 * self.katla.geomatry,
                'stats': -(417 + (38 * self.katla.change_guess)) * self.katla.geomatry
            },
            'center': {
                'hint': 600 * self.katla.geomatry,
                'info': 600 * self.katla.geomatry,
                'daily-coins': 600 * self.katla.geomatry,
                'how-to-play': 670 * self.katla.geomatry,
                'stats': (407 + (38 * self.katla.change_guess)) * self.katla.geomatry
            }
        }

        while not self.is_animation_up_end:

            current_time = self.katla.get_tick()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.katla.running = False
                    self.is_animation_up_end = True

                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_ESCAPE:
                        self.close()

                self.katla.handle_screen_resize(event)

                self.buttonClose .handle_event(event)
                self.buttonAction.handle_event(event)

            self.katla.showFreezeKatla()

            if current_time < self.move_down_time:
                self.index = const.math.get_pos_animation(
                    pos_start    = posY['start'][self.type],
                    pos_end      = const.math.get_center(self.katla.screen.get_height(), posY['center'][self.type]),
                    time_end     = 0.25,
                    current_time = current_time,
                    start_time   = self.start_time
                )
                self.show_according_type()
                self.is_animation = True

            elif current_time < self.move_up_time and self.isclosed:
                self.index = const.math.get_pos_animation(
                    pos_start    = const.math.get_center(self.katla.screen.get_height(), posY['center'][self.type]),
                    pos_end      = posY['start'][self.type],
                    time_end     = 0.25,
                    current_time = current_time,
                    start_time   = self.start_time
                )
                self.show_according_type()
                self.is_animation = True

            else:

                if not self.is_animation_up_end and self.isclosed:
                    self.is_animation_up_end = True
                else:
                    self.is_animation = False
                    self.index        = const.math.get_center(self.katla.screen.get_height(), posY['center'][self.type])
                    self.show_according_type()

            if self.buttonClose.button_event.click:
                self.katla.handle_sound('click', 'play')
                self.close()

            elif self.buttonAction.button_event.click:
                self.katla.handle_sound('click', 'play')

                if self.type == 'hint':
                    self.isbuy = True
                    self.close()

                elif self.type in ['info', 'how-to-play', 'stats']:
                    self.clicked_ok = True
                    self.close()

                elif self.type == 'daily-coins':
                    self.kw['take_coins_function']()

            pygame.display.flip()

            self.katla.clock.tick(self.katla.fps)

        if self.type == 'hint':
            return 'buy' if self.isbuy else 'not-buy'
        elif self.type == 'info':
            return self.clicked_ok

    def edit_param(self, type: str, **kw) -> None:
        self.type = type
        self.kw   = kw

    def close(self) -> None:
        if not self.is_animation:
            self.isclosed            = True
            self.is_animation_up_end = False
            self.start_time          = self.katla.get_tick()
            self.move_up_time        = self.start_time + 0.25

    def show_according_type(self) -> None:
        match self.type:
            case 'hint':
                self.show_hint()
            case 'info':
                self.show_info()
            case 'daily-coins':
                self.show_daily_coins()
            case 'how-to-play':
                self.show_how_to_play()
            case 'stats':
                self.show_stats()

    def showTile(self, pos: tuple[const.Number, const.Number], font: pygame.font.Font, feedback: const.Feedback, size_gap_outline: tuple[const.Number, const.Number, const.Number] = (60, 8, 3)) -> None:

        for x, attempt_feedback in enumerate(feedback):
            for char, color in attempt_feedback.items():

                tile_rect = pygame.Rect(
                    pos[0] + x * (size_gap_outline[0] + size_gap_outline[1]) * self.katla.geomatry,
                    pos[1],
                    size_gap_outline[0] * self.katla.geomatry,
                    size_gap_outline[0] * self.katla.geomatry
                )

                pygame.draw.rect(self.katla.screen, self.katla.themes['boxEntryTile']['box']['outline']['point-inactive'], const.math.Rect_outline(tile_rect, size_gap_outline[2] * self.katla.geomatry))
                pygame.draw.rect(self.katla.screen, self.katla.themes['boxEntryTile']['box'][color], tile_rect)

                letter = font.render(char, True, self.katla.themes['boxEntryTile']['text'])
                self.katla.screen.blit(letter, letter.get_rect(center=tile_rect.center))

    def show_how_to_play(self) -> None:
        LANG             = self.katla.languages['popup']['how-to-play']
        tiles_top        = []
        box_rect         = pygame.Rect(const.math.get_center(self.katla.screen.get_width(), 450 * self.katla.geomatry), self.index,                              450 * self.katla.geomatry, 670 * self.katla.geomatry)
        close_rect       = pygame.Rect(box_rect.right - 40 * self.katla.geomatry - 10 * self.katla.geomatry,            box_rect.top + 10 * self.katla.geomatry, 40 * self.katla.geomatry,  40 * self.katla.geomatry)
        box_rect_outline = const.math.Rect_outline(box_rect, 6 * self.katla.geomatry)
        box_rect_shadow  = pygame.Rect(box_rect_outline.left + 15 * self.katla.geomatry, box_rect_outline.top + 15 * self.katla.geomatry, box_rect_outline.width, box_rect_outline.height)
        shadow_surface   = pygame.Surface((box_rect_shadow.width, box_rect_shadow.height))

        if not self.list_wrapped_text:
            # Save the wrapped text list to minimize lag due to the continuous wrapping process (executed once every time the popup is opened)
            self.list_wrapped_text = [
                wrap_text(self.font_title, LANG['title'], box_rect.width - 100 * self.katla.geomatry),
                wrap_text(
                    self.font_how_to_play_text,
                    LANG['label'].replace('<TILE-TOP>', '\u200b', 3)
                                 .replace('<CHANGE-GUESS>', str(self.katla.change_guess), 1),
                    box_rect.width - 10 * self.katla.geomatry
                )
            ]
            self.buttonClose.edit_param(inactive_cursor=pygame.SYSTEM_CURSOR_ARROW, active_cursor=pygame.SYSTEM_CURSOR_HAND)

        shadow_surface.fill(self.katla.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.katla.screen.blit(shadow_surface, box_rect_shadow)

        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['outline'],    box_rect_outline)
        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['background'], box_rect)

        for i, ln in enumerate(self.list_wrapped_text[0]):
            surface_text = self.font_title.render(ln, True, self.katla.themes['popup']['text'])
            self.katla.screen.blit(surface_text, (
                box_rect.left + const.math.get_center(box_rect.width, surface_text.get_width()),
                close_rect.top + const.math.get_center(close_rect.height, surface_text.get_height()) + i * surface_text.get_height()
            ))

        for i, ln in enumerate(self.list_wrapped_text[1]):
            top = self.index + 75 * self.katla.geomatry + i * surface_text.get_height()
            if ln.startswith('\u200b'):
                tiles_top.append(top)
            else:
                surface_text = self.font_how_to_play_text.render(ln, True, self.katla.themes['popup']['text'])
                self.katla.screen.blit(surface_text, (box_rect.left + 5 * self.katla.geomatry, top))

        self.showTile((box_rect.left + 5 * self.katla.geomatry, tiles_top[0]), self.font_how_to_play_tile, [{char: 'green'  if i == 0 else 'not-inputed'} for i, char in enumerate(LANG['tiles']['example-1'])])
        self.showTile((box_rect.left + 5 * self.katla.geomatry, tiles_top[1]), self.font_how_to_play_tile, [{char: 'yellow' if i == 1 else 'not-inputed'} for i, char in enumerate(LANG['tiles']['example-2'])])
        self.showTile((box_rect.left + 5 * self.katla.geomatry, tiles_top[2]), self.font_how_to_play_tile, [{char: 'red'    if i == 4 else 'not-inputed'} for i, char in enumerate(LANG['tiles']['example-3'])])

        self.buttonClose.rect = close_rect

        self.buttonClose.draw_and_update()

    def show_stats(self) -> None:
        LANG             = self.katla.languages['popup']['stats']
        box_rect         = pygame.Rect(const.math.get_center(self.katla.screen.get_width(), 500 * self.katla.geomatry), self.index,                              500 * self.katla.geomatry, (407 + (38 * self.katla.change_guess)) * self.katla.geomatry)
        close_rect       = pygame.Rect(box_rect.right - 40 * self.katla.geomatry - 10 * self.katla.geomatry,            box_rect.top + 10 * self.katla.geomatry, 40 * self.katla.geomatry,  40 * self.katla.geomatry)
        box_rect_outline = const.math.Rect_outline(box_rect, 6 * self.katla.geomatry)
        box_rect_shadow  = pygame.Rect(box_rect_outline.left + 15 * self.katla.geomatry, box_rect_outline.top + 15 * self.katla.geomatry, box_rect_outline.width, box_rect_outline.height)
        shadow_surface   = pygame.Surface((box_rect_shadow.width, box_rect_shadow.height))

        if not self.list_wrapped_text or self.last_game_data != self.katla.game_data:
            date_split = self.katla.game_data['joined-date']['date'].split('/')
            stats_label = {
                LANG['label']['joined-date']:     f'{date_split[3]}/{date_split[4]}/{date_split[5]} {date_split[0]}:{date_split[1]}',
                LANG['label']['play-time-hours']: f"{self.hours_format.parse(self.katla.game_data['play-time-seconds'] / 3600)} {LANG['label']['hours']}",
                LANG['label']['has-been-played']: self.katla.num_format.parse(self.katla.game_data['have-played']),
                LANG['label']['daily-coins']:     self.katla.num_format.parse(self.katla.game_data['prize-taken']),
                LANG['label']['hints']:           self.katla.num_format.parse(self.katla.game_data['hint']['count']) + f" [{self.katla.num_format.parse(self.katla.game_data['hint']['coins'])} {LANG['label']['coins']}]",
                LANG['label']['losses']:          self.katla.num_format.parse(self.katla.game_data['losses'])        + f" ({self.percent_format.parse(((self.katla.game_data['losses']        / self.katla.game_data['have-played']) * 100) if self.katla.game_data['have-played'] > 0 else 0)}%)",
                LANG['label']['wins']:            self.katla.num_format.parse(self.katla.game_data['wins']['total']) + f" ({self.percent_format.parse(((self.katla.game_data['wins']['total'] / self.katla.game_data['have-played']) * 100) if self.katla.game_data['have-played'] > 0 else 0)}%)",
                LANG['label']['wins-streak']:     self.katla.num_format.parse(self.katla.game_data['wins']['streak']),
                LANG['label']['max-wins-streak']: self.katla.num_format.parse(self.katla.game_data['wins']['max-streak'])
            }
            self.list_wrapped_text = [
                wrap_text(self.font_title,           LANG['title'],                   box_rect.width - 100 * self.katla.geomatry),
                wrap_text(self.font_stats_stat_text, '\n'.join(stats_label.keys()),   box_rect.width - 10 * self.katla.geomatry),
                wrap_text(self.font_stats_stat_text, '\n'.join(stats_label.values()), box_rect.width - 10 * self.katla.geomatry)
            ]
            self.buttonClose.edit_param(inactive_cursor=pygame.SYSTEM_CURSOR_ARROW, active_cursor=pygame.SYSTEM_CURSOR_HAND)
            self.last_game_data = self.katla.game_data.copy()

        shadow_surface.fill(self.katla.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.katla.screen.blit(shadow_surface, box_rect_shadow)

        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['outline'],    box_rect_outline)
        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['background'], box_rect)

        max_win = 0

        for i in range(1, self.katla.change_guess + 1):
            max_win = max(max_win, self.katla.game_data['wins'][str(i)])

        for i, ln in enumerate(self.list_wrapped_text[0]):
            surface_text = self.font_title.render(ln, True, self.katla.themes['popup']['text'])
            self.katla.screen.blit(surface_text, (
                box_rect.left + const.math.get_center(box_rect.width, surface_text.get_width()),
                close_rect.top + const.math.get_center(close_rect.height, surface_text.get_height()) + i * surface_text.get_height()
            ))

        for i, ln in enumerate(self.list_wrapped_text[1]):
            top           = self.index + 65 * self.katla.geomatry + i * surface_text.get_height()
            surface_info  = self.font_stats_stat_text.render(ln, True, self.katla.themes['popup']['text'])
            surface_stats = self.font_stats_stat_text.render(self.list_wrapped_text[2][i], True, self.katla.themes['popup']['text'])

            self.katla.screen.blit(surface_info,  (box_rect.left + 5 * self.katla.geomatry, top))
            self.katla.screen.blit(surface_stats, (box_rect.right - surface_stats.get_width() - 5 * self.katla.geomatry, top))

        surface_text = self.font_stats_stat_text.render(LANG['label']['distribution'], True, self.katla.themes['popup']['text'])

        self.katla.screen.blit(surface_text, (
            box_rect.left + const.math.get_center(box_rect.width, surface_text.get_width()),
            self.index + 330 * self.katla.geomatry + surface_text.get_height()
        ))

        for i in range(self.katla.change_guess):
            top                   = self.index + 410 * self.katla.geomatry + i * (38 * self.katla.geomatry)
            bar_distribution_w    = (self.katla.game_data['wins'][str(i + 1)] / max_win if max_win > 0 else 0) * (box_rect.width - 45 * self.katla.geomatry) if self.katla.game_data['wins']['total'] != 0 else 0
            bar_distribution_rect = pygame.Rect(box_rect.left + 5 * self.katla.geomatry + 35 * self.katla.geomatry, top + 2.5 * self.katla.geomatry, bar_distribution_w, 25 * self.katla.geomatry)

            self.showTile((box_rect.left + 5 * self.katla.geomatry, top), self.font_stats_distribution, [{str(i+1): 'not-inputed'}], size_gap_outline=(30, 8, 3))

            pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['outline' if (i + 1) != self.katla.last_win_line else 'win-bar'], bar_distribution_rect)

            surface_text = self.font_stats_stat_text.render(self.katla.num_format.parse(self.katla.game_data['wins'][str(i + 1)]), True, self.katla.themes['popup']['text'])
            self.katla.screen.blit(surface_text, (
                bar_distribution_rect.right - surface_text.get_width() - 5 * self.katla.geomatry if bar_distribution_rect.width > surface_text.get_width() + 10 * self.katla.geomatry else bar_distribution_rect.right + 5 * self.katla.geomatry,
                bar_distribution_rect.top + const.math.get_center(bar_distribution_rect.height, surface_text.get_height())
            ))

        self.buttonClose.rect = close_rect

        self.buttonClose.draw_and_update()

    def show_hint(self) -> None:
        box_rect         = pygame.Rect(const.math.get_center(self.katla.screen.get_width(), 450 * self.katla.geomatry), self.index,                                      450 * self.katla.geomatry, 600 * self.katla.geomatry)
        buttonBuy_rect   = pygame.Rect(box_rect.left + (box_rect.width - 200 * self.katla.geomatry) / 2,                box_rect.bottom - 80 * self.katla.geomatry,      200 * self.katla.geomatry, 60 * self.katla.geomatry)
        close_rect       = pygame.Rect(box_rect.right - 40 * self.katla.geomatry - 10 * self.katla.geomatry,            box_rect.top + 10 * self.katla.geomatry,         40 * self.katla.geomatry,  40 * self.katla.geomatry)
        box_rect_outline = const.math.Rect_outline(box_rect, 6 * self.katla.geomatry)
        box_rect_shadow  = pygame.Rect(box_rect_outline.left + 15 * self.katla.geomatry, box_rect_outline.top + 15 * self.katla.geomatry, box_rect_outline.width, box_rect_outline.height)
        shadow_surface   = pygame.Surface((box_rect_shadow.width, box_rect_shadow.height))

        if not self.list_wrapped_text:
            self.list_wrapped_text = [
                wrap_text(self.font_title,   self.kw['title'], box_rect.width - 100 * self.katla.geomatry),
                wrap_text(self.font_message, self.kw['label'], box_rect.width - 10 * self.katla.geomatry)
            ]

        shadow_surface.fill(self.katla.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.katla.screen.blit(shadow_surface, box_rect_shadow)

        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['outline'],    box_rect_outline)
        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['background'], box_rect)

        for i, ln in enumerate(self.list_wrapped_text[0]):
            surface_text = self.font_title.render(ln, True, self.katla.themes['popup']['text'])
            self.katla.screen.blit(surface_text, (
                box_rect.left + const.math.get_center(box_rect.width, surface_text.get_width()),
                close_rect.top + const.math.get_center(close_rect.height, surface_text.get_height()) + i * surface_text.get_height()
            ))

        for i, ln in enumerate(self.list_wrapped_text[1]):
            surface_text = self.font_message.render(ln, True, self.katla.themes['popup']['text'])
            self.katla.screen.blit(surface_text, (
                box_rect.left + const.math.get_center(box_rect.width, surface_text.get_width()),
                self.index + (box_rect.height - surface_text.get_height() * len(self.list_wrapped_text[1])) / 2 + i * surface_text.get_height()
            ))

        set_cursor_buttons(
            self.buttonClose,
            self.buttonAction,
            active_cursor   = pygame.SYSTEM_CURSOR_HAND,
            inactive_cursor = pygame.SYSTEM_CURSOR_ARROW
        )

        self.buttonClose .rect = close_rect
        self.buttonAction.rect = buttonBuy_rect
        self.buttonAction.font = self.font_action
        self.buttonAction.text = self.kw['button_label']

        self.buttonClose .draw_and_update()
        self.buttonAction.draw_and_update()

    def show_info(self) -> None:
        box_rect           = pygame.Rect(const.math.get_center(self.katla.screen.get_width(), 450 * self.katla.geomatry),  self.index,                                 450 * self.katla.geomatry, 600 * self.katla.geomatry)
        buttonAction1_rect = pygame.Rect(box_rect.left + const.math.get_center(box_rect.width, 200 * self.katla.geomatry), box_rect.bottom - 80 * self.katla.geomatry, 200 * self.katla.geomatry, 60 * self.katla.geomatry)
        close_rect         = pygame.Rect(box_rect.right - 40 * self.katla.geomatry - 10 * self.katla.geomatry,             box_rect.top + 10 * self.katla.geomatry,    40 * self.katla.geomatry,  40 * self.katla.geomatry)
        box_rect_outline   = const.math.Rect_outline(box_rect, 6 * self.katla.geomatry)
        box_rect_shadow    = pygame.Rect(box_rect_outline.left + 15 * self.katla.geomatry, box_rect_outline.top + 15 * self.katla.geomatry, box_rect_outline.width, box_rect_outline.height)
        shadow_surface     = pygame.Surface((box_rect_shadow.width, box_rect_shadow.height))

        if not self.list_wrapped_text:
            self.list_wrapped_text = [
                wrap_text(self.font_title,   self.kw['title'], box_rect.width - 100 * self.katla.geomatry),
                wrap_text(self.font_message, self.kw['label'], box_rect.width - 10 * self.katla.geomatry)
            ]

        shadow_surface.fill(self.katla.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.katla.screen.blit(shadow_surface, box_rect_shadow)

        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['outline'],    box_rect_outline)
        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['background'], box_rect)

        for i, ln in enumerate(self.list_wrapped_text[0]):
            surface_text = self.font_title.render(ln, True, self.katla.themes['popup']['text'])
            self.katla.screen.blit(surface_text, (
                box_rect.left  + const.math.get_center(box_rect.width,    surface_text.get_width()),
                close_rect.top + const.math.get_center(close_rect.height, surface_text.get_height()) + i * surface_text.get_height()
            ))

        for i, ln in enumerate(self.list_wrapped_text[1]):
            surface_text = self.font_message.render(ln, True, self.katla.themes['popup']['text'])
            self.katla.screen.blit(surface_text, (
                box_rect.left + const.math.get_center(box_rect.width, surface_text.get_width()),
                self.index + (box_rect.height - surface_text.get_height() * len(self.list_wrapped_text[1])) / 2 + i * surface_text.get_height()
            ))

        set_cursor_buttons(
            self.buttonClose,
            self.buttonAction,
            active_cursor   = pygame.SYSTEM_CURSOR_HAND,
            inactive_cursor = pygame.SYSTEM_CURSOR_ARROW
        )

        self.buttonClose .rect = close_rect
        self.buttonAction.rect = buttonAction1_rect
        self.buttonAction.font = self.font_action
        self.buttonAction.text = self.kw['button_ok']

        self.buttonClose .draw_and_update()
        self.buttonAction.draw_and_update()

    def show_daily_coins(self) -> None:
        LANG                 = self.katla.languages['popup']['daily-coins']
        box_rect             = pygame.Rect(const.math.get_center(self.katla.screen.get_width(), 450 * self.katla.geomatry),  self.index,                                  450 * self.katla.geomatry,                       600 * self.katla.geomatry)
        box_coin_rect        = pygame.Rect(box_rect.left + const.math.get_center(box_rect.width, 400 * self.katla.geomatry), box_rect.bottom - 175 * self.katla.geomatry, 400 * self.katla.geomatry,                       150 * self.katla.geomatry)
        buttonTakeDaily_rect = pygame.Rect(box_coin_rect.left + const.math.get_center(box_coin_rect.width,                   200 * self.katla.geomatry),                  box_coin_rect.bottom - 60 * self.katla.geomatry, box_coin_rect.width - 200 * self.katla.geomatry, 50 * self.katla.geomatry)
        close_rect           = pygame.Rect(box_rect.right - 40 * self.katla.geomatry - 10 * self.katla.geomatry,             box_rect.top + 10 * self.katla.geomatry,     40 * self.katla.geomatry,                        40 * self.katla.geomatry)
        box_rect_outline     = const.math.Rect_outline(box_rect, 6 * self.katla.geomatry)
        box_rect_shadow      = pygame.Rect(box_rect_outline.left + 15 * self.katla.geomatry, box_rect_outline.top + 15 * self.katla.geomatry, box_rect_outline.width, box_rect_outline.height)
        shadow_surface       = pygame.Surface((box_rect_shadow.width, box_rect_shadow.height))

        if not self.list_wrapped_text:
            self.list_wrapped_text = [
                wrap_text(self.font_title, LANG['title'], box_rect.width - 100 * self.katla.geomatry),
                wrap_text(
                    self.font_message,
                    LANG['label'].replace('<DAILY-COINS>', str(const.DAILY_COINS), 1)
                                 .replace('<HOURS>', '24', 1)
                                 .replace('<COINS-REWAND>',  '1 / 2', 1),
                    box_rect.width - 10 * self.katla.geomatry
                )
            ]

        shadow_surface.fill(self.katla.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.katla.screen.blit(shadow_surface, box_rect_shadow)

        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['outline'],    box_rect_outline)
        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['background'], box_rect)
        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['outline'],    const.math.Rect_outline(box_coin_rect, 6 * self.katla.geomatry))
        pygame.draw.rect(self.katla.screen, self.katla.themes['popup']['background'], box_coin_rect)

        for i, ln in enumerate(self.list_wrapped_text[0]):
            surface_text = self.font_title.render(ln, True, self.katla.themes['popup']['text'])
            self.katla.screen.blit(surface_text, (
                box_rect.left + const.math.get_center(box_rect.width, surface_text.get_width()),
                close_rect.top + const.math.get_center(close_rect.height, surface_text.get_height()) + i * surface_text.get_height()
            ))

        for i, ln in enumerate(self.list_wrapped_text[1]):
            surface_text = self.font_message.render(ln, True, self.katla.themes['popup']['text'])
            self.katla.screen.blit(surface_text, (
                box_rect.left + const.math.get_center(box_rect.width, surface_text.get_width()),
                self.index + (box_rect.height - surface_text.get_height() * len(self.list_wrapped_text[1])) / 2 + i * surface_text.get_height()
            ))

        text = self.katla.get_daily_countdown()

        surface_coins = self.font_daily_countdown.render(
            LANG['coin-label']['coins'].replace('<DAILY-COINS>', str(const.DAILY_COINS), 1) if text is True else LANG['coin-label']['count-down'].replace('<COUNT-DOWN>', text, 1),
            True, self.katla.themes['popup']['text']
        )

        set_cursor_buttons(
            self.buttonClose,
            self.buttonAction,
            inactive_cursor          = pygame.SYSTEM_CURSOR_ARROW,
            set_active_cursor_button = False
        )

        self.buttonClose .rect          = close_rect
        self.buttonAction.rect          = buttonTakeDaily_rect
        self.buttonAction.font          = self.font_daily_take
        self.buttonAction.text          = LANG['button-take']
        self.buttonAction.active_cursor = pygame.SYSTEM_CURSOR_HAND

        self.buttonClose .draw_and_update()

        if text is True:
            self.buttonAction.draw_and_update()
        else:
            self.buttonAction.draw_inactive()
            self.buttonAction.button_event.ismousehover = buttonTakeDaily_rect.collidepoint(pygame.mouse.get_pos())

        case_button = self.buttonAction.button_event.ismousehover and text is not True

        if case_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

        self.katla.screen.blit(surface_coins, (
            box_coin_rect.left + const.math.get_center(box_coin_rect.width, surface_coins.get_width()),
            box_coin_rect.top + const.math.get_center(box_coin_rect.height-buttonTakeDaily_rect.height-(box_coin_rect.bottom-buttonTakeDaily_rect.bottom), surface_coins.get_height())
        ))

class Notification:

    def __init__(self, katla: const.Any) -> None:

        self.katla = katla
        self.move_down_time = .25
        self.move_up_time = .25
        self.text: str = ''
        self.ntype: const.Literal['default', 'win', 'lose'] = 'default'
        self.height_font = self.katla.font_notification.size(const.HELLO)[1]
        self.static_time = 3
        self.box_rect = None
        self.wrap_message = None
        self.t = False
        self.timeanimation = self.katla.get_tick()

    def __call__(self) -> str | None:
        if not self.t:
            self.wrap_message = wrap_text(self.katla.font_notification, self.text, self.katla.screen.get_width() - 25 * self.katla.geomatry)
            self.t = True

        current_time   = self.katla.get_tick()
        move_down_time = self.timeanimation + self.move_down_time
        static_time    = move_down_time + self.static_time
        move_up_time   = static_time + self.move_up_time
        pos_start      = -(self.height_font * len(self.wrap_message) + 12 * self.katla.geomatry)
        pos_end        = 130 * self.katla.geomatry

        if current_time < move_down_time:
            self.box(const.math.get_pos_animation(
                pos_start    = pos_start,
                pos_end      = pos_end,
                time_end     = self.move_down_time,
                current_time = current_time,
                start_time   = self.timeanimation
            ))

        elif current_time < static_time:
            self.box(pos_end)

        elif current_time < move_up_time:
            self.box(const.math.get_pos_animation(
                pos_end      = pos_start,
                pos_start    = pos_end,
                time_end     = self.move_up_time,
                current_time = current_time,
                start_time   = static_time
            ))

        else:
            self.t = False
            return 'END'

    def box(self, index: const.Number) -> None:
        self.box_rect = pygame.Rect(
            const.math.get_center(self.katla.screen.get_width(), self.katla.screen.get_width() - 20 * self.katla.geomatry),
            index,
            self.katla.screen.get_width() - 20 * self.katla.geomatry,
            50 * self.katla.geomatry
        )

        self.wrap_message = wrap_text(self.katla.font_notification, self.text, self.box_rect.width - 5 * self.katla.geomatry)

        if (lencontent := len(self.wrap_message)) > 1:
            self.box_rect.height = self.height_font * lencontent + 12.5 * self.katla.geomatry

        pygame.draw.rect(self.katla.screen, self.katla.themes['notification'][self.ntype]['outline'], const.math.Rect_outline(self.box_rect, 6 * self.katla.geomatry))
        pygame.draw.rect(self.katla.screen, self.katla.themes['notification'][self.ntype]['background'], self.box_rect)

        for i, ln in enumerate(self.wrap_message):
            surface_text = self.katla.font_notification.render(ln, True, self.katla.themes['notification'][self.ntype]['text'])
            self.katla.screen.blit(surface_text, surface_text.get_rect(center=(self.box_rect.centerx, self.box_rect.top + 25 * self.katla.geomatry + i * surface_text.get_height())))