import queue

import core.EntityManager as EntityManager
from core.Telegram import Telegram
from core.Entity import Entity

__priorityQ = None
__deltaTime = float()


def init():
    global __priorityQ
    __priorityQ = queue.PriorityQueue()


def setDeltaTime(deltaTime: float):
    global __deltaTime
    __deltaTime = deltaTime


def messageDispatch(delay: float, sender: int, receiver: int, msg: str, extraInfo: dict = {}):
    telegram = Telegram(sender, receiver, msg, 0, extraInfo)
    pReceiver = EntityManager.getEntityById(receiver)
    if delay <= 0:
        discharge(pReceiver, telegram)
    else:
        global __priorityQ
        telegram.dispatchTime = __deltaTime + delay
        # noinspection PyUnresolvedReferences
        __priorityQ.put_nowait((telegram.dispatchTime, telegram))


def dispatchDelayedMessages(delayTime: float):
    global __priorityQ
    # noinspection PyUnresolvedReferences
    if 0 < delayTime < __priorityQ.queue[0][0]:
        # noinspection PyUnresolvedReferences
        telegram = __priorityQ.get_nowait()
        pReceiver = EntityManager.getEntityById(telegram.receiver)
        discharge(pReceiver, telegram)


def discharge(pReceiver: Entity, telegram: Telegram):
    pReceiver.onMessage(telegram)
