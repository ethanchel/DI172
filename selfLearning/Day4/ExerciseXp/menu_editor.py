from menu_item import MenuItem
from menu_manager import MenuManager


def show_user_menu():
    """Display the program menu and handle user input."""
    while True:
        print("\n===== Restaurant Menu Manager =====")
        print("(V) View an Item")
        print("(A) Add an Item")
        print("(D) Delete an Item")
        print("(U) Update an Item")
        print("(S) Show the Menu")
        print("(Q) Quit")
        print("===================================")

        choice = input("Enter your choice: ").strip().upper()

        if choice == "V":
            view_item()
        elif choice == "A":
            add_item_to_menu()
        elif choice == "D":
            remove_item_from_menu()
        elif choice == "U":
            update_item_from_menu()
        elif choice == "S":
            show_restaurant_menu()
        elif choice == "Q":
            print("\n--- Final Restaurant Menu ---")
            show_restaurant_menu()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def view_item():
    """View a specific item by name."""
    name = input("Enter the item name to view: ").strip()
    item = MenuManager.get_by_name(name)
    if item:
        print(f"Item: {item.name} - Price: {item.price}")
    else:
        print(f"Item '{name}' not found.")


def add_item_to_menu():
    """Add a new item to the menu."""
    name = input("Enter the item name: ").strip()
    try:
        price = int(input("Enter the item price: ").strip())
    except ValueError:
        print("Invalid price. Please enter a number.")
        return

    item = MenuItem(name, price)
    if item.save():
        print("Item was added successfully.")
    else:
        print("Error: Could not add the item.")


def remove_item_from_menu():
    """Remove an item from the menu."""
    name = input("Enter the name of the item to delete: ").strip()
    item = MenuItem(name, 0)
    if item.delete():
        print("Item was deleted successfully.")
    else:
        print("Error: Could not delete the item. Item may not exist.")


def update_item_from_menu():
    """Update an existing item in the menu."""
    old_name = input("Enter the current name of the item to update: ").strip()

    # Check if item exists
    existing_item = MenuManager.get_by_name(old_name)
    if not existing_item:
        print(f"Error: Item '{old_name}' not found.")
        return

    new_name = input("Enter the new name: ").strip()
    try:
        new_price = int(input("Enter the new price: ").strip())
    except ValueError:
        print("Invalid price. Please enter a number.")
        return

    item = MenuItem(old_name, existing_item.price)
    if item.update(new_name, new_price):
        print("Item was updated successfully.")
    else:
        print("Error: Could not update the item.")


def show_restaurant_menu():
    """Display all items in the restaurant menu."""
    items = MenuManager.all_items()
    if items:
        print("\n--- Restaurant Menu ---")
        for item in items:
            print(f"  {item.name}: ${item.price}")
        print("-----------------------")
    else:
        print("The menu is empty.")


if __name__ == "__main__":
    show_user_menu()
