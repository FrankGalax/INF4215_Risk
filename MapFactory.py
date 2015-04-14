from Country import *
from Map import *

class MapFactory:
    def __init__(self, mapName):
        self._mapName = mapName

    def _build(self):
        if self._mapName == "NorthAmericaSimplified":
            canada = Country("Canada")
            usa = Country("USA")
            mexico = Country("Mexico")

            canada._addNeighbour(usa)

            usa._addNeighbour(canada)
            usa._addNeighbour(mexico)

            mexico._addNeighbour(usa)

            return Map([canada, usa, mexico])
        elif self._mapName == "Americas":
            alaska = Country("Alaska")
            northWestTerritory = Country("Northwest Territory")
            alberta = Country("Alberta")
            ontario = Country("Ontario")
            quebec = Country("Quebec")
            greenland = Country("Greenland")
            westernUnitedStates = Country("Western United States")
            easternUnitedStates = Country("Eastern United States")
            centralAmerica = Country("Central America")
            venezuela = Country("Venezuela")
            brazil = Country("Brazil")
            peru = Country("Peru")
            argentina = Country("Argentina")

            alaska._addNeighbour(northWestTerritory)
            alaska._addNeighbour(alberta)

            northWestTerritory._addNeighbour(alaska)
            northWestTerritory._addNeighbour(alberta)
            northWestTerritory._addNeighbour(ontario)
            northWestTerritory._addNeighbour(greenland)

            greenland._addNeighbour(northWestTerritory)
            greenland._addNeighbour(quebec)

            alberta._addNeighbour(alaska)
            alberta._addNeighbour(northWestTerritory)
            alberta._addNeighbour(ontario)
            alberta._addNeighbour(westernUnitedStates)

            ontario._addNeighbour(alberta)
            ontario._addNeighbour(northWestTerritory)
            ontario._addNeighbour(quebec)
            ontario._addNeighbour(easternUnitedStates)
            ontario._addNeighbour(westernUnitedStates)

            quebec._addNeighbour(greenland)
            quebec._addNeighbour(ontario)
            quebec._addNeighbour(easternUnitedStates)

            westernUnitedStates._addNeighbour(alberta)
            westernUnitedStates._addNeighbour(ontario)
            westernUnitedStates._addNeighbour(easternUnitedStates)
            westernUnitedStates._addNeighbour(centralAmerica)

            easternUnitedStates._addNeighbour(westernUnitedStates)
            easternUnitedStates._addNeighbour(ontario)
            easternUnitedStates._addNeighbour(quebec)
            easternUnitedStates._addNeighbour(centralAmerica)

            centralAmerica._addNeighbour(westernUnitedStates)
            centralAmerica._addNeighbour(easternUnitedStates)
            centralAmerica._addNeighbour(venezuela)

            venezuela._addNeighbour(centralAmerica)
            venezuela._addNeighbour(peru)
            venezuela._addNeighbour(brazil)

            peru._addNeighbour(venezuela)
            peru._addNeighbour(brazil)
            peru._addNeighbour(argentina)

            brazil._addNeighbour(venezuela)
            brazil._addNeighbour(peru)
            brazil._addNeighbour(argentina)

            argentina._addNeighbour(peru)
            argentina._addNeighbour(brazil)

            continents = []
            continents.append((2, "South America", [venezuela, peru, brazil, argentina]))
            continents.append((5, "North America", [alaska, northWestTerritory, greenland, alberta, ontario, quebec, westernUnitedStates,
                                   easternUnitedStates, centralAmerica]))

            return Map([alaska, northWestTerritory, greenland, alberta, ontario,
                        quebec, westernUnitedStates, easternUnitedStates, centralAmerica,
                        venezuela, peru, brazil, argentina], continents)