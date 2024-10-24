import csv
import os
import re
from collections import Counter

# File name for the published records
FILE_NAME = "news_feed.txt"
WORD_COUNT_CSV = "word_count.csv"
LETTER_STATS_CSV = "letter_stats.csv"

# Function to calculate word counts and write to CSV
def update_word_count(text):
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words, converted to lowercase
    word_counts = Counter(words)

    with open(WORD_COUNT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['word', 'count'])  # Header
        writer.writerows(word_counts.items())  # Write word and count


# Function to calculate letter statistics and write to CSV
def update_letter_stats(text):
    letters = [c for c in text if c.isalpha()]  # Only alphabetic characters
    total_letters = len(letters)
    letter_counts = Counter(letters)

    with open(LETTER_STATS_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['letter', 'count_all', 'count_uppercase', 'percentage'])  # Header

        for letter, count_all in letter_counts.items():
            count_upper = sum(1 for c in text if c == letter.upper())  # Count uppercase occurrences
            percentage = (count_all / total_letters) * 100 if total_letters > 0 else 0
            writer.writerow([letter.lower(), count_all, count_upper, f"{percentage:.2f}%"])


# Function to read the file and update both CSVs
def process_text_file():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file:
            text = file.read()

        # Update both word count and letter stats CSVs
        update_word_count(text)
        update_letter_stats(text)
        print("CSV files updated successfully.")
    else:
        print(f"File '{FILE_NAME}' does not exist.")


# Example usage: Process the text file and update CSVs
if __name__ == "__main__":
    process_text_file()
