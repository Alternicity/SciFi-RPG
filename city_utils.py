# city_manager.py
#made to avoid circular import issue
from generators.generate import generate_city_data
  # Import the generate_city_data function

def regenerate_city_data():
    """Generate new city data by calling generate.py."""
    print("Regenerating city data...")
    #generate_city_data() temporarily disabled 
    print("City data regenerated.")
