import pygame


class Overlay:
    def __init__(self, sc: pygame.Surface, ticks, alpha: int, direction: int) -> None:
        self.sc = sc
        self.surf = pygame.Surface((sc.get_width(), sc.get_height()), pygame.SRCALPHA)

        self.step = (255 / ticks) * direction
        self.alpha = alpha
        self.direction = direction


    def __update_alpha(self) -> None:
        self.surf.fill((0, 0, 0, self.alpha if self.alpha % 256 == self.alpha else 255))


    def __call__(self) -> bool:
        self.sc.blit(
            source=self.sc,
            dest=(0, 0)
        )

        self.alpha += self.step
        self.__update_alpha()
        if self.alpha % 256 != self.alpha:
            print(self.alpha % 256,  self.alpha)
            return True
        return False