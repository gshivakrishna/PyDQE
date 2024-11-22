import sqlite3
import math

DB_FILE = "city_coordinates.db"


# Database Manager
class DatabaseManager:
    """Manages the database for storing city coordinates."""

    def __init__(self, db_file=DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._initialize_table()

    def _initialize_table(self):
        """Creates the city coordinates table if not exists."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS CityCoordinates (
                                city_name TEXT UNIQUE,
                                latitude REAL,
                                longitude REAL
                              )''')
        self.conn.commit()

    def get_coordinates(self, city_name):
        """Fetches the coordinates for a city from the database."""
        self.cursor.execute("SELECT latitude, longitude FROM CityCoordinates WHERE city_name = ?", (city_name,))
        return self.cursor.fetchone()

    def add_city(self, city_name, latitude, longitude):
        """Adds a city's coordinates to the database."""
        try:
            self.cursor.execute("INSERT INTO CityCoordinates (city_name, latitude, longitude) VALUES (?, ?, ?)",
                                (city_name, latitude, longitude))
            self.conn.commit()
            print(f"City {city_name} added to the database.")
        except sqlite3.IntegrityError:
            print(f"City {city_name} already exists in the database.")

    def close(self):
        """Closes the database connection."""
        self.conn.close()


# Haversine Distance Calculation
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculates the great-circle distance between two points on the Earth."""
    R = 6371.0  # Radius of Earth in kilometers

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


# Main Tool Logic
class DistanceCalculator:
    """Main tool to calculate distances between cities."""

    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_or_add_city(self, city_name):
        """Gets city coordinates, asks user if not found."""
        coordinates = self.db_manager.get_coordinates(city_name)
        if coordinates:
            return coordinates

        print(f"Coordinates for {city_name} not found in the database.")
        latitude = float(input(f"Enter latitude for {city_name}: "))
        longitude = float(input(f"Enter longitude for {city_name}: "))
        self.db_manager.add_city(city_name, latitude, longitude)
        return latitude, longitude

    def calculate_distance_between_cities(self):
        """Calculates and displays the distance between two cities."""
        city1 = input("Enter the name of the first city: ").strip()
        city2 = input("Enter the name of the second city: ").strip()

        lat1, lon1 = self.get_or_add_city(city1)
        lat2, lon2 = self.get_or_add_city(city2)

        distance = calculate_distance(lat1, lon1, lat2, lon2)
        print(f"The straight-line distance between {city1} and {city2} is {distance:.2f} km.")

    def close(self):
        """Closes the database manager."""
        self.db_manager.close()


# Entry Point
if __name__ == "__main__":
    print("City Distance Calculator")
    calculator = DistanceCalculator()

    try:
        while True:
            print("\nOptions:")
            print("1. Calculate distance between two cities")
            print("2. Exit")
            choice = input("Enter your choice (1/2): ").strip()
            if choice == '1':
                calculator.calculate_distance_between_cities()
            elif choice == '2':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        calculator.close()
