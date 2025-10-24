import string
import random
from typing import List, Dict, Tuple
import re

#Refactor of module 2 using function approach

def generate_dicts_list() -> List[Dict[str, int]]:
    """Generates a list of random dictionaries"""
    dicts_list = []
    number_of_dicts = random.randint(2, 10)

    for i in range(number_of_dicts):
        number_of_keys = random.randint(1, 10)
        keys = random.sample(string.ascii_lowercase, number_of_keys)
        random_dict = {key: random.randint(0, 100) for key in keys}
        dicts_list.append(dict(sorted(random_dict.items())))

    return dicts_list

def get_max_value_indices(dicts_list: List[Dict[str, int]]) -> Dict[str, Tuple[int, int]]:
    """Returns a dictionary mapping each key to max_value, dict_index_with_max_value."""
    common_dict = {}
    for dict_index, single_dict in enumerate(dicts_list):
        for key, value in single_dict.items():
            if key in common_dict:
                current_value, max_index = common_dict[key]
                if value > current_value:
                    common_dict[key] = (value, dict_index + 1)
            else:
                common_dict[key] = (value, dict_index + 1)
    return common_dict

def merge_and_sort_dicts(common_dict: Dict[str, Tuple[int, int]]) -> Dict[str, int]:
    """Merges the list of dictionaries, renames keys, and returns a sorted dictionary."""
    final_dict = {}
    for key, (value, max_index) in common_dict.items():
        if max_index == 1:
            final_key = key
        else:
            final_key = f"{key}_{max_index}"
        final_dict[final_key] = value
    final_dict = dict(sorted(final_dict.items()))
    return final_dict

print ("Module 2 Output::")
dicts_list = generate_dicts_list()
print("Generated list of dicts:", dicts_list)

common_dict = get_max_value_indices(dicts_list)

final_dict = merge_and_sort_dicts(common_dict)
print("Final dict:", final_dict)

#Refactor of module 3 using function approach

def normalize_sentences(text):
    """Normalize sentences: lowercase all, capitalize first letter of each sentence."""
    sentences = re.split(r'(?<=\.)\s+', text.strip())
    normalized = [s.lower().capitalize() for s in sentences]
    return ' '.join(normalized)


def fix_iz_misspelling(text):
    """Replace ' iz ' with ' is ' only when it's a separate word."""
    return re.sub(r'\b iz\b', ' is', text)


def extract_last_words(text):
    """Extract last word from each sentence and form a new sentence."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    last_words = [s.rstrip('.!?').split()[-1] for s in sentences if s]
    return ' '.join(last_words) + '.'


def count_whitespaces(text):
    """Count all whitespace characters in the text."""
    return text.count(" ")+text.count("\n")+text.count("\t")


text = """  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

normalized = normalize_sentences(text)
fixed_text = fix_iz_misspelling(normalized)
new_sentence = extract_last_words(fixed_text)
final_text = fixed_text + ' ' + new_sentence

print ("\nModule 3 Output::")
print(final_text)
print("Number of Whitespaces in provided text is", count_whitespaces(text))