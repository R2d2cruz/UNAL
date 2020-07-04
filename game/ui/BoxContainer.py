from .gui import gui
from .Container import Container
from .Control import Control


class BoxContainer(Container):
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'

    CENTER = 'CENTER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'

    def __init__(self, boxType: str, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        super().__init__(x, y, width, height)
        self.__boxType = boxType
        self.__direction = BoxContainer.CENTER

    def addControl(self, control: Control):
        super().addControl(control)
        self.refresh()

    def render(self, surface, camera):
        gui.renderElement(surface, self.rect, "panel")
        super().render(surface, camera)

    def refresh(self):
        n = len(self.children)
        innerWidth = self.width - self.padding * 2
        innerHeight = self.height - self.padding * 2
        for i in range(n):
            if self.__boxType == BoxContainer.HORIZONTAL:
                # noinspection DuplicatedCode
                if i == 0:
                    self.children[i].left = self.left + self.padding
                else:
                    self.children[i].left = self.children[i - 1].right + 1

                if self.__direction == BoxContainer.CENTER:
                    self.children[i].centery = self.centery
                elif self.__direction == BoxContainer.TOP:
                    self.children[i].top = self.top
                elif self.__direction == BoxContainer.BOTTOM:
                    self.children[i].bottom = self.bottom
                self.children[i].height = min(self.children[i].height, innerHeight)

            elif self.__boxType == BoxContainer.VERTICAL:
                # noinspection DuplicatedCode
                if i == 0:
                    self.children[i].top = self.top + self.padding
                else:
                    self.children[i].top = self.children[i - 1].bottom + 1

                if self.__direction == BoxContainer.CENTER:
                    self.children[i].centerx = self.centerx
                elif self.__direction == BoxContainer.LEFT:
                    self.children[i].left = self.left
                elif self.__direction == BoxContainer.BOTTOM:
                    self.children[i].right = self.right
                self.children[i].width = min(self.children[i].width, innerWidth)
            self.children[i].refresh()
