'''''
Gidon Tobin
320518020
01
ex7
'''''


import sys


''''
Function Name: get_store
Input: void
Output: dict
Function Operation: The function gets the categories, items and prices from the 
                    text that is given, and adds them to a dict type, that is 
                    sent back to the main function.
'''''
def get_store():
    store = open(sys.argv[ONE], "r")
    categories = dict()
    # the function will reed each line, and add the items to the catagory they are in in the dict
    for count in range(sum(ONE for line in open(sys.argv[ONE]))):
        line = store.readline()
        # incase a blank line
        if line == '\n':
            continue
        name_of_category, next_input = line.split(COLON)
        name_of_category = name_of_category.lstrip()
        # getting items and prices
        next_input = next_input.split(SEMICOLON)
        next_input.remove('\n')
        # this dict is the value in the dict categories
        products = dict()
        # adding the item and price
        for i in range(len(next_input)):
            product_name, price = next_input[i].split(COMA)
            product_name = product_name.lstrip()
            price = price.lstrip()
            products[product_name] = price
        categories[name_of_category] = products
    return categories


''''
Function Name: print_menu
Input: void
Output: void
Function Operation: The function prints the main menu of the program
'''''
def print_menu():
    print('Please select an operation:')
    print('\t0. Exit.')
    print('\t1. Query by category.')
    print('\t2. Query by item.')
    print('\t3. Purchase an item.')
    print('\t4. Admin panel.')


''''
Function Name: query_two_product_categories
Input: store (a dict type), caching (a dict type)
Output: void
Function Operation: The function gets an input from the user, and works accordingly. 
                    If the input of the user is valid, the function will print what the
                    query that the user wanted. If the input of the user is not valid, 
                    the function will print an error. If the function receives an input that 
                    a query that it has already been printed is asked for - the function
                    will print the saved query, with the word "Cached:" before.
                    Every query that is printed will be saved to caching, so that it can be reused
                    if necessary. There are three options of querys that can be printed: a union group
                    of two categories, a intersection, or the symmetric_difference of the two.
'''''
def query_two_product_categories(store, caching):
    the_query = input()
    # if query doesnt have enough comas
    if len(the_query.split(COMA)) < THREE:
        print('Error: not enough data.')
        return caching
    category_1, category_2, operator = the_query.split(COMA, TWO)
    category_1 = category_1.lstrip()
    category_2 = category_2.lstrip()
    operator = operator.lstrip()
    # the query is now a set with the three arguments
    the_query = {category_1, category_2, operator}
    the_query = frozenset(the_query)
    # if cached
    if the_query in set(caching[ONE].keys()):
        print('Cached: ', end="")
        print(caching[ONE][the_query])
        return
    if category_1 not in store.keys() or category_2 not in store.keys():
        print('Error: one of the categories does not exist.')
        return
    if operator == '|':
        query_two_product_list = list(set(store[category_1].keys()).union(set(store[category_2].keys())))
    elif operator == '&':
        query_two_product_list = list(set(store[category_1].keys()).intersection(set(store[category_2].keys())))
    elif operator == '^':
        query_two_product_list = list(set(store[category_1].keys()).symmetric_difference(set(store[category_2].keys())))
    # if operator not valid
    else:
        print('Error: unsupported query operation.')
        return
    query_two_product_list = sorted(query_two_product_list)
    print(query_two_product_list)
    # adding the printed str to caching[ONE][the_query] for future use
    caching[ONE][the_query] = query_two_product_list


''''
Function Name: query_by_item
Input: store (a dict type), caching (a dict type)
Output: void
Function Operation: The function gets an input from the user, and works accordingly. 
                    If the input of the user is valid, the function will print what the
                    query that the user wanted. If the input of the user is not valid, 
                    the function will print an error. If the function receives an input that 
                    a query that it has already been printed is asked for - the function
                    will print the saved query, with the word "Cached:" before.
                    Every query that is printed will be saved to caching, so that it can be reused
                    if necessary. The query that will be printed in the union group of the items
                    in all categoreis that the item is in, beside the item itself.   
'''''
def query_by_item(store, caching):
    the_query = input()
    the_query = the_query.lstrip()
    if the_query in list(caching[TWO].keys()):
        print('Cached: ', end="")
        print(caching[TWO][the_query])
        return
    query_item = []
    for i in store.keys():
        if the_query in store[i].keys():
            query_item = list(set(store[i].keys()).union(set(query_item)))
    if not query_item:
        print("Error: no such item exists.")
        return
    query_item.remove(the_query)
    query_item = sorted(query_item)
    print(query_item)
    caching[TWO][the_query] = query_item


''''
Function Name: purchase_an_item
Input: store (a dict type), caching (a dict type)
Output: void
Function Operation: The function gets an input from the user, that is supposed to be 
                    an item that he want to purchase from the store. If the item does not 
                    exist in the store, the function will print an error. If the function 
                    exists, the function will print that it was bought, an then erase the
                    item from the dict store, and erase all the query's that were saved. 
                       
'''''
def purchase_an_item(store, caching):
    item = input()
    item = item.lstrip()
    price = False
    for category in store.keys():
        if item not in store[category]:
            continue
        price = store[category][item]
        store[category].pop(item)
    if not price:
        print('Error: no such item exists.')
        return
    print('You bought a brand new "' + item + '" for', price + '$.')
    for i in caching.keys():
        caching[i].clear()


''''
Function Name: admin_panel
Input: store (a dict type), caching (a dict type)
Output: void
Function Operation: The function asks for a password from the user. If the password is incorrect,
                    the function print an error, and return to the main menu. If the password is
                    good, the function will print an admin panel, that enables the user to pick
                    one of three options. If a non valid option was chosen, the function will print
                    an error, and then will ask again for a valid option, after printing the panel again.  
'''''
def admin_panel(store, caching):
    in_password = input('Password: ')
    the_pass = open(sys.argv[TWO], "r")
    the_pass = the_pass.readline()
    # the password is not correct
    if in_password != the_pass:
        print('Error: incorrect password, returning to main menu.')
        return
    while True:
        print('Admin panel:')
        print('\t0. Return to main menu.')
        print('\t1. Insert or update an item.')
        print('\t2. Save.')
        option = input()
        if option == '0':
            return
        if option == '1':
            insert_update_an_item(store, caching)
            continue
        if option == '2':
            save(store)
            continue
        print('Error: unrecognized operation.')


''''
Function Name: insert_update_an_item
Input: store (a dict type), caching (a dict type)
Output: void
Function Operation: The function gets an input from the admin, and checks if it is valid.
                    A valid input has categories, name and price of an item. If the input 
                    is invalid, the function will print an error, and return. If the input
                    is valid, the function will add the item to the store, and then will
                    erase the caching.   
'''''
def insert_update_an_item(store, caching):
    list_items = input()
    if len(list_items.split(COLON)) < TWO or len((list_items.split(COLON))[ONE].split(COMA)) < TWO:
        print('Error: not enough data.')
        return
    list_items = list_items.split(COLON, ONE)
    category_names = list_items[ZERO].split(COMA)
    category_names = [i.lstrip() for i in category_names]
    for a_category in category_names:
        if a_category not in store.keys():
            print('Error: one of the categories does not exist.')
            return
    name_item, price_item = list_items[ONE].split(COMA, ONE)
    name_item = name_item.lstrip()
    price_item = price_item.lstrip()
    if not price_item.isdigit() or int(price_item) < ZERO:
        print('Error: price is not a positive integer.')
        return
    for a_category in store.keys():
        if name_item in store[a_category].keys() or a_category in category_names:
            store[a_category][name_item] = price_item
    print('Item "' + name_item + '" added.')
    for i in caching.keys():
        caching[i].clear()


''''
Function Name: save
Input: store (a dict type)
Output: void
Function Operation: The function will save the store to out.txt, in the correct order.   
'''''
def save(store):
    out = open(sys.argv[THREE], "w")
    store = dict(sorted(store.items()))
    for category in store.keys():
        out.write(category + COLON)
        for name_item in sorted(store[category].keys()):
            out.write(SPACE + name_item + COMA + SPACE + store[category][name_item] + SEMICOLON)
        out.write('\n')
    out.close()
    print('Store saved to "out.txt".')


''''
Function Name: main
Input: void
Output: void
Function Operation: The function is the main function of the program, 
                    and will operate and get the option of the user to
                    what action he wants to do. The function will end,
                    and the program will end only if the user presses 0.   
'''''
def main():
    store = get_store()
    caching = dict()
    caching[ONE] = dict()
    caching[TWO] = dict()
    while True:
        print_menu()
        option = input()
        if option == '0':
            return
        if option == '1':
            query_two_product_categories(store, caching)
            continue
        if option == '2':
            query_by_item(store, caching)
            continue
        if option == '3':
            purchase_an_item(store, caching)
            continue
        if option == '4':
            admin_panel(store, caching)
            continue
        print('Error: unrecognized operation.')


if __name__ == '__main__':
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    SEMICOLON = ';'
    COLON = ':'
    COMA = ','
    SPACE = ' '
    main()