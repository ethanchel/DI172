# #Exercise 1
# Create a set called my_fav_numbers and populate it with your favorite numbers.
# Add two new numbers to the set.
# Remove the last number you added to the set.
# Create another set called friend_fav_numbers and populate it with your friend’s favorite numbers.
# Concatenate my_fav_numbers and friend_fav_numbers to create a new set called our_fav_numbers.
# Note: Sets are unordered collections, so ensure no duplicate numbers are added.

# Creating a set of my favorite numbers
my_fav_numbers = {2, 8, 26, 4}

# Adding two new numbers to the set
my_fav_numbers.add(23)
my_fav_numbers.add(18)

# Removing the last number added to the set
my_fav_numbers.remove(18)

# Creating a set of friend's favorite numbers
friend_fav_numbers = {31, 72, 113, 223}
# Concatenating both sets to create a new set of our favorite numbers
our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)

#Exercise 2
# Given a tuple of integers, try to add more integers to the tuple.
# Hint: Tuples are immutable, meaning they cannot be changed after creation. Think about why you can’t add more integers to a tuple.
# Creating a tuple of integers
my_tuple = (1, 2, 3, 4, 5)
# Attempting to add more integers to the tuple will result in an error
# my_tuple.append(6)  # This will raise an AttributeError because tuples are immutable
# Tuples cannot be modified after creation, so we cannot add more integers to it.
# To add more integers, we would need to create a new tuple
new_tuple = my_tuple + (6, 7)

#Exercise 3
# You have a list: basket = ["Banana", "Apples", "Oranges", "Blueberries"]
# Remove "Banana" from the list.
# Remove "Blueberries" from the list.
# Add "Kiwi" to the end of the list.
# Add "Apples" to the beginning of the list.
# Count how many times "Apples" appear in the list.
# Empty the list.
# Print the final state of the list.

# Creating the initial list
basket = ["Banana", "Apples", "Oranges", "Blueberries"]
# Removing "Banana" from the list
basket.remove("Banana")
# Removing "Blueberries" from the list
basket.remove("Blueberries")
# Adding "Kiwi" to the end of the list
basket.append("Kiwi")
# Adding "Apples" to the beginning of the list
basket.insert(0, "Apples")
# Counting how many times "Apples" appear in the list
apples_count = basket.count("Apples")
# Emptying the list
basket.clear()
# Printing the final state of the list
print(basket)

#4
# Recap: What is a float? What’s the difference between a float and an integer?
# Create a list containing the following sequence of mixed types: floats and integers:
# 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.
# Avoid hard-coding each number manually.
# Think: Can you generate this sequence using a loop or another method?

# A float is a number that has a decimal point, while an integer is a whole number without a decimal point.
# Creating a list of mixed types: floats and integers
mixed_numbers = [float(i) if i % 1 != 0 else int(i) for i in [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]]
# Option 2
# generated_numbers = []
# for i in range(2, 6):
#     generated_numbers.append(float(i) - 0.5)
#     generated_numbers.append(i)
# The generated_numbers list will contain the same sequence as mixed_numbers

#Exercise 5
# Write a for loop to print all numbers from 1 to 20, inclusive.
# Write another for loop that prints every number from 1 to 20 where the index is even.
for i in range(1, 21):
    print(i)
for i in range(1, 21):
    if i % 2 == 0:
        print(i)
# Exercise 6
# Use an input to ask the user to enter their name.
# Using a while True loop, check if the user gave a proper name (not digits and at least 3 letters long)
# hint: check for the method isdigit()
# if the input is incorrect, keep asking for the correct input until it is correct
# if the input is correct print “thank you” and break the loop

user_name = input("Please enter your name: ")
while True:
    if user_name.isdigit() or len(user_name) < 3:
        user_name = input("give the correct name: ")
    else:
        print("Thank you")
        break

# Exercise 7
# Ask the user to input their favorite fruits (they can input several fruits, separated by spaces).
# Store these fruits in a list.
# Ask the user to input the name of any fruit.
# If the fruit is in their list of favorite fruits, print:
# "You chose one of your favorite fruits! Enjoy!"
# If not, print:
# "You chose a new fruit. I hope you enjoy it!"

favorite_fruits = input("Please enter your favorite fruits, separated by spaces: ").split()
fruit_choice = input("Please enter the name of any fruit: ")
if fruit_choice in favorite_fruits:
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")

# Exercise 8
# Write a loop that asks the user to enter pizza toppings one by one.
# Stop the loop when the user types 'quit'.
# For each topping entered, print:
# "Adding [topping] to your pizza."
# After exiting the loop, print all the toppings and the total cost of the pizza.
# The base price is $10, and each topping adds $2.50.
toppings = []
while True:
    topping = input("Enter a pizza topping (or type 'quit' to finish): ")
    if topping.lower() == 'quit':
        break
    toppings.append(topping)
    print(f"Adding {topping} to your pizza.")

# After exiting the loop, print all the toppings and the total cost of the pizza.
print("Toppings added to your pizza:", toppings)
total_cost = 10 + len(toppings) * 2.5
print(f"Total cost of the pizza: ${total_cost:.2f}")

# Exercise 9
# Ask for the age of each person in a family who wants to buy a movie ticket.
# Calculate the total cost based on the following rules:
# Free for people under 3.
# $10 for people aged 3 to 12.
# $15 for anyone over 12.
# Print the total ticket cost.

total_cost = 0
while True:
    age = input("Enter the age of a family member (or type 'done' to finish): ")
    if age.lower() == 'done':
        break
    if not age.isdigit():
        print("Please enter a valid age.")
        continue
    age = int(age)
    if age < 3:
        cost = 0
    elif 3 <= age <= 12:
        cost = 10
    else:
        cost = 15
    total_cost += cost

print(f"Total ticket cost: ${total_cost}")

#Bonus Exercise
# Imagine a group of teenagers wants to see a restricted movie (only for ages 16–21).
# Write a program to:
# Ask for each person’s age.
# Remove anyone who isn’t allowed to watch.
# Print the final list of attendees.
attendees = []
while True:
    age = input("Enter the age of a teenager (or type 'done' to finish): ")
    if age.lower() == 'done':
        break
    if not age.isdigit():
        print("Please enter a valid age.")
        continue
    age = int(age)
    if 16 <= age <= 21:
        attendees.append(age)
print("Final list of attendees:", attendees)
