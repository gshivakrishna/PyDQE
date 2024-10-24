import datetime
import os

# Define file name to store published records
FILE_NAME = "news_feed.txt"
DEFAULT_INPUT_FILE = "input_records.txt"  # Default input file if not provided


class NewsFeed:
    def __init__(self, output_file=FILE_NAME):
        self.output_file = output_file

    # Function to write content to the file
    def write_to_file(self, content):
        """Appends the given content to the file."""
        with open(self.output_file, 'a') as file:
            file.write(content + "\n\n")  # Add two new lines after each record for readability

    # Function to publish news
    def publish_news(self, text, city):
        """Publishes a News record."""
        date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        news_record = f"News -----------\n{text}\nCity: {city}, Date: {date_published}"
        self.write_to_file(news_record)
        print("News published successfully!\n")

    # Function to publish private ad with error handling for invalid dates
    def publish_private_ad(self, text, expiration_date_input):
        """Publishes a Private Ad record."""
        try:
            # Try to parse the date and calculate days left
            expiration_date = datetime.datetime.strptime(expiration_date_input, "%Y-%m-%d")
            days_left = (expiration_date - datetime.datetime.now()).days

            if days_left < 0:
                print("Expiration date is in the past. Cannot publish this ad.")
                return

            private_ad_record = f"Private Ad -----------\n{text}\nExpires: {expiration_date_input}, Days Left: {days_left}"
            self.write_to_file(private_ad_record)
            print("Private ad published successfully!\n")
        except ValueError:
            print("Invalid date format. Skipping this record.")

    # Function to publish a unique record
    def publish_unique_record(self, text):
        """Publishes a Unique Record."""
        reversed_text = text[::-1]
        unique_record = f"Unique Record -----------\nOriginal: {text}\nReversed: {reversed_text}\nPublished on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        self.write_to_file(unique_record)
        print("Unique record published successfully!\n")

    def process_file(self, file_path=DEFAULT_INPUT_FILE):
        """Processes records from a text file and publishes them."""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    record_data = line.strip().split('|')
                    if len(record_data) >= 2:
                        record_type = record_data[0]
                        text = record_data[1]

                        if record_type == 'News' and len(record_data) == 3:
                            city = record_data[2]
                            self.publish_news(text, city)
                        elif record_type == 'PrivateAd' and len(record_data) == 3:
                            expiration_date = record_data[2]
                            self.publish_private_ad(text, expiration_date)
                        elif record_type == 'UniqueRecord' and len(record_data) == 2:
                            self.publish_unique_record(text)
                        else:
                            print(f"Invalid record format: {line.strip()}")
                    else:
                        print(f"Incomplete record: {line.strip()}")

            # If the file was processed successfully, remove it
            os.remove(file_path)
            print(f"File '{file_path}' processed and deleted successfully.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")


def main_menu():
    """Displays the menu and lets the user choose what type of record to publish."""
    news_feed = NewsFeed()  # Create an instance of the NewsFeed class

    while True:
        print("Choose an option to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Unique Record")
        print("4. Process records from file")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            text = input("Enter news text: ")
            city = input("Enter city: ")
            news_feed.publish_news(text, city)
        elif choice == '2':
            text = input("Enter ad text: ")
            expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
            news_feed.publish_private_ad(text, expiration_date)
        elif choice == '3':
            text = input("Enter your unique record text: ")
            news_feed.publish_unique_record(text)
        elif choice == '4':
            file_path = input(f"Enter the file path (default: {DEFAULT_INPUT_FILE}): ").strip()
            if not file_path:
                file_path = DEFAULT_INPUT_FILE
            news_feed.process_file(file_path)
        elif choice == '5':
            print("Exiting the tool. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main_menu()
