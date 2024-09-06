"""
Katla Popup components
"""

import pygame
from typing import TYPE_CHECKING

import pygame.ftfont
from . import constants as const
from ..module.pygameui.button import button_color, Button, set_cursor_buttons
from ..module.pygameui.textwrap import wrap_text, render_wrap
from ..module.format_number import NumberFormat

if TYPE_CHECKING:
    # This block will only be executed during `Development Time`.
    # This block is only needed for type checking.
    from ...Katla import Katla
    katla = Katla
else:
    # This block will only be executed at `Run Time` (Running code).
    # This block becomes a block of any type. Python doesn't care about the data type given.
    katla = const.Any

class Popup:

    def __init__(self, app: katla) -> None:
        self.app = app
        self.type = None
        self.kw = None

        self.buttonClose = Button(
            surface_screen  = self.app.screen,
            rect            = self.app.init_rect,
            hide            = True,
            image           = self.app.image_close,
            image_scale     = 0,
            active_cursor   = pygame.SYSTEM_CURSOR_HAND,
            inactive_cursor = pygame.SYSTEM_CURSOR_ARROW,
            click_speed     = 0
        )
        self.buttonAction = Button(
            surface_screen = self.app.screen,
            rect           = self.app.init_rect,
            outline_size   = 5 * self.app.geomatry,
            text_color     = self.app.single_color_button(self.app.themes['popup']['text']),
            color          = button_color(
                self.app.themes['popup']['button']['buy']['inactive'],
                self.app.themes['popup']['button']['buy']['active'],
                self.app.themes['popup']['button']['buy']['hover']
            ),
            outline_color  = self.app.single_color_button(self.app.themes['popup']['outline']),
            click_speed    = 0
        )

        self.file = const.File()

        self.font_action             = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(35 * self.app.geomatry))
        self.font_how_to_play_text   = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(19 * self.app.geomatry))
        self.font_how_to_play_tile   = pygame.font.Font(self.file.FONT_BAKSOSAPI_REGULAR, int(60 * self.app.geomatry))
        self.font_stats_stat_text    = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(26 * self.app.geomatry))
        self.font_title              = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,       int(27 * self.app.geomatry))
        self.font_stats_distribution = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(25 * self.app.geomatry))
        self.font_message            = self.app.font_notification
        self.font_daily_countdown    = self.app.font_notification
        self.font_daily_take         = self.app.font_notification

        self.sizefont_title            = self.font_title           .size(const.HELLO)
        self.sizefont_how_to_play_text = self.font_how_to_play_text.size(const.HELLO)

        self.animation_start_time = 0
        self.slide_in_duration    = 0.3
        self.slide_out_duration   = 0.3
        self.slide_in_time        = 0
        self.slide_out_time       = 0
        self.y_pos                = 0
        self.percent_format       = NumberFormat(self.app.languages['exponents-number'], anchor_decimal_places=True, reach=(3, 'thousand'))
        self.hours_format         = NumberFormat(self.app.languages['exponents-number'], decimal_places=2, anchor_decimal_places=True, rounded=False, reach=(3, 'thousand'))
        self.last_game_data       = self.app.game_data.copy()
        self.list_wrapped_text    = []
        self.clicked_ok           = False
        self.isbuy                = False
        self.isclosed             = False
        self.is_animation_up_end  = False
        self.is_animation         = False

    def __call__(self) -> str | bool | None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.animation_start_time = self.app.get_tick()
        self.slide_in_time        = self.animation_start_time + self.slide_in_duration
        self.list_wrapped_text    = []
        self.clicked_ok           = False
        self.isbuy                = False
        self.isclosed             = False
        self.is_animation_up_end  = False
        self.is_animation         = False
        popup_height              = 0
        
        if self.type == 'how-to-play':
            popup_height = self.show_how_to_play(get_height=True)

        posY = {
            'start': {
                'hint':        -610 * self.app.geomatry,
                'info':        -610 * self.app.geomatry,
                'daily-coins': -610 * self.app.geomatry,
                'how-to-play': -(popup_height + 10 * self.app.geomatry),
                'stats':       -(417 + (38 * self.app.change_guess)) * self.app.geomatry
            },
            'height': {
                'hint':        600 * self.app.geomatry,
                'info':        600 * self.app.geomatry,
                'daily-coins': 600 * self.app.geomatry,
                'how-to-play': popup_height,
                'stats':       (407 + (38 * self.app.change_guess)) * self.app.geomatry
            }
        }

        while not self.is_animation_up_end:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.app.running = False
                    self.is_animation_up_end = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()

                self.app.handle_screen_resize(event)

                self.buttonClose .handle_event(event)
                self.buttonAction.handle_event(event)

            self.app.showFreezeKatla()

            current_time = self.app.get_tick()

            pos_start = posY['start'][self.type]
            pos_end   = const.math.get_center(self.app.screen.get_height(), posY['height'][self.type])

            if current_time < self.slide_in_time:
                self.y_pos = const.math.get_pos_animation(
                    pos_start    = pos_start,
                    pos_end      = pos_end,
                    time_end     = self.slide_in_duration,
                    current_time = current_time,
                    start_time   = self.animation_start_time
                )
                self.show_according_type()
                self.is_animation = True

            elif current_time < self.slide_out_time and self.isclosed:
                self.y_pos = const.math.get_pos_animation(
                    pos_start    = pos_end,
                    pos_end      = pos_start,
                    time_end     = self.slide_out_duration,
                    current_time = current_time,
                    start_time   = self.animation_start_time
                )
                self.show_according_type()
                self.is_animation = True

            else:
                if not self.is_animation_up_end and self.isclosed:
                    self.is_animation_up_end = True
                else:
                    self.is_animation = False
                    self.y_pos        = pos_end
                    self.show_according_type()

            if self.buttonClose.button_event.click:
                self.app.handle_sound('click', 'play')
                self.close()

            elif self.buttonAction.button_event.click:
                self.app.handle_sound('click', 'play')

                if self.type == 'hint':
                    self.isbuy = True
                    self.close()

                elif self.type in ['info', 'how-to-play', 'stats']:
                    self.clicked_ok = True
                    self.close()

                elif self.type == 'daily-coins':
                    self.kw['take_coins_function']()

            pygame.display.flip()

            self.app.clock.tick(self.app.fps)

        if self.type == 'hint':
            return 'buy' if self.isbuy else 'not-buy'

        elif self.type == 'info':
            return self.clicked_ok

    def refresh(self) -> None:
        self.buttonClose = Button(
            surface_screen  = self.app.screen,
            rect            = self.app.init_rect,
            hide            = True,
            image           = self.app.image_close,
            image_scale     = 0,
            active_cursor   = pygame.SYSTEM_CURSOR_HAND,
            inactive_cursor = pygame.SYSTEM_CURSOR_ARROW,
            click_speed     = 0
        )
        self.buttonAction = Button(
            surface_screen = self.app.screen,
            rect           = self.app.init_rect,
            outline_size   = 5 * self.app.geomatry,
            text_color     = self.app.single_color_button(self.app.themes['popup']['text']),
            color          = button_color(
                self.app.themes['popup']['button']['buy']['inactive'],
                self.app.themes['popup']['button']['buy']['active'],
                self.app.themes['popup']['button']['buy']['hover']
            ),
            outline_color  = self.app.single_color_button(self.app.themes['popup']['outline']),
            click_speed    = 0
        )

        self.font_action             = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(35 * self.app.geomatry))
        self.font_how_to_play_text   = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(19 * self.app.geomatry))
        self.font_how_to_play_tile   = pygame.font.Font(self.file.FONT_BAKSOSAPI_REGULAR, int(60 * self.app.geomatry))
        self.font_stats_stat_text    = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(26 * self.app.geomatry))
        self.font_title              = pygame.font.Font(self.file.FONT_ROBOTO_BOLD,       int(27 * self.app.geomatry))
        self.font_stats_distribution = pygame.font.Font(self.file.FONT_ROBOTO_MEDIUM,     int(25 * self.app.geomatry))
        self.font_message            = self.app.font_notification
        self.font_daily_countdown    = self.app.font_notification
        self.font_daily_take         = self.app.font_notification

        self.sizefont_title            = self.font_title           .size(const.HELLO)
        self.sizefont_how_to_play_text = self.font_how_to_play_text.size(const.HELLO)

        self.percent_format = NumberFormat(self.app.languages['exponents-number'], anchor_decimal_places=True, reach=(3, 'thousand'))
        self.hours_format   = NumberFormat(self.app.languages['exponents-number'], decimal_places=2, anchor_decimal_places=True, rounded=False, reach=(3, 'thousand'))
        self.last_game_data = self.app.game_data.copy()

    def edit_param(self, type: const.Literal['hint', 'info', 'daily-coins', 'how-to-play', 'stats'], **kw) -> None:
        self.type = type
        self.kw   = kw

    def close(self) -> None:
        if not self.is_animation:
            self.isclosed             = True
            self.is_animation_up_end  = False
            self.animation_start_time = self.app.get_tick()
            self.slide_out_time       = self.animation_start_time + self.slide_out_duration

    def showTile(self, pos: tuple[const.Number, const.Number], font: pygame.font.Font, feedback: const.Feedback, size_gap_outline: tuple[const.Number, const.Number, const.Number] = (60, 8, 3)) -> None:
        for x, attempt_feedback in enumerate(feedback):
            for char, color in attempt_feedback.items():

                tile_rect = pygame.Rect(
                    pos[0] + x * (size_gap_outline[0] + size_gap_outline[1]) * self.app.geomatry,
                    pos[1],
                    size_gap_outline[0] * self.app.geomatry,
                    size_gap_outline[0] * self.app.geomatry
                )

                pygame.draw.rect(self.app.screen, self.app.themes['tile']['box']['outline']['point-inactive'], const.math.Rect_outline(tile_rect, size_gap_outline[2] * self.app.geomatry))
                pygame.draw.rect(self.app.screen, self.app.themes['tile']['box'][color],                       tile_rect)

                letter = font.render(char, True, self.app.themes['tile']['text'])
                self.app.screen.blit(letter, letter.get_rect(center=tile_rect.center))

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

    def show_how_to_play(self, get_height: bool = False) -> const.Number | None:
        LANG = self.app.languages['popup']['how-to-play']

        popup_rect_width = 450 * self.app.geomatry

        if not self.list_wrapped_text:
            # Save the wrapped text list to minimize lag due to the continuous wrapping process (executed once every time the popup is opened)
            self.list_wrapped_text = [
                render_wrap(
                    font       = self.font_title,
                    text       = LANG['title'],
                    wraplength = popup_rect_width - 100 * self.app.geomatry,
                    antialias  = True,
                    color      = self.app.themes['popup']['text'],
                    wrap_type  = 'center'
                ),
                wrap_text(
                    font       = self.font_how_to_play_text,
                    text       = LANG['label'].replace('<TILE-TOP>',     '\u200b',                   3)
                                              .replace('<CHANGE-GUESS>', str(self.app.change_guess), 1),
                    wraplength = popup_rect_width - 10 * self.app.geomatry,
                )
            ]
            self.buttonClose.edit_param(
                inactive_cursor = pygame.SYSTEM_CURSOR_ARROW,
                active_cursor   = pygame.SYSTEM_CURSOR_HAND
            )

        tiles_pos_y = []

        title_surf = self.list_wrapped_text[0]
        label_surf = self.list_wrapped_text[1]

        popup_rect         = pygame.Rect(const.math.get_center(self.app.screen.get_width(), popup_rect_width), self.y_pos,                              popup_rect_width,       len(label_surf) * self.sizefont_how_to_play_text[1] + 90 * self.app.geomatry)
        popup_rect_outline = const.math.Rect_outline(popup_rect, 6 * self.app.geomatry)
        close_rect         = pygame.Rect(popup_rect.right - 40 * self.app.geomatry - 10 * self.app.geomatry,   popup_rect.top + 10 * self.app.geomatry, 40 * self.app.geomatry, 40 * self.app.geomatry)
        shadow_surface     = pygame.Surface((popup_rect_outline.width, popup_rect_outline.height))

        if get_height:
            return popup_rect.height

        shadow_surface.fill(self.app.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.app.screen.blit(shadow_surface, (
            popup_rect_outline.left + 15 * self.app.geomatry,
            popup_rect_outline.top + 15 * self.app.geomatry
        ))

        pygame.draw.rect(self.app.screen, self.app.themes['popup']['outline'],    popup_rect_outline)
        pygame.draw.rect(self.app.screen, self.app.themes['popup']['background'], popup_rect)

        self.app.screen.blit(title_surf, (
            popup_rect.left + const.math.get_center(popup_rect.width, title_surf.get_width()),
            close_rect.top + const.math.get_center(close_rect.height, self.sizefont_title[1])
        ))

        for i, ln in enumerate(label_surf):
            top = self.y_pos + 75 * self.app.geomatry + i * self.sizefont_how_to_play_text[1]

            if ln.startswith('\u200b'):
                tiles_pos_y.append(top)
            else:
                surface_text = self.font_how_to_play_text.render(ln, True, self.app.themes['popup']['text'])
                self.app.screen.blit(surface_text, (popup_rect.left + 5 * self.app.geomatry, top))

        self.showTile((popup_rect.left + 5 * self.app.geomatry, tiles_pos_y[0]), self.font_how_to_play_tile, [{char: 'green'  if i == 0 else 'not-inputed'} for i, char in enumerate(LANG['tiles']['example-1'])])
        self.showTile((popup_rect.left + 5 * self.app.geomatry, tiles_pos_y[1]), self.font_how_to_play_tile, [{char: 'yellow' if i == 1 else 'not-inputed'} for i, char in enumerate(LANG['tiles']['example-2'])])
        self.showTile((popup_rect.left + 5 * self.app.geomatry, tiles_pos_y[2]), self.font_how_to_play_tile, [{char: 'red'    if i == 4 else 'not-inputed'} for i, char in enumerate(LANG['tiles']['example-3'])])

        self.buttonClose.rect = close_rect

        self.buttonClose.draw_and_update()

    def show_stats(self) -> None:
        LANG = self.app.languages['popup']['stats']

        popup_rect         = pygame.Rect(const.math.get_center(self.app.screen.get_width(), 500 * self.app.geomatry), self.y_pos,                              500 * self.app.geomatry, (407 + (38 * self.app.change_guess)) * self.app.geomatry)
        popup_rect_outline = const.math.Rect_outline(popup_rect, 6 * self.app.geomatry)
        close_rect         = pygame.Rect(popup_rect.right - 40 * self.app.geomatry - 10 * self.app.geomatry,          popup_rect.top + 10 * self.app.geomatry, 40 * self.app.geomatry,  40 * self.app.geomatry)
        shadow_surface     = pygame.Surface((popup_rect_outline.width, popup_rect_outline.height))

        if not self.list_wrapped_text or self.last_game_data != self.app.game_data:
            self.last_game_data = self.app.game_data.copy()
            date_split          = self.app.game_data['joined-date']['date'].split('/')
            stats_label         = {
                LANG['label']['joined-date']:     f'{date_split[3]}/{date_split[4]}/{date_split[5]} {date_split[0]}:{date_split[1]}',
                LANG['label']['play-time-hours']: f"{self.hours_format.parse(self.app.game_data['play-time-seconds'] / 3600)} {LANG['label']['hours']}",
                LANG['label']['has-been-played']: self.app.num_format.parse(self.app.game_data['have-played']),
                LANG['label']['daily-coins']:     self.app.num_format.parse(self.app.game_data['prize-taken']),
                LANG['label']['hints']:           self.app.num_format.parse(self.app.game_data['hint']['count']) + f" [{self.app.num_format.parse(self.app.game_data['hint']['coins'])} {LANG['label']['coins']}]",
                LANG['label']['losses']:          self.app.num_format.parse(self.app.game_data['losses'])        + f" ({self.percent_format.parse(((self.app.game_data['losses']        / self.app.game_data['have-played']) * 100) if self.app.game_data['have-played'] > 0 else 0)}%)",
                LANG['label']['wins']:            self.app.num_format.parse(self.app.game_data['wins']['total']) + f" ({self.percent_format.parse(((self.app.game_data['wins']['total'] / self.app.game_data['have-played']) * 100) if self.app.game_data['have-played'] > 0 else 0)}%)",
                LANG['label']['wins-streak']:     self.app.num_format.parse(self.app.game_data['wins']['streak']),
                LANG['label']['max-wins-streak']: self.app.num_format.parse(self.app.game_data['wins']['max-streak'])
            }
            self.list_wrapped_text = [
                render_wrap(font=self.font_title,           text=LANG['title'],                   wraplength=popup_rect.width - 100 * self.app.geomatry, antialias=True, color=self.app.themes['popup']['text'], wrap_type='center'),
                render_wrap(font=self.font_stats_stat_text, text='\n'.join(stats_label.keys()),   wraplength=popup_rect.width - 10 * self.app.geomatry,  antialias=True, color=self.app.themes['popup']['text'], wrap_type='left'),
                render_wrap(font=self.font_stats_stat_text, text='\n'.join(stats_label.values()), wraplength=popup_rect.width - 10 * self.app.geomatry,  antialias=True, color=self.app.themes['popup']['text'], wrap_type='right')
            ]
            self.buttonClose.edit_param(
                inactive_cursor = pygame.SYSTEM_CURSOR_ARROW,
                active_cursor   = pygame.SYSTEM_CURSOR_HAND
            )

        max_win         = 0
        stat_info_y_pos = self.y_pos + 65 * self.app.geomatry

        title_surf        = self.list_wrapped_text[0]
        stat_keys_surf    = self.list_wrapped_text[1]
        stat_values_surf  = self.list_wrapped_text[2]
        distribution_surf = self.font_stats_stat_text.render(LANG['label']['distribution'], True, self.app.themes['popup']['text'])

        shadow_surface.fill(self.app.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.app.screen.blit(shadow_surface, (
            popup_rect_outline.left + 15 * self.app.geomatry,
            popup_rect_outline.top + 15 * self.app.geomatry
        ))

        pygame.draw.rect(self.app.screen, self.app.themes['popup']['outline'],    popup_rect_outline)
        pygame.draw.rect(self.app.screen, self.app.themes['popup']['background'], popup_rect)

        self.app.screen.blit(title_surf, (
            popup_rect.left + const.math.get_center(popup_rect.width, title_surf.get_width()),
            close_rect.top + const.math.get_center(close_rect.height, self.sizefont_title[1])
        ))
        self.app.screen.blit(stat_keys_surf, (popup_rect.left + 5 * self.app.geomatry, stat_info_y_pos))
        self.app.screen.blit(stat_values_surf, (popup_rect.right - 5 * self.app.geomatry - stat_values_surf.get_width(), stat_info_y_pos))
        self.app.screen.blit(distribution_surf, (
            popup_rect.left + const.math.get_center(popup_rect.width, distribution_surf.get_width()),
            self.y_pos + 330 * self.app.geomatry + distribution_surf.get_height()
        ))

        for i in range(1, self.app.change_guess + 1):
            max_win = max(max_win, self.app.game_data['wins'][str(i)])

        for i in range(self.app.change_guess):
            top                    = self.y_pos + 410 * self.app.geomatry + i * (38 * self.app.geomatry)
            bar_distribution_width = (self.app.game_data['wins'][str(i + 1)] / max_win if max_win > 0 else 0) * (popup_rect.width - 45 * self.app.geomatry) if self.app.game_data['wins']['total'] != 0 else 0

            bar_distribution_rect = pygame.Rect(popup_rect.left + 5 * self.app.geomatry + 35 * self.app.geomatry, top + 2.5 * self.app.geomatry, bar_distribution_width, 25 * self.app.geomatry)

            self.showTile((popup_rect.left + 5 * self.app.geomatry, top), self.font_stats_distribution, [{str(i+1): 'not-inputed'}], size_gap_outline=(30, 8, 3))

            pygame.draw.rect(self.app.screen, self.app.themes['popup']['outline' if (i + 1) != self.app.last_win_line else 'win-bar'], bar_distribution_rect)

            surface_text = self.font_stats_stat_text.render(self.app.num_format.parse(self.app.game_data['wins'][str(i + 1)]), True, self.app.themes['popup']['text'])
            self.app.screen.blit(surface_text, (
                bar_distribution_rect.right - surface_text.get_width() - 5 * self.app.geomatry if bar_distribution_rect.width > surface_text.get_width() + 10 * self.app.geomatry else bar_distribution_rect.right + 5 * self.app.geomatry,
                bar_distribution_rect.top + const.math.get_center(bar_distribution_rect.height, surface_text.get_height())
            ))

        self.buttonClose.rect = close_rect

        self.buttonClose.draw_and_update()

    def show_hint(self) -> None:
        popup_rect         = pygame.Rect(const.math.get_center(self.app.screen.get_width(), 450 * self.app.geomatry), self.y_pos,                                 450 * self.app.geomatry, 600 * self.app.geomatry)
        popup_rect_outline = const.math.Rect_outline(popup_rect, 6 * self.app.geomatry)
        close_rect         = pygame.Rect(popup_rect.right - 40 * self.app.geomatry - 10 * self.app.geomatry,          popup_rect.top + 10 * self.app.geomatry,    40 * self.app.geomatry,  40 * self.app.geomatry)
        buttonBuy_rect     = pygame.Rect(popup_rect.left + (popup_rect.width - 200 * self.app.geomatry) / 2,          popup_rect.bottom - 80 * self.app.geomatry, 200 * self.app.geomatry, 60 * self.app.geomatry)
        shadow_surface     = pygame.Surface((popup_rect_outline.width, popup_rect_outline.height))

        if not self.list_wrapped_text:
            self.list_wrapped_text = [
                render_wrap(
                    font       = self.font_title,
                    text       = self.kw['title'],
                    wraplength = popup_rect.width - 100 * self.app.geomatry,
                    antialias  = True,
                    color      = self.app.themes['popup']['text'],
                    wrap_type  = 'center'
                ),
                render_wrap(
                    font       = self.font_message,
                    text       = self.kw['label'],
                    wraplength = popup_rect.width - 10 * self.app.geomatry,
                    antialias  = True,
                    color      = self.app.themes['popup']['text'],
                    wrap_type  = 'center'
                )
            ]

        title_surf = self.list_wrapped_text[0]
        label_surf = self.list_wrapped_text[1]

        shadow_surface.fill(self.app.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.app.screen.blit(shadow_surface, (
            popup_rect_outline.left + 15 * self.app.geomatry,
            popup_rect_outline.top + 15 * self.app.geomatry
        ))

        pygame.draw.rect(self.app.screen, self.app.themes['popup']['outline'],    popup_rect_outline)
        pygame.draw.rect(self.app.screen, self.app.themes['popup']['background'], popup_rect)

        self.app.screen.blit(title_surf, (
            popup_rect.left + const.math.get_center(popup_rect.width, title_surf.get_width()),
            close_rect.top + const.math.get_center(close_rect.height, self.sizefont_title[1])
        ))
        self.app.screen.blit(label_surf, (
            popup_rect.left + const.math.get_center(popup_rect.width, label_surf.get_width()),
            self.y_pos + const.math.get_center(popup_rect.height, label_surf.get_height())
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
        popup_rect         = pygame.Rect(const.math.get_center(self.app.screen.get_width(), 450 * self.app.geomatry),        self.y_pos,                                 450 * self.app.geomatry, 600 * self.app.geomatry)
        popup_rect_outline = const.math.Rect_outline(popup_rect, 6 * self.app.geomatry)
        close_rect         = pygame.Rect(popup_rect.right - 40 * self.app.geomatry - 10 * self.app.geomatry,                 popup_rect.top + 10 * self.app.geomatry,    40 * self.app.geomatry,  40 * self.app.geomatry)
        buttonAction1_rect = pygame.Rect(popup_rect.left + const.math.get_center(popup_rect.width, 200 * self.app.geomatry), popup_rect.bottom - 80 * self.app.geomatry, 200 * self.app.geomatry, 60 * self.app.geomatry)
        shadow_surface     = pygame.Surface((popup_rect_outline.width, popup_rect_outline.height))

        if not self.list_wrapped_text:
            self.list_wrapped_text = [
                render_wrap(
                    font       = self.font_title,
                    text       = self.kw['title'],
                    wraplength = popup_rect.width - 100 * self.app.geomatry,
                    antialias  = True,
                    color      = self.app.themes['popup']['text'],
                    wrap_type  = 'center'
                ),
                render_wrap(
                    font       = self.font_message,
                    text       = self.kw['label'],
                    wraplength = popup_rect.width - 10 * self.app.geomatry,
                    antialias  = True,
                    color      = self.app.themes['popup']['text'],
                    wrap_type  = 'center'
                )
            ]

        title_surf = self.list_wrapped_text[0]
        label_surf = self.list_wrapped_text[1]

        shadow_surface.fill(self.app.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.app.screen.blit(shadow_surface, (
            popup_rect_outline.left + 15 * self.app.geomatry,
            popup_rect_outline.top + 15 * self.app.geomatry
        ))

        pygame.draw.rect(self.app.screen, self.app.themes['popup']['outline'],    popup_rect_outline)
        pygame.draw.rect(self.app.screen, self.app.themes['popup']['background'], popup_rect)

        self.app.screen.blit(title_surf, (
            popup_rect.left + const.math.get_center(popup_rect.width, title_surf.get_width()),
            close_rect.top + const.math.get_center(close_rect.height, self.sizefont_title[1])
        ))
        self.app.screen.blit(label_surf, (
            popup_rect.left + const.math.get_center(popup_rect.width, label_surf.get_width()),
            self.y_pos + const.math.get_center(popup_rect.height, label_surf.get_height())
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
        LANG = self.app.languages['popup']['daily-coins']

        popup_rect           = pygame.Rect(const.math.get_center(self.app.screen.get_width(), 450 * self.app.geomatry),              self.y_pos,                                    450 * self.app.geomatry,                       600 * self.app.geomatry)
        popup_rect_outline   = const.math.Rect_outline(popup_rect, 6 * self.app.geomatry)
        close_rect           = pygame.Rect(popup_rect.right - 40 * self.app.geomatry - 10 * self.app.geomatry,                       popup_rect.top + 10 * self.app.geomatry,       40 * self.app.geomatry,                        40 * self.app.geomatry)
        box_coin_rect        = pygame.Rect(popup_rect.left + const.math.get_center(popup_rect.width, 400 * self.app.geomatry),       popup_rect.bottom - 175 * self.app.geomatry,   400 * self.app.geomatry,                       150 * self.app.geomatry)
        buttonTakeDaily_rect = pygame.Rect(box_coin_rect.left + const.math.get_center(box_coin_rect.width, 200 * self.app.geomatry), box_coin_rect.bottom - 60 * self.app.geomatry, box_coin_rect.width - 200 * self.app.geomatry, 50 * self.app.geomatry)
        shadow_surface       = pygame.Surface((popup_rect_outline.width, popup_rect_outline.height))

        if not self.list_wrapped_text:
            self.list_wrapped_text = [
                render_wrap(
                    font       = self.font_title,
                    text       = LANG['title'],
                    wraplength = popup_rect.width - 100 * self.app.geomatry,
                    antialias  = True,
                    color      = self.app.themes['popup']['text'],
                    wrap_type  = 'center'
                ),
                render_wrap(
                    font       = self.font_message,
                    text       = LANG['label'].replace('<DAILY-COINS>',  str(const.DAILY_COINS), 1)
                                              .replace('<HOURS>',        '24',                   1)
                                              .replace('<COINS-REWAND>', '1 / 2',                1),
                    wraplength = popup_rect.width - 10 * self.app.geomatry,
                    antialias  = True,
                    color      = self.app.themes['popup']['text'],
                    wrap_type  = 'center'
                )
            ]

        text = self.app.get_daily_countdown()

        title_surf = self.list_wrapped_text[0]
        label_surf = self.list_wrapped_text[1]

        shadow_surface.fill(self.app.themes['popup']['shadow'])
        shadow_surface.set_alpha(150)

        self.app.screen.blit(shadow_surface, (
            popup_rect_outline.left + 15 * self.app.geomatry,
            popup_rect_outline.top + 15 * self.app.geomatry
        ))

        pygame.draw.rect(self.app.screen, self.app.themes['popup']['outline'],    popup_rect_outline)
        pygame.draw.rect(self.app.screen, self.app.themes['popup']['background'], popup_rect)
        pygame.draw.rect(self.app.screen, self.app.themes['popup']['outline'],    const.math.Rect_outline(box_coin_rect, 6 * self.app.geomatry))
        pygame.draw.rect(self.app.screen, self.app.themes['popup']['background'], box_coin_rect)

        self.app.screen.blit(title_surf, (
            popup_rect.left + const.math.get_center(popup_rect.width, title_surf.get_width()),
            close_rect.top + const.math.get_center(close_rect.height, self.sizefont_title[1])
        ))
        self.app.screen.blit(label_surf, (
            popup_rect.left + const.math.get_center(popup_rect.width, label_surf.get_width()),
            self.y_pos + const.math.get_center(popup_rect.height, label_surf.get_height())
        ))

        surface_coins = self.font_daily_countdown.render(
            LANG['coin-label']['coins'].replace('<DAILY-COINS>', str(const.DAILY_COINS), 1) if text is True else LANG['coin-label']['count-down'].replace('<COUNT-DOWN>', text, 1),
            True, self.app.themes['popup']['text']
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

        self.buttonClose.draw_and_update()

        if text is True:
            self.buttonAction.draw_and_update()
        else:
            self.buttonAction.draw_inactive()
            self.buttonAction.button_event.ismousehover = buttonTakeDaily_rect.collidepoint(pygame.mouse.get_pos())

        case_button = self.buttonAction.button_event.ismousehover and text is not True

        if case_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

        self.app.screen.blit(surface_coins, (
            box_coin_rect.left + const.math.get_center(box_coin_rect.width, surface_coins.get_width()),
            box_coin_rect.top + const.math.get_center(box_coin_rect.height-buttonTakeDaily_rect.height-(box_coin_rect.bottom-buttonTakeDaily_rect.bottom), surface_coins.get_height())
        ))

class Notification:

    def __init__(self, app: katla, notif_kind: const.Literal['Win', 'Lose', 'StreakEnded'] | str) -> None:
        self.app        = app
        self.notif_kind = notif_kind

        self.animation_start_time = 0
        self.slide_in_duration    = 0.25
        self.slide_out_duration   = 0.25
        self.target_pos_y         = self.app.notification_initial_y
        self.display_duration     = (5 if notif_kind in ('Win', 'Lose', 'StreakEnded') else 3)
        self.color_scheme         = notif_kind.lower() if notif_kind in ('Win', 'Lose') else 'default'
        self.text                 = ''
        self.notif_rect           = None
        self.wrapped_message      = None
        self.position_finalized   = False
        self.is_visible           = False

    def __call__(self) -> None:
        if not self.is_visible:
            if self.notif_kind in self.app.notifications_layer:
                self.app.notifications_layer.remove(self.notif_kind)
            return

        self.wrapped_message = render_wrap(self.app.font_notification, self.text, self.app.screen.get_width() - 25 * self.app.geomatry, True, self.app.themes['notification'][self.color_scheme]['text'], wrap_type='center')

        current_time   = self.app.get_tick()
        slide_in_time  = self.animation_start_time + self.slide_in_duration
        display_time   = slide_in_time + self.display_duration
        slide_out_time = display_time + self.slide_out_duration

        pos_start = -(self.wrapped_message.get_height() + 20 * self.app.geomatry)
        pos_end   = self.target_pos_y

        if current_time < slide_in_time:
            self.draw(const.math.get_pos_animation(
                pos_start    = pos_start,
                pos_end      = pos_end,
                time_end     = self.slide_in_duration,
                current_time = current_time,
                start_time   = self.animation_start_time
            ))
            if not self.position_finalized:
                self.target_pos_y                = self.app.notification_initial_y
                self.app.notification_initial_y += self.notif_rect.height + 15 * self.app.geomatry
                self.position_finalized          = True

        elif current_time < display_time:
            self.draw(pos_end)

        elif current_time < slide_out_time:
            self.draw(const.math.get_pos_animation(
                pos_end      = pos_start,
                pos_start    = pos_end,
                time_end     = self.slide_out_duration,
                current_time = current_time,
                start_time   = display_time
            ))

        else:
            self.is_visible = False

            if self.notif_kind in ('Win', 'Lose'):
                self.app.reset()
                self.app.notifications_layer.clear()
                self.app.play_lose_or_win = 0
            else:
                self.app.notifications_layer.remove(self.notif_kind)

    def refresh(self) -> None:
        self.is_visible         = False
        self.position_finalized = False
        self.target_pos_y       = self.app.notification_initial_y

    def start(self) -> None:
        is_win_or_lose = self.notif_kind in ('Win', 'Lose')

        if not (self.is_visible or self.app.notifications_layer):
            self.target_pos_y       = self.app.notification_initial_y
            self.position_finalized = False

        if is_win_or_lose:
            self.target_pos_y       = self.app.notification_initial_y = 130 * self.app.geomatry
            self.position_finalized = True

        self.is_visible           = True
        self.animation_start_time = self.app.get_tick()

        if not is_win_or_lose:
            if self.notif_kind in self.app.notifications_layer:
                self.app.notifications_layer.remove(self.notif_kind)

            self.app.notifications_layer.append(self.notif_kind)

        else:
            self.app.notifications_layer.clear()

    def draw(self, index: const.Number) -> None:
        self.notif_rect = pygame.Rect(
            const.math.get_center(self.app.screen.get_width(), self.app.screen.get_width() - 20 * self.app.geomatry),
            index,
            self.app.screen.get_width() - 20 * self.app.geomatry,
            self.wrapped_message.get_height() + 15 * self.app.geomatry
        )

        pygame.draw.rect(self.app.screen, self.app.themes['notification'][self.color_scheme]['outline'],    const.math.Rect_outline(self.notif_rect, 6 * self.app.geomatry))
        pygame.draw.rect(self.app.screen, self.app.themes['notification'][self.color_scheme]['background'], self.notif_rect)

        self.app.screen.blit(self.wrapped_message, self.wrapped_message.get_rect(center=self.notif_rect.center))