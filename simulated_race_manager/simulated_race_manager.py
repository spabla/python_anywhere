
import sys
sys.path.insert(0, '/home/sundevp/mysite')

from database_manager.database_manager import Database_Manager

class Simulated_Race_Manager:

    def __init__(self,theDatabaseManager):
        self.theDatabaseManager = theDatabaseManager

    def runSimulatedRaces(self,driver1,driver2):

        currentCircuits = self.theDatabaseManager.getCurrentCircuitsData()

        # A list to store the results of the simulated race
        simulateRaceData = []
        driver1Wins = 0
        driver2Wins = 0

        for circuit in currentCircuits:
            # Get data for both driver 1 and driver 2
            driver1RaceData = self.theDatabaseManager.getRaceData(circuit,driver1)
            driver2RaceData = self.theDatabaseManager.getRaceData(circuit,driver2)

            # Check to see if both driver 1 and driver 2 have a time at the circuit
            if (len(driver1RaceData) != 0 ) and (len(driver2RaceData) != 0):
                # Need to find best time for both drivers at a given circuit
                # Sort the results so the best time is at the top
                driver1RaceDataSorted = sorted(driver1RaceData, key=lambda x: x['time'], reverse=True)
                driver2RaceDataSorted = sorted(driver2RaceData, key=lambda x: x['time'], reverse=True)

                driver1BestRace = driver1RaceDataSorted[0]
                driver1BestRaceYear = driver1BestRace['year']
                driver1Name = driver1BestRace['driver']
                driver1BestTime = driver1BestRace['time']
                drviver1YearComp = self.theDatabaseManager.getYearComp(driver1BestRaceYear)
                driver1BestTimeAfterComp = driver1BestTime + drviver1YearComp[0]

                driver2BestRace = driver2RaceDataSorted[0]
                driver2BestRaceYear = driver2BestRace['year']
                driver2Name = driver2BestRace['driver']
                driver2BestTime = driver2BestRace['time']
                drviver2YearComp = self.theDatabaseManager.getYearComp(driver2BestRaceYear)
                driver2BestTimeAfterComp = driver2BestTime + drviver2YearComp[0]

                # Now the moment of truth, lets determine the winner of our simulated race
                if driver1BestTimeAfterComp < driver2BestTimeAfterComp:
                    raceWinner = driver1Name
                    driver1Wins+=1
                else:
                    raceWinner = driver2Name
                    driver2Wins+=1


                raceDataDictionary = {"circuit": circuit,
                                      "Driver 1 Best Year":driver1BestRaceYear,
                                      "Driver 1 Best Time":driver1BestTime,
                                      "Driver 1 Best Time after Comp": driver1BestTimeAfterComp,
                                      "Driver 2 Best Year":driver2BestRaceYear,
                                      "Driver 2 Best Time":driver2BestTime,
                                      "Driver 2 Best Time after Comp": driver2BestTimeAfterComp,
                                      "Race Winner after Comp": raceWinner
                                      }

                simulateRaceData.append(raceDataDictionary)
                print(raceDataDictionary)

        if driver1Wins > driver2Wins:
            print(f"Simulated F1 Champion of Champions is: {driver1Name} with {driver1Wins} wins to {driver2Name} with {driver2Wins} wins")

        else:
            print(f"Simulated F1 Champion of Champions is: {driver2Name} with {driver2Wins} wins to {driver1Name} with {driver1Wins} wins")

        return simulateRaceData


