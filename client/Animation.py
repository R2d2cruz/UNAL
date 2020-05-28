class Animation:
    frames = []
    lapse = 0
    N = 0
    loop = False
    time = 0

    def __init__(self, frames, lapse=1, loop=False):
        self.frames = frames
        self.lapse = lapse
        self.N = len(frames)
        self.loop = loop

    def update(self, deltaTime: float):
        self.time += deltaTime

    def reset(self):
        self.time = 0

    def get_frame(self, loop):
        n = int(self.time / self.lapse)
        if loop and n > self.N:
            n = n % self.N
        return self.frames[n - 1]
