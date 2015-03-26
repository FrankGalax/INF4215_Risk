class AttackResult:
    def __init__(self, attackId, attackingCountry, defendingCountry, attackingPlayer, defendingPlayer, nbAttackingDice, nbDefendingDice):
        self._attackId = attackId
        self._nbAttackingLost = 0
        self._nbDefendingLost = 0
        self._attackingCountry = attackingCountry
        self._defendingCountry = defendingCountry
        self._attackingPlayer = attackingPlayer
        self._defendingPlayer = defendingPlayer
        self._nbAttackingDice = nbAttackingDice
        self._nbDefendingDice = nbDefendingDice

    def getAttackId(self):
        return self._attackId

    def getNbAttackingLost(self):
        return self._nbAttackingLost

    def getNbDefendingLost(self):
        return self._nbDefendingLost

    def getAttackingCountry(self):
        return self._attackingCountry

    def getDefendingCountry(self):
        return self._defendingCountry

    def getAttackingPlayer(self):
        return self._attackingPlayer

    def getDefendingPlayer(self):
        return self._defendingPlayer

    def getNbAttackingDice(self):
        return self._nbAttackingDice

    def getNbDefendingDice(self):
        return self._nbDefendingDice