from random import Random
from AttackAction import AttackAction
from MoveAction import MoveAction
from PlaceTroopsAction import PlaceTroopsAction
from RandomAI import RandomAI

__author__ = 'Nicolas'

class MLAgent(RandomAI):

    def __init__(self):
        self._nbVictories = 0
        self._lastGameWon = False

        self.Q_ChooseAction = 0
        self.Q_MoveAction = 1
        self.Q_AttackAction = 2
        self.Q_PlaceAction = 3
        self.Q_AttackWonMoveAction = 4

        self.nbQ = {self.Q_ChooseAction: {}, self.Q_MoveAction: {}, self.Q_AttackAction: {}, self.Q_PlaceAction: {}, self.Q_AttackWonMoveAction: {}}
        self.q = {self.Q_ChooseAction: {}, self.Q_MoveAction: {}, self.Q_AttackAction: {}, self.Q_PlaceAction: {}, self.Q_AttackWonMoveAction: {}}
        self.alpha = {self.Q_ChooseAction: {}, self.Q_MoveAction: {}, self.Q_AttackAction: {}, self.Q_PlaceAction: {}, self.Q_AttackWonMoveAction: {}}

        self.random = Random()
        self.random.seed()

        self.executedActions = []

    def countQ(self, actionState, state, action):
        if state in self.nbQ[actionState]:
            for (sAction, value) in self.nbQ[actionState][state]:
                if sAction == action:
                    return value
        return 0

    def alphaValue(self, actionState, state, action):
        if state in self.alpha[actionState]:
            for (sAction, value) in self.alpha[actionState][state]:
                if sAction == action:
                    return value
        return 1.0

    def QValue(self, actionState, state, action):
        if state in self.q[actionState]:
            for (sAction, value) in self.q[actionState][state]:
                if sAction == action:
                    return value
        return 0.0

    def setQ(self, actionState, state, action, value):
        if state not in self.q[actionState]:
            self.q[actionState][state] = []

        index = -1
        for i, (sAction, value) in enumerate(self.q[actionState][state]):
            if sAction == action:
                self.q[actionState][state][i] = (action, value)
                index = i
                break

        if index == -1:
            self.q[actionState][state].append((action, value))

        if state not in self.nbQ[actionState]:
            self.nbQ[actionState][state] = []

        if index != -1:
            self.nbQ[actionState][state][index] = (action, self.nbQ[actionState][state][index][1] + 1)
        else:
            self.nbQ[actionState][state].append((action, 1))

        if state not in self.alpha[actionState]:
            self.alpha[actionState][state] = []

        if index != -1:
            self.alpha[actionState][state][index] = (action, self.alpha[actionState][state][index][1] * 0.99)
        else:
            self.alpha[actionState][state].append((action, 1.0))

    def chooseBestAction(self, actionState, state, notEvaluatedAction):
        if state in self.q[actionState]:
            action = max(self.q[actionState][state], key=lambda item:item[1])[0]
            if action > 0.0:
                return action

        return notEvaluatedAction

    # Choose a starting country one at the time
    #
    # remainingCountries : the countries that are not chosen yet
    # ownedCountries : the countries that you own so far
    # allCountries : all countries
    #
    # return : one element of the remainingCountries list
    def chooseStartingCountry(self, remainingCountries, ownedCountries, allCountries):
        state = (tuple([country.getName() for country in remainingCountries]),
                 tuple([country for country in ownedCountries]))

        default = RandomAI.chooseStartingCountry(self, remainingCountries, ownedCountries, allCountries)
        action = self.chooseBestAction(self.Q_ChooseAction, state, default)

        self.executedActions.append((self.Q_ChooseAction, state, action))
        return action

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
        # The code below is bad, but at least I can get my name
        me = ""
        for country in ownedCountries:
            me = ownedCountries[country].getOwner()
            break

        state = tuple([(country.getName(), country.getNbTroops(), country.getOwner() == me) for country in allCountries])

        defaultActions = RandomAI.declareAttacks(self, ownedCountries, allCountries)

        actions = self.chooseBestAction(self.Q_AttackAction, state, defaultActions)
        self.executedActions.append((self.Q_AttackAction, state, actions))

        return actions

    # Place troops at the start of your turn. You need to place all available troops at one
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    def placeTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        state = tuple([country for country in ownedCountries])

        placeTroopsAction = RandomAI.placeTroops(self, nbTroopsToPlace, ownedCountries, allCountries)

        action = self.chooseBestAction(self.Q_PlaceAction, state, placeTroopsAction)
        self.executedActions.append((self.Q_PlaceAction, state, action))

        return action

    # Move troops after attacking. You can only move one per turn
    #
    # turnAttackResults : the result of all the attacks you declared this turn
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a lsingle MoveTroopAction
    def moveTroops(self, turnAttackResults, ownedCountries, allCountries):
        me = ""
        for country in ownedCountries:
            me = ownedCountries[country].getOwner()
            break

        state = tuple([(country.getName(), country.getNbTroops(), country.getOwner() == me) for country in allCountries])

        default = RandomAI.moveTroops(self, turnAttackResults, ownedCountries, allCountries)

        action = self.chooseBestAction(self.Q_MoveAction, state, default)
        self.executedActions.append((self.Q_MoveAction, state, action))

        return action

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
        startNbOfEnnemies = 0
        for country in startCountry.getNeighbours():
            if country.getOwner() != startCountry.getOwner():
                startNbOfEnnemies += country.getNbTroops()

        endNbOfEnnemies = 0
        for country in endCountry.getNeighbours():
            if country.getOwner() != startCountry.getOwner():
                endNbOfEnnemies += country.getNbTroops()

        state = (startCountry.getNbTroops, startNbOfEnnemies, endNbOfEnnemies)

        default = RandomAI.decideNbTransferingTroops(self, attackResult, startCountry, endCountry, ownedCountries, allCountries)

        action = self.chooseBestAction(self.Q_AttackWonMoveAction, state, default)
        self.executedActions.append((self.Q_AttackWonMoveAction, state, action))

        return action

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
        self._learnAtEnd(1.0)
        self._nbVictories += 1
        self._lastGameWon = True
            #self.setQ(actionState ,state, action,
            #             self.QValue(actionState, state, action) +
            #             self.alphaValue(actionState, state, action) * (reward + gamma * agent.getMaxQValue(newState) -
            #             self.QValue(actionState, state, action)))

    # Called when your AI lost the game
    #
    # allCountries : all countries, you own no countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onGameLost(self, allCountries):
        self._learnAtEnd(-1.0)
        self._lastGameWon = False

    def GetNbVictories(self):
        return self._nbVictories

    def HasWon(self):
        return self._lastGameWon

    def _learnAtEnd(self, reward):
        for (actionState, state, action) in self.executedActions:
            self.setQ(actionState ,state, action,
                         self.QValue(actionState, state, action) +
                         self.alphaValue(actionState, state, action) * reward)
        self.executedActions = []
