from abc import ABC


class Part(ABC):

    def __init__(self, SKU, weight, volume):
        self.SKU = SKU
        self.weight = weight
        self.volume = volume
