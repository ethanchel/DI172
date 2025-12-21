# # #Exercie 1
# Instructions
# You are given two lists. Convert them into a dictionary where the first list contains the keys and the second list contains the corresponding values.
# Lists:

# keys = ['Ten', 'Twenty', 'Thirty']
# values = [10, 20, 30]


# Expected Output:

# {'Ten': 10, 'Twenty': 20, 'Thirty': 30}
keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]
result = dict(zip(keys, values))

#Exercice 2
# Instructions
# Write a program that calculates the total cost of movie tickets for a family based on their ages.

# Family members’ ages are stored in a dictionary.
# The ticket pricing rules are as follows:
# Under 3 years old: Free
# 3 to 12 years old: $10
# Over 12 years old: $15


# Family Data:

# family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}


# Loop through the family dictionary to calculate the total cost.
# Print the ticket price for each family member.
# Print the total cost at the end.


# Bonus:

# Allow the user to input family members’ names and ages, then calculate the total ticket cost.
family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}
total_cost = 0
for name, age in family.items():
    if age < 3:
        price = 0
    elif 3 <= age <= 12:
        price = 10
    else:
        price = 15
    total_cost += price
    print(f"{name.capitalize()} (age {age}): ${price}")
print(f"Total cost for the family: ${total_cost}")
# Bonus part
family = {}
num_members = int(input("Enter the number of family members: "))
for _ in range(num_members):
    name = input("Enter the family member's name: ")
    age = int(input(f"Enter {name}'s age: "))
    family[name] = age


total_cost = 0
for name, age in family.items():
    if age < 3:
        price = 0
    elif 3 <= age <= 12:
        price = 10
    else:
        price = 15
    total_cost += price
    print(f"{name.capitalize()} (age {age}): ${price}")
print(f"Total cost for the family: ${total_cost}")

##Exercice 3
# Instructions
# Create and manipulate a dictionary that contains information about the Zara brand.

# Brand Information:

# name: Zara
# creation_date: 1975
# creator_name: Amancio Ortega Gaona
# type_of_clothes: men, women, children, home
# international_competitors: Gap, H&M, Benetton
# number_stores: 7000
# major_color:
#     France: blue,
#     Spain: red,
#     US: pink, green


# Create a dictionary called brand with the provided data.
# Modify and access the dictionary as follows:
# Change the value of number_stores to 2.
# Print a sentence describing Zara’s clients using the type_of_clothes key.
# Add a new key country_creation with the value Spain.
# Check if international_competitors exists and, if so, add “Desigual” to the list.
# Delete the creation_date key.
# Print the last item in international_competitors.
# Print the major colors in the US.
# Print the number of keys in the dictionary.
# Print all keys of the dictionary.
brand = {
    "name": "Zara",
    "creation_date": 1975,
    "creator_name": "Amancio Ortega Gaona",
    "type_of_clothes": ["men", "women", "children", "home"],
    "international_competitors": ["Gap", "H&M", "Benetton"],
    "number_stores": 7000,
    "major_color": {
        "France": ["blue"],
        "Spain": ["red"],
        "US": ["pink", "green"]
    }
}
brand["number_stores"] = 2
print(f"Zara's clients are: {', '.join(brand['type_of_clothes'])}.")
brand["country_creation"] = "Spain"
if "international_competitors" in brand:
    brand["international_competitors"].append("Desigual")
del brand["creation_date"]
print(f"Last international competitor: {brand['international_competitors'][-1]}")
print(f"Major colors in the US: {', '.join(brand['major_color']['US'])}")
print(f"Number of keys in the dictionary: {len(brand)}")
print("All keys in the dictionary:")
for key in brand.keys():
    print(key)

##Exercice 4
# Instructions
# You are given a list of Disney characters. Create three dictionaries based on different patterns as shown below:



# Character List:

# users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]


# Expected Results:

# 1. Create a dictionary that maps characters to their indices:

# {"Mickey": 0, "Minnie": 1, "Donald": 2, "Ariel": 3, "Pluto": 4}


# 2. Create a dictionary that maps indices to characters:

# {0: "Mickey", 1: "Minnie", 2: "Donald", 3: "Ariel", 4: "Pluto"}


# 3. Create a dictionary where characters are sorted alphabetically and mapped to their indices:

# {"Ariel": 0, "Donald": 1, "Mickey": 2, "Minnie": 3, "Pluto": 4}

users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]
# 1. Characters to indices
char_to_index = {char: index for index, char in enumerate(users)}
print(char_to_index)
# 2. Indices to characters
index_to_char = {index: char for index, char in enumerate(users)}
print(index_to_char)
# 3. Sorted characters to indices
sorted_char_to_index = {char: index for index, char in enumerate(sorted(users))}
print(sorted_char_to_index)
