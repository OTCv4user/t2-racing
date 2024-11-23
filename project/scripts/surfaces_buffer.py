"""
It's a defense against the st**id
"""

import os

import pygame

from scripts import constants


class SurfBuffer:
    def __init__(self) -> None:
        self.surfaces = {
            None: pygame.Surface((50, 50))
        }
    
    
    def __find(self, find_key: str) -> str:
        """Generate full path on key

        Args:
            find_key (str)

        Returns:
            str: return path if key is valid, else None
        """
        for key in constants.paths.keys():
            if find_key in constants.paths[key]:
                return os.path.join(key, constants.paths[key][find_key])
            
        return None


    def __load(self, path: str) -> pygame.Surface:
        """Load image

        Args:
            path (str): path to image

        Returns:
            pygame.Surface
        """
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            return None
    
    
    def __add(self, key: str, surf: pygame.Surface) -> None:
        """Add key:surf to dictionary

        Args:
            key (str)
            surf (pygame.Surface)
        """
        self.surfaces.update(
            {key: surf}
        )
        
        return None


    def to_screen(self, surf: pygame.Surface, screen: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale(
            surface=surf,
            size=(screen.get_width(), screen.get_height())
        )
    
    
    def __call__(self, key: str, scale: float = 1.) -> pygame.Surface:
        """Dynamic loading of Surfaces and buffering

        Args:
            key (str)

        Returns:
            pygame.Surface
        """
        surf = self.surfaces.get(key)
        if surf is not None:
            return pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale))
        
        path = self.__find(key)
        if path is None:
            surf = self.surfaces[None]
            return pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale))

        surf = self.__load(path)
        if surf is not None:
            self.__add(key, surf)
            return pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale))
        
        surf = self.surfaces[None]
        return pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale))