from AttackAction import *
from PlaceTroopsAction import *

# WARNING : IT IS FORBIDDEN TO USE ANY CLASS MEMBER THAT STARTS WITH _
# IN THE AI CLASS
class AI:
    def __init__(self):
        pass
    # default be
    def chooseStartingCountry(self, remainingCountries, ownedCountries, allCountries):
        return remainingCountries[0]

    def placeStartingTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        placeTroopsAction = []
        rest = nbTroopsToPlace
        for countryName in ownedCountries:
            nbTroopsAtThisCountry = nbTroopsToPlace / len(ownedCountries)
            placeTroopsAction.append(PlaceTroopsAction(countryName, nbTroopsAtThisCountry))
            rest -= nbTroopsAtThisCountry

        placeTroopsAction[0].nbTroops += rest
        return placeTroopsAction

    def declareAttacks(self, ownedCountries, allCountries):
        attackActions = []
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            for neighbour in country.getNeighbours():
                if neighbour.getOwner() != country.getOwner():
                    attackActions.append(AttackAction(country, neighbour, 3))
        return attackActions

    def placeTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        placeTroopsAction = []
        nb = nbTroopsToPlace
        while nb > 0:
            for countryName in ownedCountries:
                country = ownedCountries[countryName]
                neighbourToAttack = False
                for neighbour in country.getNeighbours():
                    if neighbour.getOwner() != country.getOwner():
                        neighbourToAttack = True
                if not neighbourToAttack:
                    continue
                placed = False
                for placeTroopAction in placeTroopsAction:
                    if placeTroopAction.countryName == countryName:
                        placeTroopAction.nbTroops += 1
                        placed = True
                        break
                if not placed:
                    placeTroopsAction.append(PlaceTroopsAction(countryName, 1))
                nb -= 1
                if nb == 0:
                    break
        return placeTroopsAction

    def moveTroops(self):
        pass

    def decideNbAttackingDice(self, attackResult, ownedCountries, allCountries):
        return 3

    def decideNbDefendingDice(self, attackResult, ownedCountries, allCountries):
        return 2

    def onAttackWon(self, attackResult, ownedCountries, allCountries):
        pass

    def onAttackLost(self, attackResult, ownedCountries, allCountries):
        pass

    def onDefendWon(self, attackResult, ownedCountries, allCountries):
        pass

    def onDefendLost(self, attackResult, ownedCountries, allCountries):
        pass