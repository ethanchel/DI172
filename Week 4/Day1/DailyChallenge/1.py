# Part 1 : Quizz :
# Answer the following questions

# What is a class?
# What is an instance?
# What is encapsulation?
# What is abstraction?
# What is inheritance?
# What is multiple inheritance?
# What is polymorphism?
# What is method resolution order or MRO?

# A class is a blueprint for creating objects. It defines a set of attributes and methods that the created objects (instances) will have.
# An instance is a specific object created from a class. It contains the data and behavior defined by the class.
# Encapsulation is the concept of bundling data (attributes) and methods (functions) that operate on that data into a single unit, typically a class. It restricts direct access to some of an object's components, which can prevent the accidental modification of data.
# Abstraction is the concept of hiding the complex implementation details and showing only the essential features of an object. It helps in reducing complexity and increasing efficiency.
# Inheritance is a mechanism in object-oriented programming that allows a new class (subclass or derived class) to inherit attributes and methods from an existing class (superclass or base class). This promotes code reusability.
# Multiple inheritance is a feature of some object-oriented programming languages where a class can inherit attributes and methods from more than one parent class. This allows for greater flexibility and code reuse.
# Polymorphism is the ability of different classes to be treated as instances of the same class through a common interface. It allows methods to do different things based on the object it is acting upon, even if
# they share the same name.
# Method Resolution Order (MRO) is the order in which Python looks for a method in a hierarchy of classes when a method is called on an instance. In the case of multiple inheritance, MRO determines the order in which base classes are searched when executing a method. Python uses the C3 linearization algorithm to determine the MRO.

# Part 2: Create a deck of cards class.
# The Deck of cards class should NOT inherit from a Card class.

# The requirements are as follows:

# The Card class should have a suit (Hearts, Diamonds, Clubs, Spades) and a value (A,2,3,4,5,6,7,8,9,10,J,Q,K)
# The Deck class :
# should have a shuffle method which makes sure the deck of cards has all 52 cards and then rearranges them randomly.
# should have a method called deal which deals a single card from the deck. After a card is dealt, it should be removed from the deck.
import random
class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"
class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.SUITS for value in Card.VALUES]

    def shuffle(self):
        if len(self.cards) != 52:
            raise ValueError("Cannot shuffle a deck that does not have 52 cards.")
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) == 0:
            raise ValueError("No cards left in the deck to deal.")
        return self.cards.pop()
# Example usage:
deck = Deck()
deck.shuffle()
card = deck.deal()
print(card)  # Example output: "7 of Diamonds"
print(len(deck.cards))  # Should print 51 after dealing one card
