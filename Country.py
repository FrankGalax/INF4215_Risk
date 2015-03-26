class Country:
    def __init__(self, name):
        self._name = name
        self._neighbours = []
        self._owner = ""
        self._nbTroops = 0

    def _addNeighbour(self, country):
        self._neighbours.append(country)

    def _changeOwner(self, newOwner):
        self._owner = newOwner
        self._nbTroops = 0

    def _addTroops(self, amount):
        self._nbTroops += amount

    def _removeTroops(self, amount):
        self._nbTroops -= amount
        if self._nbTroops < 0:
            self._nbTroops = 0

    def getName(self):
        return self._name

    def getNeighbours(self):
        return self._neighbours

    def getOwner(self):
        return self._owner

    def getNbTroops(self):
        return self._nbTroops