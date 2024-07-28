import requests
import sys
import json
import time

#from database_manager.database_manager import Database_Manager

class Historic_Data_Manager:

    def __init__(self,theDatabaseManager):
        self.theDatabaseManager = theDatabaseManager
        self.theProgressGettingChampionsData = 0
        self.theProgressCircuitsData = 0
        self.theProgressGettingRaceData = 0

    def getProgress(self):
        return self.theProgressGettingChampionsData

    def updateHistoricData(self):
        print("Getting F1 Champions Data")
        championsData = self.obtainF1ChampionsData()
        # self.theDatabaseManager.storeF1ChampionsData(championsData)
        print("Getting Current Circutits Data")
        circuitsData = self.obtainF1CurrentCircuitsData()
        # self.theDatabaseManager.storeF1CurrentCircuitsData(circuitsData)
        print("Getting All F1 Race Data")
        self.obtainF1AllRaceData() # Note for this case, the storing of data is handled in the function


    def obtainF1ChampionsData(self):
        try:
            # Ergast API URL for driver standings
            ergast_url = "http://ergast.com/api/f1/driverStandings/1.json?limit=100"

            response = requests.get(ergast_url)
            response.raise_for_status()  # Raise an exception if the request fails
            data = response.json()

            champions_data = []
            MAX_PROGRESS = len(data["MRData"]["StandingsTable"]["StandingsLists"])
            theProgressCount = 0;
            self.theProgress = 0
            for driver in data["MRData"]["StandingsTable"]["StandingsLists"]:
                champions_data.append(driver)
                theProgressCount = theProgressCount+1
                if MAX_PROGRESS > 0:
                    self.theProgressGettingChampionsData = (theProgressCount/MAX_PROGRESS) * 100
                else:
                    self.theProgressGettingChampionsData = 100

            return champions_data
        except requests.RequestException as e:
            print(f"Error fetching data from Ergast API: {e}")
            return []

    def obtainF1CurrentCircuitsData(self):
        # Send a GET request to the Ergast API for the current season
        response = requests.get('http://ergast.com/api/f1/current.json')

        # Check that the request was successful
        if response.status_code == 200:
            # Parse the response as JSON
            data = json.loads(response.text)

            # Extract the race information
            races = data['MRData']['RaceTable']['Races']

            # Print the name, date, and circuit of each Grand Prix
            # Populate a circuitsData dictionary as we loop through printing the data
            circuitsData = {}
            MAX_PROGRESS = len(races)
            theProgressCount = 0;
            self.theProgress = 0
            for race in races:
                circuitsData[race['Circuit']['circuitName']] = race['raceName']
                theProgressCount = theProgressCount + 1
                self.theProgressGettingCircuitsData = (theProgressCount/MAX_PROGRESS) * 100
        return circuitsData

    def obtainF1RaceData(self,year,round):
        url = f"http://ergast.com/api/f1/{year}/{round}/results.json"
        response = requests.get(url)
        data = response.json()

        # Include the circuit name in the returned data
        race_data = data["MRData"]["RaceTable"]["Races"][0]
        race_data["CircuitName"] = race_data["Circuit"]["circuitName"]
        # The conditions of the Erast API say do not make more than 4 calls per second
        time.sleep(0.25)

        return race_data

    def obtainF1AllRaceData(self):
        racesData = {}
        i=0;
        self.theProgress = 0
        theProgressCount = 0
        MAX_PROGRESS = 1875 # This is based on 75 years x 25 rounds
        for year in range(1950, 2025):  # Assuming races have been held from 1950 to 2024
            for round in range(1, 25):  # Assuming a maximum of 24 rounds in a season (this is what 2024 season has)
                try:
                    print(f"requesting data for {year} round {round}")
                    race_data = self.obtainF1RaceData(year, round)
                    theProgressCount = theProgressCount + 1
                    self.theProgressGettingRaceData = theProgressCount# (theProgressCount/MAX_PROGRESS) * 100
                    for result in race_data["Results"]:
                        print(f"processing result {i}")
                        # Add any historic results for current circuits to the database
                        driver_name = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
                        race_time = result['Time']['millis']
                        raceDataRecord = self.theDatabaseManager.RaceData_T(year,race_data['CircuitName'],driver_name,race_time)
                        racesData[i] = raceDataRecord
                        # Todo - uncomment this following debug.  Only commented out to prevent trashing database
                        # self.theDatabaseManager.storeF1AllRaceData(raceDataRecord)
                        i+=1
                        print(self.theProgress)
                except Exception:
                    pass

    def calculateAnnualRaceTimeCompValues(self):
        # first get a list of all current formula 1 circuits
        currentCircuits = self.theDatabaseManager.getCurrentCircuitsData()
        # Loop through each year
        annualDifferencesDictionary = {}

        for year in range(1950, 2025):
            # Loop through current circuits
            for circuit in currentCircuits:
                winningTimeForYear = self.theDatabaseManager.getWinningRaceTime(year,circuit)
                if winningTimeForYear == -999:
                    continue
                mostRecentWinningTime = self.theDatabaseManager.getWinningRaceTime(2024,circuit)
                if mostRecentWinningTime == -999:
                      # Try 2023 because the 2024 season is still in progress
                    mostRecentWinningTime = self.theDatabaseManager.getWinningRaceTime(2023,circuit)
                    if mostRecentWinningTime == -999:
                        continue

                if year not in annualDifferencesDictionary:
                    annualDifferencesDictionary[year] = {}

                annualDifferencesDictionary[year][circuit] = winningTimeForYear-mostRecentWinningTime
                print(f"{year},{circuit},{mostRecentWinningTime},{winningTimeForYear},{annualDifferencesDictionary[year][circuit]}\n")


        # We will base the annual compensation value on the median annual diff for that year
        annualCompValues = self.calculate_comp_values(annualDifferencesDictionary)

        self.theDatabaseManager.storeCompValues(annualCompValues)

    def calculate_comp_values(self, annualDifferencesDictionary):

        annualCompValues = {}
        # loop through all years, use the median different as the compensation value for the year
        for year in range(1950, 2024):
            annualDifferenesForYear = list(annualDifferencesDictionary.get(year, {}).values())
            annualDifferenesForYear.sort()

            if len(annualDifferenesForYear) % 2 == 0:
                mid = len(annualDifferenesForYear) // 2
                compValueForYear = (annualDifferenesForYear[mid - 1] + annualDifferenesForYear[mid]) / 2
            else:
                compValueForYear = annualDifferenesForYear[len(annualDifferenesForYear) // 2]

            annualCompValues[year] = compValueForYear

        return annualCompValues



