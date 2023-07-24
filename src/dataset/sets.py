import sys


class _Sets:
    def __init__(self):
        self.part_numbers = 3927
        # n_suppliers = 570
        self.n_suppliers = 30
        # LTL_zones = 34
        self.LTL_zones = 10
        self.n_transportation_modes = 3
        self.horizon = 10  # days
        self.n_possible_orders = 6
        self.types_of_load_carrier_storage_area = 3
        self.n_weight_classes_LTL = 10
        self.n_weight_classes_CES = 10
        self.n_orders_on_six_months = 11400
        self.ULC = 28
        self.SLC = 419


instance = sys.modules.setdefault("sets", _Sets())


def get_instance():
    return instance
