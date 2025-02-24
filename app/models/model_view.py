from . import get_db_connection
from psycopg2 import sql

def get_all_reservations():
    conn=get_db_connection()
    if conn:
        
        try:
            print("Getting reservations")
            with conn.cursor() as cur:
                cur.execute("""        
                    Select members.member_name,books.book_name,reservations.reservation_date,reservations.status,members.member_id,books_copies.copy_id,reservations.reservation_id 
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