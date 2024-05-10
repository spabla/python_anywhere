
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, jsonify
from historic_data_manager.historic_data_manager import Historic_Data_Manager

app = Flask(__name__)
theHistoricDataManager = Historic_Data_Manager()

@app.route('/')
def index():

    champions_data = theHistoricDataManager.fetch_champions_data()
    theHistoricDataManager.insert_champions_data(champions_data)
    drivers=[]
    for champion in champions_data:
        for driver in champion['DriverStandings']:
            driver_name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
            if driver_name not in drivers:
                drivers.append(driver_name)

    return render_template("index.html",drivers=drivers)

@app.route('/process_item', methods=['POST'])
def process_item():
    selected_item = request.form.get('selected_item')
    # Process the selected item (e.g., perform some action or return a response)
    # You can replace this with your actual backend logic
    return jsonify({'message': f'Selected item: {selected_item}'})



if __name__ == '__main__':
    app.run(debug=True)

