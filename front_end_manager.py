
# The front_end_manager for handling all interactions with the front end
import os
from flask import Flask, render_template, request, jsonify
from historic_data_manager.historic_data_manager import Historic_Data_Manager
from database_manager.database_manager import Database_Manager
from simulated_race_manager.simulated_race_manager import Simulated_Race_Manager

os.chdir('/home/sundevp/mysite')

app = Flask(__name__)

theDatabaseManager = Database_Manager()
theHistoricDataManager = Historic_Data_Manager(theDatabaseManager)
theSimulatedRaceManager = Simulated_Race_Manager(theDatabaseManager)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/champion_of_champions.html')
def champion_of_champions():
    champion_names = theDatabaseManager.getChampionsData()
    # Filter out repeats caused by same driver winning the championship multiple times
    theChampions = []
    for champion in champion_names:
        if champion not in theChampions:
            theChampions.append(champion)

    return render_template("champion_of_champions.html",drivers=theChampions)

@app.route('/driver_time_rationale.html')
def driver_time_rationale():
    return render_template('driver_time_rationale.html')

@app.route('/top_trumps.html')
def top_trumps():
    return render_template('top_trumps.html')

@app.route('/updateLocalDatabase', methods=['POST'])
def updateLocalDatabase():
    #Todo uncomment this following debug
    #theDatabaseManager.createDatabaseTables()
    theHistoricDataManager.obtainF1AllRaceData()

@app.route('/getPprogress', methods=['POST'])
def getProgress():
    theProgress = theHistoricDataManager.getProgress();
    return jsonify({'progress': theProgress})


@app.route('/runSimulatedRaces', methods=['POST'])
def runSimulatedRaces():

    driver1 = request.json.get('driver1')
    driver2 = request.json.get('driver2')

    simulatedRaceData = theSimulatedRaceManager.runSimulatedRaces(driver1,driver2)

    return jsonify(simulatedRaceData)


if __name__ == '__main__':
    pass
    app.run(debug=True)

