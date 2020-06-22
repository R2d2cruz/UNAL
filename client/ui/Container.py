from .Control import Control
from ..core.misc import getFirst


class Container(Control):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.__controls = []

    def addControl(self, control: Control):
        self.__controls.append(control)

    def removeControl(self, control: Control):
        self.__controls.remove(control)

    def render(self, surface, camera):
        for control in self.__controls:
            control.render(surface, camera)

    def handleEvent(self, event):
        for control in self.__controls:
            control.handleEvent(event)

    def getControl(self, controlId: int):
        control = getFirst(self.__controls, lambda x: x.id == controlId)
        if control is not None:
            return control
        for control in self.__controls:
            if control.id == controlId:
                return control
            if isinstance(control, Container):
                control = control.getControl(controlId)
                if control is not None:
                    return control


class GridContainer(Control):
    def __init__(self, x: int, y: int, width: int, height: int):
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
        if pos is not None and (0 <= pos[0] < self.__rows) and (0 <= pos[1] < self.__cols):
            self.__cells[pos[0]][pos[1]] = control
            control.width = self.rect.width / self.__cols
            control.height = self.rect.height / self.__rows
            control.x = control.width * pos[1]
            control.y = control.height * pos[0]

    def render(self, surface, camera):
        for row in self.__cells:
            for cell in row:
                if cell is not None:
                    cell.render(surface, camera)

    def handleEvent(self, event):
        for row in self.__cells:
            for cell in row:
                if cell is not None:
                    cell.handleEvent(event)
