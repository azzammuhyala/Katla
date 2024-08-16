import pygame
import typing


class Private:

    """ _Private - private class """

    def __init__(self) -> None:

        """
        This class is private and contains methods contained in the button element
        """

        self.init_rect = pygame.Rect(0, 0, 0, 0)

    def asserting(self, condition: bool, raise_exception: Exception) -> None:

        """
        Checks the condition if it is False then raises an exception.

        return -> `None`
        """

        if not bool(condition):
            raise raise_exception

    def get_type(self, obj: object) -> str:

        """
        Gets type object.

        return -> `str`
        """

        return type(obj).__name__

    def get_mouse_pressed(self, only_click) -> tuple[bool, bool, bool]:

        """
        Gets mouse presses corresponding to existing only_click.

        return -> `tuple[bool, bool, bool]` => (l, c, r)
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

        return -> `bool`
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


# Private Initialization
prvt = Private()