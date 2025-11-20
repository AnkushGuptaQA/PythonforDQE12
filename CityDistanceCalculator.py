import sqlite3
import math

# ---------- Database Handling ----------
class CityDatabase:
    #Function to create Database
    def __init__(self, db_name="city_coordinates.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    #Function to create Table
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            latitude REAL,
            longitude REAL
        )''')
        self.conn.commit()

    #Function to add City with coordinates
    def add_city(self, name, latitude, longitude):
        if not self.validate_coordinates(latitude, longitude):
            print(f"Invalid coordinates for {name}. Please check your input.")
            return
        try:
            self.cursor.execute("INSERT OR IGNORE INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
                                (name, latitude, longitude))
            self.conn.commit()
            print(f"Coordinates for {name} saved successfully.")
        except sqlite3.IntegrityError:
            print(f"City {name} already exists.")

    #Function to update Coordinates of City
    def update_city(self, name, latitude, longitude):
        if not self.validate_coordinates(latitude, longitude):
            print("Invalid coordinates. Update aborted.")
            return
        self.cursor.execute("UPDATE cities SET latitude = ?, longitude = ? WHERE name = ?",
                            (latitude, longitude, name))
        if self.cursor.rowcount == 0:
            print(f"No such city '{name}' found in the database.")
        else:
            self.conn.commit()
            print(f"✅ Coordinates for {name} updated successfully.")

    #Function to fetch City Coordinates
    def get_coordinates(self, city_name):
        self.cursor.execute("SELECT latitude, longitude FROM cities WHERE name = ?", (city_name,))
        return self.cursor.fetchone()

    #Function to check valid coordinates only
    def validate_coordinates(self, lat, lon):
        if not (-90 <= lat <= 90):
            print("⚠️ Latitude must be between -90 and 90.")
            return False
        if not (-180 <= lon <= 180):
            print("⚠️ Longitude must be between -180 and 180.")
            return False
        return True

    #Function to view all city details
    def view_all_cities(self):
        self.cursor.execute("SELECT name, latitude, longitude FROM cities")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"{row[0]}: Latitude = {row[1]}, Longitude = {row[2]}")

    #Function to close connection
    def close(self):
        self.conn.close()

# ---------- Haversine Formula ----------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ---------- Main Application ----------
def main():
    print("🌍 Welcome to the City Distance Calculator Tool")
    db = CityDatabase()

    while True:
        print("\nChoose an option:")
        print("1. Calculate distance between two cities")
        print("2. View stored cities")
        print("3. Update city coordinates")
        print("4. Exit")
        choice = input("Enter choice (1-4): ")

        if choice == "1":
            city1 = input("Enter the name of the first city: ").strip().title()
            city2 = input("Enter the name of the second city: ").strip().title()

            coords1 = db.get_coordinates(city1)
            if not coords1:
                print(f"Coordinates for {city1} not found.")
                lat1 = float(input(f"Enter latitude for {city1}: "))
                lon1 = float(input(f"Enter longitude for {city1}: "))
                db.add_city(city1, lat1, lon1)
                coords1 = (lat1, lon1)

            coords2 = db.get_coordinates(city2)
            if not coords2:
                print(f"Coordinates for {city2} not found.")
                lat2 = float(input(f"Enter latitude for {city2}: "))
                lon2 = float(input(f"Enter longitude for {city2}: "))
                db.add_city(city2, lat2, lon2)
                coords2 = (lat2, lon2)

            lat1, lon1 = coords1
            lat2, lon2 = coords2

            print(f"\n🔎 {city1} → Latitude: {lat1}, Longitude: {lon1}")
            print(f"🔎 {city2} → Latitude: {lat2}, Longitude: {lon2}")

            distance = haversine(lat1, lon1, lat2, lon2)
            print(f"\n📏 Distance between {city1} and {city2}: {distance:.2f} km")

        elif choice == "2":
            print("\n📍 Stored Cities:")
            db.view_all_cities()

        elif choice == "3":
            city = input("Enter the name of the city to update: ").strip().title()
            lat = float(input("Enter new latitude: "))
            lon = float(input("Enter new longitude: "))
            db.update_city(city, lat, lon)

        elif choice == "4":
            print("Goodbye!")
            db.close()
            break

        else:
            print("Invalid choice. Try again.")

# ---------- Run ----------
if __name__ == "__main__":
    main()