import datetime
import json
import os

# Define file name to store published records in JSON format
OUTPUT_FILE = "output_records.json"


# Function to write content to the JSON file
def write_to_json(record):
    """Appends the given record to the JSON file."""
    if not os.path.exists(OUTPUT_FILE):
        # If file does not exist, create it with an empty list
        with open(OUTPUT_FILE, 'w') as file:
            json.dump([], file)

    # Read existing data, append new record, and write it back to the file
    with open(OUTPUT_FILE, 'r') as file:
        data = json.load(file)

    data.append(record)

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(data, file, indent=4)


# Function to publish news
def publish_news(text, city):
    """Publishes a News record."""
    date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    news_record = {
        "type": "news",
        "text": text,
        "city": city,
        "date_published": date_published
    }
    write_to_json(news_record)
    print("News published successfully!\n")


# Function to publish private ad with error handling for invalid dates
def publish_private_ad(text, expiration_date_input):
    """Publishes a Private Ad record."""
    try:
        expiration_date = datetime.datetime.strptime(expiration_date_input, "%Y-%m-%d")
        days_left = (expiration_date - datetime.datetime.now()).days

        # Ensure that the expiration date is not in the past
        if days_left < 0:
            raise ValueError("Expiration date is in the past.")

        private_ad_record = {
            "type": "private_ad",
            "text": text,
            "expiration_date": expiration_date_input,
            "days_left": days_left
        }
        write_to_json(private_ad_record)
        print("Private ad published successfully!\n")
    except ValueError as e:
        print(f"Error: {e}. Failed to publish private ad.")


# Function to publish unique record
def publish_unique_record(text):
    """Publishes a unique record."""
    reversed_text = text[::-1]
    unique_record = {
        "type": "unique_record",
        "text": text,
        "reversed_text": reversed_text,
        "published_on": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    write_to_json(unique_record)
    print("Unique record published successfully!\n")


# Class to handle record processing from a JSON file
class RecordProcessor:
    def __init__(self, file_path=None):
        """Initializes the processor with the default or user-provided file path."""
        self.file_path = file_path or "records.json"  # Default file path

    def process_records(self):
        """Reads and processes records from the JSON file."""
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist.")
            return

        try:
            with open(self.file_path, 'r') as file:
                records = json.load(file)

            for record in records:
                record_type = record.get("type").lower()
                if record_type == "news":
                    publish_news(record["text"], record["city"])
                elif record_type == "private_ad":
                    publish_private_ad(record["text"], record["expiration_date"])
                elif record_type == "unique_record":
                    publish_unique_record(record["text"])
                else:
                    print(f"Unknown record type: {record_type}")

            # If all records are processed successfully, remove the file
            os.remove(self.file_path)
            print(f"File '{self.file_path}' processed and removed successfully.")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading or processing JSON file: {e}")


# Main menu function
def main_menu():
    """Displays the menu and lets the user choose what type of record to publish."""
    while True:
        print("Choose an option to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Unique Record")
        print("4. Process Records from JSON File")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            text = input("Enter news text: ")
            city = input("Enter city: ")
            publish_news(text, city)
        elif choice == '2':
            text = input("Enter ad text: ")
            expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
            publish_private_ad(text, expiration_date)
        elif choice == '3':
            text = input("Enter your unique record text: ")
            publish_unique_record(text)
        elif choice == '4':
            file_path = input("Enter JSON file path (or press Enter for default 'records.json'): ") or None
            processor = RecordProcessor(file_path)
            processor.process_records()
        elif choice == '5':
            print("Exiting the tool. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


# Entry point of the program
if __name__ == "__main__":
    main_menu()
