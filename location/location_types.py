#location_types.py
from location.locations import MunicipalBuilding, Farm, PoliceStation, HQ, Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalWorkshop, Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe, Warehouse, ResearchLab, Museum, Library, SportsCentre, Holotheatre, Park, VacantLot, ApartmentBlock, House
#one very long line of imports, can we encapsulate this import in something to break it into shorter lines?

WORKPLACES = (Shop, CorporateStore, MechanicalRepairWorkshop, ElectricalWorkshop,
              Factory, Nightclub, Mine, Powerplant, Airport, Port, Cafe, Farm, 
              Warehouse, ResearchLab, Museum, Library, SportsCentre, Holotheatre)

PUBLIC_PLACES = (Museum, Library, SportsCentre, Holotheatre, Park, VacantLot)
RESIDENTIAL = (ApartmentBlock, House)