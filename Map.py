class Map:
    def __init__(self, countries, continents):
        self._countries = countries
        self._continents = continents

    def getCountries(self):
        return self._countries

    def getContinents(self):
        return self._continents