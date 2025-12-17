# # Challenge 1 
# 1. Ask the user for two inputs:
# A number (integer).
# A length (integer).
# 2. Create a program that generates a list of multiples of the given number.
# 3. The list should stop when it reaches the length specified by the user.

number = int(input("Enter a number (integer): "))
length = int(input("Enter the length of the list (integer): "))
multiples = [number * i for i in range(1, length + 1)]

# Challenge 2
# 1. Ask the user for a string.
# 2. Write a program that processes the string to remove consecutive duplicate letters.

# The new string should only contain unique consecutive letters.
# For example, “ppoeemm” should become “poem” (removes consecutive duplicates like ‘pp’, ‘ee’, and ‘mm’).
# 3. The program should print the modified string.
# The final string will not include any consecutive duplicates, but non-consecutive duplicates are allowed.
# Example: In "recursive", the two ‘r’s and two ‘e’s are allowed because they are not consecutive
user_string = input("Enter a string;")
if user_string:
    quoted_string = [user_string[0]]
    for char in user_string[1:]:
        if char != quoted_string[-1]:
            quoted_string.append(char)  
    modified_string = "".join(quoted_string)