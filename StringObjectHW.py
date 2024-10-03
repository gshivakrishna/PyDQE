import re

# Step 1: Assign the given text to a variable
text = """
tHis iz your homeWork, copy these Text to variable.

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""


# Step 2: Normalize text case - sentence capitalization
def normalize_case(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    normalized_sentences = [sentence.capitalize() for sentence in sentences]
    return ' '.join(normalized_sentences)


normalized_text = normalize_case(text)


# Step 3: Fix "iZ" to "is" only where it is a mistake
def fix_misspelling(text):
    return re.sub(r'\b[iI][zZ]\b', 'is', text)


corrected_text = fix_misspelling(normalized_text)


# Step 4: Create a new sentence with the last word of each existing sentence
def create_last_word_sentence(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    last_words = [sentence.rstrip('.!?').split()[-1] for sentence in sentences if sentence]
    return ' '.join(last_words).capitalize() + '.'


last_word_sentence = create_last_word_sentence(corrected_text)

# Step 5: Add the new sentence to the paragraph
final_text = corrected_text.strip() + " " + last_word_sentence

# Step 6: Count the number of whitespace characters (spaces, tabs, newlines)
whitespace_count = sum(1 for char in text if char.isspace())

# Output results
print("Normalized and Corrected Text:\n")
print(final_text)
print("\nNumber of whitespace characters:", whitespace_count)
