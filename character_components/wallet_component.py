#character_components.wallet_component.py


class WalletComponent:
    def __init__(self, owner, bankCardCash=0, cash=0):
        self.owner = owner
        self.bankCardCash = bankCardCash
        self.cash = cash

    def add_cash(self, amount):
        self.cash += amount

    def remove_cash(self, amount):
        if amount > self.cash:
            return False
        self.cash -= amount
        return True

    def add_bank(self, amount):
        self.bankCardCash += amount

    def remove_bank(self, amount):
        if amount > self.bankCardCash:
            return False
        self.bankCardCash -= amount
        return True
