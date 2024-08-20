from dotenv import load_dotenv
import pandas as pd
import mysql.connector
import os
from datetime import datetime
# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_NAME')

class Db:

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host=db_host,
                                    user=db_user,
                                    password=db_pass,
                                    database = db_database)
            self.my_curr = self.conn.cursor()
            print(f"connection id :{self.conn.connection_id}")
        except mysql.connector.error as err:
            print(f'ERROR:{err}')
    
    def fetch_all_cities(self):
        cities = []
        self.my_curr.execute("""
        SELECT DISTINCT source FROM flight
        UNION
        SELECT DISTINCT destination FROM flight
        """)

        data = self.my_curr.fetchall()

        for records in data:
            cities.append(records[0])
        return cities

    def search_flights(self, source, destination, journey_date):
        if source == destination:
            return "No flight exists between the same cities"
        else:
            # Format the date correctly for SQL
            formatted_date = journey_date.strftime('%Y-%m-%d')

            self.my_curr.execute(f"""
                SELECT Airline,Date_of_Journey,Source,Destination,Dep_Time AS "Dep_time",Duration,Total_Stops,Price FROM flight
                WHERE Source = '{source}' AND Destination = '{destination}' AND Date_of_Journey = '{formatted_date}'
            """)

            data = self.my_curr.fetchall()
            column_names = [desc[0] for desc in self.my_curr.description]
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=column_names)
            return df
    
    def fetch_airline_frequency(self):
        self.my_curr.execute("""
        SELECT Airline, COUNT(*) FROM flight GROUP BY Airline
        """)

        data = self.my_curr.fetchall()
        airline = [item[0] for item in data]
        num_of_flights = [item[1] for item in data]
        
        return airline, num_of_flights
    
    def num_flights_airport(self):
        self.my_curr.execute("""
        SELECT Source, COUNT(*) AS "num_of_flights"
        FROM
        (SELECT Source FROM flight
        UNION ALL
        SELECT Destination FROM flight) t
        GROUP BY t.Source
        ORDER BY COUNT(*) DESC
        """)

        data = self.my_curr.fetchall()
        airport = [item[0] for item in data]
        num_flights = [item[1] for item in data]

        return airport, num_flights
    
    def daily_flight_frequency(self):
        self.my_curr.execute("""
        SELECT DATE(Date_of_Journey), count(*) FROM flight
                    GROUP BY DATE(Date_of_Journey)
                    ORDER BY DATE(Date_of_Journey)
            """)
        
        data = self.my_curr.fetchall()
        date = [item[0] for item in data]
        number_flights = [item[1] for item in data]

        return date, number_flights
    
    def flight_between_cities(self):
        self.my_curr.execute("""
        SELECT Source,Destination,COUNT(*) FROM flight
        GROUP BY Source,Destination
        ORDER BY COUNT(*) DESC
        """)

        data = self.my_curr.fetchall()
        city_set = [item[0]+"-"+item[1] for item in data]
        number_of_flights = [item[2] for item in data]

        return city_set,number_of_flights

    def flight_fare_between_cities(self):
        self.my_curr.execute("""
        SELECT Source,Destination, ROUND(AVG(price),2) FROM flight
        GROUP BY Source,Destination
        ORDER BY ROUND(AVG(price),2) DESC
        """)

        data = self.my_curr.fetchall()
        city_set = [item[0]+"-"+item[1] for item in data]
        avg_fare_of_flights = [item[2] for item in data]

        return city_set,avg_fare_of_flights
    
    def avg_duration_between_cities(self):
        self.my_curr.execute("""
        SELECT Source,Destination, ROUND(AVG(Duration),0) FROM flight
        GROUP BY Source,Destination
        ORDER BY ROUND(AVG(Duration),0) DESC
        """)

        data = self.my_curr.fetchall()
        city_set = [item[0]+"-"+item[1] for item in data]
        avg_duration_of_flights = [item[2] for item in data]

        return city_set,avg_duration_of_flights