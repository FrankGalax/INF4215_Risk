from AI import *
import csv
from random import Random
from collections import deque

# WARNING : IT IS FORBIDDEN TO USE ANY CLASS MEMBER THAT STARTS WITH _
# IN THE AI CLASS
class FMAI(AI):
    def __init__(self, executionFactor):
        self.executionFactor = executionFactor
        self.random = Random()
        self.random.seed()

        self.loadChooseStartingCountry()
        self.loadDecideNbAttackingDice()
        self.loadPlaceStartingTroops()
        self.loadPlaceTroops()
        self.loadDeclareAttacks()

        self.chosenStartingCountries = []
        self.currentAttackChosenNbAttackingDice = []
        self.chosenPlaceTroops = []
        self.currentChosenDeclareAttack = []

    def loadChooseStartingCountry(self):
        self.cscFileName = "fm_choose_starting_country.csv"
        open(self.cscFileName, "a").close()
        cscFile = open(self.cscFileName, "r")
        cscReader = csv.reader(cscFile)
        self.cscUtility = {}
        for row in cscReader:
            countryName = row[0]
            utility = int(row[1])
            self.cscUtility[countryName] = utility
        cscFile.close()

    def loadDecideNbAttackingDice(self):
        self.dnadFileName = "fm_decide_nb_attacking_dice.csv"
        open(self.dnadFileName, "a").close()
        dnadFile = open(self.dnadFileName, "r")
        dnadReader = csv.reader(dnadFile)
        self.dnadUtility = {}
        for row in dnadReader:
            diffTroops = int(row[0])
            nbAttackingDice = int(row[1])
            utility = int(row[2])

            self.checkDnadDictionary(diffTroops, nbAttackingDice)

            self.dnadUtility[diffTroops][nbAttackingDice] += utility
        dnadFile.close()

    def loadPlaceStartingTroops(self):
        self.pstFileName = "fm_place_starting_troops.csv"
        open(self.pstFileName, "a").close()
        pstFile = open(self.pstFileName, "r")
        pstReader = csv.reader(pstFile)
        self.pstUtility = {}
        for row in pstReader:
            nbPerCountry = int(row[0])
            countryName = row[1]
            utility = int(row[2])

            self.checkPstUtility(nbPerCountry, countryName)

            self.pstUtility[nbPerCountry][countryName] += utility
        pstFile.close()

    def loadDeclareAttacks(self):
        self.daFileName = "fm_declare_attacks.csv"
        open(self.daFileName, "a").close()
        daFile = open(self.daFileName, "r")
        daReader = csv.reader(daFile)
        self.daUtility = {}
        for row in daReader:
            diff = int(row[0])
            utility = int(row[1])
            self.checkDaUtility(diff)
            self.daUtility[diff] += utility
        daFile.close()

    def loadPlaceTroops(self):
        self.ptFileName = "fm_place_troops.csv"
        open(self.ptFileName, "a").close()
        ptFile = open(self.ptFileName, "r")
        ptReader = csv.reader(ptFile)
        self.ptUtility = {}
        for row in ptReader:
            countryName = row[0]
            utility = int(row[1])

            self.checkPtUtility(countryName)

            self.ptUtility[countryName] += utility
        ptFile.close()

    # Choose a starting country one at the time
    #
    # remainingCountries : the countries that are not chosen yet
    # ownedCountries : the countries that you own so far
    # allCountries : all countries
    #
    # return : one element of the remainingCountries list
    def chooseStartingCountry(self, remainingCountries, ownedCountries, allCountries):
        r = self.random.uniform(0, 1)
        if r < self.executionFactor and len(self.cscUtility) > 0:
            maxCountry = remainingCountries[0]
            max = -9999
            for country in remainingCountries:
                countryName = country.getName()
                if countryName in self.cscUtility and self.cscUtility[countryName] > max:
                    max = self.cscUtility[countryName]
                    maxCountry = country
            self.chosenStartingCountries.append(maxCountry)
            return maxCountry
        else:
            country = self.random.choice(remainingCountries)
            self.chosenStartingCountries.append(country)
            return country

    # Place troops before the games begins. You can place only a portion of the available
    # troops. This method will be called again if you still have troops to be placed
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    def placeStartingTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        r = self.random.uniform(0, 1)
        if r < self.executionFactor and len(self.pstUtility) > 0:
            nbPerCountryMax = 0
            countryNameMax = ""
            max = -9999
            for nbPerCountry in self.pstUtility:
                for countryName in self.pstUtility[nbPerCountry]:
                    if countryName not in ownedCountries:
                        continue
                    utility = self.pstUtility[nbPerCountry][countryName]
                    if utility > max:
                        max = utility
                        countryNameMax = countryName
                        nbPerCountryMax = nbPerCountry
            if countryNameMax == "":
                nbPerCountryMax = self.random.choice([1, 2, 3])
                countryNameMax = ownedCountries.keys()[self.random.choice(xrange(len(ownedCountries)))]

            placeTroopsActions = []
            for countryName in ownedCountries:
                placeTroopsAction = PlaceTroopsAction(countryName, nbPerCountryMax)
                if countryName == countryNameMax:
                    placeTroopsAction.nbTroops += nbTroopsToPlace - (nbPerCountryMax * len(ownedCountries))
                placeTroopsActions.append(placeTroopsAction)
            self.chosenPlaceStartingTroops = (nbPerCountryMax, countryNameMax)
            return placeTroopsActions
        else:
            placeTroopsActions = []
            rest = nbTroopsToPlace
            nbPerCountry = self.random.choice([1, 2, 3])
            for countryName in ownedCountries:
                nbTroopsAtThisCountry = nbPerCountry
                if rest - nbTroopsAtThisCountry < 0:
                    nbTroopsAtThisCountry = rest
                placeTroopsActions.append(PlaceTroopsAction(countryName, nbTroopsAtThisCountry))
                rest -= nbTroopsAtThisCountry

            restCountryPlaceTroopAction = self.random.choice(placeTroopsActions)
            restCountryPlaceTroopAction.nbTroops += rest
            self.chosenPlaceStartingTroops = (nbPerCountry, restCountryPlaceTroopAction.countryName)

            return placeTroopsActions

    # Declare attacks on the other countries. You need to check if the defending country is
    # not yours, or your attack declaration will be ignored
    #
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of AttackAction.
    def declareAttacks(self, ownedCountries, allCountries):
        possibleAttackActions = []
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            for neighbour in country.getNeighbours():
                if neighbour.getOwner() != country.getOwner():
                    possibleAttackActions.append((AttackAction(country, neighbour, 3), country.getNbTroops() - neighbour.getNbTroops()))
        if len(possibleAttackActions) == 0:
            return []
        attackAction, diff = self.random.choice(possibleAttackActions)
        self.currentChosenDeclareAttack = diff

        r = self.random.uniform(0, 1)
        if r < self.executionFactor and diff in self.daUtility and self.daUtility[diff] < 0:
            return []
        else:
            return [attackAction]

    # Place troops at the start of your turn. You need to place all available troops at one
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    def placeTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        placeTroopsAction = []
        r = self.random.uniform(0, 1)
        if r < self.executionFactor and len(self.ptUtility) > 0:
            max = -9999
            countryNameMax = ""
            possibleCountriesName = []
            for countryName in self.ptUtility:
                if countryName not in ownedCountries:
                    continue

                country = ownedCountries[countryName]
                neighbourToAttack = False
                for neighbour in country.getNeighbours():
                    if neighbour.getOwner() != country.getOwner():
                        neighbourToAttack = True
                        break

                if not neighbourToAttack:
                    continue

                possibleCountriesName.append(countryName)

                utility = self.ptUtility[countryName]
                if utility > max:
                    max = utility
                    countryNameMax = countryName
            if len(possibleCountriesName) == 0:
                possibleCountriesName.append(self.random.choice(ownedCountries.keys()))
            if countryNameMax == "":
                countryNameMax = self.random.choice(possibleCountriesName)
            placeTroopsAction.append(PlaceTroopsAction(countryNameMax, nbTroopsToPlace))
            self.chosenPlaceTroops.append(countryNameMax)
        else:
            possibleCountriesName = []
            for countryName in ownedCountries:
                country = ownedCountries[countryName]
                neighbourToAttack = False
                for neighbour in country.getNeighbours():
                    if neighbour.getOwner() != country.getOwner():
                        neighbourToAttack = True
                        break
                if not neighbourToAttack:
                    continue
                possibleCountriesName.append(countryName)
            countryName = self.random.choice(possibleCountriesName)
            placeTroopsAction.append(PlaceTroopsAction(countryName, nbTroopsToPlace))
            self.chosenPlaceTroops.append(countryName)

        return placeTroopsAction

    # Move troops after attacking. You can only move one per turn
    #
    # turnAttackResults : the result of all the attacks you declared this turn
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a single MoveTroopAction
    def moveTroops(self, turnAttackResults, ownedCountries, allCountries):
        for countryName in ownedCountries:
            country = ownedCountries[countryName]
            if country.getNbTroops() <= 1:
                continue

            enemyNeighbour = False
            for neighbour in country.getNeighbours():
                if neighbour.getOwner() != country.getOwner():
                    enemyNeighbour = True
                    break
            if not enemyNeighbour:
                queue = deque([])
                visited = []
                queue.appendleft(country)
                while queue:
                    c = queue.pop()
                    visited.append(c)
                    enemyToAttack = False
                    for n in c.getNeighbours():
                        if n.getOwner() != c.getOwner():
                            enemyToAttack = True
                            break
                        elif n not in visited:
                            queue.appendleft(n)
                    if enemyToAttack:
                        return MoveAction(country, c, country.getNbTroops() - 1)

        return None

    # Decide the amount of attacking dice while attacking
    #
    # attackResult : the result of the pending attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 0 and 3, 0 means that you want to cancel the attack
    def decideNbAttackingDice(self, attackResult, ownedCountries, allCountries):
        r = self.random.uniform(0, 1)
        nbAttackingTroops = attackResult.getAttackingCountry().getNbTroops()
        nbDefendingTroops = attackResult.getDefendingCountry().getNbTroops()
        diffTroops = nbAttackingTroops - nbDefendingTroops
        if r < self.executionFactor and len(self.dnadUtility) > 0:
            if diffTroops <= 0:
                self.currentAttackChosenNbAttackingDice.append((diffTroops, 0))
                return 0
            if diffTroops in self.dnadUtility:
                dnad = self.dnadUtility[diffTroops]
                nbAttackingDiceMax = 0
                max = 0
                for nbAttackingDice in dnad:
                    utility = dnad[nbAttackingDice]
                    if utility > max:
                        nbAttackingDiceMax = nbAttackingDice
                        max = utility
                self.currentAttackChosenNbAttackingDice.append((diffTroops, nbAttackingDiceMax))
                return nbAttackingDiceMax
            else:
                nbAttackingDice = self.random.choice([0, 1, 2, 3])
                self.currentAttackChosenNbAttackingDice.append((diffTroops, nbAttackingDice))
                return nbAttackingDice
        else:
            r2 = self.random.uniform(0, 1)
            nbAttackingDice = 3
            if r2 < 0.1:
                nbAttackingDice = self.random.choice([0, 1, 2])
            self.currentAttackChosenNbAttackingDice.append((diffTroops, nbAttackingDice))
            return nbAttackingDice

    # Decide the amount of defending dice while defending
    #
    # attackResult : the result of the pending attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 1 and 2
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
    def decideNbTransferingTroops(self, attackResult, startCountry, endCountry, ownedCountries, allCountries):
        return int(startCountry.getNbTroops()/2)

    # Called when your AI wins an attack
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    def onAttackWon(self, attackResult, ownedCountries, allCountries):
        self.updateDnadUtility(1)
        self.updateDaUtility(1)
        self.currentAttackChosenNbAttackingDice = []
        self.currentChosenDeclareAttack = None
        pass

    # Called when your AI loses an attack. AKA the attack finished because you only have 1 troop left in
    # the attacking country
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    def onAttackLost(self, attackResult, ownedCountries, allCountries):
        self.updateDnadUtility(-1)
        self.updateDaUtility(-1)
        self.currentAttackChosenNbAttackingDice = []
        self.currentChosenDeclareAttack = None
        pass

    def updateDnadUtility(self, delta):
        for nbAttackingDiceInfo in self.currentAttackChosenNbAttackingDice:
            diffTroops = int(nbAttackingDiceInfo[0])
            nbAttackingDice = int(nbAttackingDiceInfo[1])
            self.checkDnadDictionary(diffTroops, nbAttackingDice)
            self.dnadUtility[diffTroops][nbAttackingDice] += delta

    def updateDaUtility(self, delta):
        if self.currentChosenDeclareAttack is None:
            return
        self.checkDaUtility(self.currentChosenDeclareAttack)
        self.daUtility[self.currentChosenDeclareAttack] += delta

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
        self.currentAttackChosenNbAttackingDice = []
        self.currentChosenDeclareAttack = None

    # Called when your AI succeeds to defend a territory.
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    def onDefendWon(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI fails to defend a territory.
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
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
    def onGameWon(self, allCountries):
        self.writeCscUtility(1)
        self.writePstUtility(1)
        self.writeDnadUtility()
        self.writePtUtility(1)
        self.writeDaUtility()

    # Called when your AI lost the game
    #
    # allCountries : all countries, you own no countries
    #
    # return : nothing
    def onGameLost(self, allCountries):
        self.writeCscUtility(-1)
        self.writePstUtility(-1)
        self.writeDnadUtility()
        self.writePtUtility(-1)
        self.writeDaUtility()

    def writeCscUtility(self, delta):
        for country in self.chosenStartingCountries:
            countryName = country.getName()
            if countryName not in self.cscUtility:
                self.cscUtility[countryName] = 0
            self.cscUtility[countryName] += delta

        cscFile = open(self.cscFileName, "w+")
        cscWriter = csv.writer(cscFile)
        for countryName in self.cscUtility:
            utility = self.cscUtility[countryName]
            cscWriter.writerow([countryName, utility])
        cscFile.close()

    def writePstUtility(self, delta):
        nbPerCountry = self.chosenPlaceStartingTroops[0]
        countryName = self.chosenPlaceStartingTroops[1]
        self.checkPstUtility(nbPerCountry, countryName)
        self.pstUtility[nbPerCountry][countryName] += delta

        pstFile = open(self.pstFileName, "w+")
        pstWriter = csv.writer(pstFile)
        for nbPerCountry in self.pstUtility:
            for countryName in self.pstUtility[nbPerCountry]:
                utility = self.pstUtility[nbPerCountry][countryName]
                pstWriter.writerow([nbPerCountry, countryName, utility])

    def writeDnadUtility(self):
        dnadFile = open(self.dnadFileName, "w+")
        dnadWriter = csv.writer(dnadFile)
        for diffTroops in self.dnadUtility:
            for nbAttackingDice in self.dnadUtility[diffTroops]:
                utility = self.dnadUtility[diffTroops][nbAttackingDice]
                dnadWriter.writerow([diffTroops, nbAttackingDice, utility])
        dnadFile.close()

    def writePtUtility(self, delta):
        for countryName in self.chosenPlaceTroops:
            self.checkPtUtility(countryName)
            self.ptUtility[countryName] += delta

        ptFile = open(self.ptFileName, "w+")
        ptWriter = csv.writer(ptFile)
        for countryName in self.ptUtility:
            utility = self.ptUtility[countryName]
            ptWriter.writerow([countryName, utility])
        ptFile.close()

    def writeDaUtility(self):
        daFile = open(self.daFileName, "w+")
        daWriter = csv.writer(daFile)
        for diff in self.daUtility:
            utility = self.daUtility[diff]
            daWriter.writerow([diff, utility])
        daFile.close()

    def checkDnadDictionary(self, diffTroops, nbAttackingDice):
        if diffTroops not in self.dnadUtility:
            self.dnadUtility[diffTroops] = {}
        if nbAttackingDice not in self.dnadUtility[diffTroops]:
            self.dnadUtility[diffTroops][nbAttackingDice] = 0

    def checkPstUtility(self, nbPerCountry, countryName):
        if nbPerCountry not in self.pstUtility:
            self.pstUtility[nbPerCountry] = {}
        if countryName not in self.pstUtility[nbPerCountry]:
            self.pstUtility[nbPerCountry][countryName] = 0

    def checkPtUtility(self, countryName):
        if countryName not in self.ptUtility:
            self.ptUtility[countryName] = 0

    def checkDaUtility(self, diff):
        if diff not in self.daUtility:
            self.daUtility[diff] = 0