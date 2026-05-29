#location_components.power_components.py

class PowerComponent:

    def __init__(self):

        # Consumer state
        self.requires_power = False
        self.has_power = False

        # Supplier state
        self.generates_power = False
        self.is_generating = False

        # Network
        self.power_supplier = None
        self.connected_consumers = []

        """NOTE:
        `is_operational` currently refers to BOTH:
            - whether a building itself has functioning power
            - whether a power supplier (e.g. Powerplant) is actively generating power

        These are conceptually different.

        Future refactor:
            Rename/split into:
                is_generating_power   # for suppliers
                has_power             # for consumers

        Current implementation is acceptable for early simulation prototyping,
        but this dual meaning will become confusing as infrastructure expands.
        """
