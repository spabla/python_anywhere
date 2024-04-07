
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, jsonify
import mysql.connector
import requests

username = "sundevp"
password = "password1@@"
hostname = "sundevp.mysql.pythonanywhere-services.com"
database_name = "sundevp$f1_champions"

app = Flask(__name__)

@app.route('/')
def index():
    create_database()
    champions_data = fetch_champions_data()
    #insert_champions_data(champions_data)

    return render_template("index.html")

@app.route('/process_item', methods=['POST'])
def process_item():
    selected_item = request.form.get('selected_item')
    # Process the selected item (e.g., perform some action or return a response)
    # You can replace this with your actual backend logic
    return jsonify({'message': f'Selected item: {selected_item}'})

def create_database():
    try:
        # Create a connection
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=hostname,
            database=database_name)

        # Create a cursor
        cursor = connection.cursor()

        # Define the SQL query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS f1_champions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            driver_name VARCHAR(255),
            team VARCHAR(255),
            year INT
        )
        """

        # Execute the query
        cursor.execute(create_table_query)

        # Commit changes
        connection.commit()

        print("Table 'f1_champions' created successfully!")

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def fetch_champions_data():
    try:
        # Ergast API URL for driver standings (season 1)
        ergast_url = "http://ergast.com/api/f1/driverStandings/1.json"

        response = requests.get(ergast_url)
        response.raise_for_status()  # Raise an exception if the request fails
        data = response.json()
        return data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
    except requests.RequestException as e:
        print(f"Error fetching data from Ergast API: {e}")
        return []

def insert_champions_data(champions_data):
    # Create a connection
    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=hostname,
        database=database_name)

    # Create a cursor
    cursor = connection.cursor()

    for champion in champions_data:
        year = int(champion["season"])
        driver_name = f"{champion['Driver']['givenName']} {champion['Driver']['familyName']}"
        team_name = champion["Constructors"][0]["name"]
        cursor.execute("INSERT INTO champions VALUES (?, ?, ?)", (driver_name, team_name, year))
    connection.commit()
    connection.close()

if __name__ == '__main__':
    app.run(debug=True)

