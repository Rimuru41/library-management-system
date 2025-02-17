from flask import Blueprint, render_template, request, redirect, url_for,jsonify,flash,session
from .models import add_book as add_book_to_db,get_all_books ,add_author,add_genre,check_author,check_genre,filter_books,register_members,login_member,fetch_genres,create_tables,get_members,check_member,get_members_name_by_email,get_all_reservations,get_all_fines_history,get_all_issued_books,get_members_fines_history_by_email,get_members_reservations_by_email,get_issued_books_by_Email,get_book_id,count_copies,register_staff
from .config import Config
import bcrypt

main = Blueprint('main', __name__)

@main.route('/initialize-db')
def initialize_db():
    result=create_tables()
    if result=='success':
        return jsonify({'error':'Database Successfully Created!'}), 201
    else:
        return jsonify({'message':'Some Erroe encountered!!!'}),409
    

    
# Home Page
@main.route("/")
def home():
    print(session)
    return render_template("home.html")


@main.route('/register',methods=['GET','POST'])
def register():
    print("Okay")
    if request.method == 'POST':
        
        data = request.form
        Member_Name = request.form.get('Member_Name')
        Email=request.form.get('Email')
        Phone_Number=request.form.get('Phone_Number')
        Address = request.form.get('Address')
        Join_Date=request.form.get('join_date')        
        password = data.get('password')

        if not Member_Name or not Email or not password:
            flash("'error': 'All fields are required'}")

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        result = register_members(Member_Name,Email,Phone_Number,Address,Join_Date,hashed_password)
        print(f"Register {result}")
        if result == 'already_registered':
            flash('Already Registered!', 'message')        
        elif result == 'success':
            return redirect(url_for('main.login'))
        else:
            flash(f"'error': 'An error occurred during registration {result}'")
        
        
        
    return render_template('register.html')


@main.route('/register_staff',methods=['GET','POST'])
def register_staffs():
    print("Okay")
    if request.method == 'POST':
        
        data = request.form
        Member_Name = request.form.get('Member_Name')
        Email=request.form.get('Email')
        Phone_Number=request.form.get('Phone_Number')
        Address = request.form.get('Address')
        role=request.form.get('role')
        Join_Date=request.form.get('join_date')        
        password = data.get('password')

        if not Member_Name or not Email or not password:
            flash("'error': 'All fields are required'}")

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        result = register_staff(Member_Name,Email,Phone_Number,Address,role,Join_Date,hashed_password)
        print("now inthe register staff function")
        if result == 'already_registered':
            flash('Already Registered!', 'message')        
        elif result == 'success':
            return redirect(url_for('main.login'))
        else:
            flash(f"'error': 'An error occurred during registration {result}'")
        
        
        
    return render_template('register_staff.html')

@main.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        Email = data.get('Email')
        password = data.get('password')
        result=login_member(Email,password)
        user=result[1]
        print(f"the resuls after the login function is {result}")
        print(f"The user of result [0[ is {user}")
        if result == 'Not Registered':
            flash('Incorrect Email or Password!', 'error')
        elif result[0] == 'Success':
            session["user_name"]=user
            session["email"]=Email
            session["role"]='member'
            print(f"The email in the login section is {Email}")
            return redirect(url_for('main.members_dashboard'))
        elif result[0] == 'Twin':
            session["user_name"] = user
            session["email"] = Email
            return render_template('choose_role.html', role=result[2])

        else:
          flash(f"The error Encountered is {result}")

    return render_template('login.html')

@main.route('/set_role', methods=['POST'])
def set_role():
    data = request.json
    session["role"] = data["role"]
    
    # Redirect based on role
    if data["role"] == "Member":
        return jsonify({"redirect": url_for('main.members_dashboard')})
    elif data["role"] == "Admin":
        return jsonify({"redirect": url_for('main.admin_dashboard')})
    else:  # Default for Staff or others
        return jsonify({"redirect": url_for('main.staff_dashboard')})

# Logout route
@main.route("/logout")
def logout():
    session.clear()  # Clears all session data
    flash("Logged out successfully!", "success")
    return redirect(url_for("main.login"))


# Route: Add Book
@main.route('/add_book', methods=['GET', 'POST'])

def add_book():
    print("ADD Books entry")
    if request.method == 'POST':
        print("add books")
        # Retrieve form data
        Book_Name = request.form.get('Book_Name')
        Author=request.form.get('Author')
        BirthDate=request.form.get('BirthDate')
        Email = request.form.get('Email')
        Genre=request.form.get('Genre')        
        Pages=request.form.get('Pages')
        Publication_Year=request.form.get('Publication_Year')
        ISBN=request.form.get('ISBN')
        # Add logic to save the book to the database (placeholder for now)
        print(f"check if the page is printed{Pages}")
        print(f"The first Email is {Email}")
        Author_ID=check_author(Email)
      
        if Author_ID==-1:
            print("adding author now")
            Author_ID=add_author(Author,BirthDate,Email)
        Genre_ID=check_genre(Genre)
        if Genre_ID==-1:
            print("Adding Genre now")
            Genre_ID=add_genre(Genre,description="New genre pending to be described")
       
        # add_genre(Genre)
        add_book_to_db(Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN,Author)

        # print(f"Book added: {Book_Name} by {Author_ID}")
        return redirect(url_for('main.admin_dashboard'))
    return render_template('add_books.html')

# Route: View Books
@main.route('/books')
def view_books():
    # Replace this with a database query to fetch books
    books =get_all_books()
    return render_template('view_books.html', books=books)
@main.route('/get_books',methods=['GET'])
def get_books():
    books =get_all_books()
    return jsonify([
        {
            'title': book[0],
            'author': book[1],
            'genre': book[2],
            'year': book[3].year
        }
        for book in books
        ])
@main.route('/book/<int:book_id>')
def book_details(book_id):
    print(f"The book id is {book_id}")
    books =get_book_id(book_id)
    copies=count_copies(book_id)
    print(copies)
    books=('okay','jane','fantasy','2018-05-10',250,"the very classical journeyy for this",20)
    print(f"Coming from the get_book_id function and the books is {books}")
    if books:
        print("jsonifying")
        print("finish!!!")
           
        book_data = {
            "Book_Name": books[0],
            "Author_Name": books[1],
            "Genre": books[2],
            "Publication_Year": books[3],
            "Pages": books[4],
            "Synopsis": books[5],
            "Copies": books[6]
        }
        return render_template('individual_books.html',book=book_data)
    else:
        return "Book not found", 404
    
@main.route('/fines')
def fines():
    fines_history=get_all_fines_history()
    print(f"the fines is {fines_history}")
    return render_template('all_fines_history.html',fines_history=fines_history)
@main.route('/reservation')
def reservations():
    reservations=get_all_reservations()
    print("The reservations are:")
    print(reservations)
    return render_template('all_reservations.html',reservations=reservations)
@main.route('/Members')
def view_members():
    members=get_members()
    print(members)
    return render_template('view_members.html',books=members)

@main.route('/admin_dashboard')
def admin_dashboard():
    print(session)
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("main.login"))
    
    return render_template("admin_dashboard.html", user_name=session["user_name"])

@main.route('/staff_dashboard')
def staff_dashboard():
    print(session)
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("main.login"))
    
    return render_template("staff_dashboard.html", user_name=session["user_name"])


@main.route('/filter_books', methods=['POST'])
def filter_books_route():
    try:
        data = request.get_json()
        genres = data.get('genres', [])
        year_operator = data.get('yearOperator', '=')
        year_value = data.get('yearValue')
        sort_by = data.get('sortBy', 'title')
        sort_order = data.get('sortOrder', 'asc')


        #converting genre into genre_id
        genres_id=[check_genre(genre) for genre in genres]

        #converting author into author_id
      
        print(genres_id,year_operator,year_value,sort_by,sort_order)
        print("fetching the books")
        # Call your filter_books function
        books = filter_books(genres_id, year_operator, year_value, sort_by, sort_order)
        print(f"Finished fetching the books{books}")
        # Return the filtered results as JSON
        return jsonify([
        {
            'title': book[0],
            'author': book[1],
            'genre': book[2],
            'year': book[3].year
        }
        for book in books
        ])
    except Exception as e:
        print(f"Error in /filter_books: {e}")
        flash(f"Error in/filter_books:{e} ")

@main.route('/issued_books')
def issued_books():
    issued_books=get_all_issued_books()
    return render_template('all_issued_books.html',issued_books=issued_books)

@main.route('/genres')
def get_genre():
    genres=fetch_genres()
    return jsonify(genres)
    



@main.route('/members_dashboard')
def members_dashboard():
    print(session["email"])
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("main.login"))
    return render_template("members_dashboard.html", user_name=session["user_name"])

@main.route('/members_fines')
def members_fines():
    email=session["email"]
    fines_history=get_members_fines_history_by_email(email)
    return render_template('all_fines_history.html',fines_history=fines_history)


@main.route('/members_reservations')
def members_reservations():
    email=session["email"]
    reservations=get_members_reservations_by_email(email)
    print("The reservations are:")
    print(reservations)
    return render_template('all_reservations.html',reservations=reservations)


@main.route('/members_issued_books')
def members_issued_books():
    email=session["email"]
    print(email)
    issued_books=get_issued_books_by_Email(email)
    return render_template('all_issued_books.html',issued_books=issued_books)
