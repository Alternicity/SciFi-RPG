#location_types.py
from location import MunicipalBuilding, PoliceStation, HQ, Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalWorkshop, Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe, Warehouse, ResearchLab, Museum, Library, SportsCentre, Holotheatre, Park, VacantLot, ApartmentBlock, House


WORKPLACES = (Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalWorkshop,
              Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe,
              Warehouse, ResearchLab, Museum, Library, SportsCentre, Holotheatre)
#These now refer to actual classes not strings.

PUBLIC_PLACES = (Museum, Library, SportsCentre, Holotheatre, Park, VacantLot)
RESIDENTIAL = (ApartmentBlock, House)