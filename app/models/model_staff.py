from .model_members import get_all_fines_history
from . import get_db_connection
from psycopg2 import sql

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

def get_all_issued_books():
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    Select members.member_name,books.book_name,issued.issued_date,issued_id,issued.status FROM issued
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
