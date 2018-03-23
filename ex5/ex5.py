#############################################################
# FILE : ex5.py
# AUTHOR1 : Shimon Heimowitz, heimy4prez , 203631676
# AUTHOR2 : Raz Karl, razkarl, 311143127
# EXERCISE : intro2cs ex5 2016-2017
# DESCRIPTION:
# A library for ex5_gui.py to compare between prices of 
# shopping carts. 
# Supports up to 3 stores, represented in xml format 
# complying with Misrad Hakalkala standard.
#############################################################
import xml.etree.ElementTree as ET
import copy

PENALTY         = 1.25 # 25% penalty on price
NOT_FOUND       = -1

TAG_ITEM_CODE   = 'ItemCode'
TAG_ITEM_NAME   = 'ItemName'
TAG_ITEM_PRICE  = 'ItemPrice'
TAG_STORE_ID    = 'StoreId'
TAG_ITEMS_DICT  = 'Items'

# Tuple sections
PART_LEFT       = 0
PART_DELIMITER  = 1
PART_RIGHT      = 2

# ItemCode borders. Useful for extracting Itemcodes.
ITEMCODE_OPEN   = '['
ITEMCODE_CLOSE  = ']'

NUMBER_OF_STORES = 3


def get_attribute(store_db, ItemCode, tag):
    """
    Returns the attribute (tag)
    of an Item with code: Itemcode in the given store
    """
    return store_db[ItemCode][tag]


def string_item(item):
    """
    Textual representation of an item in a store.
    Returns a string in the format of '[ItemCode] (ItemName)'
    Return string format:
    '[Code]\t{Name}'
    """

    return "[{0}]\t{{{1}}}".format(item[TAG_ITEM_CODE], item[TAG_ITEM_NAME])


def string_store_items(store_db):
    """
    Textual representation of a store.
    Returns a string in the format of:
    string representation of item1
    string representation of item2
    ...
    """
    store_string = ''

    for item in store_db:
        store_string += "{0}\n".format(string_item(store_db[item]))

    return store_string


def read_prices_file(filename):
    """
    Read a file of item prices into a dictionary.  The file is assumed to
    be in the standard XML format of "misrad haclcala".
    Returns a tuple: store_id and a store_db,
    where the first variable is the store name
    and the second is a dictionary describing the store.
    The keys in this db will be ItemCodes of the different items and the
    values smaller  dictionaries mapping attribute names to their values.
    Important attributes include 'ItemCode', 'ItemName', and 'ItemPrice'
    """

    tree = ET.parse(filename)
    root = tree.getroot()

    # Retreive store id
    store_id = root.find(TAG_STORE_ID).text

    # Build Dictionary of dictionaries using nested loop.
    store_db = {}
    items = root.find(TAG_ITEMS_DICT)
    for item in items:
        item_dict = {item_property.tag : item_property.text for 
                                         item_property in item}
        store_db[item_dict[TAG_ITEM_CODE]] = item_dict

    return (store_id, store_db)


def filter_store(store_db, filter_txt):
    """
    Create a new dictionary that includes only the items
    that were filtered by user.
    I.e. items that text given by the user is part of their ItemName.
    Args:
    store_db: a dictionary of dictionaries as created in read_prices_file.
    filter_txt: the filter text as given by the user.
    """

    filtered_store_data = {}

    for item in store_db:
        # Collect all the items with the given text in their name.
        # Not_found represents -1, which is .find's return value.
        item_name = get_attribute(store_db, item , TAG_ITEM_NAME)
        if item_name.find(filter_txt) != NOT_FOUND:
            filtered_store_data[item] = store_db[item]

    return filtered_store_data


def list_vals_between_chars(text, open_char, close_char):
    """
    Receives string of text - containing occurrences of values
    enclosed in character borders. (Possible garbage between occurrences.)
    Returns a list of all the values.
    Example:
        open_char  =  '['
        close_char =  ']'
        text = "...[Value1]...[Value2]..."
        returns [Value1,Value2]
    """
    # Create list of all post open_char appearances
    open_parts = lambda text : text.split(open_char)[PART_DELIMITER:]
    # Trims single section until close_char
    closed_part = lambda text: text.split(close_char)[PART_LEFT]
    # List open parts in text
    opened_with_close = [part for part in open_parts(text) if 
                        close_char in part]
    # Trim open parts until close_char
    opened_and_closed = [closed_part(part) for part in opened_with_close]
    return opened_and_closed


def create_basket_from_txt(basket_txt):
    """
    Receives text representation of some items (and maybe some garbage
    at the edges)
    Returns a basket - list of ItemCodes that were included in basket_txt
    """
    return list_vals_between_chars(basket_txt, ITEMCODE_OPEN, ITEMCODE_CLOSE)


def get_basket_prices(store_db, basket):
    """
     Arguments: a store - dictionary of dictionaries and a basket -
       a list of ItemCodes
    Go over all the items in the basket and create a new list
      that describes the prices of store items
    In case one of the items is not part of the store,
      its price will be None.
    """
    price_list = []
    for code in basket:
        if code in store_db:
            price_list.append(float(
                get_attribute(store_db, code, TAG_ITEM_PRICE)))
        else:
            price_list.append(None)
    return price_list


def sum_basket(price_list):
    """
    Receives a list of prices
    Returns a tuple - the sum of the list (when ignoring Nones)
    and the number of missing items (Number of Nones)
    """
    sum = 0
    none_count = 0
    for price in price_list:
        if price == None:
            none_count += 1
        else:
            sum += price
    return (sum, none_count)


def basket_item_name(stores_db_list, ItemCode):
    """
    stores_db_list is a list of stores (list of dictionaries of
      dictionaries)
    Find the first store in the list that contains the item and return its
    string representation (as in string_item())
    If the item is not available in any of the stores return only [ItemCode]
    """
    for store in stores_db_list:
        if ItemCode in store:
            return string_item(store[ItemCode])
    return ITEMCODE_OPEN + ItemCode + ITEMCODE_CLOSE

def save_basket(basket, filename):
    '''
    Save the basket into a file
    The basket representation in the file will be in the following format:
    [ItemCode1]
    [ItemCode2]
    ...
    [ItemCodeN]
    '''
    # Will create file under filename is doesn't exist.
    with open(filename, 'a') as f:
        for ItemCode in basket:
            n = f.write(ITEMCODE_OPEN + ItemCode + ITEMCODE_CLOSE + '\n')


def load_basket(filename):
    '''
    Create basket (list of ItemCodes) from the given file.
    The file is assumed to be in the format of:
    [ItemCode1]
    [ItemCode2]
    ...
    [ItemCodeN]
    '''
    code_list = []
    with  open(filename, 'r') as file:
        # Extracts ItemCodes from each line
        for line in file:
            code_list.append(list_vals_between_chars(line, 
                                                    ITEMCODE_OPEN, 
                                                    ITEMCODE_CLOSE)[0])

    return code_list


def best_basket(list_of_price_list):
    '''
    Arg: list of lists, where each inner list is list of prices as created
    by get_basket_prices.
    Returns the cheapest store (index of the cheapest list) given that a
    missing item has a price of its maximal price in the other stores *1.25

    '''
    total_prices_list = []

    number_of_active_stores = 0
    for store in list_of_price_list:
        if store:
            number_of_active_stores +=1

    # Makes a safe copy of list of lists where each list holds prices for a 
    # single item.
    # This allows for a comfortable caparison of prices for a given item.
    # See documentation.
    lists_per_item = invert_list(list_of_price_list)

    for prices_per_item in lists_per_item:
        if None in prices_per_item:
            penalty = penalty_calculator(prices_per_item)
        # After calculating penalty once, runs through the prices and amends.
        for index in range(len(prices_per_item)):
            if prices_per_item[index] == None:
                prices_per_item[index] = penalty

    for store_num in range(number_of_active_stores):
        price_total = 0
        for prices_per_item in lists_per_item:
            price_total += prices_per_item[store_num]
        total_prices_list.append(price_total)
    for store_num in range(number_of_active_stores):
        if total_prices_list[store_num] == min(total_prices_list):
            return store_num


def invert_list(list_of_lists):
    """
    Receives list of lists
    Returns a new list of lists with the rows to be columns inverted.
    Example:
    list of lists = [[a , b ,  c],
                     [1 , 2 ,  3],
                     [do, re, mi]]

    returns:       [[a , 1 , do],
                    [b , 2 , re],
                    [c , 3 , mi]]
    Note! All lists must be of same length
    """
    inverted_list = []
    # All lists are assumed to be same length
    list_length = len(list_of_lists[0])
    for index in range(list_length):
        new_row = []
        for row in list_of_lists:
            # Assert list (row) is not empty list
            if row:
                new_row.append(row[index])
            inverted_list.append(new_row)
    return inverted_list


def penalty_calculator(prices_per_item):
    """
    Receives a list of prices (float or None) for 1 item from separate stores.
    Returns calculation of penalty price based on the most expensive price
    between the stores.
    If no store holds the item, the penalty is 0.
    """
    # Undesired changes are made on the list
    new_list = prices_per_item.copy()
    for index in range(len(new_list)):
        if new_list[index] == None:
            new_list[index] = 0 # 0 can be compared in max() function.
    penalty = max(new_list) * PENALTY
    return penalty
