from ..config import DB_CONFIG
import psycopg2
from datetime import datetime, timedelta

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None



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
