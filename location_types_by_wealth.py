#location types by wealth
from dataclasses import dataclass

from location import (
    HQ, Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalRepairWorkshop, Stash,
    Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe, Park, Museum, Library, VacantLot, 
    PoliceStation, SportsCentre, Holotheatre, ApartmentBlock,
    House, Warehouse, ResearchLab
)

@dataclass
class LocationTypes():
# Define minimum types of locations, per region,  by wealth level of that region
    location_types_by_wealth = {

        "Rich": [(CorporateStore, 2), (Museum, 1), (Library, 1), (Shop, 3), (ElectricalRepairWorkshop, 1), (PoliceStation, 1), (SportsCentre, 1), (House, 2), (ApartmentBlock, 1), (ResearchLab, 1)],

        "Normal": [(Shop, 3), (Cafe, 3), (Park, 1), (Port, 1), (Nightclub, 1), (ElectricalRepairWorkshop, 1), (Airport, 1), (Factory, 2), (HQ, 2), (PoliceStation, 1), (Holotheatre, 1), (SportsCentre, 1), (House, 1), (ApartmentBlock, 1), (MechanicalRepairWorkshop, 1)],

        "Poor": [(Stash, 5), (Factory, 2), (MechanicalRepairWorkshop, 1), (Shop, 3), (Mine, 1), (Powerplant, 1), (Port, 1), (Cafe, 3), (HQ, 3), (PoliceStation, 1), (House, 1), (ApartmentBlock, 1), (Warehouse, 2), (VacantLot, 3)],
    }
