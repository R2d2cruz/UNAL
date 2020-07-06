from game.ui import Control, Button, gui


class ScrollBar(Control):
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'

    def __init__(self, x: int, y: int, width: int, height: int, font):
        super().__init__(x, y, width, height)
        self.__minHeight = gui.skin['button'].styles['minWidth'] or 28
        self.__minWidth = gui.skin['button'].styles['minHeight'] or 28
        self.__minValue: int = 0
        self.__maxValue: int = 100
        self.__step: int = 5
        self.__direction = ScrollBar.HORIZONTAL
        self.__value: int = 0

        self.__minButton = Button(0, 0, self.__minWidth, self.__minHeight, font, '<')
        self.__minButton.name = self.name + '__minButton'
        self.__minButton.onClick = self.__onClickMin
        self.__minButton.parent = self

        self.__maxButton = Button(0, 0, self.__minWidth, self.__minHeight, font, '>')
        self.__maxButton.name = self.name + '__maxButton'
        self.__maxButton.onClick = self.__onClickMax
        self.__maxButton.parent = self

        self.__scrollButton = Button(0, 0, self.__minWidth, self.__minHeight, font, '')
        self.__scrollButton.name = self.name + '__scrollButton'
        self.__scrollButton.onMouseMove = self.__onMouseMove
        self.__scrollButton.parent = self

        self.__startScroll = 0
        self.__endScroll = 0

        self.activeControl = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: int):
        self.__value = max(min(value, self.__maxValue), self.__minValue)
        self.refresh()

    @property
    def minValue(self):
        return self.__minValue

    @minValue.setter
    def minValue(self, minValue: int):
        self.__minValue = minValue  # min(minValue, self.__maxValue - 1)
        self.__value = max(self.__value, self.__minValue)
        self.refresh()

    @property
    def maxValue(self):
        return self.__maxValue

    @maxValue.setter
    def maxValue(self, maxValue: int):
        self.__maxValue = maxValue  # max(maxValue, self.__minValue + 1)
        self.__value = min(self.__value, self.__maxValue)
        self.refresh()

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction
        self.refresh()

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, step):
        self.__step = step
        self.refresh()

    def __onClickMin(self, event, sender):
        self.value -= self.__step
        self.refresh()
        self.onChange(self)

    def __onClickMax(self, event, sender):
        self.value += self.__step
        self.refresh()
        self.onChange(self)

    def __onMouseMove(self, event, sender):
        if sender.isPressed():
            # self.value += self.__step

            mPos = (event.pos[0] - self.__startScroll)
            offset = mPos * (self.__endScroll - self.__startScroll - self.__scrollButton.width) // (self.__maxValue - self.__minValue)

            # print(event.pos, offset, mPos)
            self.refresh()
            self.onChange(self)

    def onMouseUp(self, event, sender):
        scale = (self.__maxValue - self.__minValue) / (self.__endScroll - self.__startScroll)
        # falta el ajuste por el ancho del boton pero eso puede esperar
        if self.direction == ScrollBar.HORIZONTAL:
            value = event.pos[0] - self.__startScroll
        elif self.direction == ScrollBar.VERTICAL:
            value = event.pos[1] - self.__startScroll
        self.value = self.__minValue + scale * value
        self.onChange(self)

    def setActiveControl(self, control: Control):
        self.activeControl = control
        if self.parent is not None:
            self.parent.setActiveControl(control)

    def handleMouseEvent(self, event) -> bool:
        if self.rect.collidepoint(event.pos):
            for control in [self.__minButton, self.__scrollButton, self.__maxButton]:
                if control.handleMouseEvent(event):
                    return True
            super().handleMouseEvent(event)
            return True
        return False

    def refresh(self):
        self.__minButton.width = self.__minWidth
        self.__minButton.height = self.__minHeight
        self.__scrollButton.width = self.__minWidth
        self.__scrollButton.height = self.__minHeight
        self.__maxButton.width = self.__minWidth
        self.__maxButton.height = self.__minHeight

        self.__minButton.top = self.rect.top
        self.__minButton.left = self.rect.left
        value = self.__value - self.minValue

        if self.direction == ScrollBar.HORIZONTAL:
            self.rect.height = self.__minHeight
            self.__scrollButton.top = self.rect.top
            self.__startScroll = self.__minButton.left + self.__minButton.width
            self.__endScroll = self.rect.right - self.__maxButton.width
            offset = value * (self.__endScroll - self.__startScroll - self.__scrollButton.width) // (
                        self.__maxValue - self.__minValue)
            self.__scrollButton.left = self.__startScroll + offset
            self.__maxButton.top = self.rect.top
            self.__maxButton.left = self.__endScroll

        elif self.direction == ScrollBar.VERTICAL:
            self.rect.width = self.__minWidth
            self.__scrollButton.left = self.rect.left
            self.__startScroll = self.__minButton.top + self.__minButton.height
            self.__endScroll = self.rect.bottom - self.__maxButton.height
            offset = value * (self.__endScroll - self.__startScroll - self.__scrollButton.height) // (
                        self.__maxValue - self.__minValue)
            self.__scrollButton.top = self.__startScroll + offset
            self.__maxButton.top = self.__endScroll
            self.__maxButton.left = self.rect.left

        # self.__scrollButton.text = str(self.__value)

    def render(self, surface, camera):
        gui.renderElement(surface, self.rect, "panel")
        self.__minButton.render(surface, camera)
        self.__scrollButton.render(surface, camera)
        self.__maxButton.render(surface, camera)

    def onChange(self, sender):
        pass
