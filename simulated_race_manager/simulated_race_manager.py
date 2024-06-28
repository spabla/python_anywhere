
import sys
sys.path.insert(0, '/home/sundevp/mysite')

from database_manager.database_manager import Database_Manager

class Simulated_Race_Manager:

    def __init__(self,theDatabaseManager):
        self.theDatabaseManager = theDatabaseManager

    def runSimulatedRaces(self,driver1,driver2):

        currentCircuits = theDatabaseManager.getCurrentCircuitsData()

        for circuit in currentCircuits:
            driver1RaceData = theDatabaseManager.getRaceData(circuit,driver1)
            for row in driver1RaceData:
                print(row)


theDatabaseManager = Database_Manager()
theSimulatedRaceManager = Simulated_Race_Manager(theDatabaseManager)
theSimulatedRaceManager.runSimulatedRaces("Michael Schumacher","CD")

