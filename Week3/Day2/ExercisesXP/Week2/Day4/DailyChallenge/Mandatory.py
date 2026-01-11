#Challenge 1: Sorting
# Write a Python program that takes a single string of words as input, where the words are separated by commas (e.g., ‘apple,banana,cherry’). The program should output these words sorted in alphabetical order, with the sorted words also separated by commas.
# Step 1: Get Input

# Use the input() function to get a string of words from the user.
# The words will be separated by commas.
input_string = input("Enter words separated by commas: ")
#Step 2: Split the String

# Use the split() method to divide the input string into a list of words.
words_list = input_string.split(',')
#Step 3: Sort the List
# Use the sort() method to sort the list of words in alphabetical order.
words_list.sort()
#Step 4: Join the Sorted List
# Use the join() method to combine the sorted list of words back into a single string, with words separated by commas.
sorted_string = ','.join(words_list)
#Step 5: Output the Result
# Print the sorted string.
print("Sorted words:", sorted_string)

#Challenge 2: Longest Word
#Write a function that takes a sentence as input and returns the longest word in the sentence. If there are multiple longest words, return the first one encountered. Characters like apostrophes, commas, and periods should be considered part of the word.
# Step 1: Define the Function

# Define a function that takes a string (the sentence) as a parameter.
def longest_word(sentence):
    # Step 2: Split the Sentence into Words
    # Use the split() method to divide the sentence into a list of words.
    words = sentence.split()
    # Step 3: Initialize Variables
    # Create variables to keep track of the longest word and its length.
    longest_word = ""
    max_length = 0

    # Step 4: Iterate Through Words
    # Loop through each word in the list.
    for word in words:
        # Check if the current word's length is greater than max_length.
        if len(word) > max_length:
            # If it is, update longest_word and max_length.
            longest_word = word
            max_length = len(word)
    # Step 5: Compare Word Lengths
    # After checking all words, return the longest word found.
    return longest_word
# Test cases
print(longest_word("Margaret's toy is a pretty doll."))
print(longest_word("A thing of beauty is a joy forever."))
print(longest_word("Forgetfulness is by all means powerless!"))
