class AttackAction:
    def __init__(self, attackingCountry, defendingCountry, nbAttackingDice):
        self._attackingCountry = attackingCountry
        self._defendingCountry = defendingCountry
        self._nbAttackingDice = nbAttackingDice
        self._nbDefendingDice = 2