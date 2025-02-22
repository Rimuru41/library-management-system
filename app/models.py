import psycopg2
from psycopg2 import sql
import bcrypt
import re
from datetime import datetime, timedelta



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
                        ISBN VARCHAR(13) UNIQUE,
                        Synopsis text,
                        image_filename text
                    );
                """)
                conn.commit()   
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS  Books_Copies (
                        Copy_ID SERIAL PRIMARY KEY,
                        Book_ID INT,
                        Foreign KEY (Book_ID) REFERENCES Books(Book_ID) ON DELETE CASCADE,
                        Condition VARCHAR(50) check(Condition in ('New','Old')),
                        Status VARCHAR(50) DEFAULT 'Available' check(status in ('Available','pending','issued'))
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
                        Role VARCHAR(5) CHECK(Role IN ('staff','admin')), -- Can be 'Staff' or 'Admin'
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
                        Due_Date TIMESTAMP GENERATED ALWAYS AS (Issued_Date + INTERVAL '15 days') STORED,
                        Status VARCHAR(50) check(Status in ('issued','Returned','expired')),
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
                        Status VARCHAR(50) DEFAULT 'Pending' check(Status in ('Returned','Pending','issued','expired'))
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
                cur.execute("SELECT B.Book_Name,A.author_name,G.genre,B.Publication_Year,B.Pages,B.image_filename,B.synopsis FROM books as B inner join authors as A On B.Author_ID=A.Author_ID inner join Genres as G On G.Genre_ID=B.Genre_ID where B.book_id=%s;",(book_id,))
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
                cur.execute("SELECT B.Book_Name,A.author_name,G.genre,B.Publication_Year,B.Pages,B.book_id FROM books as B inner join authors as A On B.Author_ID=A.Author_ID inner join Genres as G On G.Genre_ID=B.Genre_ID;")
                books = cur.fetchall()
                return books
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
        finally:
            conn.close()

def get_all_genres():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT genre_id,genre,description from genres;")
                books = cur.fetchall()
                if books:
                    return books
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
        finally:
            conn.close()


def get_all_authors():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT author_id,author_name,birthdate,email from authors;")
                books = cur.fetchall()
                if books:
                    return books
        except Exception as e:
            print(f"Error fetching authors: {e}")
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
                print(f"The new aauthor is {new_author}")
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

def register_staff(Member_Name,Email,Phone_Number,Address,role,Join_Date,hashed_password):
    print("now in rregister_staff function!!")
    conn = get_db_connection()
    roles=role.lower()
    if not conn:
        return 'db_error'
    print("established connection")
    try:
        with conn.cursor() as cur:
            # Check if the member already exists
            print("Executing the task in staff!!")
            cur.execute('SELECT staff_id FROM staff WHERE staff_name = %s and email = %s', (Member_Name, Email))
            existing_member = cur.fetchone()
            print("okay query done!!!")
            if existing_member:
                return 'already_registered'

            # Insert the new member into the database
            cur.execute("""
                    INSERT INTO staff (staff_name,Email,Phone_Number,Address,role,Join_Date,password)
                    VALUES (%s, %s, %s, %s, %s,%s,%s);
            """, (Member_Name,Email,Phone_Number,Address,roles,Join_Date,hashed_password))
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
                print(f"the content of the user from members table is {user}")
                # if not user:
                #     print("Notxx")
                #     return 'Not Registered'
                # hashed_password=bytes.fromhex(user[1].replace('\\x', ''))
                # print(hashed_password)
                # # Verify the password
                # if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                #    print("Not")
                #    return 'Not Registered'
                # print("Not")
                staff=login_staff(Email,password)
                if not staff and not user:
                    return 'Not Registered'
                elif not staff and user:
                    return 'success',user[0]
                elif staff and not user:
                    return 'staff',staff[0],staff[1]
                return 'Twin',staff[0],staff[1]            
        except Exception as e:
             print(f"Error login: {e}")
        finally:
            conn.close()

def login_staff(Email,password):

    conn=get_db_connection
    if conn:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
            # Fetch the user from the database
                cur.execute('SELECT staff_name,role, password FROM staff WHERE email ILIKE %s', (Email,))
                user = cur.fetchone()
                print(f"the content of the user from staff is {user}")
                if not user:
                    print("Not")
                    return []
                hashed_password=bytes.fromhex(user[2].replace('\\x', ''))
                print(hashed_password)
                # Verify the password
                if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                   print("Not")
                   return []
                print("Not")
                return user[0],user[1]
        except Exception as e:
             print(f"Error login in staff: {e}")
             return []
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



def get_staff_id_by_email(email):
    query = "SELECT staff_id FROM staff WHERE Email ILIKE %s;"
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print("start")
                cur.execute(query, (email,))  # Execute query with email as parameter
                result = cur.fetchone()  # Fetch one row
                print(f"The member by email{result}")
                if result:
                    print(result[0])
                    return result[0] # Assuming result[0] is Member_Name
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
                cur.execute("Select Member_Name,Email,Phone_Number,Address,Join_Date,member_id From Members;")
                members= cur.fetchall()
                print(members)
                return members
            

        except Exception as e:
            print(f"Error Fetching the members:{e}")
            return []

        finally:
            conn.close()

def get_staffs():

    conn=get_db_connection()
    if conn:
        try:
            print("GETting mEMBERS")
            with conn.cursor() as cur:
                cur.execute("Select staff_name,Email,Phone_Number,Address,Join_Date,staff_id,role From staff;")
                members= cur.fetchall()
                print(members)
                return members
            

        except Exception as e:
            print(f"Error Fetching the members:{e}")
            return []

        finally:
            conn.close()

def get_all_books_copies():
    conn=get_db_connection()
    if conn:
        try:
            print("GETting books_copies")
            with conn.cursor() as cur:
                cur.execute("Select C.copy_id,B.book_name,C.condition,C.status From books_copies as C inner join Books as B ON B.book_id=C.book_id;")
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
                    Select members.member_name,books.book_name,reservations.reservation_date,reservations.status,members.member_id,books_copies.copy_id 
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




def get_member_reservations(member_id,status):
    conn=get_db_connection()
    if conn:
        
        try:
            print("Getting reservations")
            with conn.cursor() as cur:
                if len(status)==2:
                    cur.execute("""        
                        Select copy_id from reservations where member_id=%s and lower(status) IN %s
                    """,(member_id,status))
                    reservations=cur.fetchall()
                    print(f"The copy id of memerPid {member_id} with {status} is {reservations}")
                    print(reservations)
                    return reservations
                else:
                    cur.execute("""        
                        Select copy_id from reservations where member_id=%s and status ILIKE %s
                    """,(member_id,status))
                    reservations=cur.fetchall()
                    print(f"The copy_id fetched with {status} of {member_id} is {reservations}")
                    print(reservations)
                    return reservations


        except Exception as e:
            print(f"The error is {e}")
            return[]
        finally:
            conn.close()

def get_book_id_from_copy_ids(copy_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                Select book_id from books_copies where copy_id=%s
                """,(copy_id,))
                book_id=cur.fetchone()
                if book_id:
                    return book_id[0]
        except Exception as e:
            print("SOMETHING IS WRONG IN GETTING BOOK ID FROM COPY ID ")
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

def get_copy_id_from_book_id(book_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    select B.book_id,C.copy_id,C.status from books_copies as C inner join books as B
                    On C.book_id=B.book_id
                    where C.status ILIKE 'Available' and B.book_id=%s;

                """,(book_id,))
                copy_id=cur.fetchone()
                if copy_id:
                    print(f"find the copy{copy_id}")
                    return 'success',copy_id[1]
                return 'Not available'

        except Exception as e:
            print(f"the error is {e}")
            return e
        finally:
            conn.close()

def get_copy_id_from_book_id_for_reservation(book_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    select C.copy_id from books_copies as C inner join books as B
                    On C.book_id=B.book_id
                    where C.status ILIKE 'pending' and B.book_id=%s;

                """,(book_id,))
                copy_id=cur.fetchall()
                if copy_id:
                    print(f"find the copy{copy_id}")
                    return copy_id
                return 'Not available'

        except Exception as e:
            print(f"the error is {e}")
            return e
        finally:
            conn.close()


def reserve_book(copies_id,Member_ID):
    conn=get_db_connection()
    Copy_ID=copies_id[1]
    print(f"the copy_id is {Copy_ID} and {copies_id}")
    if conn:
        try:
            with conn.cursor() as cur:
                print("Inserting in Reservaations")
                cur.execute("""INSERT INTO Reservations (Copy_ID, Member_ID)
                VALUES (%s,%s) Returning reservation_id;
                """,(Copy_ID,Member_ID))
                conn.commit()
                reserv_id=cur.fetchone()

                print("The book is reserved!!!!!!!!!!!!!!!!")
                return reserv_id
                

        except Exception as e:
            print(f"Error while reserveing books:{e}")
            
        finally:
            conn.close()

def get_member_id_by_email(email):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
              select member_id from members where email ILIKE %s
                """,(email,))
                member_id=cur.fetchone()
                if member_id:
                    return member_id
                else:
                    return "Error"

        except Exception as e:
            print(f"Error while getting member id from email {e}")
            conn.rollback()
            
        finally:
            conn.close()

def check_reserve_by_member_id(member_id,copy_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
              select reservation_id from reservations where member_id = %s and copy_id=%s
                """,(member_id,copy_id))
                reserve_id=cur.fetchone()
                if reserve_id:
                    return reserve_id
                return "Error"

        except Exception as e:
            print(f"Error while getting member id from email {e}")
            conn.rollback()
            
        finally:
            conn.close()

# def delete_reservation_by_id(reserve_id,book_id):
#     conn=get_db_connection()
#     if conn:
#         try:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                     Delete from reservations where reservation_id=%s and copy_id=%s
#                 """,(reserve_id,book_id))
#                 conn.commit()
#                 print(f"Reservation with ID {reserve_id} deleted successfully.")

#         except Exception as e:
#             print(f"Error while getting member id from email {e}")
#             conn.rollback()
            
#         finally:
#             conn.close()


def delete_reservation_by_id(reserve_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    Delete from reservations where reservation_id=%s
                """,(reserve_id,))
                conn.commit()
                print(f"Reservation with ID {reserve_id} deleted successfully.")

        except Exception as e:
            print(f"Error while getting member id from email {e}")
            conn.rollback()
            
        finally:
            conn.close()


def update_book_copies(copy_id,status):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print("Executing in books copies table")
                cur.execute("""
                    Update books_copies
                    set status=%s
                    where copy_id=%s 
                """,(status,copy_id))
                conn.commit()
                print(f"Upadated book copies with ID {copy_id}  successfully.")

        except Exception as e:
            print(f"Error while getting member id from email {e}")
            conn.rollback()
            
        finally:
            conn.close()



def update_reservations_for_issued(copy_id,member_id,status,status_check):
    conn=get_db_connection()
    print(f"The update resrvation parameters are {copy_id},{member_id},{status}")
    if conn:
        try:
            with conn.cursor() as cur:
                print("Executing in books copies table")
                cur.execute("""
                    Update reservations
                    set status=%s
                    where copy_id=%s and member_id=%s and status ILIKE %s
                """,(status,copy_id,member_id,status_check))
                conn.commit()
                print(f"Upadated resrvatsions with ID {copy_id}  successfully.")

        except Exception as e:
            print(f"Error while getting member id from email {e}")
            conn.rollback()
            
        finally:
            conn.close()

            
def issue_books(copy_id,member_id,status,handled_by):
    print(copy_id,member_id,status,handled_by)
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO Issued (Copy_ID, Member_ID,Status,Staff_ID)
                    VALUES 
                    (%s, %s, %s, %s) Returning issued_id;
                """,(copy_id,member_id,status,handled_by))
                conn.commit()
                issuedbook=cur.fetchone()
                print("okay inserted done!!!!!")
                if issuedbook:
                    return "success"
                else:
                    return "failure"

        except Exception as e:
            conn.rollback()
            print(f"The error is {e}")
            return e
        finally:
            conn.close()

def Update_issued_books(copy_id,member_id,status):
    conn=get_db_connection()
    print(f"The update issued books are {copy_id},{status}")
    if conn:
        try:
            with conn.cursor() as cur:
                print("Executing in uupdated issued book  table")
                cur.execute("""
                    Update issued
                    set status=%s
                    where copy_id=%s and member_id=%s
                """,(status,copy_id,member_id))
                conn.commit()
                print(f"Upadated issued books with ID {copy_id}  successfully.")
                return 'success'
        except Exception as e:
            print(f"Error while getting member id from email {e}")
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


def edits_table(table,id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                select *from %s
                """,(table,id))
        

        except Exception as e:
            conn.rollback()
            print(f"Error while editing in {table} is {e}")
            return e 
        finally:
            conn.close()


import re

def get_columns_from_table(table, primary_key):
    """
    Retrieves CHECK constraints, all column names (except primary key), and foreign keys for a given table.

    Parameters:
      table (str): The table name.
      primary_key (str): The primary key column name.

    Returns:
      dict: A dictionary with:
          - 'check_constraints': {column_name: [valid_values]}  (CHECK constraints)
          - 'columns': [list of all column names except primary key]
          - 'foreign_keys': [list of foreign key columns]
    """
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Query for all columns except the primary key
                cur.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = %s AND ordinal_position > 1;
                """, (table, ))
                columns = [row[0] for row in cur.fetchall()]

                # Query for CHECK constraints
                cur.execute("""
                    SELECT kcu.column_name, cc.check_clause
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.constraint_column_usage kcu 
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.check_constraints cc
                        ON tc.constraint_name = cc.constraint_name
                    WHERE tc.table_name = %s AND tc.constraint_type = 'CHECK';
                """, (table,))
                check_constraints = {}
                
                for column_name, check_clause in cur.fetchall():
                    # Extract valid values using regex
                    matches = re.findall(r"'([^']*)'", check_clause)
                    if matches:
                        check_constraints[column_name] = matches

                # Query for foreign keys
                cur.execute("""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu 
                        ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_name = %s AND tc.constraint_type = 'FOREIGN KEY';
                """, (table,))
                foreign_keys = [row[0] for row in cur.fetchall()]

                result = {
                    'check_constraints': check_constraints,
                    'columns': columns,
                    'foreign_keys': foreign_keys
                }

                print(f"Constraints, columns, and foreign keys for table {table}: {result}")
                return result

        except Exception as e:
            print(f"Error while getting constraints, columns, and foreign keys for table {table}: {e}")
        finally:
            conn.close()


# def get_columns_from_table(table):
#     conn=get_db_connection()
#     if conn:
#         try:
#             with conn.cursor() as cur:
#                 if table =='genres':
#                     return ('Description',)
#                 elif table =='books_copies':
#                     return ('Condition',)
#                 cur.execute("""SELECT column_name FROM information_schema.columns 
#                     WHERE table_name = %s AND ordinal_position > 1;
#                 """,(table,))
#                 columns=cur.fetchall()
#                 columns_tuple=tuple(item[0] for item in columns)

#                 if columns:
#                     print(f"the columns from the {table} are {columns_tuple}")
#                     return columns_tuple
#         except Exception as e:
#             print(f"Error while getting column name from {table} is {e}")
#         finally:
#             conn.close()

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


def delete_information_from_table(updated_values):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                table=updated_values["table"]
                record_id=updated_values["recordId"]
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
                cur.execute(f"""
                                
                    Delete from {table} WHERE {id} = %s  

                    """,(record_id,))
                conn.commit()
                print(f"It is successful in deleting the row with id{record_id} from {table}")
                return 'success'
        

        except Exception as e:
            conn.rollback()
            print(f"the error while editing is {e}")
        finally:
            conn.close()


def check_and_apply_fines():
    conn = get_db_connection()
    fine_amount_per_day = 5  # Example fine amount per day overdue

    if conn:
        try:
            with conn.cursor() as cur:
                # Step 1: Find overdue books
                cur.execute("""
                    SELECT Issued_ID, Due_Date, CURRENT_TIMESTAMP - Due_Date AS time_overdue,copy_id
                    FROM Issued
                    WHERE Due_Date < CURRENT_TIMESTAMP AND Status IN ('issued', 'expired');
                """)
                overdue_books = cur.fetchall()

                for issued_id, due_date, time_overdue in overdue_books:
                    days_overdue = time_overdue.days
                    if days_overdue > 0:
                        # Step 2: Update the Issued table to mark as 'expired' if still 'issued'
                        cur.execute("""
                            UPDATE Issued
                            SET Status = 'expired'
                            WHERE Issued_ID = %s AND Status = 'issued';
                        """, (issued_id,))

                        # Step 3: Check if a fine already exists
                        cur.execute("""
                            SELECT Fine_ID, Amount
                            FROM Fines
                            WHERE Issued_ID = %s;
                        """, (issued_id,))
                        fine_record = cur.fetchone()

                        fine_amount = fine_amount_per_day * days_overdue

                        if fine_record:
                            # Step 4a: Update existing fine
                            cur.execute("""
                                UPDATE Fines
                                SET Amount = %s, Fine_Date = CURRENT_TIMESTAMP
                                WHERE Fine_ID = %s;
                            """, (fine_amount, fine_record[0]))
                        else:
                            # Step 4b: Insert new fine
                            cur.execute("""
                                INSERT INTO Fines (Issued_ID, Amount)
                                VALUES (%s, %s);
                            """, (issued_id, fine_amount))

                conn.commit()
                print(f"Processed fines for {len(overdue_books)} overdue books.")
                print(overdue_books)
                return overdue_books
        except Exception as e:
            print(f"Error while applying fines: {e}")
            conn.rollback()
        finally:
            conn.close()


def check_and_apply_reservations():
    conn = get_db_connection()
    expiration_period = timedelta(days=10)  # Max reservation period

    if conn:
        try:
            with conn.cursor() as cur:
                # Step 1: Find reservations older than 10 days
                cur.execute("""
                    SELECT Reservation_ID, Reservation_Date,copy_id
                    FROM Reservations
                    WHERE Status IN ('Pending', 'issued') 
                    AND Reservation_Date < (CURRENT_TIMESTAMP - INTERVAL '10 days');
                """)
                expired_reservations = cur.fetchall()

                for reservation_id, reservation_date in expired_reservations:
                    # Step 2: Update the reservation status to 'expired'
                    cur.execute("""
                        UPDATE Reservations
                        SET Status = 'expired'
                        WHERE Reservation_ID = %s;
                    """, (reservation_id,))

                conn.commit()
                print(f"Expired {len(expired_reservations)} reservations.")
                return expired_reservations

        except Exception as e:
            print(f"Error while expiring reservations: {e}")
            conn.rollback()
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