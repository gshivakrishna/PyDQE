import re


# Function to normalize sentence case
def normalize_sentence(sentence):
    """Capitalizes the first letter of the sentence and lowercases the rest."""
    return sentence.capitalize()


# Function to normalize all sentences in the text
def normalize_case(text):
    """Normalizes the case for all sentences in the given text."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())  # Split sentences by punctuation
    normalized_sentences = list(map(normalize_sentence, sentences))  # Apply normalization to each sentence
    return ' '.join(normalized_sentences)  # Join sentences back


# Function to fix "iZ" to "is" where it's incorrect
def fix_misspelling(word):
    """Replaces 'iZ' with 'is' in the text where appropriate."""
    return re.sub(r'\b[iI][zZ]\b', 'is', word)  # Fix "iZ" or case variations


# Function to fix misspellings across the entire text
def correct_misspellings(text):
    """Fixes all known misspellings in the text."""
    return fix_misspelling(text)


# Function to extract the last word from a sentence
def extract_last_word(sentence):
    """Returns the last word of a given sentence."""
    return sentence.rstrip('.!?').split()[-1]


# Function to create a sentence from the last words of all sentences
def create_last_word_sentence(text):
    """Creates a new sentence from the last words of each sentence in the text."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())  # Split sentences
    last_words = list(map(extract_last_word, sentences))  # Extract last words
    return ' '.join(last_words).capitalize() + '.'  # Create a new sentence


# Function to count all whitespace characters
def count_whitespaces(text):
    """Counts all whitespace characters (spaces, tabs, newlines) in the text."""
    return sum(1 for char in text if char.isspace())


# Function to process the entire text step by step
def process_text(text):
    """Processes the text by normalizing, fixing misspellings, creating a new sentence, and counting whitespaces."""
    # Normalize case
    normalized_text = normalize_case(text)

    # Fix misspellings
    corrected_text = correct_misspellings(normalized_text)

    # Create a new sentence from last words
    last_word_sentence = create_last_word_sentence(corrected_text)

    # Combine corrected text and new sentence
    final_text = corrected_text.strip() + " " + last_word_sentence

    # Count whitespaces in the original text (including tabs, newlines, etc.)
    whitespace_count = count_whitespaces(text)

    return final_text, whitespace_count


# Input text
text = """
tHis iz your homeWork, copy these Text to variable.

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

# Process the text
final_text, whitespace_count = process_text(text)

# Output the results
print("Normalized and Corrected Text:\n")
print(final_text)
print("\nNumber of whitespace characters:", whitespace_count)
