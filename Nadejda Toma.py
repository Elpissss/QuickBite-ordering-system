import json
from datetime import datetime

# Main function to run the program
def main():
    print("Welcome to QuickBite!")
    menu = load_menu()  # Load the menu from a JSON file
    while True:
        # Display the main menu options
        print("\nMain Menu:")
        print("1. Place an order")
        print("2. Edit the menu")
        print("3. Exit")
        choice = input("Please choose an option: ")
        
        # Handle user choice
        if choice == '1':
            order = take_order(menu)  # Take the customer's order
            display_receipt(order)    # Display the receipt
        elif choice == '2':
            edit_menu(menu)  # Enter menu editing mode
        elif choice == '3':
            print("Thank you for visiting QuickBite. Goodbye!")
            break  # Exit the program
        else:
            print("Invalid option, please try again.")

# Load menu from a JSON file
def load_menu():
    try:
        # Try to read the menu data from 'menu.json'
        with open('menu.json', 'r') as file:
            menu = json.load(file)
        # Validate the structure of the menu data
        if isinstance(menu, list) and all(isinstance(item, dict) and 'name' in item and 'price' in item for item in menu):
            return menu
        else:
            # Raise an error if the data format is incorrect
            raise ValueError("Menu JSON is not in the expected format")
    except Exception as e:
        # If there's an error, print a message and load a default menu
        print(f"Failed to load menu: {e}. A default menu will be used instead.")
        return [{"name": "Default Pizza", "price": 10.00}]

# Take customer orders
def take_order(menu):
    order = {}  # Initialize an empty dictionary for the order
    print("\n--- Place Your Order ---")
    display_menu(menu)  # Display the menu to the customer
    while True:
        # Prompt the user to enter a menu item number or 'done' to finish
        choice = input("Enter the menu item number to order (or 'done' to finish): ")
        if choice.lower() == 'done':
            break
        # Validate user input
        if choice.isdigit() and 1 <= int(choice) <= len(menu):
            while True:
                try:
                    quantity = int(input("Enter the quantity: "))
                    if quantity > 0:
                        item = menu[int(choice) - 1]
                        # Update the order dictionary with the selected item
                        if item['name'] in order:
                            order[item['name']] += quantity
                        else:
                            order[item['name']] = quantity
                        print(f"Added {quantity} x {item['name']} to your order.")
                        break  # Exit the quantity input loop
                    else:
                        print("Please choose at least 1 item. Thank you.")
                except ValueError:
                    # Handle invalid quantity input
                    print("Invalid input. Please enter a valid integer.")
        else:
            # Handle invalid menu item selection
            print("Invalid choice. Please try again.")
    return order

# Display the receipt and process payment
def display_receipt(order, final=False):
    if not order:
        # If no items were ordered, exit the function
        print("No items ordered. Exiting.")
        return
    current_time = datetime.now()
    date_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n--- Your Receipt ---")
    print(f"Date/Time: {date_time}\n")
    print('=' * 45)
    # Print receipt header
    header = "{:<10} {:>10} {:>10} {:>10}".format("Item", "Quantity", "Price", "Total")
    print(header)
    print('=' * 45)

    total = 0
    # Calculate total cost and print each item in the order
    for item, quantity in order.items():
        price = next((x['price'] for x in load_menu() if x['name'] == item), 0)
        item_total = quantity * price
        row = "{:<10} {:>10} {:>10.2f} {:>10.2f}".format(item, quantity, price, item_total)
        print(row)
        total += item_total

    print('=' * 45)
    print(f"Total to pay: £{total:.2f}")
    print('=' * 45)
    if final:
        print("Thank you for your payment.")
    process_payment(total)

# Process payment
def process_payment(total):
    print("Please proceed to payment.")
    while True:
        try:
            paid = float(input("Enter the amount paid (£): "))
            if paid >= total:
                # If payment is sufficient, calculate and display change
                print(f"Thank you! Your change: £{paid - total:.2f}")
                break
            else:
                # Handle insufficient payment
                print("Insufficient amount paid. Please try again or type 'cancel' to return to the main menu.")
                continue_input = input("Would you like to try again? (yes/no): ")
                if continue_input.lower() != 'yes':
                    print("Transaction cancelled. Returning to the main menu.")
                    break
        except ValueError:
            # Handle invalid input for payment
            print("Invalid input. Please enter a valid amount.")

# Display the menu to the customer
def display_menu(menu):
    print("\n--- Today's Menu ---")
    for index, item in enumerate(menu):
        print(f"{index + 1}. {item['name']} - £{item['price']:.2f}")

# Function to edit the menu
def edit_menu(menu):
    print("\n--- Menu Editor ---")
    # Display options for editing the menu
    print("1. Add a new item")
    print("2. Remove an item")
    print("3. Update an item's price")
    print("4. Exit")
    choice = input("Select an option: ")
    # Add a new item to the menu
    if choice == '1':
        name = input("Enter the name of the new item: ")
        price = float(input("Enter the price: "))
        # Append the new item as a dictionary to the menu list
        menu.append({"name": name, "price": price})
        save_menu(menu) # Save the updated menu
    elif choice == '2':
        remove_item(menu) # Remove an existing item from the menu
    # Update the price of an existing item
    elif choice == '3':
        for idx, item in enumerate(menu):
            print(f"{idx + 1}. {item['name']} - £{item['price']:.2f}")
        index = int(input("Select the number of the item to update: ")) - 1
        if 0 <= index < len(menu):
            new_price = float(input("Enter the new price: "))
            menu[index]['price'] = new_price
            save_menu(menu)
        else:
            print("Invalid selection.")

# Remove an item from the menu
def remove_item(menu):
    print("Select an item to remove:")
    for idx, item in enumerate(menu):
        print(f"{idx + 1}. {item['name']} - £{item['price']:.2f}")
    try:
        # Ask the user to enter the item number to remove
        index = int(input("Enter the number of the item to remove: ")) - 1
        # Check if the entered number is within the valid range
        if 0 <= index < len(menu):
            menu.pop(index)
            save_menu(menu)
            print("Item removed successfully.")
        else:
            print("Invalid selection. Please try again.")
    except ValueError:
        print("Please enter a valid integer for the item number.")

# Save the updated menu back to the JSON file
def save_menu(menu):
    try:
        with open('menu.json', 'w') as file:
            json.dump(menu, file, indent=4)
        print("Menu has been successfully updated.")
    except Exception as e:
        print(f"Failed to save menu: {e}")

if __name__ == "__main__":
    main()
