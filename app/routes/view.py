from flask import render_template,redirect,url_for,flash,session
from ..models.model_view import get_all_genres,get_all_authors,get_all_reservations
from ..models.model_members import get_all_books_copies
from ..models.model_add_and_edit import get_all_books
from flask import Blueprint
main = Blueprint('view_main', __name__)

@main.route('/view_books')
def view_books_latter():
    books =get_all_books()
    return render_template('view_books_latter.html', books=books,role= session["role"])


@main.route('/view_books_copies')
def view_books_copies():
    books =get_all_books_copies()
    return render_template('view_books_copies.html', books=books,role= session["role"])

@main.route('/view_genres')
def view_genres():
    genres =get_all_genres()
    return render_template('view_genres.html', books=genres,role= session["role"])

@main.route('/view_authors')
def view_authors():
    authors =get_all_authors()
    return render_template('view_authors.html', books=authors,role= session["role"])


@main.route('/Views')
def Views():
    if "user_name" not in session:
        flash("please log in first!!","error")
        return redirect(url_for('auth_main.login'))
    return render_template('views.html',role= session["role"])



@main.route('/all_members_reservations')
def all_members_reservations():
    reservations=get_all_reservations()
    print("The reservations are:")
    print(reservations)
    return render_template('all_reservations_for_staff.html',reservations=reservations,role= session["role"])
