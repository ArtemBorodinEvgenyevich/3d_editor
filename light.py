from vector import Normalize


class Light:
    def __init__(self, position):
        self.position = position
        self.direction = Normalize(self.position)
