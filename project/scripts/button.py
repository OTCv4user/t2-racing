import pygame


class Button:
    def __init__(self, surface: pygame.Surface, surf_unpressed: pygame.Surface, surf_pressed: pygame.Surface, pressed_scale: float, offset: tuple[int, int], position: tuple[float, float], on_click: object) -> None:
        """This is button generator

        Args:
            surf_unpressed (pygame.Surface)
            surf_pressed (pygame.Surface)
            pressed_scale (float): .01 - 1.
        """
        self.sc = surface
        self.unpressed = surf_unpressed
        self.pressed = pygame.transform.scale(
            surf_pressed,
            (
                surf_pressed.get_width() * pressed_scale,
                surf_pressed.get_height() * pressed_scale
            )
        )
        self.on_click = on_click
        
        position = (position[0] + offset[0], position[1] + offset[1])
        
        self.rect_unpressed = self.unpressed.get_rect(center=position)
        self.rect_pressed = self.pressed.get_rect(center=position)
        
        self.is_pressed = False
    
    
    def __update(self, pos: tuple[float, float], lkm_pressed: bool) -> any:
        """Handle button

        Args:
            pos (tuple[float, float])
            lkm_pressed (bool)
        """
        if lkm_pressed:
            if self.rect_unpressed.collidepoint(*pos):
                if not self.is_pressed:
                    self.is_pressed = True
            else:
                self.is_pressed = False
                
        elif self.is_pressed:
            if self.rect_unpressed.collidepoint(*pos):
                self.is_pressed = False
                return self.on_click
        
        return None
    
    
    def __draw(self) -> None:
        """Draw button on surface

        Args:
            sc (pygame.Surface)
        """
        self.sc.blit(
            self.pressed if self.is_pressed else self.unpressed,
            self.rect_pressed if self.is_pressed else self.rect_unpressed,
        )
    
    
    def __call__(self, pos: tuple[float, float], lkm_pressed: bool) -> object:
        func = self.__update(pos, lkm_pressed)
        self.__draw()
        return func
                