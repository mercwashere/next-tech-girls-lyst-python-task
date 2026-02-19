"""
Product Filtering Module

This module contains functions to filter product data based on various criteria.
Students will implement the filtering logic for each function below.
"""

import json
import psycopg2 as psycopg


def load_products(filename="data.jsonl"):
    """
    Load products from the JSONL data file.

    Args:
        filename (str): Path to the data file (default: "data.jsonl")

    Returns:
        list: List of product dictionaries
    """
    products = []
    with open(filename, "r") as file:
        for line in file:
            products.append(json.loads(line.strip()))
    return products

def database_products():
    TABLE_NAME = "products"
    with psycopg.connect(dbname="postgres", user="techforgirls", password="") as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # First, check if the 'products' table already exists! This will be true if you re-run this cell...
            cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (TABLE_NAME,))
            table_exists = cur.fetchone()[0]

            if not table_exists:
                print("table does not exist! Creating table: ", TABLE_NAME)
                # Execute a command: this creates a new 'products' table if it doesn't already exist!
                cur.execute("""
                    CREATE TABLE {} (
                        product_id bigint PRIMARY KEY,
                        color text,
                        gender text,
                        product_type text,
                        category text,
                        subcategory text,
                        designer text,
                        retailer text,
                        on_sale boolean,
                        regular_price float,
                        discount_price float,
                        short_description text,
                        long_description text,
                        image_url text,
                        item_score float
                    )
                    """.format(TABLE_NAME))
        
                # Pass data to fill a query placeholders and let Psycopg perform
                # the correct conversion (no SQL injections!)
                cur.executemany(
                    """INSERT INTO {} (
                        product_id,
                        color,
                        gender,
                        product_type,
                        category,
                        subcategory,
                        designer, 
                        retailer, 
                        on_sale, 
                        regular_price, 
                        discount_price, 
                        short_description, 
                        long_description, 
                        image_url,
                        item_score
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(TABLE_NAME),
                    [tuple(product.values()) for product in products]
                )
                print(f"Inserted {len(products)} products into the database!")
            else:
                print("Table already exists, skipping creation and data insertion.")

            # Query the database and obtain data as Python objects.
            cur.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 1;")
            sample_record = cur.fetchone()
            print(f"Sample record from the {TABLE_NAME} table: {sample_record}")

            # Get total count
            cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
            total_count = cur.fetchone()[0]
            print(f"Total records in database: {total_count}")

            # Make the changes to the database persistent
            conn.commit()


def filter_by_color(products, color):
    """
    Filter products by a specific color.

    Args:
        products (list): List of product dictionaries
        color (str): The color to filter by (e.g., "red", "blue", "black")

    Returns:
        list: Filtered list of products matching the specified color
    """
    # YOUR CODE HERE
    with psycopg.connect(dbname="postgres", user="techforgirls", password="") as conn:
    # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Query the database and obtain data as Python objects.
            cur.execute("SELECT * FROM products WHERE color = color;")
            items_of_colour = cur.fetchall()

    return items_of_colour
        
        
def filter_by_price_range(products, min_price, max_price):
    """
    Filter products within a specific price range.

    Args:
        products (list): List of product dictionaries
        min_price (float): Minimum price (inclusive)
        max_price (float): Maximum price (inclusive)

    Returns:
        list: Filtered list of products within the price range

    TODO: Implement this function to return only products within the price range.
    Hint: Consider both 'regular_price' and 'discount_price' fields.
    For items on sale, use the discount_price, otherwise use regular_price.
    """
    # YOUR CODE HERE
    with psycopg.connect(dbname="postgres", user="rosesyrett", password="") as conn:
    # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Query the database and obtain data as Python objects.
            cur.execute("SELECT * FROM products WHERE color = color;")
            items_of_colour = cur.fetchall()

    return items_of_colour
    
    return items_in_price_range



def filter_by_sale_status(products, on_sale=True):
    """
    Filter products by their sale status.

    Args:
        products (list): List of product dictionaries
        on_sale (bool): If True, return only products on sale.
                       If False, return only products not on sale.

    Returns:
        list: Filtered list of products matching the sale status

    TODO: Implement this function to return only products that match the sale status.
    Hint: Each product has an 'on_sale' field (True/False).
    """
    # YOUR CODE HERE
    
    items_on_sale = []
    for product in products:
        if product["on_sale"] == True:
            items_on_sale.append(product)
    
    return items_on_sale


def filter_by_brand(products, brand):
    """
    Filter products by a specific brand (designer).

    Args:
        products (list): List of product dictionaries
        brand (str): The brand to filter by (e.g., "gucci", "dolce-gabbana")

    Returns:
        list: Filtered list of products from the specified brand

    TODO: Implement this function to return only products from the given brand.
    Hint: Each product has a 'designer' field you can check.
    """
    # YOUR CODE HERE
    items_of_brand = []
    for product in products:
        if product["designer"] == brand:
            items_of_brand.append(product)
    
    return items_of_brand



def sort_by_price_high_to_low(products):
    """
    Sort products by price from highest to lowest.

    Args:
        products (list): List of product dictionaries

    Returns:
        list: Sorted list of products (highest to lowest price)

    TODO: Implement this function to sort products by price (descending).
    Hint: Use the discount_price if the item is on_sale, otherwise use regular_price.
    You can use Python's sorted() function with a key parameter.
    """
    # YOUR CODE HERE
    
    for product in products:
        if product["on_sale"] == True:
            product["sorting_price"] = product["discount_price"]
        else:
            product["sorting_price"] = product["regular_price"]

    return sorted(products, key=lambda x:x["sorting_price"], reverse=True)
    


        
def sort_by_price_low_to_high(products):
    """
    Sort products by price from lowest to highest.

    Args:
        products (list): List of product dictionaries

    Returns:
        list: Sorted list of products (lowest to highest price)

    TODO: Implement this function to sort products by price (ascending).
    Hint: Use the discount_price if the item is on_sale, otherwise use regular_price.
    You can use Python's sorted() function with a key parameter.
    """
    # YOUR CODE HERE
    for product in products:
        if product["on_sale"] == True:
            product["sorting_price"] = product["discount_price"]
        else:
            product["sorting_price"] = product["regular_price"]

    return sorted(products, key=lambda x:x["sorting_price"])


def sort_by_popularity(products):
    """
    Sort products by popularity score from highest to lowest.

    Args:
        products (list): List of product dictionaries

    Returns:
        list: Sorted list of products (most popular first)

    TODO: Implement this function to sort products by item_score (descending).
    Hint: Each product has a 'item_score' field.
    You can use Python's sorted() function with a key parameter.
    """
    # YOUR CODE HERE
    return sorted(products, key=lambda x:x["item_score"], reverse=True)

def filter_by_gender(products,gender):
    items_of_gender = []
    for product in products:
        if product["gender"] == gender:
            items_of_gender.append(product)
    
    return items_of_gender



def apply_filters(products, color=None, price_range=None, on_sale=None, brand=None, gender=None):
    """
    Apply multiple filters to the product list.
    This function combines all individual filters.

    Args:
        products (list): List of product dictionaries
        color (str, optional): Color to filter by
        price_range (tuple, optional): Tuple of (min_price, max_price)
        on_sale (bool, optional): Filter by sale status
        brand (str, optional): Brand to filter by

    Returns:
        list: Filtered list of products matching all specified criteria

    TODO: Implement this function to apply multiple filters in combination.
    Hint: Start with all products, then apply each filter one at a time if the
    parameter is provided (not None).
    """
    filtered_products = products

    # YOUR CODE HERE
    # Apply each filter if the parameter is provided
    # Example structure:
    if color is not None:
        filtered_products = filter_by_color(filtered_products, color)
    if price_range is not None:
         filtered_products = filter_by_price_range(filtered_products, price_range[0], price_range[1])
    if on_sale is not None:
        filtered_products = filter_by_sale_status(filtered_products,on_sale=True)
    if brand is not None:
        filtered_products = filter_by_brand(filtered_products,brand)
    if gender is not None:
        filtered_products = filter_by_gender(filtered_products,gender)


    return filtered_products


def save_filtered_results(products, output_filename="filtered_data.jsonl"):
    """
    Save filtered products to a new JSONL file.

    Args:
        products (list): List of product dictionaries to save
        output_filename (str): Path to the output file
    """
    with open(output_filename, "w") as file:
        for product in products:
            file.write(json.dumps(product) + "\n")
    print(f"Saved {len(products)} products to {output_filename}")


# Example usage (for testing your functions)
if __name__ == "__main__":
    # Load all products
    all_products = load_products()
    print(f"Loaded {len(all_products)} products")

    # Example: Test filtering by color
    # Uncomment the lines below once you've implemented the functions

    red_products = filter_by_color(all_products, "red")
    print(f"Found {len(red_products)} red products")

    # Example: Test filtering by price range
    affordable_products = filter_by_price_range(all_products, 0, 100)
    print(f"Found {len(affordable_products)} products under $100")

    # Example: Test filtering by sale status
    sale_products = filter_by_sale_status(all_products, on_sale=True)
    print(f"Found {len(sale_products)} products on sale")

    # Example: Test filtering by brand
    gucci_products = filter_by_brand(all_products, "gucci")
    print(f"Found {len(gucci_products)} Gucci products")

    womens_products = filter_by_gender(all_products,"F")
    print(f"Found {len(womens_products)} womens' products")


    # Example: Apply multiple filters
    filtered = apply_filters(
         all_products,
         color="black",
         price_range=(100, 500),
         on_sale=True,
         brand="gucci",
         gender = "F"
     )
    print(f"Found {len(filtered)} products matching all criteria")

    # Save filtered results
    save_filtered_results(filtered)
