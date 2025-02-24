from . import get_db_connection
from psycopg2 import sql

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
                    return 'success',copy_id[1]
                return 'Not available'

        except Exception as e:
            return e
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
            return []
        finally:
            conn.close()

            


def get_all_fines_history():
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                        Select members.member_name,books.book_name,fines.amount,issued.issued_date,fines.fine_date,fines.payment_date,fines.paid_status,staff.staff_name,fine_id FROM fines
                        inner join issued On issued.issued_id=fines.issued_id
                        inner join members ON members.member_id=issued.member_id
                        inner join books_copies On books_copies.copy_id=issued.copy_id
                        inner join books ON books.book_id=books_copies.book_id
                        inner join staff ON staff.staff_id=fines.staff_id;
                """)
                fines=cur.fetchall()
                return fines

        except Exception as e:
            return[]
        finally:
            conn.close()

def get_member_reservations(member_id,status):
    conn=get_db_connection()
    if conn:
        
        try:
            with conn.cursor() as cur:
                if len(status)==2:
                    cur.execute("""        
                        Select copy_id from reservations where member_id=%s and lower(status) IN %s
                    """,(member_id,status))
                    reservations=cur.fetchall()
                    return reservations
                else:
                    cur.execute("""        
                        Select copy_id from reservations where member_id=%s and status ILIKE %s
                    """,(member_id,status))
                    reservations=cur.fetchall()
                    return reservations


        except Exception as e:
            return[]
        finally:
            conn.close()
def get_issued_books_by_Email(email):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    Select members.member_name,books.book_name,issued.issued_date,issued.issued_id,issued.issued_status FROM issued
                    inner join members ON members.member_id=issued.member_id
                    inner join books_copies On books_copies.copy_id=issued.copy_id
                    inner join books ON books.book_id=books_copies.book_id
                    Where members.email ILIKE %s

                """,(email,))
                issued_books=cur.fetchall()
                return issued_books
        except Exception as e:
            return []

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
            conn.rollback()
            
        finally:
            conn.close()
def get_all_books_copies():
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("Select C.copy_id,B.book_name,C.condition,C.status From books_copies as C inner join Books as B ON B.book_id=C.book_id;")
                members= cur.fetchall()
                return members
            

        except Exception as e:
            return []

        finally:
            conn.close()

def get_members_reservations_by_email(email):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""        
                    Select members.member_name,books.book_name,reservations.reservation_date,reservations.status,reservations.reservation_id 
                    from reservations
                    inner join members On reservations.member_id=members.member_id
                    inner join books_copies On reservations.copy_id=books_copies.copy_id
                    inner join books on books.book_id=books_copies.book_id
                    Where members.email ILIKE %s;
                """,(email,))
                reservations=cur.fetchall()
                return reservations
        except Exception as e:
            return []

        finally:
            conn.close()
def get_members_fines_history_by_email(email):
    conn=get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                        Select members.member_name,books.book_name,fines.amount,issued.issued_date,fines.fine_date,fines.payment_date,fines.paid_status,staff.staff_name,fines.fine_id FROM fines
                        inner join issued On issued.issued_id=fines.issued_id
                        inner join members ON members.member_id=issued.member_id
                        inner join books_copies On books_copies.copy_id=issued.copy_id
                        inner join books ON books.book_id=books_copies.book_id
                        inner join staff ON staff.staff_id=fines.staff_id
                        Where members.email ILIKE %s;
                """,(email,))
                fines=cur.fetchall()
                return fines
        except Exception as e:
            return []

        finally:
            conn.close()
