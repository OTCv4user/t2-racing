import os
import sys

import pygame
import win32api

from scripts.constants import (
    DISPLAY_SIZE, TICKRATE, PRESSED_SCALE, STEERING_SPEED
)
from scripts.surfaces_buffer import SurfBuffer
from scripts.button import Button
from scripts.road import RoadSystem
from scripts.cars import Car
#from scripts.overlay import Overlay


def exit(*args) -> None:
    pygame.quit()
    sys.exit(0)


def game(sc: pygame.Surface, clock: pygame.time.Clock) -> object:
    road = RoadSystem(
        asphalt=surfaces('asphalt'),
        roadside=surfaces('roadside'),
        width=sc.get_width() * 0.9,
        center_x=sc.get_width() / 2

    )
    model = surfaces(
        'cybertruck'
    )
    scale = road.scale

    player_car = Car(
        model=pygame.transform.scale(
            surface=model,
            size=(model.get_width() * scale, model.get_height() * scale)
        ),
        pos=(sc.get_width() / 2, sc.get_height() * .8),
        speed=0
    ) # 3 часа ночи, хочу спать...

    speed = 80

    while True:
        sc.fill((255, 255, 255))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        btns = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return main_menu

        if keys[pygame.K_a]:
            player_car.model_rect.x -= STEERING_SPEED
        if keys[pygame.K_d]:
            player_car.model_rect.x += STEERING_SPEED

        if btns[0]:
            if mouse_x < sc.get_width() / 2:
                player_car.model_rect.x -= STEERING_SPEED
            else:
                player_car.model_rect.x += STEERING_SPEED

        road(
            sc=sc,
            speed=speed
        )
        player_car(
            sc=sc
        )

        pygame.display.update()
        clock.tick(TICKRATE)

    
def main_menu(sc: pygame.Surface, clock: pygame.time.Clock) -> object:
    background = surfaces(
        'main'
    )
    background = pygame.transform.scale(
        surface=background,
        size=(sc.get_width(), sc.get_height())
    )

    start_unpressed = surfaces(
        key='start_unpressed'
    )
    start_pressed = surfaces(
        key='start_pressed'
    )
    scale = (sc.get_width() / start_unpressed.get_width()) * 0.9

    start_unpressed = surfaces(
        key='start_unpressed',
        scale=scale
    )
    start_pressed = surfaces(
        key='start_pressed',
        scale=scale
    )

    start_button = Button(
        surface=sc,
        surf_unpressed=start_unpressed,
        surf_pressed=start_pressed,
        pressed_scale=PRESSED_SCALE,
        offset=(0, 0),
        position=(sc.get_width() / 2, sc.get_height() - start_unpressed.get_height()),
        on_click=game
    )

    '''overlay = Overlay(
        sc=sc,
        ticks=30,
        alpha=0,
        direction=1
    )'''

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        btns = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return exit

        sc.blit(
            source=background,
            dest=(0, 0)
        )

        func = start_button(
            pos=(mouse_x, mouse_y),
            lkm_pressed=btns[0]
        )
        if func:
            return func
        #print(
        #overlay()
        #)

        pygame.display.update()
        clock.tick(TICKRATE)

        
def main():
    pygame.init()
    
    scale = (win32api.GetSystemMetrics(1) / DISPLAY_SIZE[1]) - 0.05 # Pseudo-emulation phone
    display_size = tuple(map(lambda e: e * scale, DISPLAY_SIZE))
    print(display_size)

    sc = pygame.display.set_mode(display_size)
    clock = pygame.time.Clock()
    
    pygame.display.set_caption('T2 Racing')
    pygame.display.set_icon(surfaces('t2_racing'))
    
    function_buffer = main_menu
    while True:
        function_buffer = function_buffer(sc, clock)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    surfaces = SurfBuffer()
    main()