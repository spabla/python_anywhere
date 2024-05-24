import requests
import sys
import json
import time

from database_manager.database_manager import Database_Manager

class Historic_Data_Manager:

    def __init__(self,theDatabaseManager):
        self.theDatabaseManager = theDatabaseManager

    def updateHistoricData(self):
        print("Getting F1 Champions Data")
        championsData = self.obtainF1ChampionsData()
        self.theDatabaseManager.storeF1ChampionsData(championsData)
        print("Getting Current Circutits Data")
        circuitsData = self.obtainF1CurrentCircuitsData()
        self.theDatabaseManager.storeF1CurrentCircuitsData(circuitsData)
        print("Getting All F1 Race Data")
        self.obtainF1AllRaceData()


    def obtainF1ChampionsData(self):
        try:
            # Ergast API URL for driver standings
            ergast_url = "http://ergast.com/api/f1/driverStandings/1.json?limit=100"

            response = requests.get(ergast_url)
            response.raise_for_status()  # Raise an exception if the request fails
            data = response.json()

            champions_data = []
            for driver in data["MRData"]["StandingsTable"]["StandingsLists"]:
                champions_data.append(driver)
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
            for race in races:
                circuitsData[race['Circuit']['circuitName']] = race['raceName']

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
        for year in range(1950, 2025):  # Assuming races have been held from 1950 to 2024
            for round in range(1, 25):  # Assuming a maximum of 24 rounds in a season (this is what 2024 season has)
                try:
                    print(f"requesting data for {year} round {round}")
                    race_data = self.obtainF1RaceData(year, round)
                    for result in race_data["Results"]:
                        print(f"processing result {i}")
                        # Add any historic results for current circuits to the database
                        driver_name = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
                        race_time = result['Time']['millis']
                        raceDataRecord = self.theDatabaseManager.RaceData_T(year,race_data['CircuitName'],driver_name,race_time)
                        racesData[i] = raceDataRecord
                        self.theDatabaseManager.storeF1AllRaceData(raceDataRecord)
                        i+=1
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
                print(f"{year},{circuit},{mostRecentWinningTime},{winningTimeForYear},{annualDifferencesDictionary[year][circuit]}")
                with open('race_time_diffs.csv', 'w') as file:
                    # Write the formatted string to the file
                    file.write(f"{year},{circuit},{mostRecentWinningTime},{winningTimeForYear},{annualDifferencesDictionary[year][circuit]}\n")



