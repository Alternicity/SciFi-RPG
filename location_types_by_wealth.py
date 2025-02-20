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

        "Rich": [(CorporateStore, 1), (Museum, 1), (Library, 1), (Shop, 1), (ElectricalRepairWorkshop, 1), (PoliceStation, 1), (SportsCentre, 1), (House, 1), (ApartmentBlock, 1), (ResearchLab, 1)],

        "Normal": [(Shop, 1), (Cafe, 1), (Park, 1), (Port, 1), (Nightclub, 1), (ElectricalRepairWorkshop, 1), (Airport, 1), (Factory, 1), (HQ, 1), (PoliceStation, 1), (Holotheatre, 1), (SportsCentre, 1), (House, 1), (ApartmentBlock, 1), (MechanicalRepairWorkshop, 1)],

        "Poor": [(Stash, 1), (Factory, 1), (MechanicalRepairWorkshop, 1), (Shop, 1), (Mine, 1), (Powerplant, 1), (Port, 1), (Cafe, 1), (HQ, 1), (PoliceStation, 1), (House, 1), (ApartmentBlock, 1), (Warehouse, 1), (VacantLot, 1)],
    }
