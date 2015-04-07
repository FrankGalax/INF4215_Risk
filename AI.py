from AttackAction import *
from PlaceTroopsAction import *
from MoveAction import *

# WARNING : IT IS FORBIDDEN TO USE ANY CLASS MEMBER THAT STARTS WITH _
# IN THE AI CLASS
class AI:
    def __init__(self):
        pass

    # Choose a starting country one at the time
    #
    # remainingCountries : the countries that are not chosen yet
    # ownedCountries : the countries that you own so far
    # allCountries : all countries
    #
    # return : one element of the remainingCountries list
    #
    # default behaviour : chooses the first country of the list
    def chooseStartingCountry(self, remainingCountries, ownedCountries, allCountries):
        return remainingCountries[0]

    # Place troops before the games begins. You can place only a portion of the available
    # troops. This method will be called again if you still have troops to be placed
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    #
    # default behaviour : split the troops equaly between all owned countries. The
    # remainder is place in the first owned country
    def placeStartingTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        placeTroopsAction = []
        rest = nbTroopsToPlace
        for countryName in ownedCountries:
            nbTroopsAtThisCountry = nbTroopsToPlace / len(ownedCountries)
            placeTroopsAction.append(PlaceTroopsAction(countryName, nbTroopsAtThisCountry))
            rest -= nbTroopsAtThisCountry

        placeTroopsAction[0].nbTroops += rest
        return placeTroopsAction

    # Declare attacks on the other countries. You need to check if the defending country is
    # not yours, or your attack declaration will be ignored
    #
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of AttackAction.
    #
    # default behaviour : Declare an attack for each country that has a neighbour country owned
    # by the other player
    def declareAttacks(self, ownedCountries, allCountries):
        attackActions = []
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            for neighbour in country.getNeighbours():
                if neighbour.getOwner() != country.getOwner():
                    attackActions.append(AttackAction(country, neighbour, 3))
        return attackActions

    # Place troops at the start of your turn. You need to place all available troops at one
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    #
    # default behaviour : split the troops equaly between all owned countries that have a
    # neighbour country owned by an enemy player
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

    # Move troops after attacking. You can only move one per turn
    #
    # turnAttackResults : the result of all the attacks you declared this turn
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a lsingle MoveTroopAction
    #
    # default behaviour : choose a country that has more than 1 troops, move all
    # troops except 1 to a neighbour country that has a neighbour enemy country
    def moveTroops(self, turnAttackResults, ownedCountries, allCountries):
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            if country.getNbTroops() <= 1:
                continue

            for neighbour in country.getNeighbours():
                if neighbour.getOwner() != country.getOwner():
                    continue
                for secondNeighbour in neighbour.getNeighbours():
                    if secondNeighbour == country:
                        continue
                    if secondNeighbour.getOwner() != country.getOwner():
                        return MoveAction(country, neighbour, country.getNbTroops()-1)
        return None

    # Decide the amount of attacking dice while attacking
    #
    # attackResult : the result of the pending attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 0 and 3, 0 means that you want to cancel the attack
    #
    # default behaviour : always choose 3
    def decideNbAttackingDice(self, attackResult, ownedCountries, allCountries):
        return 3

    # Decide the amount of defending dice while defending
    #
    # attackResult : the result of the pending attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 1 and 2
    #
    # default behaviour : always choose 2
    def decideNbDefendingDice(self, attackResult, ownedCountries, allCountries):
        return 2

    # Decide the amount of troops to be transfered to the new country after winning a battle
    #
    # attackResult : the result of the attack
    # startCountry : the country to move from
    # endCountry : the country to move to
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 1 and the amount of troops in startCountry
    #
    # default behaviour : move half of the troops to the new country
    def decideNbTransferingTroops(self, attackResult, startCountry, endCountry, ownedCountries, allCountries):
        return int(startCountry.getNbTroops()/2)

    # Called when your AI wins an attack
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onAttackWon(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI loses an attack. AKA the attack finished because you only have 1 troop left in
    # the attacking country
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onAttackLost(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI cancels an attack. AKA you return 0 as the number of attacking dice
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onAttackCanceled(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI succeeds to defend a territory.
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onDefendWon(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI fails to defend a territory.
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onDefendLost(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI quits defending because the attacker canceled the attack.
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onDefendCanceled(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI wins the game
    #
    # allCountries : all countries, you own all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onGameWon(self, allCountries):
        pass

    # Called when your AI lost the game
    #
    # allCountries : all countries, you own no countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onGameLost(self, allCountries):
        pass