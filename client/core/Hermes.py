import queue

from .Entity import Entity
from .EntityManager import entityManager
from .Telegram import Telegram


class _Hermes: 

    def __init__(self):
        self.__deltaTime = float()
        self.__priorityQ = queue.PriorityQueue()


    def setDeltaTime(self, deltaTime: float):
        self.__deltaTime = deltaTime


    def messageDispatch(self, delay: float, sender: int, receiver: int, msg: str, extraInfo: dict = {}):
        telegram = Telegram(sender, receiver, msg, 0, extraInfo)
        pReceiver = entityManager.getEntityById(receiver)
        if delay <= 0:
            self.discharge(pReceiver, telegram)
        else:
            telegram.dispatchTime = self.__deltaTime + delay
            # noinspection PyUnresolvedReferences
            self.__priorityQ.put_nowait((telegram.dispatchTime, telegram))


    def dispatchDelayedMessages(self, delayTime: float):
        # noinspection PyUnresolvedReferences
        if 0 < delayTime < self.__priorityQ.queue[0][0]:
            # noinspection PyUnresolvedReferences
            telegram = self.__priorityQ.get_nowait()
            pReceiver = entityManager.getEntityById(telegram.receiver)
            self.discharge(pReceiver, telegram)

    @staticmethod
    def discharge(pReceiver: Entity, telegram: Telegram):
        pReceiver.onMessage(telegram)

hermes = _Hermes()
