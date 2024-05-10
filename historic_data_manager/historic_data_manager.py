import mysql.connector
import requests

username = "sundevp"
password = "password1@@"
hostname = "sundevp.mysql.pythonanywhere-services.com"
database_name = "sundevp$f1_champions"

class Historic_Data_Manager:
    def __init__(self):
        self.create_database

    def updateHistoricData():
        pass

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

    def fetch_champions_data(self):
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

    def insert_champions_data(self,champions_data):
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
            for driver in champion['DriverStandings']:
                driver_name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
            print(str(year) + str(' ') + driver_name)
            cursor.execute("INSERT INTO f1_champions (driver_name,year) VALUES (%s, %s)", (driver_name, year))
        connection.commit()
        connection.close()