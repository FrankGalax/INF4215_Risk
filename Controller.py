from MapFactory import *
from Player import *
from random import *
from AttackResult import *

class Controller:

    def __init__(self, mapName, firstPlayerName, secondPlayerName, firstPlayerAI, secondPlayerAI):
        self._mapFactory = MapFactory(mapName)
        self._map = self._mapFactory._build()
        self._nbStartingTroops = 40;
        self._players = [Player(firstPlayerName, self._nbStartingTroops), Player(secondPlayerName, self._nbStartingTroops)]
        self._ais = [firstPlayerAI, secondPlayerAI]

        self.CHOOSING_COUNTRY_STATE = 0
        self.PLACING_STARTING_TROOPS = 1
        self.PLAY_STATE = 2
        self.END_STATE = 3

        self._enterState = True

        self._gameState = self.CHOOSING_COUNTRY_STATE
        self._unownedCountries = []
        for country in self._map._countries:
            self._unownedCountries.append(country)
        self._turn = 0
        self._step = 0
        self._attackId = 0

        self._winner = None

    def play(self):
        while (self._gameState != self.END_STATE):
            self._print()
            self._update()
        print "*** WE HAVE A WINNER ***"
        print self._winner, "won! Congratulations"

    def _update(self):
        self._step += 1
        player = self._players[self._turn]
        otherPlayer = self._players[1 - self._turn]
        ai = self._ais[self._turn]
        otherAi = self._ais[1 - self._turn]

        if self._gameState == self.CHOOSING_COUNTRY_STATE:
            if self._enterState:
                print "*** CHOOSING STARTING COUNTRIES ***"
                self._enterState = False
            chosenCountry = ai.chooseStartingCountry(self._unownedCountries, player._ownedCountries, self._map._countries)
            self._unownedCountries.remove(chosenCountry)
            chosenCountry._changeOwner(player._name)
            player._addOwnedCountry(chosenCountry)

            if len(self._unownedCountries) == 0:
                self._gameState = self.PLACING_STARTING_TROOPS
                self._enterState = True

        elif self._gameState == self.PLACING_STARTING_TROOPS:
            if self._enterState:
                print "*** PLACING STARTING TROOPS ***"
                self._enterState = False
            if player._remainingTroopsToPlace > 0:
                placeTroopsAction = ai.placeStartingTroops(player._remainingTroopsToPlace, player._ownedCountries, self._map._countries)
                nb = 0
                for placeTroopAction in placeTroopsAction:
                    country = player._ownedCountries[placeTroopAction.countryName]
                    nbTroops = placeTroopAction.nbTroops
                    nb += nbTroops
                    country._addTroops(nbTroops)

                player._remainingTroopsToPlace -= nb

            if self._players[0]._remainingTroopsToPlace <= 0 and self._players[1]._remainingTroopsToPlace <= 0:
                self._enterState = True
                self._gameState = self.PLAY_STATE

        elif self._gameState == self.PLAY_STATE:
            if self._enterState:
                print "*** PLAYING ***"
                self._enterState = False
            placeTroopsAction = ai.placeTroops(3, player._ownedCountries, self._map._countries)
            for placeTroopAction in placeTroopsAction:
                country = player._ownedCountries[placeTroopAction.countryName]
                country._addTroops(placeTroopAction.nbTroops)
                print player._name, "placed", placeTroopAction.nbTroops, "troops in", placeTroopAction.countryName

            attackActions = ai.declareAttacks(player._ownedCountries, self._map._countries)
            for attackAction in attackActions:
                self._doAttack(attackAction, player, ai, otherPlayer, otherAi)

            self._winner = self._getWinner()
            if self._winner is not None:
                self._gameState = self.END_STATE

        self._turn = 1 - self._turn

    def _print(self):
        print "TURN", self._step
        self._players[0]._printTroops()
        self._players[1]._printTroops()

    def _doAttack(self, attackAction, attackingPlayer, attackingAi, defendingPlayer, defendingAi):
        attackingCountry = attackAction._attackingCountry
        defendingCountry = attackAction._defendingCountry

        print attackingCountry._name, "declared an attack on", defendingCountry._name, "!"
        attackResult = AttackResult(
            self._attackId,
            attackAction._attackingCountry,
            attackAction._defendingCountry,
            attackingPlayer,
            defendingPlayer,
            attackAction._nbAttackingDice,
            attackAction._nbDefendingDice
        )
        self._attackId += 1
        while attackingCountry._nbTroops > 1 and defendingCountry._nbTroops > 0 and attackAction._nbAttackingDice > 0:
            attackDices = []
            nbAttackingDices = min(attackAction._nbAttackingDice, attackingCountry._nbTroops)
            for i in xrange(nbAttackingDices):
                attackDices.append(self._rollDice())
            attackDices.sort(reverse=True)

            print "Attack dices :", attackDices

            attackAction.nbDefendingDice = defendingAi.decideNbDefendingDice(
                attackResult,
                defendingPlayer._ownedCountries,
                self._map._countries
            )
            if attackAction._nbDefendingDice > 2:
                attackAction._nbDefendingDice = 2
            elif attackAction._nbDefendingDice < 1:
                attackAction._nbDefendingDice = 1
            attackResult._nbDefendingDice = attackAction._nbDefendingDice

            defendingDices = []
            nbDefendingDices = min(attackAction._nbDefendingDice, defendingCountry._nbTroops)

            for i in xrange(nbDefendingDices):
                defendingDices.append(self._rollDice())
            defendingDices.sort(reverse=True)

            print "Defend dices :", defendingDices

            nbAttackingLost = 0
            nbDefendingLost = 0
            for i in xrange(len(defendingDices)):
                if i >= len(attackDices):
                    break
                if attackDices[i] > defendingDices[i]:
                    defendingCountry._removeTroops(1)
                    nbDefendingLost += 1
                    if defendingCountry._nbTroops == 0:
                        break
                else:
                    attackingCountry._removeTroops(1)
                    nbAttackingLost += 1
                    if attackingCountry._nbTroops == 1:
                        attackingAi.onAttackLost(attackResult, attackingPlayer._ownedCountries, self._map._countries)
                        defendingAi.onDefendWon(attackResult, defendingPlayer._ownedCountries, self._map._countries)
                        break
            attackResult._nbAttackingLost += nbAttackingDices
            attackResult._nbDefendingLost += nbDefendingLost

            if nbAttackingLost > 0:
                print attackingCountry._name, "lost", nbAttackingLost, "troops!"
            if nbDefendingLost > 0:
                print defendingCountry._name, "lost", nbDefendingLost, "troops!"

            attackAction.nbAttackingDice = attackingAi.decideNbAttackingDice(
                attackResult,
                attackingPlayer._ownedCountries,
                self._map._countries
            )
            if attackAction.nbAttackingDice > 3:
                attackAction.nbAttackingDice = 3
            elif attackAction.nbAttackingDice < 1:
                attackAction.nbAttackingDice = 1
            attackResult._nbAttackingDice = attackAction._nbAttackingDice

            print attackingCountry._name, ":", attackingCountry._nbTroops
            print defendingCountry._name, ":", defendingCountry._nbTroops
            print "---------------------"

        if defendingCountry._nbTroops == 0 and attackingCountry._nbTroops >= 2:
            print defendingCountry._name, "could not defend itself!", attackingPlayer._name, "takes", defendingCountry._name
            defendingCountry._changeOwner(attackingPlayer._name)
            nbTransfer = int(attackingCountry._nbTroops / 2)
            print nbTransfer, "troops transfered"
            defendingCountry._addTroops(nbTransfer)
            attackingCountry._removeTroops(nbTransfer)
            attackingPlayer._addOwnedCountry(defendingCountry)
            defendingPlayer._removeOwnedCountry(defendingCountry)
            attackingAi.onAttackWon(attackResult, attackingPlayer._ownedCountries, self._map._countries)
            defendingAi.onDefendLost(attackResult, defendingPlayer._ownedCountries, self._map._countries)
        elif attackAction._nbAttackingDice == 0:
            print attackingPlayer.name, "chose to cancel the attack"

    def _getWinner(self):
        firstCountryOwner = self._map._countries[0]._owner
        for country in self._map._countries:
            if country._owner != firstCountryOwner:
                return None
        return firstCountryOwner

    def _rollDice(self):
        return randint(1, 6)