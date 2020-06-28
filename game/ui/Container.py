from .Control import Control
from ..core.misc import getFirst


class Container(Control):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.children = []
        self.__padding = 10
        self.activeControl = None

    @property
    def padding(self):
        return self.__padding

    @padding.setter
    def padding(self, padding):
        self.__padding = padding
        self.refresh()

    def addControl(self, control: Control):
        self.children.append(control)
        control.parent = self
        control.zIndex = len(self.children)
        self.children.sort(key=lambda x: x.zIndex, reverse=False)
        self.refresh()

    def removeControl(self, control: Control):
        control.parent = None
        self.children.remove(control)

    def setActiveControl(self, control: Control):
        self.activeControl = control
        if self.parent is not None:
            self.parent.setActiveControl(control)

    def render(self, surface, camera):
        # gui.renderElement(surface, self.rect, "panel")
        for control in self.children:
            control.render(surface, camera)

    def handleKeyEvent(self, event) -> bool:
        if self.activeControl:
            return self.activeControl.handleKeyEvent(event)
        return False

    def handleMouseEvent(self, event) -> bool:
        if self.rect.collidepoint(event.pos):
            for control in reversed(self.children):
                if issubclass(type(control), Control) and control.handleMouseEvent(event):
                    return True
            # hacer handle del panel como tal
            return self.parent is not None
        return False

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
            if issubclass(type(control), Container):
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
            if issubclass(type(control), Container):
                control = control.getControlByName(controlName)
                if control is not None:
                    return control
