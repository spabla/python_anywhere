import requests
import sys
import json

#from database_manager.database_manager import Database_Manager

class Historic_Data_Manager:
    def __init__(self,theDatabaseManager):
        self.theDatabaseManager = theDatabaseManager


    def updateHistoricData(self):
        championsData = self.obtainF1ChampionsData()
        self.theDatabaseManager.storeF1ChampionsData(championsData)
        circuitsData = self.obtainF1CurrentCircuitsData()
        self.theDatabaseManager.storeF1CurrentCircuitsData(circuitsData)

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
                print(f"Grand Prix Name: {race['raceName']}")
                print(f"Date: {race['date']}")
                print(f"Circuit: {race['Circuit']['circuitName']}")
                print('---')

        return circuitsData
