from game.ui import Control, Button, gui


class ScrollBar(Control):
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'
    __minHeight = 28
    __minWidth = 28

    def __init__(self, x: int, y: int, width: int, height: int, font):
        super().__init__(x, y, width, height)
        self.__minValue: int = 0
        self.__maxValue: int = 100
        self.__step: int = 5
        self.__direction = ScrollBar.HORIZONTAL
        self.__value: int = 0

        self.__minButton = Button(0, 0, ScrollBar.__minWidth, ScrollBar.__minHeight, font, '<')
        self.__minButton.name = self.name + '__minButton'
        self.__minButton.onClick = self.__onClickMin
        self.__minButton.parent = self

        self.__maxButton = Button(0, 0, ScrollBar.__minWidth, ScrollBar.__minHeight, font, '>')
        self.__maxButton.name = self.name + '__maxButton'
        self.__maxButton.onClick = self.__onClickMax
        self.__maxButton.parent = self

        self.__scrollButton = Button(0, 0, ScrollBar.__minWidth, ScrollBar.__minHeight, font, '')
        self.__scrollButton.name = self.name + '__scrollButton'
        self.__scrollButton.onMouseMove = self.__onMouseMove
        self.__scrollButton.parent = self

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
        self.__minValue = min(minValue, self.__maxValue - 1)
        self.refresh()

    @property
    def maxValue(self):
        return self.__maxValue

    @maxValue.setter
    def maxValue(self, maxValue: int):
        self.__maxValue = max(maxValue, self.__minValue + 1)
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

    def __onClickMax(self, event, sender):
        self.value += self.__step
        self.refresh()

    def __onMouseMove(self, event, sender):
        if sender.isPressed():
            # self.value += self.__step
            startScroll = self.__minButton.left + self.__minButton.width
            endScroll = self.rect.right - self.__maxButton.width

            mPos = (event.pos[0] - startScroll)

            offset = mPos * (endScroll - startScroll - self.__scrollButton.width) // (self.__maxValue - self.__minValue)

            print(event.pos, offset, mPos)
            self.refresh()

    def setActiveControl(self, control: Control):
        self.activeControl = control
        if self.parent is not None:
            self.parent.setActiveControl(control)

    def handleMouseEvent(self, event) -> bool:
        if self.rect.collidepoint(event.pos):
            for control in [self.__minButton, self.__scrollButton, self.__maxButton]:
                if control.handleMouseEvent(event):
                    return True
            # hacer handle del panel como tal
            return True
        return False

    def refresh(self):
        self.__minButton.width = ScrollBar.__minWidth
        self.__minButton.height = ScrollBar.__minHeight
        self.__scrollButton.width = ScrollBar.__minWidth
        self.__scrollButton.height = ScrollBar.__minHeight
        self.__maxButton.width = ScrollBar.__minWidth
        self.__maxButton.height = ScrollBar.__minHeight

        self.__minButton.top = self.rect.top
        self.__minButton.left = self.rect.left

        if self.direction == ScrollBar.HORIZONTAL:
            startScroll = self.__minButton.left + self.__minButton.width
            endScroll = self.rect.right - self.__maxButton.width

            offset = self.__value * (endScroll - startScroll - self.__scrollButton.width) // (
                        self.__maxValue - self.__minValue)

            self.__scrollButton.top = self.rect.top
            self.__minButton.top = self.rect.top

            self.rect.height = ScrollBar.__minHeight
            self.__minButton.left = self.rect.left
            self.__scrollButton.left = startScroll + offset

            self.__maxButton.top = self.rect.top
            self.__maxButton.left = endScroll
        self.__scrollButton.text = str(self.__value)

    def render(self, surface, camera):
        gui.renderElement(surface, self.rect, "panel")
        if self.direction == ScrollBar.HORIZONTAL:
            self.__minButton.render(surface, camera)
            self.__scrollButton.render(surface, camera)
            self.__maxButton.render(surface, camera)
