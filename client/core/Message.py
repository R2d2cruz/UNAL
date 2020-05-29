class Message:
    DISCONNECTED = 'disconnected'

    def __init__(self, type, data=None):
        self.type = self.DISCONNECTED
        self.data = data
