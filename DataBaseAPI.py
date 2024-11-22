import os
import datetime
import xml.etree.ElementTree as ET
import sqlite3

# Constants for file names and folders
DEFAULT_FILE_NAME = "news_feed.xml"
DEFAULT_FOLDER_PATH = "."
DB_FILE = "news_feed.db"


# Database class for managing records in SQLite
class DatabaseManager:
    def __init__(self, db_file=DB_FILE):
        """Initializes the database and creates tables if they do not exist."""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.initialize_tables()

    def initialize_tables(self):
        """Creates tables for each record type if they do not already exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS News (
                                id INTEGER PRIMARY KEY,
                                text TEXT UNIQUE,
                                city TEXT,
                                date_published TEXT
                              )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS PrivateAd (
                                id INTEGER PRIMARY KEY,
                                text TEXT UNIQUE,
                                expiration_date TEXT,
                                days_left INTEGER
                              )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS UniqueRecord (
                                id INTEGER PRIMARY KEY,
                                original_text TEXT UNIQUE,
                                reversed_text TEXT,
                                published_on TEXT
                              )''')
        self.conn.commit()

    def add_news(self, text, city, date_published):
        """Adds a news record to the News table if it is unique."""
        try:
            self.cursor.execute("INSERT INTO News (text, city, date_published) VALUES (?, ?, ?)",
                                (text, city, date_published))
            self.conn.commit()
            print("News record added to database successfully.")
        except sqlite3.IntegrityError:
            print("Duplicate News record. Skipping insertion.")

    def add_private_ad(self, text, expiration_date, days_left):
        """Adds a private ad record to the PrivateAd table if it is unique."""
        try:
            self.cursor.execute("INSERT INTO PrivateAd (text, expiration_date, days_left) VALUES (?, ?, ?)",
                                (text, expiration_date, days_left))
            self.conn.commit()
            print("Private Ad record added to database successfully.")
        except sqlite3.IntegrityError:
            print("Duplicate Private Ad record. Skipping insertion.")

    def add_unique_record(self, original_text, reversed_text, published_on):
        """Adds a unique record to the UniqueRecord table if it is unique."""
        try:
            self.cursor.execute(
                "INSERT INTO UniqueRecord (original_text, reversed_text, published_on) VALUES (?, ?, ?)",
                (original_text, reversed_text, published_on))
            self.conn.commit()
            print("Unique record added to database successfully.")
        except sqlite3.IntegrityError:
            print("Duplicate Unique record. Skipping insertion.")

    def close(self):
        """Closes the database connection."""
        self.conn.close()


# XML and File Management class
class XMLNewsFeed:
    def __init__(self, folder_path=None):
        """Initialize with a default or user-provided file path."""
        self.folder_path = folder_path or DEFAULT_FOLDER_PATH
        os.makedirs(self.folder_path, exist_ok=True)
        self.file_path = os.path.join(self.folder_path, DEFAULT_FILE_NAME)
        self.initialize_xml()

    def initialize_xml(self):
        """Initialize XML file with a root element if it doesn't exist."""
        if not os.path.exists(self.file_path):
            root = ET.Element("Records")
            tree = ET.ElementTree(root)
            tree.write(self.file_path)

    def write_to_xml(self, record_type, content):
        """Writes content to XML file."""
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        record = ET.SubElement(root, record_type)
        for key, value in content.items():
            element = ET.SubElement(record, key)
            element.text = value

        tree.write(self.file_path, encoding="utf-8", xml_declaration=True)

    def publish_news(self, db_manager):
        """Collects user input for a News record, publishes it to XML, and saves to database."""
        text = input("Enter news text: ")
        city = input("Enter city: ")
        date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        content = {
            "text": text,
            "city": city,
            "date_published": date_published
        }
        self.write_to_xml("News", content)
        db_manager.add_news(text, city, date_published)

    def publish_private_ad(self, db_manager):
        """Collects user input for a Private Ad record, publishes it to XML, and saves to database."""
        text = input("Enter ad text: ")

        while True:
            expiration_date_input = input("Enter expiration date (YYYY-MM-DD): ")
            try:
                expiration_date = datetime.datetime.strptime(expiration_date_input, "%Y-%m-%d")
                days_left = (expiration_date - datetime.datetime.now()).days

                if days_left < 0:
                    print("Expiration date is in the past. Please enter a valid future date.")
                    continue

                content = {
                    "text": text,
                    "expiration_date": expiration_date_input,
                    "days_left": str(days_left)
                }
                self.write_to_xml("PrivateAd", content)
                db_manager.add_private_ad(text, expiration_date_input, days_left)
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    def publish_unique_record(self, db_manager):
        """Collects user input for a unique record type, publishes it to XML, and saves to database."""
        text = input("Enter your unique record text: ")
        reversed_text = text[::-1]
        published_on = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        content = {
            "original_text": text,
            "reversed_text": reversed_text,
            "published_on": published_on
        }
        self.write_to_xml("UniqueRecord", content)
        db_manager.add_unique_record(text, reversed_text, published_on)

    def process_file_input(self, db_manager, input_file_path=None):
        """Reads records from a provided XML file, adds them to XML and database, then deletes file."""
        input_file_path = input_file_path or input("Enter the path of the XML file to process: ")
        try:
            tree = ET.parse(input_file_path)
            root = tree.getroot()
            for record in root:
                record_type = record.tag
                content = {elem.tag: elem.text for elem in record}
                self.write_to_xml(record_type, content)

                if record_type == "News":
                    db_manager.add_news(content["text"], content["city"], content["date_published"])
                elif record_type == "PrivateAd":
                    db_manager.add_private_ad(content["text"], content["expiration_date"], int(content["days_left"]))
                elif record_type == "UniqueRecord":
                    db_manager.add_unique_record(content["original_text"], content["reversed_text"],
                                                 content["published_on"])

            os.remove(input_file_path)
            print(f"File '{input_file_path}' processed and removed successfully!\n")
        except (ET.ParseError, FileNotFoundError, PermissionError) as e:
            print(f"Error processing file: {e}\n")


def main_menu():
    """Displays the menu and lets the user choose what type of record to publish."""
    folder_path = input("Enter folder path to store XML (leave blank for default): ").strip()
    feed = XMLNewsFeed(folder_path if folder_path else None)
    db_manager = DatabaseManager()

    while True:
        print("Choose an option to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Unique Record")
        print("4. Process XML Input File")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            feed.publish_news(db_manager)
        elif choice == '2':
            feed.publish_private_ad(db_manager)
        elif choice == '3':
            feed.publish_unique_record(db_manager)
        elif choice == '4':
            input_file_path = input("Enter the path of the XML file to process: ").strip()
            feed.process_file_input(db_manager, input_file_path)
        elif choice == '5':
            db_manager.close()
            print("Exiting the tool. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


# Entry point of the program
if __name__ == "__main__":
    main_menu()
