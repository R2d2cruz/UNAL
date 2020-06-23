from . import gui
from .Control import Control
from ..core.misc import getFirst


class Container(Control):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.children = []
        self.__padding = 10

    @property
    def padding(self):
        return self.__padding

    @padding.setter
    def padding(self, padding):
        self.__padding = padding
        self.refresh()

    def addControl(self, control: Control):
        self.children.append(control)
        self.refresh()

    def removeControl(self, control: Control):
        self.children.remove(control)

    def render(self, surface, camera):
        # gui.renderElement(surface, self.rect, "panel")
        for control in self.children:
            control.render(surface, camera)

    def handleEvent(self, event):
        for control in self.children:
            control.handleEvent(event)

    def refresh(self):
        for control in self.children:
            control.refresh()

    def getControlById(self, controlId: int):
        control = getFirst(self.children, lambda x: x.id == controlId or x.name == controlId)
        if control is not None:
            return control
        for control in self.children:
            if control.id == controlId:
                return control
            if isinstance(control, (Container, GridContainer, BoxContainer)):
                control = control.getControlById(controlId)
                if control is not None:
                    return control

    def getControlByName(self, controlName: str):
        control = getFirst(self.children, lambda x: x.name == controlName)
        if control is not None:
            return control
        for control in self.children:
            if control.name == controlName:
                return control
            if isinstance(control, (Container, GridContainer, BoxContainer)):
                control = control.getControlByName(controlName)
                if control is not None:
                    return control


class GridContainer(Container):
    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        super().__init__(x, y, width, height)
        self.__cells = []
        self.__rows = 0
        self.__cols = 0
        self.__numControls = 0

    def setGrid(self, rows: int, cols: int):
        if rows > 0 and cols > 0:
            self.__rows = rows
            self.__cols = cols
            for row in range(0, rows):
                self.__cells.append([None] * cols)
        else:
            self.__cells = []

    def addControl(self, control: Control, pos: tuple):
        super().addControl(control)
        if pos is not None and (0 <= pos[0] < self.__rows) and (0 <= pos[1] < self.__cols):
            self.__cells[pos[0]][pos[1]] = control
            self.refresh()

    def render(self, surface, camera):
        gui.renderElement(surface, self.rect, "panel")
        for row in self.__cells:
            for cell in row:
                if cell is not None:
                    cell.render(surface, camera)

    def handleEvent(self, event):
        for row in self.__cells:
            for cell in row:
                if cell is not None:
                    cell.handleEvent(event)

    def refresh(self):
        cellWidth = self.width / self.__cols
        cellHeight = self.height / self.__rows
        innerWidth = cellWidth - self.padding * 2
        innerHeight = cellHeight - self.padding * 2
        for row in range(self.__rows):
            for col in range(self.__cols):
                control = self.__cells[row][col]
                if control is not None:
                    control.centerx = self.x + (cellWidth * col) + (cellWidth / 2)
                    control.centery = self.y + (cellHeight * row) + (cellHeight / 2)
                    control.width = innerWidth if control.width == 0 else min(innerWidth, control.width)
                    control.height = innerHeight if control.height == 0 else min(innerHeight, control.height)
                    control.refresh()


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
