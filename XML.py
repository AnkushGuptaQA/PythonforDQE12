import datetime
import os
import csv
import string
import json
import xml.etree.ElementTree as ET
from collections import Counter

def sentence_case(text):
    """Converts text to sentence case."""
    return text[:1].upper() + text[1:]

# Function to handle the 'News' type record
def create_news_record(city, text):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    record = f"News: {sentence_case(text)} | City: {sentence_case(city)} | Date: {current_date}\n"
    return record

# Function to handle the 'Private Ad' type record
def create_private_ad_record(text, expiration_date_str):
    try:
        expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format.\n"
    current_date = datetime.datetime.now()
    days_left = (expiration_date - current_date).days
    record = f"Private Ad: {sentence_case(text)} | Expiration Date: {expiration_date_str} | Days Left: {days_left}\n"
    return record

# Function to handle the 'Event' type record
def create_event_record(event_name, event_date_str):
    try:
        event_date = datetime.datetime.strptime(event_date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format.\n"
    current_date = datetime.datetime.now()
    days_until_event = (event_date - current_date).days
    record = f"Event: {sentence_case(event_name)} | Event Date: {event_date_str} | Days Until Event: {days_until_event}\n"
    return record

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

# Main application logic
def main():
    print("Welcome to the News Feed Generator Tool!")

    while True:
        print("\nChoose an option:")
        print("1. Add record manually")
        print("2. Add records from text file")
        print("3. Add records from JSON file")
        print("4. Add records from XML file")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

# Run the program
if __name__ == "__main__":
    main()