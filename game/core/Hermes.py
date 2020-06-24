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

    def messageDispatch(self, delay: float, sender: int, receiver: int, msg: str, extraInfo: dict = None):
        telegram = Telegram(sender, receiver, msg, 0, extraInfo)
        receiver = entityManager.getEntityById(receiver)
        if delay <= 0:
            self.discharge(receiver, telegram)
        else:
            telegram.dispatchTime = self.__deltaTime + delay
            # noinspection PyUnresolvedReferences
            self.__priorityQ.put_nowait((telegram.dispatchTime, telegram))

    def dispatchDelayedMessages(self, delayTime: float):
        # noinspection PyUnresolvedReferences
        if 0 < delayTime < self.__priorityQ.queue[0][0]:
            # noinspection PyUnresolvedReferences
            telegram = self.__priorityQ.get_nowait()
            receiver = entityManager.getEntityById(telegram.receiver)
            self.discharge(receiver, telegram)

    @staticmethod
    def discharge(receiver: Entity, telegram: Telegram):
        if receiver is not None:
            receiver.onMessage(telegram)
        else:
            print('Enviando mensaje a entidad nula. ID:', telegram.receiver, telegram.message)


hermes = _Hermes()
