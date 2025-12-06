import random
from objects.InWorldObjects import Wallet

# Default base amounts by character type
BASE_AMOUNTS = {
    "Boss": 3000,
    "Captain": 1000,
    "GangMember": 300,

    "CEO": 4000,
    "Manager": 1000,
    "CorporateSecurity": 400,
    "Employee": 200,
    "Accountant": 2000,
    "CorporateAssasin": 2500,
    
    "VIP": 5000,
    "Detective": 1500,
    "RiotCop": 300,
    "Taxman": 1500,

    "Babe": 100,
    "Civilian": 100,
    "Child": 5,
    "Influencer": 1500,
    "Adepta": 200,
}

def generate_wallet(character_type="civilian", cash_ratio=0.2, variance=0.5):
    """Return a Wallet with randomized bank and cash based on character type."""
    base = BASE_AMOUNTS.get(character_type.lower(), 200)
    total = int(base + base * random.uniform(-variance, variance))
    cash = int(total * cash_ratio)
    card = total - cash
    return Wallet(cash=cash, bankCardCash=card)



    #possibly deprecated function, pasted here
def get_total_money(self):
    """Return the total money available (cash + bank card)."""
    return self.wallet.total_balance()