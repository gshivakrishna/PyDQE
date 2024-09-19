import random

# Create a list of 100 random numbers from 0 to 1000
random_numbers = [random.randint(0, 1000) for _ in range(100)]


# Function to sort a list from min to max using Bubble Sort algorithm
def bubble_sort(arr):
    n = len(arr)
    # Traverse through all elements in the list
    for i in range(n):
        # Last i elements are already in place, so we skip them
        for j in range(0, n - i - 1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# Sort the list using the bubble_sort function
bubble_sort(random_numbers)

# Initialize variables to calculate the sum and count of even and odd numbers
sum_even = 0
count_even = 0
sum_odd = 0
count_odd = 0

# Iterate over the sorted list to calculate the sum and count of even and odd numbers
for num in random_numbers:
    if num % 2 == 0:
        # If the number is even, add it to the even sum and increment the even count
        sum_even += num
        count_even += 1
    else:
        # If the number is odd, add it to the odd sum and increment the odd count
        sum_odd += num
        count_odd += 1

# Calculate the average of even numbers
average_even = sum_even / count_even if count_even != 0 else 0

# Calculate the average of odd numbers
average_odd = sum_odd / count_odd if count_odd != 0 else 0

# Print the average results for even and odd numbers to the console
print(f"Average of even numbers: {average_even}")
print(f"Average of odd numbers: {average_odd}")
