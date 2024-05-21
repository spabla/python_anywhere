
# The front_end_manager for handling all interactions with the front end
import os
from flask import Flask, render_template, request, jsonify
from historic_data_manager.historic_data_manager import Historic_Data_Manager
from database_manager.database_manager import Database_Manager


os.chdir('/home/sundevp/mysite')

app = Flask(__name__)

theDatabaseManager = Database_Manager()
theHistoricDataManager = Historic_Data_Manager(theDatabaseManager)
#theHistoricDataManager.updateHistoricData()

@app.route('/')
def index():
    champion_names = theDatabaseManager.getChampionsData()
    # Filter out repeats caused by same driver winning the championship multiple times
    theChampions = []
    for champion in champion_names:
        if champion not in theChampions:
            theChampions.append(champion)

    return render_template("index.html",drivers=theChampions)

@app.route('/process_item', methods=['POST'])
def process_item():
    selected_item = request.form.get('selected_item')
    # Process the selected item (e.g., perform some action or return a response)
    # You can replace this with your actual backend logic
    return jsonify({'message': f'Selected item: {selected_item}'})



if __name__ == '__main__':
    app.run(debug=True)

