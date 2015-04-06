from random import Random
from AI import AI
from AttackAction import AttackAction
from MoveAction import MoveAction
from PlaceTroopsAction import PlaceTroopsAction

__author__ = 'Nicolas'


class RandomAI(AI):

    def __init__(self):
        self.random = Random()
        self.random.seed()

    # Choose a starting country one at the time
    #
    # remainingCountries : the countries that are not chosen yet
    # ownedCountries : the countries that you own so far
    # allCountries : all countries
    #
    # return : one element of the remainingCountries list
    def chooseStartingCountry(self, remainingCountries, ownedCountries, allCountries):
        return self.random.choice(remainingCountries)

    # Place troops before the games begins. You can place only a portion of the available
    # troops. This method will be called again if you still have troops to be placed
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    def placeStartingTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        return self.placeTroops(nbTroopsToPlace, ownedCountries, allCountries)

    # Declare attacks on the other countries. You need to check if the defending country is
    # not yours, or your attack declaration will be ignored
    #
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of AttackAction.
    def declareAttacks(self, ownedCountries, allCountries):
        allPossibilities = []
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            for neighbour in country.getNeighbours():
                if neighbour.getOwner() != country.getOwner():
                    allPossibilities.append(AttackAction(country, neighbour, 3))

        return self.random.sample(allPossibilities, self.random.randint(0, len(allPossibilities)))

    # Place troops at the start of your turn. You need to place all available troops at one
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    def placeTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        placeTroopsAction = []
        rest = nbTroopsToPlace
        for countryName in ownedCountries:
            nbTroopsAtThisCountry = 1
            placeTroopsAction.append(PlaceTroopsAction(countryName, nbTroopsAtThisCountry))
            rest -= nbTroopsAtThisCountry

        while rest > 0:
            troopAction = self.random.choice(placeTroopsAction)
            toAdd = self.random.randint(1, rest)
            troopAction.nbTroops += toAdd
            rest -= toAdd

        return placeTroopsAction

    # Move troops after attacking. You can only move one per turn
    #
    # turnAttackResults : the result of all the attacks you declared this turn
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a lsingle MoveTroopAction
    def moveTroops(self, turnAttackResults, ownedCountries, allCountries):
        possibleMoves = []
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            if country.getNbTroops() <= 1:
                continue

            for neighbour in country.getNeighbours():
                if neighbour.getOwner() == country.getOwner():
                    possibleMoves.append(MoveAction(country, neighbour, country.getNbTroops()-1))

        if len(possibleMoves) > 0:
            return self.random.choice(possibleMoves)
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
        return self.random.randint(1, startCountry.getNbTroops() - 1)

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

