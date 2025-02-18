from flask import Blueprint, render_template, request, redirect, url_for,jsonify,flash,session,current_app
from .models import add_book as add_book_to_db,get_all_books ,add_author,add_genre,check_author,check_genre,filter_books,register_members,login_member,fetch_genres,create_tables,get_members,check_member,get_members_name_by_email,get_all_reservations,get_all_fines_history,get_all_issued_books,get_members_fines_history_by_email,get_members_reservations_by_email,get_issued_books_by_Email,get_book_id,count_copies,register_staff,add_to_copies,get_copy_id_from_book_id
from werkzeug.utils import secure_filename
import os
import bcrypt
import numpy as np
from PIL import Image, ImageDraw, ImageFont




def resize_image(image_path, max_size=(300, 450)):
    """Resizes the image while maintaining aspect ratio."""
    with Image.open(image_path) as img:
        img.thumbnail(max_size)  # Resize while keeping aspect ratio
        img.save(image_path)  # Overwrite the original file
        print(f"Image resized to {img.size}")



# import textwrap
# from PIL import Image, ImageDraw, ImageFont

# def create_default_cover(book_name, file_path, bg_image_path="app/static/background.jpg"):
#     """Create a book cover with a textured background and properly formatted text."""
    
#     width, height = 300, 450
#     padding = 20  # Padding for text from edges

#     # Load background image
#     bg_image = Image.open(bg_image_path).resize((width, height)).convert("RGBA")

#     # Create a semi-transparent overlay for better contrast
#     overlay = Image.new("RGBA", (width, height), (211, 211, 211, 180))  # Light gray with opacity
#     img = Image.alpha_composite(bg_image, overlay)  # Blend overlay and background

#     draw = ImageDraw.Draw(img)

#     # Load font
#     try:
#         font = ImageFont.truetype("arial.ttf", 30)  # Adjust font size as needed
#     except IOError:
#         font = ImageFont.load_default()

#     # Wrap text if it's too long
#     wrapped_text = textwrap.fill(book_name, width=15)  # Break into lines

#     # Get text size and center it
#     bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
#     text_width = bbox[2] - bbox[0]
#     text_height = bbox[3] - bbox[1]

#     text_x, text_y = (width - text_width) / 2, (height / 3) - (text_height / 2)

#     # Add text shadow for better readability
#     shadow_offset = 2
#     draw.multiline_text((text_x + shadow_offset, text_y + shadow_offset), wrapped_text, font=font, fill="gray", align="center")
    
#     # Draw main text
#     draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill="black", align="center")

#     # Save final cover
#     img = img.convert("RGB")  # Remove alpha for JPEG compatibility
#     img.save(file_path)
#     print(f"Generated default cover at {file_path}")


from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap

def create_default_cover(book_name, file_path):
    """Create a visually appealing default cover that handles long titles."""
    width, height = 300, 450
    padding = 20  # Space from edges

    # Create a blank image with a gradient background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Gradient effect
    for i in range(height):
        color = (200 - i // 5, 200 - i // 5, 200 - i // 5)  # Light to dark gray gradient
        draw.line([(0, i), (width, i)], fill=color)

    # Try to load a nice font
    try:
        font = ImageFont.truetype("arial.ttf", 35)
    except IOError:
        font = ImageFont.load_default()

    # Wrap text to fit within the cover width
    max_width = width - (2 * padding)
    wrapped_text = textwrap.fill(book_name, width=15)  # Adjust width for wrapping

    # Reduce font size if text is too long
    while True:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_width <= max_width and text_height <= (height / 3):  # Limit text height to upper third
            break  # Font size is okay

        # Reduce font size
        font_size = font.size - 2
        if font_size < 15:  # Prevent text from getting too small
            break
        font = ImageFont.truetype("arial.ttf", font_size) if font.size > 15 else ImageFont.load_default()

    # Center the text
    text_x = (width - text_width) / 2
    text_y = (height / 3) - (text_height / 2)

    # Text shadow
    draw.multiline_text((text_x + 2, text_y + 2), wrapped_text, font=font, fill="gray", align="center")

    # Main text
    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill="black", align="center")

    # Add a simple border
    border_width = 5
    draw.rectangle([(border_width, border_width), (width - border_width, height - border_width)], outline="black", width=border_width)

    # Save the cover
    img.save(file_path)
    print(f"Generated cover at {file_path}")


def generate_filename_with_isbn(filename, isbn):
    """Generate a unique filename by appending ISBN to the original filename."""
    secure_name = secure_filename(filename)  # Secure the original filename
    name, ext = secure_name.rsplit('.', 1)  # Split name and extension
    return f"{name}_{isbn}.{ext}"  # Append ISBN to the name part

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
            Genre_ID=add_genre(Genre,description="New genre pending to be described")
       
        # add_genre(Genre)
        Book_ID=add_book_to_db(Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN,Author,image_filename=filename,Synopsis=Description)
        print(f"The book_id for adding the copies is {Book_ID}")
        copies=add_to_copies(Book_ID)

        # print(f"Book added: {Book_Name} by {Author_ID}")
        if copies=="success":
            return jsonify({"success": True, "message": "Book Added Successfully!", "redirect_url": url_for('main.admin_dashboard')})
    return render_template('add_books.html')

# Route: View Books
@main.route('/books')
def view_books():
    # Replace this with a database query to fetch books
    books =get_all_books()
    
    for i, book in enumerate(books):
        copy_id = get_copy_id_from_book_id(book[5])
        if copy_id[0] == 'success':
            books[i] = book + ('reserve',)  # Modify the book directly in books
        else:
            books[i] = book + ('Not Available',)  # Modify the book directly in books
        
        print(f"\n{books[i]}\n")
    print(f"\n\n\n\n\n\n\n\{books}")
    return render_template('view_books.html', books=books)

@main.route('/get_books',methods=['GET'])
def get_books():
    books =get_all_books()
    return jsonify([
        {
            'title': book[0],
            'author': book[1],
            'genre': book[2],
            'year': book[3].year,
        }
        for book in books
        ])
@main.route('/book/<int:book_id>')
def book_details(book_id):
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
            "Publication_Year": books[3],
            "Pages": books[4],
            "image_filename":books[5],
            "Synopsis": books[6],
            "Copies": books[7]
        }
        print(f"The image file name is {books[5]}")
        return render_template('individual_books.html',book=book_data)
    else:
        return "Book not found", 404
    
@main.route('/fines')
def fines():
    fines_history=get_all_fines_history()
    print(f"the fines is {fines_history}")
    return render_template('all_fines_history.html',fines_history=fines_history)
# @main.route('/reservation')
# def reservations():
#     reservations=get_all_reservations()
#     print("The reservations are:")
#     print(reservations)
#     return render_template('all_reservations.html',reservations=reservations)
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
