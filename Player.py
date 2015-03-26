class Player:
    def __init__(self, name, remainingTroopsToPlace):
        self._name = name
        self._ownedCountries = {}
        self._remainingTroopsToPlace = remainingTroopsToPlace

    def _addOwnedCountry(self, country):
        if country not in self._ownedCountries:
            self._ownedCountries[country._name] = country

    def _removeOwnedCountry(self, country):
        if country._name in self._ownedCountries:
            del self._ownedCountries[country._name]

    def _printTroops(self):
        print "Troops for", self._name
        for countryName in self._ownedCountries:
            country = self._ownedCountries[countryName]
            print "Country :", country._name
            print "Troops :", country._nbTroops
        print "-------------"

    def getName(self):
        return self._name

    def getOwnedCountries(self):
        return self._ownedCountries

    def getRemainingTroopsToPlace(self):
        return self._remainingTroopsToPlace