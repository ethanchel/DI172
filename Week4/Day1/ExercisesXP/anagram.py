# Now create another Python file, called anagrams.py. This will contain all the UI (user interface) functionality of your program, and will rely on AnagramChecker for the anagram-related logic.

# It should do the following:
# Show a menu, offering the user to input a word or exit. Keep showing the menu until the user chooses to exit.

# If the user chooses to input a word, it must be accepted from the user’s keyboard input, and then be validated:
# Only a single word is allowed. If the user typed more than one word, show an error message. (Hint: how do we know how many words were typed?)
# Only alphabetic characters are allowed. No numbers or special characters.
# Whitespace should be removed from the start and end of the user’s input.

# Once your code has decided that the user’s input is valid, it should find out the following:
# All possible anagrams to the user’s word.
# Create an AnagramChecker instance and apply it to the steps created above.
# Display the information about the word in a user-friendly, nicely-formatted message such as:


# YOUR WORD :”MEAT”
# this is a valid English word.
# Anagrams for your word: mate, tame, team.
from anagram_checker import AnagramChecker
def main():
    checker = AnagramChecker('sowpods.txt')

    while True:
        print("\nMenu:")
        print("1. Input a word")
        print("2. Exit")
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == '2':
            print("Exiting the program.")
            break
        elif choice == '1':
            user_input = input("Please enter a word: ").strip()

            # Validate input
            if len(user_input.split()) != 1:
                print("Error: Please enter only a single word.")
                continue
            if not user_input.isalpha():
                print("Error: Only alphabetic characters are allowed.")
                continue

            word = user_input.lower()
            is_valid = checker.is_valid_word(word)
            anagrams = checker.get_anagrams(word)

            # Display results
            print(f"\nYOUR WORD: \"{user_input.upper()}\"")
            if is_valid:
                print("This is a valid English word.")
            else:
                print("This is not a valid English word.")

            if anagrams:
                print("Anagrams for your word: " + ", ".join(anagrams) + ".")
            else:
                print("No anagrams found for your word.")
        else:
            print("Invalid option. Please choose 1 or 2.")
if __name__ == "__main__":
    main()
