import pygame

class Scene:
  KEYDOWN = {
      pygame.K_UP: "up",
      pygame.K_DOWN: "down",
      pygame.K_LEFT: "left",
      pygame.K_RIGHT: "right"
  }

  KEYUP = {
      pygame.K_UP: "stand_up",
      pygame.K_DOWN: "stand_down",
      pygame.K_LEFT: "stand_left",
      pygame.K_RIGHT: "stand_right"
  }

  def init(self):
    pass
  
  def onEnter(self, game):
    pass
  
  def onExit(self, game):
    pass

  def handleEvent(self, event):
    pass

  def update(self):
    pass

  def render(self, screen):
    pass