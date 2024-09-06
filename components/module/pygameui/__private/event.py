from .private import (
    pygame,
    prvt as _prvt
)
from .const import (
    ModElementEvent as ModElementEvent,
    ModsElementEvent as ModsElementEvent,
    ElementID as _ElementID,
    ButtonEventClick as _ButtonEventClick,
    RealNumber as _RealNumber
)


BUTTON_CLICK: int = pygame.USEREVENT + 1
SCROLLER: int = pygame.USEREVENT + 2


AllElement = []

for mods in ModsElementEvent.values():
    for el in mods:
        AllElement.append(el)


class ElementEvent:

    """ ElementEvent - The event of element function """

    def __init__(self, element: ModElementEvent, id: _ElementID = None) -> None:

        _prvt.asserting(element in AllElement, TypeError(f'element: unknown element {repr(element)}'))

        self.element: ModElementEvent = element
        self.id: _ElementID = id

        if element in ('Button', 'Range'):
            self.click: _ButtonEventClick = ''
            self.ismousehover: bool = None
            self.cursor_active: bool = None
            self.cursor_inactive: bool = None

        elif element in ('Scroller', 'ScrollerX', 'ScrollerY'):
            self.offset: tuple[_RealNumber, _RealNumber] = None
            self.isanchor: bool = None
            self.isanchordrag: bool = None
            self.isanchormousescroller: bool = None
            self.isanchorkeyboard: bool = None
            self.isdragging: bool = None
            self.isscrolling: bool = None
            self.iskeyscrolling: bool = None

        match element:

            case 'Button':
                self.isbuttoninactive: bool = None
                self.isbuttonhover: bool = None
                self.isbuttonactive: bool = None

            case 'Range':
                self.israngeinactive: bool = None
                self.israngehover: bool = None
                self.israngeactive: bool = None
                self.isdragging: bool = None
                self.rect_thumb: pygame.Rect = None
                self.rect_track_fill: pygame.Rect = None
                self.range_value: _RealNumber = None

            case 'Scroller':
                self.offset_x: _RealNumber = None
                self.offset_y: _RealNumber = None

            case 'ScrollerX':
                self.offset_x: _RealNumber = None
                self.y_pos: _RealNumber = None

            case 'ScrollerY':
                self.offset_y: _RealNumber = None
                self.x_pos: _RealNumber = None

    def __copy__(self):
        return self.copy()

    def __repr__(self) -> str:
        return f'ElementEvent(element={repr(self.element)}, id={repr(self.id)})'

    def __str__(self) -> str:
        return f'element={repr(self.element)},id={repr(self.id)}'

    def __eq__(self, order) -> bool | None:
        if isinstance(order, ElementEvent):
            return (self.element, self.id) == (order.element, order.id)
        return None

    def __ne__(self, order) -> bool | None:
        eq = self.__eq__(order)
        return (not eq if eq is not None else None)

    def _reset_property(self) -> None:
        self.__init__(self.element, self.id)

    def _send_event(self) -> None:
        match self.element:

            case 'Button':
                event = pygame.event.Event(
                    BUTTON_CLICK,
                    id = self.id,
                    element = self.element,
                    click = self.click,
                    element_event = self
                )

            case 'Range':
                event = pygame.event.Event(
                    BUTTON_CLICK,
                    id = self.id,
                    element = self.element,
                    click = self.click,
                    range_value = self.range_value,
                    element_event = self
                )
            
            case 'Scroller':
                event = pygame.event.Event(
                    SCROLLER,
                    id = self.id,
                    element = self.element,
                    offset = self.offset,
                    offset_x = self.offset_x,
                    offset_y = self.offset_y,
                    element_event = self
                )

            case 'ScrollerX':
                event = pygame.event.Event(
                    SCROLLER,
                    id = self.id,
                    element = self.element,
                    offset = self.offset,
                    offset_x = self.offset_x,
                    element_event = self
                )

            case 'ScrollerY':
                event = pygame.event.Event(
                    SCROLLER,
                    id = self.id,
                    element = self.element,
                    offset = self.offset,
                    offset_y = self.offset_y,
                    element_event = self
                )

        pygame.event.post(event)

    def copy(self):
        return ElementEvent(element=self.element, id=self.id)