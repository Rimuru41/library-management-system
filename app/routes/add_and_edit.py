from flask import Blueprint
main = Blueprint('main', __name__)
from flask import render_template, request, redirect, url_for,jsonify,flash,session,current_app
from ..models.model_add_and_edit import check_author,add_author,add_genre,check_genre,add_book_copy,get_all_books,get_isbn_from_book_id,update_tables,count_copies,get_book_id,add_to_copies,add_book as add_book_to_db
import os
from ..images import generate_filename_with_isbn,create_default_cover,resize_image,allowed_file
from werkzeug.utils import secure_filename

# Route: Add Book
@main.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
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
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                resize_image(file_path)
            else:
                return "File type not allowed", 400
        else:
            filename = f"{secure_filename(Book_Name)}_{ISBN}_cover.jpg"  # Generate a unique filename
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            create_default_cover(Book_Name, file_path)
        Author_ID=check_author(Email)
        if Author_ID==-1:
            Author_ID=add_author(Author,BirthDate,Email)
        Genre_ID=check_genre(Genre)
        if Genre_ID==-1:
            print("Adding Genre now")            
            Genre_ID=add_genre(Genre,description="New genre pending to be described")
        Book_ID=add_book_to_db(Book_Name,Author_ID,Genre_ID,Pages,Publication_Year,ISBN,Author,image_filename=filename,Synopsis=Description)
        copies=add_to_copies(Book_ID)
        if copies=="success":
            if session["role"]=='admin':
                return jsonify({"success": True, "message": "Book Added Successfully!", "redirect_url": url_for('staff_main.admin_dashboard')})
            else:
                return jsonify({"success": True, "message": "Book Added Successfully!", "redirect_url": url_for('staff_main.staff_dashboard')})
    return render_template('add_books.html',role= session["role"])


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



@main.route('/book/<int:book_id>')
def book_details(book_id):
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("auth_main.login"))
    books =get_book_id(book_id) 
    copies=count_copies(book_id)
    books=books+copies
    if books:
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
        return render_template('individual_books.html',book=book_data,role=session["role"])
    else:
        return "Book not found", 404
   