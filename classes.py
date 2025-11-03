import datetime


# Function to handle the 'News' type record
def create_news_record():
    city = input("Enter the city for the News: ")
    text = input("Enter the text for the News: ")
    # Get today's date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    record = f"News: {text} | City: {city} | Date: {current_date}\n"
    return record


# Function to handle the 'Private Ad' type record
def create_private_ad_record():
    text = input("Enter the text for the Private Ad: ")
    expiration_date_str = input("Enter the expiration date (YYYY-MM-DD): ")
    # Parse the expiration date
    expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d")
    # Calculate days left until expiration
    current_date = datetime.datetime.now()
    days_left = (expiration_date - current_date).days
    record = f"Private Ad: {text} | Expiration Date: {expiration_date_str} | Days Left: {days_left}\n"
    return record


# Function to handle the 'Event' type record (unique record with custom rules)
def create_event_record():
    event_name = input("Enter the event name: ")
    event_date_str = input("Enter the event date (YYYY-MM-DD): ")
    # Parse the event date
    event_date = datetime.datetime.strptime(event_date_str, "%Y-%m-%d")
    # Calculate days until the event
    current_date = datetime.datetime.now()
    days_until_event = (event_date - current_date).days
    record = f"Event: {event_name} | Event Date: {event_date_str} | Days Until Event: {days_until_event}\n"
    return record


# Function to add record to a text file
def add_record_to_file(record, filename="news_feed.txt"):
    with open(filename, "a") as file:
        file.write(record)
    print("Record added successfully!")


# Main function to handle user input and record generation
def main():
    print("Welcome to the News Feed Generator Tool!")

    while True:
        # Ask user to choose record type
        print("\nChoose a record type:")
        print("1. News")
        print("2. Private Ad")
        print("3. Event (Unique record with custom rules)")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            record = create_news_record()
        elif choice == "2":
            record = create_private_ad_record()
        elif choice == "3":
            record = create_event_record()
        else:
            print("Invalid choice, please try again.")
            continue

        # Add the record to the file
        add_record_to_file(record)


# Execute the main function
if __name__ == "__main__":
    main()