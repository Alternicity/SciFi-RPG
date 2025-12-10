#city_vars.py

#File to hold a class and object creation code to make accesible variables for other files to easily access
#get_game_state() is not a hack in a negative sense — it’s a service locator pattern

#"Resolve core references like region inside constructors using get_game_state() — but make sure upstream code
#  never hands it None accidentally."

MAX_CIVILIANS_PER_LOCATION = 5
CIVILIANS_PER_REGION = 15
SHOP_PATRONS_MIN = 2
SHOP_PATRONS_MAX = 4

class GameState:
    def __init__(self):
        GAME_MODE_PLAYER = "player"
        GAME_MODE_SIMULATION = "simulation"

        self.game_mode = GAME_MODE_PLAYER
        self.tick = 0 # 1 hour
        self.day = 1

        self.primary = None
        self.secondary = None
        self.civilian_test = None
        self.debug_npcs = {}

        self.state = None
        self.civilians = []
        self.families = []
        self.extant_family_names = []
        self.all_employees =  {}
        self.gangs = []
        self.all_street_gangs = []
        self.corporations = []
        self.homes = [] #might need populating
        self.public_places = [] #might need populating
        self.all_regions = []
        self.all_locations = []
        self.factions = [] #is not used
        self.all_characters = [] #oof...integrate characters = []
        self.state_staff = []
        self.corp_hqs = []
        self.player_character = None
        self.orphans = []
        self.downtown_gangs = []
        self.northville_gangs = []
        self.easternhole_gangs = []
        self.westborough_gangs = []
        self.southville_gangs = []
        self.downtown_corps = []
        self.northville_corps = []
        self.easternhole_corps = []
        self.westborough_corps = []
        self.southville_corps = []
        self.municipal_buildings = {}  # Format: {region_name: MunicipalBuilding}
        self.all_shops = []
        #placeholders
        hiring  =  {} #employers with job vacancies. Employer/character class wanted
        recruiting =  {} # gangs with vacancies to fill. Gang/type character wanted

    def advance_tick(self):
        self.tick += 1
        if self.tick % 24 == 0:# e.g., 24 ticks = 1 day
            self.day += 1

    def set_state(self, state):
        self.state = state #State object is initialized as State, but that becomes undefined here

    def add_employee(self, faction_name, employee):
        if faction_name not in self.all_employees:
            self.all_employees[faction_name] = []  # Initialize list if faction not present
        self.all_employees[faction_name].append(employee)


    def add_civilian(self, civilian):
        self.civilians.append(civilian) #note there is also a GeneralPopulation faction, used to make some code work

    def add_gang(self, gang):
        self.gangs.append(gang)

    def add_corporation(self, corporation):
        self.corporations.append(corporation)
        self.factions.append(corporation)

    def add_state_staff(self, staff_member):
        self.state_staff.append(staff_member)

    

    
