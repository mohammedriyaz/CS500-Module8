from datetime import datetime

class ItemToPurchase:
    ''''
    Class to represent an item to purchase and print the purchase cost of the purchased item quantity
    '''
    def __init__(self, item_name = "none", item_desc = "", item_price = 0, item_quantity = 0):
        self.item_name = item_name
        self.item_desc = item_desc
        self.item_price = item_price
        self.item_quantity = item_quantity
        
    def print_item_cost(self):
        items_cost = self.item_price * self.item_quantity
        print_centered_text(f'{self.item_name} {self.item_quantity} @ ${self.item_price:.2f} = ${items_cost:.2f}')
        return items_cost
    
    def print_item_description(self):
        print_centered_text(f"{self.item_name}: {self.item_desc}")

class ShoppingCart:
    '''
    Manager class to manage the shopping cart and purchase items
    '''
    duplicate_item_tracker = {} 
    cart_items = []
    def __init__(self, customer_name="none", current_date="January 1, 2020"):
        self.customer_name = customer_name
        self.current_date = current_date
    
    def get_user_input(self, for_update_item=False):
        """
        Get user input for adding or updating an item to the cart
        """
        cart_items_count = len(self.cart_items)
        # if not for_update_item:
        #     print_centered_text(f"Item {cart_items_count + 1}", line_spacing="top")
        item_name = get_inp_centered_cursur_position("Enter the item name: ", line_spacing=True, move_cursor_next_line=True)
        exisitng_item = self.fetch_item_by_name(item_name) if not for_update_item else None
        if exisitng_item != None:
            print_centered_text("Item already exists", line_spacing="top")
            exisitng_item.item_quantity += int(get_inp_centered_cursur_position("Enter the item quantity you want add:", line_spacing=True))
        else:
            if for_update_item:
                item_quantity = int(get_inp_centered_cursur_position("Enter the new quantity: ", line_spacing=True, move_cursor_next_line=True))
                self.modify_item(ItemToPurchase(item_name=item_name, item_quantity=item_quantity))
            else:
                item_desc = get_inp_centered_cursur_position("Enter the item description: ", line_spacing=True, move_cursor_next_line=True)
                item_price = float(get_inp_centered_cursur_position("Enter the item price: ", line_spacing=True, move_cursor_next_line=True))
                item_quantity = int(get_inp_centered_cursur_position("Enter the item quantity: ", line_spacing=True, move_cursor_next_line=True))
                self.add_item(item_name, item_desc, item_price, item_quantity)
                self.duplicate_item_tracker[item_name] = cart_items_count
        
    def fetch_item_by_name(self, item_name, return_position=False):
        position = self.duplicate_item_tracker[item_name] if item_name in self.duplicate_item_tracker else -1
        if position > -1:
            '''
            If the item is found in the cart, then check if the item is in the correct position
            If not, then update the position
            '''
            update_position = False
            if position < len(self.cart_items):
                item_in_position = self.cart_items[position]
                if item_in_position.item_name != item_name:
                    update_position = True
            else :
                update_position = True
            if update_position:
                for index, item in enumerate(self.cart_items):
                    if item.item_name == item_name:
                        position = index
                        break
        if return_position:
            return position
        if position > -1:
            return self.cart_items[position]
        return None
    
    def add_item(self, item_name, item_desc, item_price, item_quantity):
        item = ItemToPurchase(item_name=item_name, item_desc=item_desc, item_price=item_price, item_quantity=item_quantity)            
        self.cart_items.append(item)
        
    def remove_item(self, item_name):
        """
        Remove an item from the cart
        """
        cart_index = self.fetch_item_by_name(item_name, return_position=True)
        if cart_index > -1:
            del self.duplicate_item_tracker[item_name]
            self.cart_items.pop(cart_index)
            print_centered_text(f"{item_name} removed from the cart", line_spacing="top")
        else:
            print_centered_text("Item not found in the cart")
        
    def modify_item(self, item_to_update):
        """
        Modify an item in the cart
        """
        item = self.fetch_item_by_name(item_to_update.item_name)
        if item != None:
            is_updated = False
            if item_to_update.item_desc and item.item_desc != item_to_update.item_desc:
                item.item_desc = item_to_update.item_desc
                is_updated = True
            if item_to_update.item_quantity != 0 and item.item_quantity != item_to_update.item_quantity:
                item.item_quantity = item_to_update.item_quantity
                is_updated = True
            if item_to_update.item_price != 0 and item.item_price != item_to_update.item_price:
                item.item_price = item_to_update.item_price
                is_updated = True
            if is_updated:
                print_centered_text(f"{item.item_name} updated in the cart", line_spacing="top")
            else:
                print_centered_text(f"No changes found, so {item.item_name} is not updated in the cart", line_spacing="top")
        else:
            print_centered_text("Item not found in the cart")
        
        
    def get_num_items_in_cart(self):
        """
        Return the number of items in the cart
        """
        totalQunatity = 0
        for item in self.cart_items:
            totalQunatity += item.item_quantity
        return totalQunatity
    
    def get_cost_of_cart(self, print_item_cost=False):
        """
        Return the total cost of the cart
        """
        total_cart_cost = 0
        for item in self.cart_items:
            total_cart_cost += (item.item_price * item.item_quantity) if not print_item_cost else item.print_item_cost()
        return total_cart_cost
    
    def print_total(self):
        if (len(self.cart_items) == 0):
            print_centered_text("SHOPPING CART IS EMPTY")
        else:
            print_centered_text("OUTPUT SHOPPING CART", line_spacing="both", underline=True)
            print_centered_text(f"{self.customer_name}'s Shopping Cart - {self.current_date}", underline=True)
            print_centered_text(f"Number of Items: {self.get_num_items_in_cart()}", line_spacing="bottom")
            total_cost = self.get_cost_of_cart(True)
            print_centered_text(f"Total: ${total_cost}", line_spacing="top")
        
    
    def print_descriptions(self):
        print_centered_text("OUTPUT ITEMS' DESCRIPTIONS", line_spacing="both", underline=True)
        print_centered_text(f"{self.customer_name}'s Shopping Cart - {self.current_date}", underline=True)
        print_centered_text("Item Descriptions", line_spacing="both", underline=True)
        for item in self.cart_items:
            item.print_item_description()

def underline_text(text, underline_char="-"):
    """
    Underline the text with the given character
    """
    # \x1B[ is the escape sequence initiator
    # 4m is the underline attribute
    # 0m is the reset attribute to reset the formatting to the default
    return f"\x1B[4m{text}\x1B[0m"

def bold_text(text):
    """
    Bold the text
    """
    # \x1B[1m is the bold attribute
    # 0m is the reset attribute to reset the formatting to the default
    return f"\x1B[1m{text}\x1B[0m"

def get_inp_centered_cursur_position(input_label, right_justification=75, line_spacing=False, move_cursor_next_line=False):
    """
    Get the input from the user at the center of the screen
    """
    lbl_len = len(input_label)
    if line_spacing:
        print()
    # here right_justification is the half the value of our centering value
    if move_cursor_next_line:
        print(f"{input_label.rjust(right_justification + (lbl_len //2 ) )}")
    return  input(f"{''.rjust(right_justification - (lbl_len //4 ) )}") if move_cursor_next_line else input(f"{input_label.rjust(right_justification + (lbl_len //2 ) )}")

def print_centered_text(text, line_width=150, line_spacing=False, underline=False):
    """
    Print the text at the center of the screen
    """
    if line_spacing == "top" or line_spacing == "both":
        print()
    text = underline_text(text) if underline else text
    print(text.center(line_width))
    if line_spacing == "bottom" or line_spacing == "both":
        print()
        
def get_menu_option():
    print_centered_text("MENU", line_spacing="both", underline=True)
    print_centered_text(bold_text("a") + " - Add item to cart")
    print_centered_text(bold_text("r") + " - Remove item from cart")
    print_centered_text(bold_text("c") + " - Change item quantity")
    print_centered_text(bold_text("i") + " - Output items' descriptions")
    print_centered_text(bold_text("o") + " - Output shopping cart")
    print_centered_text(bold_text("q") + " - Quit", line_spacing="bottom")
    input_label = "Choose an option: "
    lbl_len = len(input_label)
    return get_inp_centered_cursur_position(input_label, right_justification=75, move_cursor_next_line=True)

def print_menu(cart):    
    option = get_menu_option()
    while option != "q":
        if option == "a":
            print_centered_text("ADD ITEM TO CART", line_spacing="both", underline=True)
            cart.get_user_input()
        elif option == "r":
            print_centered_text("REMOVE ITEM FROM CART", line_spacing="both", underline=True)
            cart.remove_item(get_inp_centered_cursur_position("Enter name of item to remove: ", line_spacing=True, move_cursor_next_line=True))
        elif option == "c":
            print_centered_text("CHANGE ITEM QUANTITY", line_spacing="both", underline=True)
            cart.get_user_input(for_update_item=True)
        elif option == "i":
            cart.print_descriptions()
        elif option == "o":
            cart.print_total()
        option = get_menu_option()
    print_centered_text("Come back sooner! Goodbye for now!", line_spacing="both")
    
# main
def main():
    customer_name = get_inp_centered_cursur_position("Enter your name: ", line_spacing=True, move_cursor_next_line=True)
    current_date = get_inp_centered_cursur_position("Enter today's date: (press n to auto generate)", line_spacing=True, move_cursor_next_line=True)
    current_date = datetime.now().strftime("%B %d, %Y") if current_date == "n" else current_date
    print_centered_text("Customer name: " + customer_name, line_spacing="top")
    print_centered_text("Today's date: " + current_date, line_spacing="top")
    cart = ShoppingCart(customer_name, current_date)
    print_menu(cart)
    # cart.purchase_items()
    
if __name__ == "__main__":
    main()
