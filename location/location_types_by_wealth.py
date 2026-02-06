#location_types_by_wealth.py
from dataclasses import dataclass

from location.locations import (
    HQ, Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalWorkshop, Stash,
    Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe, Park, Museum, Library, VacantLot, 
    PoliceStation, SportsCentre, Holotheatre, ApartmentBlock,
    House, Warehouse, ResearchLab, Restaurant
)

@dataclass
class LocationTypes():
# Define minimum types of locations, per region,  by wealth level of that region
    location_types_by_wealth = {

        "Rich": [(CorporateStore, 1), (Museum, 1), (Library, 1), (Shop, 1), (ElectricalWorkshop, 1), (PoliceStation, 1), (SportsCentre, 1), (House, 1), (HQ, 4), (Park, 1), (ApartmentBlock, 1), (ResearchLab, 1), (Cafe, 1), (VacantLot, 1), (Restaurant, 3)],

        "Normal": [(Shop, 1), (Cafe, 1), (Park, 1), (Port, 1), (Nightclub, 1), (ElectricalWorkshop, 1), (Airport, 1), (Factory, 1), (HQ, 5), (PoliceStation, 1), (Holotheatre, 1), (SportsCentre, 1), (House, 1), (ApartmentBlock, 1), (VacantLot, 1), (MechanicalRepairWorkshop, 1), (Restaurant, 2)],

        "Poor": [(Stash, 1), (Factory, 1), (MechanicalRepairWorkshop, 1), (Shop, 1), (Mine, 1), (Powerplant, 1), (Port, 1), (Cafe, 1), (HQ, 8), (PoliceStation, 1), (House, 1), (ApartmentBlock, 1), (Warehouse, 1), (Park, 1), (VacantLot, 1), (Restaurant, 1)], 
    }
