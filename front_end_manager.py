
# The front_end_manager for handling all interactions with the front end
import os, threading
from flask import Flask, render_template, request, jsonify,redirect, url_for, session, flash
from historic_data_manager.historic_data_manager import Historic_Data_Manager
from database_manager.database_manager import Database_Manager
from simulated_race_manager.simulated_race_manager import Simulated_Race_Manager

os.chdir('/home/sundevp/mysite')

app = Flask(__name__)

# Admin password
app.secret_key = 'your_secret_key'
ADMIN_PASSWORD = 'admin123'

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_only'))
        else:
            flash('Incorrect password')
    return render_template('login.html')

@app.route('/admin_only.html')
def admin_only():
    if 'admin' in session:
        return render_template('admin_only.html')
    else:
        flash('You must be logged in to view this page.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/updateLocalDatabase', methods=['POST'])
def updateLocalDatabase():
    #Todo uncomment this following debug
    #theDatabaseManager.createDatabaseTables()
    updateLocalDatabaseThread = threading.Thread(target=theHistoricDataManager.obtainF1ChampionsData)
    updateLocalDatabaseThread.start()
    return jsonify({"mesaage": "Update Started"})

@app.route('/getProgress', methods=['POST'])
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

