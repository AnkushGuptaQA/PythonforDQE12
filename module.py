import datetime
import os


def sentence_case(text):
    """Converts text to sentence case."""
    return text.capitalize()


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


# Function to add record to a text file
def add_record_to_file(record, filename="news_feed.txt"):
    with open(filename, "a") as file:
        file.write(record)
    print("Record added successfully!")


# Class to process records from file
class FileRecordProcessor:
    def __init__(self, folder_path="input_files"):
        self.folder_path = folder_path

    def process_file(self, filename=None):
        # Get user file path or use default
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

            # Remove the file after processing
            os.remove(file_path)
            print(f"File '{file_path}' processed and removed.")

        except Exception as e:
            print(f"Error processing file: {e}")


# Main function to handle user input and record generation
def main():
    print("Welcome to the News Feed Generator Tool!")

    while True:
        print("\nChoose an option:")
        print("1. Add record manually")
        print("2. Add records from file")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


# Execute the main function
if __name__ == "__main__":
    main()
