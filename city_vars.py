#city_vars.py
#File to hold a class and object creation code to make accesible variables for other files to easily access


#Actual code
class GameState:
    def __init__(self):
        self.state = None
        self.civilians = []
        self.all_employees =  {}
        self.gangs = []
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

    def add_state_staff(self, staff_member):
        self.state_staff.append(staff_member)

    

# Initialize the game_state globally
game_state = GameState()