from . import get_db_connection
from psycopg2 import sql

def count_copies(book_id):
    
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                select Count(book_id) from books_copies
                Where book_id = %s
                Group by book_id
                """,(book_id,))
                book_copies=cur.fetchone()
                print(f"Entered to count the copies and found the available number of copies is{book_copies}")
                return book_copies
        except Exception as e:
            print(f"The error is {e}")
            return[]
        finally:
            conn.close()

def update_tables(updated_values,record_id,table):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                set_clause = ", ".join([f"{col} = '{updated_values[col]}'" for col in updated_values.keys()])
                values = list(updated_values.values())
                if table.lower()=='books_copies':
                    id='copy_id'
                elif table.lower()=='genres':
                    id='genre_id'
                elif table.lower()=='books':
                    id='book_id'
                elif table.lower()=='members':
                    id='member_id'
                elif table.lower()=='staff':
                    id='staff_id'
                else:
                    id='author_id'
                print(f"The set clause is {set_clause} and id is {id} with record id equal to {record_id}")
                cur.execute(f"""
                                
                    UPDATE {table} SET {set_clause} WHERE {id} = %s  

                    """,(record_id,))
                conn.commit()
                print(f"It is success")
                return 'success'
        

        except Exception as e:
            conn.rollback()
            print(f"the error while editing is {e}")
        finally:
            conn.close()

def get_book_id(book_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print("okay")
                cur.execute("SELECT B.Book_Name,A.author_name,G.genre,B.Publication_Year,B.Pages,B.image_filename,B.synopsis FROM books as B inner join authors as A On B.Author_ID=A.Author_ID inner join Genres as G On G.Genre_ID=B.Genre_ID where B.book_id=%s;",(book_id,))
                books=cur.fetchone()
                print(f"The book is{books}")
                return books
        except Exception as e:
            print(f"The error is {e}")
            return[]
        finally:
            conn.close()
    
def get_isbn_from_book_id(book_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("Select isbn from books where book_id is %s;",(book_id,))
                isbn=cur.fetchone()
                if isbn:
                    return isbn
                else:
                    print("Book not found which indicates some error")
        except Exception as e:
            print(f"The erro while getting isbn is {e}")
        finally:
            conn.close()
       
def get_all_books():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT B.Book_Name,A.author_name,G.genre,B.Publication_Year,B.Pages,B.book_id FROM books as B inner join authors as A On B.Author_ID=A.Author_ID inner join Genres as G On G.Genre_ID=B.Genre_ID;")
                books = cur.fetchall()
                return books
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
        finally:
            conn.close()

def add_genre(genre_name, description):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print(f"The adding genere is {genre_name}")
                cur.execute("""
                    INSERT INTO genres (Genre, description)
                    VALUES (%s, %s) Returning Genre_ID;
                """, (genre_name, description))
                new_genres=cur.fetchone()

                conn.commit()
                print(f"The Genre_ID of {new_genres[0]}")
                return new_genres[0]
                print(f"Genre '{genre_name}' added successfully.")
        except Exception as e:
            print(f"Error adding genre: {e}")
            conn.rollback()
        finally:
            conn.close()

def add_book(Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN,Author_Name,image_filename,Synopsis):
    print(f"the book name is {Book_Name}")
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO books (Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN,image_filename,synopsis)
                    VALUES (%s, %s, %s ,%s ,%s ,%s,%s,%s) Returning book_id;
                """, (Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN,image_filename,Synopsis))
                conn.commit()
                books=cur.fetchone()
                print(f"Book '{Book_Name}' by {Author_Name} added successfully.")
                return books[0]
        except Exception as e:
            print(f"Error adding book: {e}")
            conn.rollback()
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")

def check_author(Email):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print(f"The Email is {Email}")
                cur.execute("SELECT Author_ID FROM Authors WHERE Email ILIKE %s;",(Email,))
                author = cur.fetchone()
                print(f"The check author function {author}")
                if author:
                    print("Arrived here!!")
                    return author[0]
                else:
                    return -1
        except Exception as e:
            print(f"Error checking books: {e}")
            return []
        finally:
            conn.close()    

def add_author(author_name,BirthDate,Email):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO authors (author_name,BirthDate,Email)
                    VALUES (%s,%s,%s) Returning author_id;
                """, (author_name,BirthDate,Email))

                new_author = cur.fetchone()
                print(f"The new aauthor is {new_author}")
                conn.commit()  # Commit the transaction
                return new_author[0]
                print(f"Author '{author_name}' added successfully.")
        except Exception as e:
            print(f"Error adding author name: {e}")
            conn.rollback()
        finally:
            conn.close()

def check_genre(genre_name):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print(f"The check genre Genre name is {genre_name}")
                cur.execute("""
                  SELECT Genre_ID FROM Genres WHERE Genre ILIKE %s;
                """, (genre_name,))
                old_genre=cur.fetchone()
                if old_genre:
                    print(f"Already Existed  {old_genre[0]}")
                    return old_genre[0]
                else:
                    return -1
                conn.commit()
                
        except Exception as e:
            print(f"Error adding genre: {e}")
            conn.rollback()
        finally:
            conn.close()

def add_book_copy(book_id, status, condition):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                Insert into books_copies(book_id,condition,status)
                values(%s,%s,%s) Returning copy_id;
                """,(book_id,status,condition))
                conn.commit()
                book_copy=cur.fetchone()
                if book_copy:
                    return 'success'
                else:
                    return 'failure'

        except Exception as e:
            conn.rollback()
            print(f"The error while adding book copy is :{e}")
        finally:
            conn.close()




def add_to_copies(book_id):
    
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO Books_Copies (Book_ID, Condition, Status)
                    VALUES
                    (%s, 'New', 'Available') Returning copy_id;
                """,(book_id,))
                conn.commit()
                book_copies=cur.fetchone()
                print(f"Entered to add to copies{book_copies}")
                if book_copies:
                    return "success"

        except Exception as e:
            conn.rollback()
            print(f"The error is {e}")
            return e
        finally:
            conn.close()