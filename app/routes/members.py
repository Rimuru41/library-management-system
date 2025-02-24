from flask import Blueprint
main = Blueprint('members_main', __name__)
from flask import render_template, redirect, url_for,session
from ..models.model_members import get_members_fines_history_by_email,get_members_reservations_by_email,get_member_id_by_email,get_issued_books_by_Email,get_member_reservations,get_book_id_from_copy_ids,get_copy_id_from_book_id
from ..models.model_add_and_edit import get_all_books

@main.route('/members_dashboard')
def members_dashboard():
    if "user_name" not in session:
        return redirect(url_for("auth_main.login"))
    return render_template("members_dashboard.html", user_name=session["user_name"],role= session["role"])

@main.route('/members_fines')
def members_fines():
    email=session["email"]
    fines_history=get_members_fines_history_by_email(email)
    return render_template('all_fines_history.html',fines_history=fines_history,role= session["role"])


@main.route('/members_reservations')
def members_reservations():
    email=session["email"]
    reservations=get_members_reservations_by_email(email)
    return render_template('all_reservations.html',reservations=reservations,role= session["role"])


@main.route('/members_issued_books')
def members_issued_books():
    email=session["email"]
    issued_books=get_issued_books_by_Email(email)
    return render_template('all_issued_books.html',issued_books=issued_books,role= session["role"])



@main.route('/books')
def view_books():
    books =get_all_books()
    member_ids=get_member_id_by_email(session["email"])
    member_id=member_ids[0]
    copy_status=('pending','issued')
    copy_ids=get_member_reservations(member_id,copy_status)
    members_with_issued=get_member_reservations(member_id,'issued')
    book_idss=()
    book_id_issued=()

    for compared_copy_id in members_with_issued:
        compared_book_id=get_book_id_from_copy_ids(compared_copy_id)
        book_id_issued=book_id_issued+(compared_book_id,)

    for copy_id in copy_ids:
        book_ids=get_book_id_from_copy_ids(copy_id)
        book_idss=book_idss+(book_ids,)

    for i, book in enumerate(books):
        if book[5] in book_idss:
            print(f"the book_id of book is  {book[5]} being compared with {book_id_issued}")
            if book[5] in book_id_issued:
                books[i] = book + ('Issued',)
            else:
                books[i] = book + ('Reservation Pending',)
        else:
            copy_id = get_copy_id_from_book_id(book[5])
            if copy_id[0] == 'success':
                books[i] = book + ('Reserve',)  
            else:
                books[i] = book + ('Not Available',)  
    return render_template('view_books.html', books=books,role= session["role"])
