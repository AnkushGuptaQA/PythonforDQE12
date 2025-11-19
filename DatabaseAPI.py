import datetime
import os
import csv
import string
import json
import xml.etree.ElementTree as ET
from collections import Counter
import sqlite3

def sentence_case(text):
    """Converts text to sentence case."""
    return text[:1].upper() + text[1:]

# ---------- Record creation ----------
def create_news_record(city, text):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    city_cased = sentence_case(city)
    text_cased = sentence_case(text)
    db_handler.insert_news(city_cased, text_cased, current_date)
    return f"News: {text_cased} | City: {city_cased} | Date: {current_date}\n"

def create_private_ad_record(text, expiration_date_str):
    try:
        expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format.\n"
    current_date = datetime.datetime.now()
    days_left = (expiration_date - current_date).days
    text_cased = sentence_case(text)
    db_handler.insert_private_ad(text_cased, expiration_date_str, days_left)
    return f"Private Ad: {text_cased} | Expiration Date: {expiration_date_str} | Days Left: {days_left}\n"

def create_event_record(event_name, event_date_str):
    try:
        event_date = datetime.datetime.strptime(event_date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format.\n"
    current_date = datetime.datetime.now()
    days_until = (event_date - current_date).days
    name_cased = sentence_case(event_name)
    db_handler.insert_event(name_cased, event_date_str, days_until)
    return f"Event: {name_cased} | Event Date: {event_date_str} | Days Until Event: {days_until}\n"

# Function to generate word count CSV
def generate_word_count_csv(filename="news_feed.txt", output_csv="word_count.csv"):
    with open(filename, "r") as f:
        text = f.read().lower()
    words = [word.strip(string.punctuation) for word in text.split()]
    word_counts = Counter(words)

    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word", "count"])
        for word, count in word_counts.items():
            if word:  # avoid empty strings
                writer.writerow([word, count])

# Function to generate letter count CSV
def generate_letter_count_csv(filename="news_feed.txt", output_csv="letter_count.csv"):
    with open(filename, "r") as f:
        text = f.read()

    letters_only = [char for char in text if char.isalpha()]
    total_letters = len(letters_only)
    letter_counts = Counter(char.lower() for char in letters_only)
    uppercase_counts = Counter(char for char in text if char.isupper())

    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["letter", "count_all", "count_uppercase", "percentage"])
        for letter in sorted(letter_counts):
            count_all = letter_counts[letter]
            count_upper = uppercase_counts.get(letter.upper(), 0)
            percentage = (count_all / total_letters) * 100 if total_letters > 0 else 0
            writer.writerow([letter, count_all, count_upper, f"{percentage:.2f}%"])

# Function to add record to a text file and regenerate CSVs
def add_record_to_file(record, filename="news_feed.txt"):
    with open(filename, "a") as file:
        file.write(record)
    print("Record added successfully!")

    # Regenerate CSV reports
    generate_word_count_csv(filename)
    generate_letter_count_csv(filename)

# Class to process records from a plain text file
class FileRecordProcessor:
    def __init__(self, folder_path="input_files"):
        self.folder_path = folder_path

    def process_file(self, filename=None):
        file_path = filename if filename else os.path.join(self.folder_path, "input.txt")

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        try:
            with open(file_path, "r") as file:
                lines = [line.strip() for line in file if line.strip()]

            i = 0
            while i < len(lines):
                record_type = lines[i].lower()
                if record_type == "news":
                    city = lines[i+1]
                    text = lines[i+2]
                    record = create_news_record(city, text)
                    i += 3
                elif record_type == "ad":
                    text = lines[i+1]
                    exp_date = lines[i+2]
                    record = create_private_ad_record(text, exp_date)
                    i += 3
                elif record_type == "event":
                    name = lines[i+1]
                    date = lines[i+2]
                    record = create_event_record(name, date)
                    i += 3
                else:
                    print(f"Unknown record type: {lines[i]}")
                    i += 1
                    continue

                add_record_to_file(record)

            os.remove(file_path)
            print(f"File '{file_path}' processed and removed.")

        except Exception as e:
            print(f"Error processing file: {e}")

# Class to process records from a JSON file
class JSONRecordProcessor:
    def __init__(self, folder_path="input_files"):
        self.folder_path = folder_path

    def process_file(self, filename=None):
        file_path = filename if filename else os.path.join(self.folder_path, "input.json")

        if not os.path.exists(file_path):
            print(f"JSON file not found: {file_path}")
            return

        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)

            if not isinstance(data, list):
                print("Invalid JSON format. Expected a list of records.")
                return

            for record in data:
                record_type = record.get("type", "").lower()

                if record_type == "news":
                    city = record.get("city", "")
                    text = record.get("text", "")
                    if not city or not text:
                        print("Invalid News record. Skipping.")
                        continue
                    formatted_record = create_news_record(city, text)

                elif record_type == "ad":
                    text = record.get("text", "")
                    exp_date = record.get("expiration_date", "")
                    if not text or not exp_date:
                        print("Invalid Ad record. Skipping.")
                        continue
                    formatted_record = create_private_ad_record(text, exp_date)

                elif record_type == "event":
                    name = record.get("event_name", "")
                    date = record.get("event_date", "")
                    if not name or not date:
                        print("Invalid Event record. Skipping.")
                        continue
                    formatted_record = create_event_record(name, date)

                else:
                    print(f"Unknown record type: {record_type}. Skipping.")
                    continue

                add_record_to_file(formatted_record)

            os.remove(file_path)
            print(f"JSON file '{file_path}' processed and removed.")

        except Exception as e:
            print(f"Error processing JSON file: {e}")

# Class to process records from an XML file
class XMLRecordProcessor:
    def __init__(self, folder_path="input_files"):
        self.folder_path = folder_path

    def process_file(self, filename=None):
        file_path = filename if filename else os.path.join(self.folder_path, "input.xml")

        if not os.path.exists(file_path):
            print(f"XML file not found: {file_path}")
            return

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            for elem in root.findall("record"):
                record_type = elem.get("type", "").lower()

                if record_type == "news":
                    city = elem.findtext("city", default="")
                    text = elem.findtext("text", default="")
                    if not city or not text:
                        print("Invalid News record. Skipping.")
                        continue
                    formatted_record = create_news_record(city, text)

                elif record_type == "ad":
                    text = elem.findtext("text", default="")
                    exp_date = elem.findtext("expiration_date", default="")
                    if not text or not exp_date:
                        print("Invalid Ad record. Skipping.")
                        continue
                    formatted_record = create_private_ad_record(text, exp_date)

                elif record_type == "event":
                    name = elem.findtext("event_name", default="")
                    date = elem.findtext("event_date", default="")
                    if not name or not date:
                        print("Invalid Event record. Skipping.")
                        continue
                    formatted_record = create_event_record(name, date)

                else:
                    print(f"Unknown record type: {record_type}. Skipping.")
                    continue

                add_record_to_file(formatted_record)

            os.remove(file_path)
            print(f"XML file '{file_path}' processed and removed.")

        except Exception as e:
            print(f"Error processing XML file: {e}")

# ---------- Database Handler ----------
class DatabaseHandler:
    def __init__(self, db_name="records.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            text TEXT,
            date TEXT,
            UNIQUE(city, text, date)
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS private_ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            expiration_date TEXT,
            days_left INTEGER,
            UNIQUE(text, expiration_date)
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            event_date TEXT,
            days_until INTEGER,
            UNIQUE(name, event_date)
        )""")
        self.conn.commit()

    def insert_news(self, city, text, date):
        try:
            self.cursor.execute("INSERT INTO news (city, text, date) VALUES (?, ?, ?)",
                                (city, text, date))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Duplicate News record. Skipping DB insert.")

    def insert_private_ad(self, text, expiration_date, days_left):
        try:
            self.cursor.execute("INSERT INTO private_ads (text, expiration_date, days_left) VALUES (?, ?, ?)",
                                (text, expiration_date, days_left))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Duplicate Private Ad. Skipping DB insert.")

    def insert_event(self, name, event_date, days_until):
        try:
            self.cursor.execute("INSERT INTO events (name, event_date, days_until) VALUES (?, ?, ?)",
                                (name, event_date, days_until))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Duplicate Event. Skipping DB insert.")

    def close(self):
        self.conn.close()

db_handler = DatabaseHandler()

# ---------- View stored data ----------
def view_all_data(db_name="records.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    tables = {
        "news": ["city", "text", "date"],
        "private_ads": ["text", "expiration_date", "days_left"],
        "events": ["name", "event_date", "days_until"]
    }
    for table, columns in tables.items():
        print(f"\n--- {table.upper()} ---")
        cursor.execute(f"SELECT {', '.join(columns)} FROM {table}")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(dict(zip(columns, row)))
        else:
            print("No records found.")
    conn.close()

# Main application logic
def main():
    print("Welcome to the News Feed Generator Tool!")

    while True:
        print("\nChoose an option:")
        print("1. Add record manually in file and database")
        print("2. Add records from text file")
        print("3. Add records from JSON file")
        print("4. Add records from XML file")
        print("5. View stored database records")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            print("\nSelect record type:")
            print("1. News")
            print("2. Private Ad")
            print("3. Event")
            record_choice = input("Enter your choice (1-3): ")

            if record_choice == "1":
                city = input("Enter the city for the News: ")
                text = input("Enter the text for the News: ")
                record = create_news_record(city, text)
            elif record_choice == "2":
                text = input("Enter the text for the Private Ad: ")
                exp_date = input("Enter the expiration date (YYYY-MM-DD): ")
                record = create_private_ad_record(text, exp_date)
            elif record_choice == "3":
                name = input("Enter the event name: ")
                date = input("Enter the event date (YYYY-MM-DD): ")
                record = create_event_record(name, date)
            else:
                print("Invalid choice.")
                continue

            add_record_to_file(record)

        elif choice == "2":
            file_path = input("Enter file path or press Enter to use default: ")
            processor = FileRecordProcessor()
            processor.process_file(file_path if file_path else None)

        elif choice == "3":
            file_path = input("Enter JSON file path or press Enter to use default: ")
            processor = JSONRecordProcessor()
            processor.process_file(file_path if file_path else None)

        elif choice == "4":
            file_path = input("Enter XML file path or press Enter to use default: ")
            processor = XMLRecordProcessor()
            processor.process_file(file_path if file_path else None)

        elif choice == "5":
            view_all_data()

        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

# Run the program
if __name__ == "__main__":
    main()