import mysql.connector

username = "sundevp"
password = "password1@@"
hostname = "sundevp.mysql.pythonanywhere-services.com"
database_name = "sundevp$f1_champions"

class Database_Manager:
    def __init__(self):
        self.create_database()

    def create_database(self):
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

    def getChampionsData(self):
        # Create a connection
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=hostname,
            database=database_name)

        # Create a cursor
        cursor = connection.cursor()

        sql_query = "SELECT driver_name FROM f1_champions"

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

