import queue

from core.Telegram import Telegram
from core.EntityManager import EntityManager
from core.Entity import Entity


class Hermes:
    entManager = None

    def __init__(self, entManager: EntityManager):
        self.__priorityQ = queue.PriorityQueue()
        Hermes.entManager = entManager


    def messageDispatch(self, deltaTime: float, delay: float, sender: int, receiver: int, msg: str, extraInfo: str = ""):
        telegram = Telegram(sender, receiver, msg, 0, extraInfo)
        pReceiver = Hermes.entManager.getEntityById(receiver)
        if delay <= 0:
            self.discharge(pReceiver, telegram)
        else:
            telegram.dispatchTime = deltaTime + delay
            self.__priorityQ.put_nowait((telegram.dispatchTime, telegram))

    def dispatchDelayedMessages(self, delayTime: float):
        if 0 < delayTime < self.__priorityQ.queue[0][0]:
            telegram = self.__priorityQ.get_nowait()
            pReceiver = Hermes.entManager.getEntityById(telegram.receiver)
            self.discharge(pReceiver, telegram)

    def discharge(self, pReceiver: Entity, telegram: Telegram):
        pass
