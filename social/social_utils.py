#social.social_utils.py

def get_socially_favoured(self):
    if self.partner:
        return self.partner
    if hasattr(self, "get_close_friend"):
        return self.get_close_friend()
    #placeholder code, this funciton can also call:
    #get_close_friend()

    #get_friend()

    #get_partner()

    #get_pet()

    return None #to be granular, maybe this function should return an identity and presumed location?

