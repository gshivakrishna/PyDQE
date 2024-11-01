import datetime
import os
import xml.etree.ElementTree as ET

# Default file name and directory for storing records
DEFAULT_FILE_NAME = "news_feed.xml"
DEFAULT_FOLDER_PATH = "."


class XMLNewsFeed:
    def __init__(self, folder_path=None):
        """Initialize with a default or user-provided file path."""
        self.folder_path = folder_path or DEFAULT_FOLDER_PATH
        os.makedirs(self.folder_path, exist_ok=True)  # Ensure the folder path exists
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

    def publish_news(self):
        """Collects user input for a News record and publishes it to XML."""
        text = input("Enter news text: ")
        city = input("Enter city: ")
        date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        content = {
            "text": text,
            "city": city,
            "date_published": date_published
        }
        self.write_to_xml("News", content)
        print("News published successfully!\n")

    def publish_private_ad(self):
        """Collects user input for a Private Ad record and publishes it to XML."""
        text = input("Enter ad text: ")

        # Loop until a valid expiration date is entered
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
                print("Private ad published successfully!\n")
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    def publish_unique_record(self):
        """Collects user input for a unique record type and publishes it to XML."""
        text = input("Enter your unique record text: ")
        reversed_text = text[::-1]

        content = {
            "original_text": text,
            "reversed_text": reversed_text,
            "published_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.write_to_xml("UniqueRecord", content)
        print("Unique record published successfully!\n")

    def process_file_input(self, input_file_path=None):
        """Reads records from a provided XML file and adds them to the main XML file, then deletes the input file."""
        input_file_path = input_file_path or input("Enter the path of the XML file to process: ")

        try:
            tree = ET.parse(input_file_path)
            root = tree.getroot()
            for record in root:
                record_type = record.tag
                content = {elem.tag: elem.text for elem in record}
                self.write_to_xml(record_type, content)

            os.remove(input_file_path)
            print(f"File '{input_file_path}' processed and removed successfully!\n")
        except (ET.ParseError, FileNotFoundError, PermissionError) as e:
            print(f"Error processing file: {e}\n")


def main_menu():
    """Displays the menu and lets the user choose what type of record to publish."""
    folder_path = input("Enter folder path to store XML (leave blank for default): ").strip()
    feed = XMLNewsFeed(folder_path if folder_path else None)

    while True:
        print("Choose an option to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Unique Record")
        print("4. Process XML Input File")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            feed.publish_news()
        elif choice == '2':
            feed.publish_private_ad()
        elif choice == '3':
            feed.publish_unique_record()
        elif choice == '4':
            input_file_path = input("Enter the path of the XML file to process: ").strip()
            feed.process_file_input(input_file_path)
        elif choice == '5':
            print("Exiting the tool. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


# Entry point of the program
if __name__ == "__main__":
    main_menu()
