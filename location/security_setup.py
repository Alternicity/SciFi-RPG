# location.security_setup.py
from location.location_security import Security

def attach_default_security(location):
    location.security = Security(
        level=1,
        guards=[],
        difficulty_to_break_in=1,
        surveillance=False,
        alarm_system=False
    )
#You can later override this per subclass