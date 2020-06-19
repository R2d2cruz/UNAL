import pygame

from .BaseCamera import BaseCamera


class NullCamera(BaseCamera):
    def __init__(self):
        super().__init__(0, 0, 0, 0)
        pass
