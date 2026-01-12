# Instructions:

# Create a Text class to analyze text data, either from a string or a file. Then, create a TextModification class to perform text cleaning.



# Part I: Analyzing a Simple String

# Step 1: Create the Text Class

# Create a class called Text.
# The __init__ method should take a string as an argument and store it in an attribute (e.g: self.text).


# Step 2: Implement word_frequency Method

# Create a method called word_frequency(word).
# Split the text attribute into a list of words.
# Count the occurrences of the given word in the list.
# Return the count.
# If the word is not found, return None or a meaningful message.


# Step 3: Implement most_common_word Method

# Create a method called most_common_word().
# Split the text into a list of words.
# Use a dictionary to store word frequencies.
# Find the word with the highest frequency.
# Return the most common word.


# Step 4: Implement unique_words Method

# Create a method called unique_words().
# Split the text into a list of words.
# Use a set to store unique words.
# Return the unique words as a list.


# Part II: Analyzing Text from a File

# Step 5: Implement from_file Class Method

# Create a class method called from_file(file_path).
# Open the file at file_path in read mode.
# Read the file content.
# Create and return a Text instance with the file content as the text.


# Bonus: Text Modification

# Step 6: Create the TextModification Class

# Create a class called TextModification that inherits from Text.


# Step 7: Implement remove_punctuation Method

# Create a method called remove_punctuation().
# Use the string module to get a string of punctuation characters.
# Use a string method or regular expressions to remove punctuation from the text attribute.
# Return the modified text.


# Step 8: Implement remove_stop_words Method

# Create a method called remove_stop_words().
# Search online for a list of English stop words (common words like “a”, “the”, “is”).
# Split the text into a list of words.
# Filter out stop words from the list.
# Join the remaining words back into a string.
# Return the modified text.


# Step 9: Implement remove_special_characters Method

# Create a method called remove_special_characters().
# Use regular expressions to remove special characters from the text attribute.
# Return the modified text.

import string
import re
class Text:
    def __init__(self, text):
        self.text = text

    def word_frequency(self, word):
        words = self.text.split()
        count = words.count(word)
        return count if count > 0 else None

    def most_common_word(self):
        words = self.text.split()
        frequency = {}
        for word in words:
            frequency[word] = frequency.get(word, 0) + 1
        most_common = max(frequency, key=frequency.get)
        return most_common

    def unique_words(self):
        words = self.text.split()
        unique = set(words)
        return list(unique)

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return cls(content)
class TextModification(Text):
    def remove_punctuation(self):
        translator = str.maketrans('', '', string.punctuation)
        modified_text = self.text.translate(translator)
        return modified_text
    def remove_stop_words(self):
        stop_words = set([
            "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
            "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
            "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
            "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
            "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
            "himself", "his", "how", "how's",  "i",  "i'd",  "i'll",  "i'm",  "i've",
            "if",  "in",  "into",  "is",  "isn't",
            "it",  "it's",
            "its",
            "itself",
            # ... (add more stop words as needed)
        ])
        words = self.text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        modified_text = ' '.join(filtered_words)
        return modified_text
    def remove_special_characters(self):
        modified_text = re.sub(r'[^A-Za-z0-9\s]', '', self.text)
        return modified_text
# Example usage:
if __name__ == "__main__":
    sample_text = "Hello, world! This is a test. Hello again."
    text_instance = Text(sample_text)
    print("Word Frequency of 'Hello':", text_instance.word_frequency("Hello"))
    print("Most Common Word:", text_instance.most_common_word())
    print("Unique Words:", text_instance.unique_words())

    text_mod_instance = TextModification(sample_text)
    print("Text without Punctuation:", text_mod_instance.remove_punctuation())
    print("Text without Stop Words:", text_mod_instance.remove_stop_words())
    print("Text without Special Characters:", text_mod_instance.remove_special_characters())
