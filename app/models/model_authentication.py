from . import get_db_connection
from psycopg2 import sql
import psycopg2
import bcrypt

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


