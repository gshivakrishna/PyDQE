import datetime

# Define file name to store published records
FILE_NAME = "news_feed.txt"


# Function to write content to the file
def write_to_file(content):
    """Appends the given content to the file."""
    with open(FILE_NAME, 'a') as file:
        file.write(content + "\n\n")  # Add two new lines after each record for readability


# Function to publish news
def publish_news():
    """Collects user input for a News record and publishes it."""
    text = input("Enter news text: ")
    city = input("Enter city: ")
    date_published = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    news_record = f"News -----------\n{text}\nCity: {city}, Date: {date_published}"
    write_to_file(news_record)
    print("News published successfully!\n")


# Function to publish private ad with error handling for invalid dates
def publish_private_ad():
    """Collects user input for a Private Ad record and publishes it."""
    text = input("Enter ad text: ")

    # Loop until a valid expiration date is entered
    while True:
        expiration_date_input = input("Enter expiration date (YYYY-MM-DD): ")
        try:
            # Try to parse the date and calculate days left
            expiration_date = datetime.datetime.strptime(expiration_date_input, "%Y-%m-%d")
            days_left = (expiration_date - datetime.datetime.now()).days

            # Ensure that the expiration date is not in the past
            if days_left < 0:
                print("Expiration date is in the past. Please enter a valid future date.")
                continue  # Prompt again for correct input

            private_ad_record = f"Private Ad -----------\n{text}\nExpires: {expiration_date_input}, Days Left: {days_left}"
            write_to_file(private_ad_record)
            print("Private ad published successfully!\n")
            break  # Exit the loop once valid input is given
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")


# Unique record type
def publish_unique_record():
    """Collects user input for a unique record type and publishes it."""
    text = input("Enter your unique record text: ")

    # Adding custom rule: add a reversed version of the text
    reversed_text = text[::-1]

    unique_record = f"Unique Record -----------\nOriginal: {text}\nReversed: {reversed_text}\nPublished on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    write_to_file(unique_record)
    print("Unique record published successfully!\n")


# Main menu function
def main_menu():
    """Displays the menu and lets the user choose what type of record to publish."""
    while True:
        print("Choose an option to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Unique Record")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            publish_news()
        elif choice == '2':
            publish_private_ad()
        elif choice == '3':
            publish_unique_record()
        elif choice == '4':
            print("Exiting the tool. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


# Entry point of the program
if __name__ == "__main__":
    main_menu()
