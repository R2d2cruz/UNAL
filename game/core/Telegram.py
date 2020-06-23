class Telegram:
    def __init__(self, sender: int, receiver: int, msg: str, dispatchTime: float, extraInfo: {}):
        self.sender = sender
        self.receiver = receiver
        self.message = msg
        self.dispatchTime = dispatchTime
        self.extraInfo = extraInfo
