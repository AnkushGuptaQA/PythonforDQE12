import string
import random

dicts_list = []  # Initialize an empty list to store the dicts
number_of_dicts = random.randint(2, 10)  # Randomly pick the length of the list (between 2 and 10)

for i in range(number_of_dicts):
    # Randomly choose the number of keys in the dict (between 1 and 10)
    number_of_keys = random.randint(1, 10)
    # Randomly sample letters to serve as keys
    keys = random.sample(string.ascii_lowercase, number_of_keys)
    # Create a dict where values are random numbers between 0 and 100
    random_dict = {key: random.randint(0, 100) for key in keys}
    dicts_list.append(random_dict)  # Append the generated dict to the list

print(dicts_list)  # Print the generated list of dicts

common_dict = {}  # Initialize an empty dict to store the result

for dict_index, single_dict in enumerate(dicts_list):
    for key, value in single_dict.items():
        if key in common_dict:
            # If the key already exists in common_dict, compare values
            current_value, max_index = common_dict[key]
            if value > current_value:
                # Update with the larger value and the index of the dict with max value
                common_dict[key] = (value, dict_index + 1)
        else:
            # If the key does not exist in common_dict, add it
            common_dict[key] = (value, dict_index + 1)

# Transform the `common_dict` to rename keys based on dict index
final_dict = {}  # Initialize an empty dict for the final result

for key, (value, max_index) in common_dict.items():
    if max_index == 1:
        # If the key only existed in one dict, keep it as is
        final_key = key
    else:
        # Rename the key appending the dict number with the max value
        final_key = f"{key}_{max_index}"
    final_dict[final_key] = value  # Add the final key-value pair to the result

print(final_dict)  # Print the final merged dictionary
