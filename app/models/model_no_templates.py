from . import get_db_connection
from psycopg2 import sql
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

def update_fines_status(fine_id,status):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                        UPDATE fines 
                        SET paid_status = %s, payment_date = NOW()
                        WHERE fine_id = %s;
                            """,(status,fine_id))
                conn.commit()
                print('Successful')
                return 'success'
            
        except Exception as e:
            print(f"the error while updating the fines table is {e}")
        finally:
            conn.close()

def make_member_to_staff(Member_id,Member_Name,Email,Phone_Number,Address,hashed_password,Join_Date,):

    print("now in member_to_staff function!!")
    roles='staff'
    conn = get_db_connection()
    if not conn:
        return 'db_error'
    print("established connection")
    try:
        with conn.cursor() as cur:
            cur.execute("""
                    INSERT INTO staff (staff_name,Email,Phone_Number,Address,Join_Date,password,role)
                    VALUES (%s, %s, %s, %s, %s,%s,%s);
            """, (Member_Name,Email,Phone_Number,Address,Join_Date,hashed_password,roles))
            conn.commit()
            return 'success'
    except Exception as e:
        conn.rollback()
        print(f"Error registering member: {e}")
    finally:
        conn.close()

def check_is_staff(member_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                print('entereing checking staff')
                cur.execute("""
                Select staff_id from staff where email ILIKE %s;            
                """,(member_id,))
                results=cur.fetchone()
                if results:
                    print('success')
                    return 'success'
                print('failure')
                return 'failure'
        except Exception as e:
            print(f"The error while checking staff is {e}")
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

def get_member_information_from_member_id(member_id):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                Select *from members where member_id =%s;            
                """,(member_id,))
                results=cur.fetchone()

                print(results)
                if results:
                    return results
                return []
        except Exception as e:
            conn.rollback()
            print(f"The error while upgrading is {e}")
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
