# `pygameui` module
Version: 1.0.0

Explanation
-----------
pygameui is a special tool module to display common elements that are not yet available in the default pygame. Pygame does not provide common element media such as buttons and others, but the functions and methods provided by the pygame module provide various ways to create these elements. This module is used to speed your developing game.

Modules
-------

For the current version, there are 4 modules available, including:

1. **`button`**

module ini memiliki 2 element yaitu element tombol dan tombol range. Tombol berfungsi untuk memuat tombol sendangkan tombol range atau range berfungsi untuk menampilkan tombol yang memiliki jarak

2. **`scroller`**

lorem ipsum.

3. **`textwrap`**

lorem ipsum.

4. **`vgif`**

lorem ipsum.

Events
------
Some element modules have ElementEvent. In the form of a class that handles all events that occur, some also do not have this event. To access it, it can be done by taking the return result from the update method function or through the event that occurs in pygame.

Examples
--------

1. **`button`** example code

```py
import pygame # import the pygame
from pygameui import button # import the pygameui button

# pygame setup
pygame.init()
running = True

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

pygame.display.set_caption('Button Test')

font = pygame.font.SysFont('Monospace', 25, True)
showtext = lambda text : font.render(text, True, 'white')
text = showtext('Press one of the buttons')

# button rects
rect_button1 = pygame.Rect(100, (screen.get_height() - 100) / 2, 100, 100)
rect_button2 = pygame.Rect(screen.get_width() - 200, (screen.get_height() - 100) / 2, 100, 100)
# Range rects
rect_range = pygame.Rect((screen.get_width() - 400) / 2, 100, 400, 10)

# initialization button (Do not initialization Buttons in the game loop because this will be affected by time, events, etc)
button1 = button.Button(
    surface_screen=screen,
    rect=rect_button1,
    id='button1',
    text='BUTTON 1'
)

# if you want to copy an element, use the copy() method and fill it with new parameters if necessary
button2 = button1.copy(
    rect=rect_button2,
    id='button2',
    text='BUTTON 2',
    outline_size=5,
    only_click='lrc',
    click_speed=250
)

# input range parameters
range_button = button.Range(
    surface_screen=screen,
    rect=rect_range,
    id='range_button',
    thumb_size=(17, 17),
    min_value=0,
    max_value=100,
    value=50,
    step=1, 
    range_value_output=int
)

# manager (Optional) set events, draws, etc. in several buttons at once
manager = button.Manager(
    button1,
    button2,
    range_button,

    inactive_cursor=pygame.SYSTEM_CURSOR_ARROW,
    active_cursor=pygame.SYSTEM_CURSOR_HAND
)

# screen loop
while running:

    # events
    for event in pygame.event.get():
        # when the user clicks the X to close the screen (pygame)
        if event.type == pygame.QUIT:
            running = False

        # handle events of all buttons
        manager.handle_event(event)

        # event when one of the buttons is pressed
        if event.type == button.BUTTON_CLICK:
            # your case
            print(
                f'button event property: id:{event.id}, ' +
                f'element:{event.element}, ' +
                f'click:{event.click}, ' + 
                (f'range_value:{event.range_value}, ' if event.element == 'Range' else '') +
                f'ElementEvent:({event.element_event})'
            )

    # fill screen black
    screen.fill('black')

    # blit or draw and update the button
    manager.draw_and_update()

    text_range = showtext(f'Value Range: {range_button.button_event.range_value}')

    # get button event
    if button1.button_event.click:
        text = showtext('Pressed BUTTON 1 -> ' + button1.button_event.click)

    elif button2.button_event.click:
        text = showtext('Pressed BUTTON 2 -> ' + button2.button_event.click)

    # show the range event text
    screen.blit(text_range, ((screen.get_width() - text_range.get_width()) / 2, 115))
    # show the button event text
    screen.blit(text, ((screen.get_width() - text.get_width()) / 2, 450))
    # flip() the display to put your work on screen
    pygame.display.flip()
    # Set the frame-rate speed to 60 (fps)
    clock.tick(60)

# clean up pygame resources
pygame.quit()
```

2. **`scroller`** example code

```py
import pygame # import the pygame
from pygameui import scroller # import the pygame scroller

# pygame setup
pygame.init()

running = True
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

pygame.display.set_caption('Scroller Test')

# just a surface test, for example is a text
font = pygame.font.SysFont(None, 60)

testsurf = font.render('Hi!', True, 'white', 'magenta')
surfx = font.render('[]', True, 'red')
surfy = font.render('[]', True, 'blue')

sx, sy = screen.get_width(), screen.get_height()

# initialization the scrollers (Do not initialization Scrollers in the game loop because this will be affected by time, events, etc)
scroller1 = scroller.Scroller(
    max_scrolled=(sx - testsurf.get_width(), sy - testsurf.get_height()),
    clock=clock,
    reversed_keyboard=True
)
scroller2 = scroller.ScrollerX(
    min_max_scrolled=(0, sx - surfx.get_width()),
    y_pos=0,
    clock=clock,
    reversed_keyboard=True
)
scroller3 = scroller.ScrollerY(
    min_max_scrolled=(0, sy - surfy.get_height()),
    x_pos=sx - surfy.get_width(),
    clock=clock, 
    reversed_keyboard=True
)

# screen loop
while running:

    # events
    for event in pygame.event.get():
        # when the user clicks the X to close the screen (pygame)
        if event.type == pygame.QUIT:
            running = False

        # handle scroller events
        scroller1.handle_event(event)
        scroller2.handle_event(event)
        scroller3.handle_event(event)

        if event.type == scroller.SCROLLER:

            if event.element == 'Scroller':
                print(f'button event property: id:{event.id}, ' +
                    f'element:{event.element}, ' +
                    f'offset:{event.offset}, ' + 
                    f'offset_x:{event.offset_x}, ' +
                    f'offset_y:{event.offset_y}, ' +
                    f'ElementEvent:({event.element_event})'
                )
 
            if event.element == 'ScrollerX':
                print(f'button event property: id:{event.id}, ' +
                    f'element:{event.element}, ' +
                    f'offset:{event.offset}, ' + 
                    f'offset_x:{event.offset_x}, ' +
                    f'ElementEvent:({event.element_event})'
                )

            if event.element == 'ScrollerY':
                print(f'button event property: id:{event.id}, ' +
                    f'element:{event.element}, ' +
                    f'offset:{event.offset}, ' + 
                    f'offset_y:{event.offset_y}, ' +
                    f'ElementEvent:({event.element_event})'
                )

    # fill screen black
    screen.fill('black')
    # update the scrollers
    scroller1.update()
    scroller2.update()
    scroller3.update()
    # displays the image with scroller offset
    scroller1.apply(screen, testsurf)
    scroller2.apply(screen, surfx)
    scroller3.apply(screen, surfy)

    # flip() the display to put your work on screen
    pygame.display.flip()
    # Set the frame-rate speed to 60 (fps)
    clock.tick(60)

# clean up pygame resources
pygame.quit()
```