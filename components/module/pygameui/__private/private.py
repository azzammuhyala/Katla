import pygame as pygame
import typing as typing
from . import const


class Private:

    """ Private - private class """

    def __init__(self) -> None:

        """
        This class is private and contains methods contained in the button element
        """

        self.init_rect = pygame.Rect(0, 0, 0, 0)

    def asserting(self, condition: bool, raise_exception: Exception) -> None:

        """
        Checks the condition if it is False then raises an exception.

        Parameters:
            :param `condition`: boolean condition to check.
            :param `raise_exception`: exception to raise if the condition is False.

        Returns:
            `None`
        """

        if not bool(condition):
            raise raise_exception

    def get_type(self, obj: typing.Any) -> str:

        """
        Gets type object.

        Parameters:
            :param `obj`: object to get the type for.

        Returns:
            `str`
        """

        return type(obj).__name__

    def button_get_mouse_pressed(self, only_click: const.ButtonEventClick) -> tuple[bool, bool, bool]:

        """
        Gets mouse presses corresponding to existing only_click.

        Parameters:
            :param `only_click`: list of strings representing which mouse buttons should be considered.

        Returns:
            `tuple[bool, bool, bool]` => (l, c, r)
        """

        isinonlyclick = lambda click: click in only_click 
        pressed = pygame.mouse.get_pressed()
        return (
            pressed[0] if isinonlyclick('l') else False,
            pressed[1] if isinonlyclick('c') else False,
            pressed[2] if isinonlyclick('r') else False
        )

    def is_partially_outside(self, main_rect: pygame.Rect, order_rect: pygame.Rect) -> bool:

        """
        Gets whether a rect is outside the main rect area completely.

        Parameters:
            :param `main_rect`: main rectangle acting as the boundary.
            :param `order_rect`: rectangle to check if it is partially outside the main rectangle.

        Returns:
            `bool`
        """

        return not (
            main_rect.collidepoint(order_rect.left, order_rect.top) or
            main_rect.collidepoint(order_rect.right, order_rect.top) or
            main_rect.collidepoint(order_rect.left, order_rect.bottom) or
            main_rect.collidepoint(order_rect.right, order_rect.bottom) or
            order_rect.collidepoint(main_rect.left, main_rect.top) or
            order_rect.collidepoint(main_rect.right, main_rect.top) or
            order_rect.collidepoint(main_rect.left, main_rect.bottom) or
            order_rect.collidepoint(main_rect.right, main_rect.bottom)
        )
    
    def draw_srect(
    
            self,
            surface: pygame.Surface,
            color: const.ColorValue,
            rect: pygame.Rect | list | tuple,
            alpha: int = 0,
            width: int = 0,
            border_radius: int = -1,
            border_top_left_radius: int = -1,
            border_top_right_radius: int = -1,
            border_bottom_left_radius: int = -1,
            border_bottom_right_radius: int = -1

        ) -> None:

        """
        Draws a rectangle with various customizable properties such as transparency (alpha), border radius, and other styling.

        Parameters:
            :param `surface`: screen surface, `pygame.display.set_mode((x, y))` or `pygame.Surface`.
            :param `color`: color of the rectangle.
            :param `rect`: rectangle's position and size. Can be a `pygame.Rect`, list, or tuple.
            :param `alpha`: transparency level of the rectangle.
            :param `width`: thickness of the rectangle's border. If 0, the rectangle is filled.
            :param `border_radius`: overall roundedness of the rectangle's corners.
            :param `border_top_left_radius`: rounding radius for the top-left corner.
            :param `border_top_right_radius`: rounding radius for the top-right corner.
            :param `border_bottom_left_radius`: rounding radius for the bottom-left corner.
            :param `border_bottom_right_radius`: rounding radius for the bottom-right corner.

        Returns:
            `None`
        """

        if alpha == 0:
            return

        if isinstance(rect, pygame.Rect):
            pos = rect.topleft
            size = rect.size
        else:
            pos = (rect[0], rect[1])
            size = (rect[2], rect[3])

        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, *size), width, border_radius, border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius)
        surf.set_alpha(alpha)
        surface.blit(surf, pos)


# Private Initialization
prvt = Private()