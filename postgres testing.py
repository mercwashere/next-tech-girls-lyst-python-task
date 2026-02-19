import psycopg2 as psycopg
from filter import load_products

# Test connection to verify setup
with psycopg.connect(dbname="postgres", user="techforgirls", password="") as conn:
    print("Connected to PostgreSQL successfully!")
    print(f"Server version: {conn.info.server_version}")

products = load_products()

# check all product_ids are unique...

seen_ids = {product["product_id"] for product in products}

assert len(seen_ids) == len(products), "product IDs are not unique!"

print("Is 8 byte integer enough space for the product IDs? ", max(seen_ids) < 2**(8*4) -1 )
print("Is 4 byte integer enough space for the product IDs? ", max(seen_ids) < 2**(4*4) -1 )


TABLE_NAME = "products"

# Connect to an existing database
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