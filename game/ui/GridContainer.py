from . import gui
from .Container import Container
from .Control import Control


class GridContainer(Container):
    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        super().__init__(x, y, width, height)
        self.__cells = []
        self.__rows = 0
        self.__cols = 0
        self.__numControls = 0

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

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

    def handleMouseEvent(self, event) -> bool:
        if self.rect.collidepoint(event.pos):
            for row in self.__cells:
                for cell in row:
                    if cell is not None and issubclass(type(cell), Control):
                        if cell.handleMouseEvent(event):
                            return True
            # hacer handle del panel como tal
            return True
        return False

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
