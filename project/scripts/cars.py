import pygame


class Car:
    def __init__(self, model: pygame.Surface, pos: tuple[float, float], speed: float) -> None:
        self.model = model
        self.model_rect = model.get_rect(center=pos)
        self.speed = speed


    def check_collision(self, rect: tuple[float, float, float, float]) -> bool: # Is_crashed?
        return self.model_rect.colliderect(
            rect=rect
        )


    def __call__(self, sc: pygame.Surface):
        self.model_rect.centery += self.speed
        sc.blit(
            source=self.model,
            dest=self.model_rect
        )