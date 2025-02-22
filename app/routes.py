from flask import Blueprint, render_template, request, redirect, url_for,jsonify,flash,session,current_app
from .models import add_book as add_book_to_db,get_all_books ,add_author,add_genre,check_author,check_genre,filter_books,register_members,login_member,fetch_genres,create_tables,get_members,check_member,get_members_name_by_email,get_all_reservations,get_all_fines_history,get_all_issued_books,get_members_fines_history_by_email,get_members_reservations_by_email,get_issued_books_by_Email,get_book_id,count_copies,register_staff,add_to_copies,get_copy_id_from_book_id,get_member_id_by_email,reserve_book,check_reserve_by_member_id,delete_reservation_by_id,get_copy_id_from_book_id_for_reservation,update_book_copies,get_member_reservations,get_book_id_from_copy_ids,issue_books,get_staff_id_by_email,update_reservations_for_issued,Update_issued_books,add_book_copy,get_staffs,get_all_books_copies,get_all_genres,get_all_authors,get_columns_from_table,update_tables,delete_information_from_table,check_and_apply_fines,check_and_apply_reservations,get_isbn_from_book_id
import os 
import bcrypt
from .images import generate_filename_with_isbn,create_default_cover,resize_image
from werkzeug.utils import secure_filename


main = Blueprint('main', __name__)
def allowed_file(filename):
    # Use the allowed extensions from the app config.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


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
    print(session)
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
        elif result[0] == 'success':
            session["user_name"]=user
            session["email"]=Email
            session["role"]='member'
            print(f"The email in the login section is {Email}")
            return redirect(url_for('main.members_dashboard'))
        elif result[0]=='staff':
            session["user_name"] = result[1]
            session["email"] = Email
            session["role"]=result[2]
            if result[2]=='admin':
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.staff_dashboard'))
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
    if data["role"].lower() == "member":
        return jsonify({"redirect": url_for('main.members_dashboard')})
    elif data["role"].lower() == "admin":
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
        file = request.files['file']
        Book_Name = request.form.get('Book_Name')
        Author=request.form.get('Author')
        BirthDate=request.form.get('BirthDate')
        Email = request.form.get('Email')
        Genre=request.form.get('Genre')        
        Pages=request.form.get('Pages')
        Publication_Year=request.form.get('Publication_Year')
        ISBN=request.form.get('ISBN')
        Description=request.form.get('Synopsis')
        # Process the file if one was uploaded
        filename = None
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = generate_filename_with_isbn(filename, ISBN)  # Append ISBN

                print(f"The file name is {filename}")
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                print(f"Saving file to: {file_path}")
                print("Flask is looking for:", os.path.abspath(file_path))
                
                print("Current Flask directory:", os.getcwd())


                file.save(file_path)
                resize_image(file_path)
                print(f"Saved file as: {filename}")
            else:
                return "File type not allowed", 400
        else:
        # If no file is uploaded, create a default cover with the book name
            print ("The default cover page")
            filename = f"{secure_filename(Book_Name)}_{ISBN}_cover.jpg"  # Generate a unique filename
            print(f"the defauult cover image is {filename}")
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            create_default_cover(Book_Name, file_path)

        # Add logic to save book details with the generated/default cover
        print(f"Book cover used: {filename}")
        # Continue with your book saving logic...

            
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
            #write a logic here to add the genre descrioptions 
            
            Genre_ID=add_genre(Genre,description="New genre pending to be described")
       
        # add_genre(Genre)
        Book_ID=add_book_to_db(Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN,Author,image_filename=filename,Synopsis=Description)
        print(f"The book_id for adding the copies is {Book_ID}")
        copies=add_to_copies(Book_ID)

        # print(f"Book added: {Book_Name} by {Author_ID}")
        if copies=="success":
            if session["role"]=='admin':
                return jsonify({"success": True, "message": "Book Added Successfully!", "redirect_url": url_for('main.admin_dashboard')})
            else:
                return jsonify({"success": True, "message": "Book Added Successfully!", "redirect_url": url_for('main.staff_dashboard')})
    return render_template('add_books.html',role= session["role"])


# @main.route('/add_genere',methods=['POST'])
# def add)genre:

@main.route('/all_members_reservations')
def all_members_reservations():

    reservations=get_all_reservations()
    print("The reservations are:")
    print(reservations)
    return render_template('all_reservations_for_staff.html',reservations=reservations,role= session["role"])



# Route: View Books
@main.route('/books')
def view_books():
    # Replace this with a database query to fetch books
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
    print(f"The book ids are {book_idss}")
    print(f"The copy ids are {copy_ids} and the member with 'issued' is {members_with_issued}")
    for i, book in enumerate(books):
        if book[5] in book_idss:
            print(f"Got the book with reservations")
            print(f"the book_id of book is  {book[5]} being compared with {book_id_issued}")
            if book[5] in book_id_issued:
                print("Getinng book with issued ")
                books[i] = book + ('Issued',)
            else:
                books[i] = book + ('Reservation Pending',)
        else:
            copy_id = get_copy_id_from_book_id(book[5])
            print(f"the copy id  of {book[5]}  is {copy_id}")
            if copy_id[0] == 'success':
                books[i] = book + ('Reserve',)  # Modify the book directly in books
            else:
                books[i] = book + ('Not Available',)  # Modify the book directly in books
        
        print(f"\n{books[i]}\n")
    print(f"\n\n\n\n\n\n\n\{books}")
    return render_template('view_books.html', books=books,role= session["role"])

@main.route('/get_books',methods=['GET'])
def get_books():
    books =get_all_books()
    return jsonify([
        {
            'title': book[0],
            'author': book[1],
            'genre': book[2],
            'year': book[3].year,
            'pages':book[4],
            'book_id':book[5]
        }
        for book in books
        ])
# @main.route('/reserve',methods=['POST'])
# def reserve_users():
#     data = request.get_json()
#     book_id = data['book_id']
#     action = data['action']
#     print(f"The book id from the resere_users function in routes.py is {action} and {book_id}")

#     if "user_name" not in session:
#         flash("Please Log in first!!!","error")
#         return redirect(url_for("main.login"))
            
            
#     copy_id = get_copy_id_from_book_id(book_id)
#     result=get_member_id_by_email(session["email"])
#     member_id=result[0]
#     if member_id:
#         new_reserve=reserve_book(copy_id,member_id)
#         print("Came after reserving ")
#         update_book_copies(copy_id[1],'pending')
#         return jsonify({"success": True, "message": "Reservation Made Successfully!", "redirect_url": url_for('main.admin_dashboard')})



@main.route('/cancel_reserve',methods=['POST'])   
def cancel_reserve():
    data = request.get_json()
    book_id = data['book_id']
    action = data['action']

    if "user_name" not in session:
        flash("Please Log in first!!!","error")
        return redirect(url_for("main.login"))
        
    result=get_member_id_by_email(session["email"])
    print(f"the member id in cancellation reserves is {result[0]}")
    print(f"The book id is {book_id}")
    copy_ids = get_copy_id_from_book_id_for_reservation(book_id)
    print(f"The copy ids are {copy_ids}")
    for copy_idw in copy_ids:
        copy_id=copy_idw
        print(copy_id)
        reserve_id=check_reserve_by_member_id(result[0],copy_id)
        if reserve_id != 'Error':
            print("found the right reserve_ids")
            break
    print(f"The reserve id is {reserve_id} and {copy_id}")
    reserve_ids=reserve_id[0]


    if reserve_ids:
        print("yeah!!!!!!successfully deleted")
        delete_reservation_by_id(reserve_ids)
        print(copy_id)
        update_book_copies(copy_id,'Available')
        return jsonify({'status': 'success', 'message': 'Reservation cancelled successfully'},role= session["role"])


@main.route('/book/<int:book_id>')
def book_details(book_id):
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("main.login"))
    print(f"The book id is {book_id}")
    books =get_book_id(book_id)
    
    copies=count_copies(book_id)
    books=books+copies
    print(f"The books woth copies is {books}")
#     books=('okay','jane','fantasy','2018-05-10',250,"""Le Cirque des Rêves, the Circus of Dreams, arrives without warning, its black-and-white tents appearing mysteriously overnight. Unlike any other circus, it is only open at night and offers breathtaking wonders—ice gardens, cloud mazes, and performers who seem to defy the laws of nature. But behind this mesmerizing spectacle lies a deeper mystery: a competition between two young illusionists, Celia Bowen and Marco Alisdair. Bound since childhood by their mentors to a magical duel, they must push their abilities to unimaginable limits, using the circus as their battleground.

# Unbeknownst to them, this contest is not merely about skill but survival, and neither can walk away. As they weave intricate illusions to outshine one another, they fall deeply in love, complicating the game’s ruthless rules. Meanwhile, the circus’s performers and devoted followers, known as rêveurs, become unknowingly entwined in their fate.

# As tensions rise and the circus’s very existence comes into question, Celia and Marco must find a way to rewrite the game’s rules before everything unravels. Rich with poetic prose, enchanting imagery, and a dreamlike atmosphere, The Night Circus is a spellbinding tale of love, sacrifice, and the power of imagination. Erin Morgenstern crafts an immersive world that captivates readers, drawing them into a story where magic feels real, time is fluid, and dreams hold limitless possibilities. Perfect for fans of whimsical storytelling and intricate world-building, this novel lingers in the mind long after the final page.""",20)
    print(f"Coming from the get_book_id function and the books is {books}")
    if books:
        print("jsonifying")
        print("finish!!!")
           
        book_data = {
            "Book_Name": books[0],
            "Author_Name": books[1],
            "Genre": books[2],
            "Publication_Year": books[3].year,
            "Pages": books[4],
            "image_filename":books[5],
            "Synopsis": books[6],
            "Copies": books[7]

        }
        print(f"The image file name is {books[5]} and the role id is {session["role"]}")
        return render_template('individual_books.html',book=book_data,role=session["role"])
    else:
        return "Book not found", 404
    
@main.route('/fines')
def fines():
    fines_history=get_all_fines_history()
    print(f"the fines is {fines_history}")
    return render_template('all_fines_history.html',fines_history=fines_history,role= session["role"])

@main.route('/Members')
def view_members():
    members=get_members()
    print(members)
    return render_template('view_members.html',books=members,role= session["role"])

@main.route('/Staffs')
def view_staffs():
    members=get_staffs()
    print(members)
    return render_template('view_staff.html',books=members)

@main.route('/admin_dashboard')
def admin_dashboard():
    print(session)
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("main.login"))
    
    return render_template("admin_dashboard.html", user_name=session["user_name"],role= session["role"])

@main.route('/staff_dashboard')
def staff_dashboard():
    print(session)
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("main.login"))
    
    return render_template("staff_dashboard.html", user_name=session["user_name"],role= session["role"])


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
    return render_template('all_issued_books.html',issued_books=issued_books,role= session["role"])

@main.route('/genres')
def get_genre():
    genres=fetch_genres()
    return jsonify(genres)
    



@main.route('/members_dashboard')
def members_dashboard():
    print(session)
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("main.login"))
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
    print("The reservations are:")
    print(reservations)
    return render_template('all_reservations.html',reservations=reservations,role= session["role"])


@main.route('/members_issued_books')
def members_issued_books():
    email=session["email"]
    print(email)
    issued_books=get_issued_books_by_Email(email)
    return render_template('all_issued_books.html',issued_books=issued_books,role= session["role"])



@main.route('/reserve',methods=['POST'])
def reserve_users():
    data = request.get_json()
    book_id = data['book_id']
    action = data['action']
    print(f"The book id from the resere_users function in routes.py is {action} and {book_id}")

    if "user_name" not in session:
        flash("Please Log in first!!!","error")
        return redirect(url_for("main.login"))
            
            
    copy_id = get_copy_id_from_book_id(book_id)
    result=get_member_id_by_email(session["email"])
    member_id=result[0]
    if member_id:
        new_reserve=reserve_book(copy_id,member_id)
        print("Came after reserving ")
        update_book_copies(copy_id[1],'pending')
        return jsonify({"success": True, "message": "Reservation Made Successfully!", "redirect_url": url_for('main.admin_dashboard')})

@main.route('/Issue_book',methods=['POST'])
def Issue_book_by_staff():
    data = request.get_json()
    member_id = data['member_id']
    copy_id=data['copy_id']
    action = data['action']
    print(f"The member_id and copy_id from the issued book function in routes.py is {member_id} and {copy_id}")
    print(session["role"])
    if "user_name" not in session:
        flash("Please Log in first!!!","error")
        return redirect(url_for("main.login"))
    if session["role"]!='member':
        staff_id=get_staff_id_by_email(session["email"])
        print(f"got the staff id which is {staff_id} and now insrting into issued books table")
        issued_booksss=issue_books(copy_id=copy_id,member_id=member_id,status='issued',handled_by=staff_id)
        print(f"the issued book is {issued_booksss}")
        if issued_booksss=='success':
            reserve_status='issued'
            status_check='pending'
            update_reservations_for_issued(copy_id,member_id,status=reserve_status,status_check=status_check)
            print("updated successfully")
            update_book_copies(copy_id,'issued')

            return jsonify({"success": True, "message": "Book Issued  Successfully!", "redirect_url": url_for('main.admin_dashboard')})
        else:
            return jsonify({"error": True, "message": "Book Not issued Successfully!", "redirect_url": url_for('main.admin_dashboard')})


@main.route('/return_issued_book',methods=['POST'])
def return_issued_book():
    data = request.get_json()
    member_id = data['member_id']
    copy_id=data['copy_id']
    action = data['action']
    print(f"The member_id and copy_id from the issued book function in routes.py is {member_id} and {copy_id}")
    print(session["role"])
    if "user_name" not in session:
        flash("Please Log in first!!!","error")
        return redirect(url_for("main.login"))
    if session["role"]!='member':
        staff_id=get_staff_id_by_email(session["email"])
        print(f"got the staff id which is {staff_id} and now insrting into issued books table")
        issued_booksss=Update_issued_books(copy_id=copy_id,member_id=member_id,status='Returned')
        print(f"the issued book is {issued_booksss}")
        if issued_booksss=='success':
            reserve_status='Returned'
            status_check='issued'
            update_reservations_for_issued(copy_id,member_id,status=reserve_status,status_check=status_check)
            print("updated successfully")
            update_book_copies(copy_id,'Available')

            return jsonify({"success": True, "message": "Book Returned  Successfully!", "redirect_url": url_for('main.admin_dashboard')})
        else:
            return jsonify({"error": True, "message": "Error whhile returning the book", "redirect_url": url_for('main.admin_dashboard')})


@main.route('/add_books_copies', methods=['GET', 'POST'])
def add_books_copies():
    if request.method == 'POST':
        data = request.get_json()
        book_id = data.get("book_id")
        status = data.get("status")
        condition = data.get("condition")

        # Add book copy to the database
        success = add_book_copy(book_id, condition, status)

        return jsonify({"success": success})

    books = get_all_books()
    return render_template('add_books_copies.html', books=books,role= session["role"])

@main.route('/view_books')
def view_books_latter():
    # Replace this with a database query to fetch books
    books =get_all_books()
    return render_template('view_books_latter.html', books=books,role= session["role"])


@main.route('/view_books_copies')
def view_books_copies():
    # Replace this with a database query to fetch books
    books =get_all_books_copies()
    return render_template('view_books_copies.html', books=books,role= session["role"])

@main.route('/view_genres')
def view_genres():
    # Replace this with a database query to fetch books
    genres =get_all_genres()
    return render_template('view_genres.html', books=genres,role= session["role"])

@main.route('/view_authors')
def view_authors():
    # Replace this with a database query to fetch books
    authors =get_all_authors()
    return render_template('view_authors.html', books=authors,role= session["role"])


@main.route('/Views')
def Views():
    if "user_name" not in session:
        flash("please log in first!!","error")
        return redirect(url_for('main.login'))
    return render_template('views.html',role= session["role"])

@main.route('/get_columns')
def get_columns():
    table = request.args.get('table')
    record_id = request.args.get('id')

    if not table or not record_id:
        return jsonify({'error': 'Missing table or ID'}), 400

    columns = get_columns_from_table(table, record_id)  # Getting columns from table
    print(f"The columns are {columns} from {table} and extracting for {record_id}")

    column_names = columns.get('columns', [])  # List of column names
    constraints_list = columns.get('check_constraints', {})  # Dictionary of constraints
    foreign_keys = columns.get('foreign_keys', [])  # List of foreign key columns

    return jsonify({
        'columns': column_names,
        'table': table,
        'id': record_id,
        'constraints': constraints_list,
        'foreign_keys': foreign_keys
    })
@main.route('/edit_tables', methods=['POST'])
def edit_tables():
    table = request.args.get('table')
    record_id = request.args.get('id')

    if not table or not record_id:
        return jsonify({'error': 'Missing table or ID'}), 400

    updated_values = request.form.to_dict()  # Extract text data from the form
    print(f"In the edit_tables endpoint: Table={table}, Record ID={record_id}, Updated Values={updated_values}")

    # Process uploaded files
    for field_name, file in request.files.items():
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ISBN = get_isbn_from_book_id(record_id)
                filename = generate_filename_with_isbn(filename, ISBN)  # Append record ID
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                file.save(file_path)
                resize_image(file_path)
                print(f"Updated image saved as: {filename}")

                updated_values[field_name] = filename  # Store filename in the database
            else:
                return jsonify({'error': f'Invalid file type for {field_name}'}), 400

    # Update database with new values
    results = update_tables(updated_values=updated_values, record_id=record_id, table=table)

    redirect_url = "/Views" if session.get("role") != "member" else "/"

    if results == 'success':
        return jsonify({'success': 'Edited Successfully!', 'redirect_url': redirect_url})
    else:
        return jsonify({'error': 'Some error encountered!'})

 
@main.route('/edit_forms.html')
def edit_form_page():
    table = request.args.get("table", "")
    record_id = request.args.get("id", "")
    # Renders the edit_forms.html template.
    return render_template('edit_forms.html', table=table, record_id=record_id,role= session["role"])


@main.route('/delete', methods=['POST'])
def delete_contents():
    infomation = request.get_json()
    
    print(f"in the delete  endpoint The information are {infomation}")
    if not infomation:
        return jsonify({'error': 'Missing data'}), 400
    
    results=delete_information_from_table(updated_values=infomation)
    redirect_url = "/Views" if session.get("role") != "member" else "/"

    if results=='success':
        return jsonify({'success':'Deleted Successfully !','redirect_url':redirect_url})
    else:
        return jsonify({'error':'Some Error encountered!!!'})
    
@main.route('/check_fines')
def check_fines():
    overdue_books=check_and_apply_fines()
    if overdue_books:
        for copy_id in overdue_books:
            update_book_copies(copy_id,'Available')
    return render_template('all_fines_history.html')

@main.route('/expire_reservations')
def expire_reservations():
    expired_reserve=check_and_apply_reservations()
    if expired_reserve:
        for copy_id in expired_reserve:
            update_book_copies(copy_id,'Available')
    return render_template('all_reservations.html')

        