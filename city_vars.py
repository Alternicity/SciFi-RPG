#city_vars.py
#File to hold a class and object creation code to make accesible variables for other files to easily access
#get_game_state() is not a hack in a negative sense — it’s a valid service locator pattern


#"Resolve core references like region inside constructors using get_game_state() — but make sure upstream code
#  never hands it None accidentally."

class GameState:
    def __init__(self):
        GAME_MODE_PLAYER = "player"
        GAME_MODE_SIMULATION = "simulation"

        # NEW: determines whether the game is in player mode or simulation mode
        #Later: You Can Even Add a Command-Line Flag or Menu Option
        self.game_mode = GAME_MODE_PLAYER
        self.state = None
        self.civilians = []
        self.all_employees =  {}
        self.gangs = []
        self.all_street_gangs = []
        self.corporations = []
        self.homes = [] #needs populating
        self.public_places = [] #needs populating
        self.all_regions = []
        self.all_locations = []
        self.factions = [] #is not used
        self.all_characters = [] #oof...integrate characters = []
        self.state_staff = []
        corp_hqs = []
        self.player_character = None

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

        #placeholders
        hiring  =  {} #employers with job vacancies. Employer/character class wanted
        recruiting =  {} # gangs with vacancies to fill. Gang/type character wanted

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

    

    
