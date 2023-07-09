from abc import ABC


class Order(ABC):

    def __init__(self, SKU_list):
        self.SKU_list = SKU_list
        self.total_volume = self.compute_total_volume()
        self.total_weight = self.compute_total_weight()

    def compute_total_volume(self):
        total_volume = 0
        for e in self.SKU_list:
            total_volume += e.volume
        return total_volume

    def compute_total_weight(self):
        total_weight = 0
        for e in self.SKU_list:
            total_weight += e.weight
        return total_weight
