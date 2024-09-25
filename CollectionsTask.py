import random
import string

# Step 1: Generate a list of random number of dictionaries (from 2 to 10)
num_of_dicts = random.randint(2, 10)  # Random number of dictionaries between 2 and 10
list_of_dicts = []  # List to store the generated dictionaries

# Loop to create random dictionaries
for i in range(num_of_dicts):
    num_of_keys = random.randint(1, 6)  # Random number of keys in the dict (between 1 and 6)
    new_dict = {}

    # Generate random letter keys and assign random values (0-100)
    for _ in range(num_of_keys):
        random_key = random.choice(string.ascii_lowercase)  # Random lowercase letter as key
        random_value = random.randint(0, 100)  # Random number between 0 and 100 as value
        new_dict[random_key] = random_value

    list_of_dicts.append(new_dict)  # Add the newly generated dict to the list

# Output of step 1 (list of dicts)
print("Generated list of dicts:", list_of_dicts)

# Step 2: Create one common dict based on the rules provided
common_dict = {}  # Dictionary to store the final merged values

# Iterate over each dict in the list with its index
for idx, d in enumerate(list_of_dicts):
    dict_number = idx + 1  # The current dict number (1-based index)

    # Loop through each key, value pair in the current dictionary
    for key, value in d.items():
        # Check if the key already exists in the common dict
        if key in common_dict:
            # Compare values and keep the max, while renaming the key
            if value > common_dict[key][1]:
                common_dict[key] = (f"{key}_{dict_number}", value)
        else:
            # If the key doesn't exist, add it directly
            common_dict[key] = (key, value)

# Convert the common_dict back into a simplified form {key: value}
final_dict = {new_key: value for new_key, (new_key, value) in common_dict.items()}

# Output the final merged dictionary
print("Final merged dict:", final_dict)
