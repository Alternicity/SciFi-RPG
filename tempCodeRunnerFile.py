# main.py

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from menu_utils import main_menu
from game import game
from create_game_state import get_game_state



# Only define these globals once
game_state = None
all_regions = None
factions = None