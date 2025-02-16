import psycopg2
from psycopg2 import sql
import bcrypt


# Database connection details
DB_CONFIG = {
    'dbname': 'library_management_system',
    'user': 'postgres',
    'password': 'Tensura',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_tables():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
               
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS Genres (
                        Genre_ID SERIAL PRIMARY KEY,
                        Genre VARCHAR(100) NOT NULL,
                        Description TEXT
                   );
                """)
                conn.commit()  
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS Authors (
                        Author_ID SERIAL PRIMARY KEY,
                        Author_Name VARCHAR(150) NOT NULL,
                        BirthDate DATE NOT NULL,
                        Email varchar(50) UNIQUE
                    );
                """) 
                conn.commit()
                cur.execute("""
                    CREATE TABLE Books (
                        Book_ID SERIAL PRIMARY KEY,
                        Book_Name VARCHAR(255) NOT NULL,
                        Author_ID INT,
                        Foreign key( Author_ID) REFERENCES Authors(Author_ID) ON DELETE CASCADE,
                        Genre_ID INT,
                        Foreign key (Genre_ID) REFERENCES Genres(Genre_ID) ON DELETE SET NULL,
                        Pages INT,
                        Publication_Year DATE,
                        ISBN VARCHAR(13) UNIQUE
                    );
                """)
                conn.commit()   
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS  Books_Copies (
                        Copy_ID SERIAL PRIMARY KEY,
                        Book_ID INT,
                        Foreign KEY (Book_ID) REFERENCES Books(Book_ID) ON DELETE CASCADE,
                        Condition VARCHAR(50),
                        Status VARCHAR(50) DEFAULT 'Available'
                    );
                """)
                conn.commit()   
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS  Members (
                        Member_ID SERIAL PRIMARY KEY,
                        Member_Name VARCHAR(150) NOT NULL,
                        Email VARCHAR(100) UNIQUE NOT NULL,
                        Phone_Number VARCHAR(10),
                        Address TEXT,
                        Password VARCHAR(255) NOT NULL, -- Store hashed passwords
                        Join_Date DATE DEFAULT CURRENT_DATE
                    );                   
                """)
                conn.commit()   
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS  Staff (
                        Staff_ID SERIAL PRIMARY KEY,
                        Staff_Name VARCHAR(150) NOT NULL,
                        Email VARCHAR(100) UNIQUE NOT NULL,
                        Phone_Number VARCHAR(15),
                        Address TEXT,
                        Role VARCHAR(50) DEFAULT 'Staff', -- Can be 'Staff' or 'Admin'
                        Join_Date DATE DEFAULT CURRENT_DATE,
                        Password VARCHAR(255) NOT NULL -- Store hashed passwords
                    );                   
                """)
                conn.commit()   
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS Issued (
                        Issued_ID SERIAL PRIMARY KEY,
                        Copy_ID INT,
                        Foreign KEY (Copy_ID) REFERENCES Books_Copies(Copy_ID) ON DELETE CASCADE,
                        Member_ID INT,
                        Foreign key (Member_ID) REFERENCES Members(Member_ID) ON DELETE CASCADE,
                        Issued_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        Due_Date TIMESTAMP NOT NULL,
                        Status VARCHAR(50) DEFAULT 'Issued',
                        Staff_ID INT,
                        Foreign key (Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE SET NULL
                    );
                """)
                conn.commit()       
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS  Fines (
                        Fine_ID SERIAL PRIMARY KEY,
                        Issued_ID INT,
                        Foreign key (Issued_ID) REFERENCES Issued(Issued_ID) ON DELETE CASCADE,
                        Amount DECIMAL(10, 2) NOT NULL,
                        Fine_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        Paid_Status BOOLEAN DEFAULT FALSE,
                        Payment_Date TIMESTAMP,
                        Staff_ID INT,
                        Foreign Key (Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE SET NULL
                    );                
                """)
                conn.commit()     
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS  Reservations (
                        Reservation_ID SERIAL PRIMARY KEY,
                        Copy_ID INT,
                        Foreign Key (Copy_ID) References Books_Copies(Copy_ID) ON DELETE CASCADE,
                        Member_ID INT,
                        Foreign key (Member_ID) REFERENCES Members(Member_ID) ON DELETE CASCADE,
                        Reservation_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        Status VARCHAR(50) DEFAULT 'Pending'
                    );
                """) 
                conn.commit()          
            print("Tables created successfully.")
            return 'success'
        except Exception as e:
            print(f"Error creating tables: {e}")
            return []
            conn.rollback()
        finally:
            conn.close()

def add_book(Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN,Author_Name):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO books (Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN)
                    VALUES (%s, %s, %s ,%s ,%s ,%s);
                """, (Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN))
                conn.commit()
                print(f"Book '{Book_Name}' by {Author_Name} added successfully.")
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

def check_member(Email):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print(f"The Email is {Email}")
                cur.execute("SELECT Member_ID FROM Members WHERE Email ILIKE %s;",(Email,))
                member = cur.fetchone()
                print(f"The check member function {member}")
                if member:
                    print("Arrived here!!")
                    return member[0]
                else:
                    return -1
        except Exception as e:
            print(f"Error checking member: {e}")
            return []
        finally:
            conn.close() 
def get_book_id(book_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print("okay")
                cur.execute("SELECT B.Book_Name,A.author_name,G.genre,B.Publication_Year,B.Pages FROM books as B inner join authors as A On B.Author_ID=A.Author_ID inner join Genres as G On G.Genre_ID=B.Genre_ID where B.book_id=%s;",(book_id,))
                books=cur.fetchone()
                print(f"The book is{books}")
                return books
        except Exception as e:
            print(f"The error is {e}")
            return[]
        finally:
            conn.close()
            
def get_all_books():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT B.Book_Name,A.author_name,G.genre,B.Publication_Year,B.Pages FROM books as B inner join authors as A On B.Author_ID=A.Author_ID inner join Genres as G On G.Genre_ID=B.Genre_ID;")
                books = cur.fetchall()
                return books
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
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

def fetch_genres():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT genre FROM genres")
                print("GENRES FETCHED!!!!")
                genres = cur.fetchall()
                return genres
        except Exception as e:
            print(f"Failed to connect to the database{e}")
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
                conn.commit()  # Commit the transaction
                return new_author[0]
                print(f"Author '{author_name}' added successfully.")
        except Exception as e:
            print(f"Error adding author name: {e}")
            conn.rollback()
        finally:
            conn.close()
                     
def get_all_members():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email, phone_number, join_date FROM members;")
                members = cur.fetchall()
                return members
        except Exception as e:
            print(f"Error fetching members: {e}")
            return []
        finally:
            conn.close()

def delete_book(book_id):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM books WHERE id = %s;", (book_id,))
                conn.commit()
                print(f"Book with ID {book_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting book: {e}")
            conn.rollback()
        finally:
            conn.close()

def filter_books(genres, year_operator, year_value, sort_by, order):
    # Base query for joining books, genres, and authors tables
    print(f"The year operator and year value are {year_operator},{year_value}")
    query = """
        SELECT books.book_name, authors.author_name, genres.genre, books.Publication_Year
        FROM books
        INNER JOIN genres ON books.genre_id = genres.genre_id
        INNER JOIN authors ON books.author_id = authors.author_id
        WHERE 1=1
    """
    
    params = []
    
    # If genres were selected, include the genres filter in the query
    if genres:
        genre_placeholders = ', '.join(['%s'] * len(genres))
        query += f" AND books.genre_id IN ({genre_placeholders})"
        params.extend(genres)  # Add the genre ids to the parameters list
    
    # If a year filter is specified, handle the year operator and value
        if year_value and year_operator is not None:
            if year_operator == 'BETWEEN' and isinstance(year_value, list) and len(year_value) == 2:
                query += " AND Extract(YEAR FROM books.Publication_Year) BETWEEN %s AND %s"
                params.extend(year_value)  # Add both year values to the parameters list
            else:
                query += f" AND Extract(YEAR FROM books.Publication_Year) {year_operator} %s"
                params.append(year_value)  # Add the single year value to the parameters list
    
    # Add sorting based on user selection
    if sort_by == 'title':
        sort_by_column = 'books.book_name'
    else:
        sort_by_column = 'books.Publication_Year'  # Default to sorting by publication year
    
    query += f" ORDER BY {sort_by_column} {order}"
    print(f"The query is {query}")
    # Execute the query and fetch results
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                results = cur.fetchall()
                return results
        except Exception as e:
            print(f"Error filtering books: {e}")
            return []
        finally:
            conn.close()

def register_members(Member_Name,Email,Phone_Number,Address,Join_Date,hashed_password):
    print("now in rregister_member function!!")
    conn = get_db_connection()
    if not conn:
        return 'db_error'
    print("established connection")
    try:
        with conn.cursor() as cur:
            # Check if the member already exists
            print("Executing the task!!")
            cur.execute('SELECT member_id FROM members WHERE member_name = %s and email = %s', (Member_Name, Email))
            existing_member = cur.fetchone()
            print("okay query done!!!")
            if existing_member:
                return 'already_registered'

            # Insert the new member into the database
            cur.execute("""
                    INSERT INTO members (Member_Name,Email,Phone_Number,Address,Join_Date,password)
                    VALUES (%s, %s, %s, %s, %s,%s);
            """, (Member_Name,Email,Phone_Number,Address,Join_Date,hashed_password))
            conn.commit()
            return 'success'
    except Exception as e:
        print(f"Error registering member: {e}")
        return e
    finally:
        conn.close()

def login_member(Email,password):

    conn=get_db_connection
    if conn:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
            # Fetch the user from the database
                cur.execute('SELECT member_name, password FROM members WHERE email ILIKE %s', (Email,))
                user = cur.fetchone()
                print(f"the content of the user is {user}")
                if not user:
                    print("Not")
                    return 'Not Registered'
                hashed_password=bytes.fromhex(user[1].replace('\\x', ''))
                print(hashed_password)
                # Verify the password
                if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                   print("Not")
                   return 'Not Registered'
                print("Not")
                return 'Success',user[0]             
        except Exception as e:
             print(f"Error login: {e}")
             return e
        finally:

            conn.close()
def get_members_name_by_email(email):
    query = "SELECT Member_Name FROM Members WHERE Email ILIKE %s;"
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print("start")
                cur.execute(query, (email,))  # Execute query with email as parameter
                result = cur.fetchone()  # Fetch one row
                print(f"The member by email{result}")
                if result:
                    print(result[1])
                    return {"name": result[1]}  # Assuming result[0] is Member_Name
                return None  # User not found
        except Exception as e:
            print(f"Error Fetching the members:{e}")
            return []

        finally:
            conn.close()
def get_members():

    conn=get_db_connection()
    if conn:
        try:
            print("GETting mEMBERS")
            with conn.cursor() as cur:
                cur.execute("Select Member_Name,Email,Phone_Number,Address,Join_Date From Members;")
                members= cur.fetchall()
                print(members)
                return members
            

        except Exception as e:
            print(f"Error Fetching the members:{e}")
            return []

        finally:
            conn.close()






















# def add_member(Member_Name,Email,Phone_Number,Address,Join_Date):
#     conn = get_db_connection()
#     if conn:
#         try:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                     INSERT INTO members (Member_Name,Email,Phone_Number,Address,Join_Date)
#                     VALUES (%s, %s, %s, %s, %s);
#                 """), (Member_Name,Email,Phone_Number,Address,Join_Date)
#                 conn.commit()
#                 print(f"Member '{Member_Name}' added successfully.")
#         except Exception as e:
#             print(f"Error adding member: {e}")
#             conn.rollback()
#         finally:
#             conn.close()



def get_all_reservations():
    conn=get_db_connection()
    if conn:
        
        try:
            print("Getting reservations")
            with conn.cursor() as cur:
                cur.execute("""        
                    Select members.member_name,books.book_name,reservations.reservation_date,reservations.status 
                    from reservations
                    inner join members On reservations.member_id=members.member_id
                    inner join books_copies On reservations.copy_id=books_copies.copy_id
                    inner join books on books.book_id=books_copies.book_id;
                """)
                reservations=cur.fetchall()
                print(reservations)
                return reservations


        except Exception as e:
            print(f"The error is {e}")
            return[]
        finally:
            conn.close()

def get_all_fines_history():
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                        Select members.member_name,books.book_name,fines.amount,issued.issued_date,fines.fine_date,fines.payment_date,fines.paid_status,staff.staff_name FROM fines
                        inner join issued On issued.issued_id=fines.issued_id
                        inner join members ON members.member_id=issued.member_id
                        inner join books_copies On books_copies.copy_id=issued.copy_id
                        inner join books ON books.book_id=books_copies.book_id
                        inner join staff ON staff.staff_id=fines.staff_id;
                """)
                fines=cur.fetchall()
                print(f"The fines are {fines}")
                return fines

        except Exception as e:
            print(f"The error is {e}")
            return[]
        finally:
            conn.close()


def get_all_issued_books():
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    Select members.member_name,books.book_name,issued.issued_date FROM issued
                    inner join members ON members.member_id=issued.member_id
                    inner join books_copies On books_copies.copy_id=issued.copy_id
                    inner join books ON books.book_id=books_copies.book_id

                """)
                issued_books=cur.fetchall()
                print(f"The fines are {issued_books}")
                return issued_books

        except Exception as e:
            print(f"The error is {e}")
            return[]
        finally:
            conn.close()



def get_members_fines_history_by_email(email):
    query = "SELECT Member_Name FROM Members WHERE Email ILIKE %s;"
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print("start")
                cur.execute("""
                        Select members.member_name,books.book_name,fines.amount,issued.issued_date,fines.fine_date,fines.payment_date,fines.paid_status,staff.staff_name FROM fines
                        inner join issued On issued.issued_id=fines.issued_id
                        inner join members ON members.member_id=issued.member_id
                        inner join books_copies On books_copies.copy_id=issued.copy_id
                        inner join books ON books.book_id=books_copies.book_id
                        inner join staff ON staff.staff_id=fines.staff_id
                        Where members.email ILIKE %s;
                """,(email,))
                fines=cur.fetchall()
                print(f"The fines are {fines}")
                return fines
                return None  # User not found
        except Exception as e:
            print(f"Error Fetching the members:{e}")
            return []

        finally:
            conn.close()


def get_members_reservations_by_email(email):
    query = "SELECT Member_Name FROM Members WHERE Email ILIKE %s;"
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""        
                    Select members.member_name,books.book_name,reservations.reservation_date,reservations.status 
                    from reservations
                    inner join members On reservations.member_id=members.member_id
                    inner join books_copies On reservations.copy_id=books_copies.copy_id
                    inner join books on books.book_id=books_copies.book_id
                    Where members.email ILIKE %s;
                """,(email,))
                reservations=cur.fetchall()
                print(reservations)
                return reservations
        except Exception as e:
            print(f"Error Fetching the members:{e}")
            return []

        finally:
            conn.close()

def get_issued_books_by_Email(email):
    query = "SELECT Member_Name FROM Members WHERE Email ILIKE %s;"
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    Select members.member_name,books.book_name,issued.issued_date FROM issued
                    inner join members ON members.member_id=issued.member_id
                    inner join books_copies On books_copies.copy_id=issued.copy_id
                    inner join books ON books.book_id=books_copies.book_id
                    Where members.email ILIKE %s

                """,(email,))
                issued_books=cur.fetchall()
                print(f"The fines are {issued_books}")
                return issued_books
        except Exception as e:
            print(f"Error Fetching the members:{e}")
            return []

        finally:
            conn.close()

def count_copies(book_id):
    
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""select *from books_copies;
                select Count(book_id) from books_copies
                Where book_id = %s
                Group by book_id
                """,(book_id))
                book_copies=cur.fetchone()
                print(f"Entered to count the copies and found the available number of copies is{book_copies}")
                return book_copies
        except Exception as e:
            print(f"The error is {e}")
            return[]
        finally:
            conn.close()

