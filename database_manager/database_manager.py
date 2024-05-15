import mysql.connector

username = "sundevp"
password = "password1@@"
hostname = "sundevp.mysql.pythonanywhere-services.com"
database_name = "sundevp$f1_champions"

class Database_Manager:

    def __init__(self):
        self.create_database_tables()

    def create_database_tables(self):

        # Drop the current tables, they must be dropeed in a certain order due to dependencies
        self.execute_sql("DROP TABLE IF EXISTS f1_world_champions")
        self.execute_sql("DROP TABLE IF EXISTS f1_years")

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



    def execute_sql(self,sql_query):
        try:
            print(sql_query)
            # Create a connection
            connection = mysql.connector.connect(
                user=username,
                password=password,
                host=hostname,
                database=database_name)

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
