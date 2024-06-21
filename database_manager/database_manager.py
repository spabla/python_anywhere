import mysql.connector

# The Database Manager class controls access to the database.  You
# can only write or read from the database using this class.
class Database_Manager:

    # Class member variables needed for database connection
    username = "sundevp"
    password = "password1@@"
    hostname = "sundevp.mysql.pythonanywhere-services.com"
    database_name = "sundevp$f1_champions"

    class RaceData_T:
        def __init__(self, year,circuit,driver_name,race_time):
            self.year = year
            self.circuit = circuit
            self.driver_name = driver_name
            self.race_time = race_time

    def __init__(self):
        pass
        #self.createDatabaseTables()

    def createDatabaseTables(self):

        # Drop the current tables, they must be dropped in a certain order due to dependencies
        self.execute_sql("DROP TABLE IF EXISTS annual_compensation_values")
        self.execute_sql("DROP TABLE IF EXISTS f1_races")
        self.execute_sql("DROP TABLE IF EXISTS f1_world_champions")
        self.execute_sql("DROP TABLE IF EXISTS f1_years")
        self.execute_sql("DROP TABLE IF EXISTS f1_current_circuits")


        # Recreate f1_years table

        create_table_query = """
        CREATE TABLE IF NOT EXISTS f1_years (
            id INT AUTO_INCREMENT PRIMARY KEY,
            year INT

        )
        """
        self.execute_sql(create_table_query)

        # Recreate f1_world_champions table

        # Define the SQL query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS f1_world_champions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            year_id INT,
            driver_name VARCHAR(255),
            FOREIGN KEY(year_id) REFERENCES f1_years(id)
        )
        """
        # Create the table
        self.execute_sql(create_table_query)

        # Recreate F1 Circuits table

        # Define the SQL query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS f1_current_circuits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            circuit_name VARCHAR(255),
            grand_prix VARCHAR(255)
        )
        """
        # Create the table
        self.execute_sql(create_table_query)

        # Recreate F1 Races table

        # Define the SQL query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS f1_races (
            id INT AUTO_INCREMENT PRIMARY KEY,
            year_id INT,
            circuit_name INT,
            driver_name VARCHAR(255),
            race_time INT,
            FOREIGN KEY(year_id) REFERENCES f1_years(id),
            FOREIGN KEY(circuit_id) REFERENCES f1_current_circuits(id)
        )
        """
        # Create the table
        self.execute_sql(create_table_query)

        # Define the SQL query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS annual_compensation_values (
            id INT AUTO_INCREMENT PRIMARY KEY,
            year_id INT,
            comp_value INT,
            FOREIGN KEY(year_id) REFERENCES f1_years(id)
        )
        """
        # Create the table
        self.execute_sql(create_table_query)

    def execute_sql(self,sql_query):
        try:

            # Create a connection
            connection = mysql.connector.connect(
                user=Database_Manager.username,
                password=Database_Manager.password,
                host=Database_Manager.hostname,
                database=Database_Manager.database_name)

            # Create a cursor
            cursor = connection.cursor()

            # Execute the query
            cursor.execute(sql_query)

            # Commit changes
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def storeF1ChampionsData(self,champions_data):
        # Create a connection
        connection = mysql.connector.connect(
            user=Database_Manager.username,
            password=Database_Manager.password,
            host=Database_Manager.hostname,
            database=Database_Manager.database_name)

        # Create a cursor
        cursor = connection.cursor()

        for champion in champions_data:
            year = int(champion["season"])
            for driver in champion['DriverStandings']:
                driver_name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"

            # Update the year table first
            cursor.execute("INSERT INTO f1_years (year) VALUES (%s)", (year,))
            connection.commit()
            # Now get the id for the year
            sql_query = "SELECT id FROM f1_years WHERE year=(%s)"
            cursor.execute(sql_query, (year,))
            # Fetch result
            year_id = cursor.fetchone()
            cursor.execute("INSERT INTO f1_world_champions (year_id,driver_name) VALUES (%s,%s)", (year_id[0],driver_name))
            connection.commit()

        cursor.close
        connection.close()

    def getChampionsData(self):
        # Create a connection
        connection = mysql.connector.connect(
            user=Database_Manager.username,
            password=Database_Manager.password,
            host=Database_Manager.hostname,
            database=Database_Manager.database_name)

        # Create a cursor
        cursor = connection.cursor()

        sql_query = "SELECT driver_name FROM f1_world_champions"

        # Execute the query
        cursor.execute(sql_query)

        # Fetch all the results into a list
        results = cursor.fetchall()

        # Extract the DriverNames from the results
        championsData = [row[0] for row in results]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return championsData

    def storeF1CurrentCircuitsData(self,circuitsData):
        # Create a connection
        connection = mysql.connector.connect(
            user=Database_Manager.username,
            password=Database_Manager.password,
            host=Database_Manager.hostname,
            database=Database_Manager.database_name)

        # Create a cursor
        cursor = connection.cursor()

        # Loop through the circuits storing the data in the database
        for circuitName, grandPrix in circuitsData.items():
            cursor.execute("INSERT INTO f1_current_circuits (circuit_name,grand_prix) VALUES (%s,%s)", (circuitName,grandPrix))
            connection.commit()

        cursor.close()
        connection.close()

    def getCurrentCircuitsData(self):
        # Create a connection
        connection = mysql.connector.connect(
            user=Database_Manager.username,
            password=Database_Manager.password,
            host=Database_Manager.hostname,
            database=Database_Manager.database_name)

        # Create a cursor
        cursor = connection.cursor()

        sql_query = "SELECT circuit_name FROM f1_current_circuits"

        # Execute the query
        cursor.execute(sql_query)

        # Fetch all the results into a list
        results = cursor.fetchall()

        # Extract the DriverNames from the results
        currentCircuitData = [row[0] for row in results]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return currentCircuitData


    def storeF1AllRaceData(self,raceData):

        try:
            # Create a connection
            connection = mysql.connector.connect(
                user=Database_Manager.username,
                password=Database_Manager.password,
                host=Database_Manager.hostname,
                database=Database_Manager.database_name)

            # Create a cursor
            cursor = connection.cursor()

            print("----Race Result-----")
            print(raceData.year)
            print(raceData.circuit)
            print(raceData.driver_name)
            print(raceData.race_time)

            # Now get the id for the year
            sql_query = "SELECT id FROM f1_years WHERE year=(%s)"
            cursor.execute(sql_query, (raceData.year,))
            year_id = cursor.fetchone()

            # Now get the id for the circuit
            sql_query = "SELECT id FROM f1_current_circuits WHERE circuit_name=(%s)"
            cursor.execute(sql_query, (raceData.circuit,))
            # We will initialise circuit_id to 999 in case it is not a current circuit
            circuit_id = 999
            circuit_id = cursor.fetchone()

            cursor.execute("INSERT INTO f1_races (year_id,circuit_id,driver_name,race_time) VALUES (%s,%s,%s,%s)",
                (year_id[0],circuit_id[0],raceData.driver_name,raceData.race_time))

            connection.commit()

            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def getWinningRaceTime(self,year,circuit):

        # Create a connection
        connection = mysql.connector.connect(
            user=Database_Manager.username,
            password=Database_Manager.password,
            host=Database_Manager.hostname,
            database=Database_Manager.database_name)

        # Create a cursor
        cursor = connection.cursor()

        # Now get the id for the year
        sql_query = "SELECT id FROM f1_years WHERE year=(%s)"
        cursor.execute(sql_query, (year,))
        # Fetch result
        year_id = cursor.fetchone()

        # Now get the id for the circuit
        sql_query = "SELECT id FROM f1_current_circuits WHERE circuit_name=(%s)"
        cursor.execute(sql_query, (circuit,))
        # Fetch result
        circuit_id = cursor.fetchone()

        winningRaceTime = -999
        if circuit_id is not None and year_id is not None:
            sql_query = "SELECT MAX(race_time) FROM f1_races WHERE year_id=(%s) AND circuit_id=(%s)"
            # Execute the query
            cursor.execute(sql_query, (year_id[0], circuit_id[0],))
            # Fetch all the results into a list
            winningRaceTime = cursor.fetchone()
            if winningRaceTime is not None and winningRaceTime[0] is not None:
                try:
                    winningRaceTime = int(winningRaceTime[0])
                except (ValueError, IndexError) as e:
                    # Handle any conversion errors or index errors gracefully
                    print(f"Error converting winning race time: {e}")
                    winningRaceTime = -999
            else:
                winningRaceTime = -999

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return winningRaceTime

    def storeCompValues(self,comp_value_data):
        # Create a connection
        connection = mysql.connector.connect(
            user=Database_Manager.username,
            password=Database_Manager.password,
            host=Database_Manager.hostname,
            database=Database_Manager.database_name)

        # Create a cursor
        cursor = connection.cursor()

        for year, comp_value in comp_value_data.items():

            # Now get the id for the year
            sql_query = "SELECT id FROM f1_years WHERE year=(%s)"
            cursor.execute(sql_query, (year,))
            # Fetch result
            year_id = cursor.fetchone()
            cursor.execute("INSERT INTO annual_compensation_values  (year_id,comp_value) VALUES (%s,%s)", (year_id[0],int(comp_value)))
            connection.commit()

        cursor.close
        connection.close()