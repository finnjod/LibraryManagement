import psycopg2

# CONNECT TO POSTGRES
conn = psycopg2.connect(
    dbname="postgres",
    user="finnodonnell",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# reusable table thinger
def print_table(results):
    col_widths = [max(len(str(row[i])) for row in results) for i in range(len(results[0]))]
    
    def format_cell(cell):
        return str(cell).title() if isinstance(cell, str) else str(cell)

    print("\n".join(
        " | ".join(format_cell(row[i]).ljust(col_widths[i]) for i in range(len(row)))
        for row in results
    ))

def title_search(book_search):
    query = """
        SELECT * 
        FROM SPNLibrary
        WHERE title ILIKE %s;
    """
    
    cur.execute(query, (f"%{book_search}%",))
    results = cur.fetchall()
    
    if results:
        print_table(results)
    else:
        print(f"'{book_search}' is not a valid title!")

def author_search(search_author):
    query = """
        SELECT * 
        FROM SPNLibrary
        WHERE author ILIKE %s;
    """
    
    cur.execute(query, (f"%{search_author}%",))
    results = cur.fetchall()
    
    if results:
        print_table(results)
    else:
        print(f"'{search_author}' is not a valid author!")

# SIMPLE USER INTERFACE
running = True

while running:
    print("\nWhat would you like to do?\n"
          "1. Search by title\n"
          "2. Search by author\n"
          "3. Search by genre")

    user_input = input("Choice or 'quit': ")

    if user_input.lower() == "quit":
        running = False

    elif user_input == "1":
        search = input("Enter book title: ")
        title_search(search)

    elif user_input == "2":
        search = input("Enter author: ")
        author_search(search)

    elif user_input == "3":
        print("Genre search not implemented yet.")

cur.close()
conn.close()