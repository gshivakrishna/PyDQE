import random
import string


# Function to generate a random dictionary
def generate_random_dict(num_of_keys):
    """Generates a random dictionary with a given number of keys (letters) and values (0-100)."""
    random_dict = {}
    while len(random_dict) < num_of_keys:
        random_key = random.choice(string.ascii_lowercase)
        random_value = random.randint(0, 100)
        random_dict[random_key] = random_value
    return random_dict


# Function to generate a list of random dictionaries
def generate_list_of_dicts():
    """Generates a list of random dictionaries, with a random count of dicts (between 2 and 10)."""
    num_of_dicts = random.randint(2, 10)
    return [generate_random_dict(random.randint(1, 6)) for _ in range(num_of_dicts)]


# Function to merge multiple dictionaries according to the rules
def merge_dicts(list_of_dicts):
    """Merges a list of dictionaries by keeping the max value for each key and renaming keys as needed."""
    common_dict = {}

    for idx, d in enumerate(list_of_dicts, 1):  # Enumerate starting at 1 for dict number
        for key, value in d.items():
            if key in common_dict:
                if value > common_dict[key][1]:  # Keep the max value and update key
                    common_dict[key] = (f"{key}_{idx}", value)
            else:
                common_dict[key] = (key, value)  # Add new key-value pair

    # Convert back to the simplified dictionary format {new_key: value}
    return {new_key: value for new_key, (_, value) in common_dict.items()}


# Function to execute the overall process
def main():
    """Main function to generate and merge random dictionaries."""
    # Step 1: Generate a list of random dictionaries
    list_of_dicts = generate_list_of_dicts()
    print("Generated list of dicts:", list_of_dicts)

    # Step 2: Merge the list of dictionaries
    final_dict = merge_dicts(list_of_dicts)
    print("Final merged dict:", final_dict)


# Run the main function
if __name__ == "__main__":
    main()
