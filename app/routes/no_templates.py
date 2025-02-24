from flask import render_template, request, redirect, url_for,jsonify,flash,session,current_app
from ..models.model_no_templates import reserve_book,update_book_copies,get_copy_id_from_book_id_for_reservation,check_reserve_by_member_id,delete_reservation_by_id,get_staff_id_by_email,update_reservations_for_issued,filter_books,get_columns_from_table,Update_issued_books,fetch_genres,issue_books,make_member_to_staff,update_fines_status,delete_information_from_table,get_member_information_from_member_id
from ..models.model_add_and_edit import get_all_books,check_genre
from ..models.model_members import get_member_id_by_email,get_copy_id_from_book_id
from flask import Blueprint
main = Blueprint('direct_main', __name__)

@main.route('/reserve',methods=['POST'])
def reserve_users():
    data = request.get_json()
    book_id = data['book_id']
    action = data['action']

    if "user_name" not in session:
        flash("Please Log in first!!!","error")
        return redirect(url_for("auth_main.login"))
            
    copy_id = get_copy_id_from_book_id(book_id)
    result=get_member_id_by_email(session["email"])
    member_id=result[0]
    if member_id:
        new_reserve=reserve_book(copy_id,member_id)
        update_book_copies(copy_id[1],'pending')
        return jsonify({"success": True, "message": "Reservation Made Successfully!", "redirect_url": url_for('staff_main.admin_dashboard')})
    

@main.route('/cancel_reserve',methods=['POST'])   
def cancel_reserve():
    data = request.get_json()
    book_id = data['book_id']
    action = data['action']

    if "user_name" not in session:
        flash("Please Log in first!!!","error")
        return redirect(url_for("auth_main.login"))
        
    result=get_member_id_by_email(session["email"])
    copy_ids = get_copy_id_from_book_id_for_reservation(book_id)
    for copy_idw in copy_ids:
        copy_id=copy_idw
        reserve_id=check_reserve_by_member_id(result[0],copy_id)
        if reserve_id != 'Error':
            break
    reserve_ids=reserve_id[0]
    if reserve_ids:
        delete_reservation_by_id(reserve_ids)
        update_book_copies(copy_id,'Available')
        return jsonify({'status': 'success', 'message': 'Reservation cancelled successfully'},role= session["role"])


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





@main.route('/Issue_book',methods=['POST'])
def Issue_book_by_staff():
    data = request.get_json()
    member_id = data['member_id']
    copy_id=data['copy_id']
    action = data['action']
    if "user_name" not in session:
        flash("Please Log in first!!!","error")
        return redirect(url_for("auth_main.login"))
    if session["role"]!='member':
        staff_id=get_staff_id_by_email(session["email"])
        issued_booksss=issue_books(copy_id=copy_id,member_id=member_id,status='issued',handled_by=staff_id)
        if issued_booksss=='success':
            reserve_status='issued'
            status_check='pending'
            update_reservations_for_issued(copy_id,member_id,status=reserve_status,status_check=status_check)
            update_book_copies(copy_id,'issued')
            return jsonify({"success": True, "message": "Book Issued  Successfully!", "redirect_url": url_for('staff_main.admin_dashboard')})
        else:
            return jsonify({"error": True, "message": "Book Not issued Successfully!", "redirect_url": url_for('staff_main.admin_dashboard')})


@main.route('/return_issued_book',methods=['POST'])
def return_issued_book():
    data = request.get_json()
    member_id = data['member_id']
    copy_id=data['copy_id']
    action = data['action']

    if "user_name" not in session:
        flash("Please Log in first!!!","error")
        return redirect(url_for("auth_main.login"))
    if session["role"]!='member':
        staff_id=get_staff_id_by_email(session["email"])
        issued_booksss=Update_issued_books(copy_id=copy_id,member_id=member_id,status='Returned')
        if issued_booksss=='success':
            reserve_status='Returned'
            status_check='issued'
            update_reservations_for_issued(copy_id,member_id,status=reserve_status,status_check=status_check)
            update_book_copies(copy_id,'Available')

            return jsonify({"success": True, "message": "Book Returned  Successfully!", "redirect_url": url_for('staff_main.admin_dashboard')})
        else:
            return jsonify({"error": True, "message": "Error whhile returning the book", "redirect_url": url_for('staff_main.admin_dashboard')})

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




@main.route('/genres')
def get_genre():
    genres=fetch_genres()
    return jsonify(genres)
    


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
    

@main.route('/make_member_staff', methods=['POST'])
def make_member_staff():
    infomation = request.get_json()
    
    print(f"in the make member to staff  endpoint The information are {infomation}")
    if not infomation:
        return jsonify({'error': 'Missing data'}), 400
    
    print(f"Type of infomation: {type(infomation)}")

    record_id=infomation["recordId"]
    members_information=get_member_information_from_member_id(record_id)
    print(f"Type of members_information: {type(members_information)}")
    

    if not members_information:
        return jsonify({'error':'Some Error encountered!!!'})
    results=make_member_to_staff(*members_information)
    print(f"Type of results: {type(results)}")

    redirect_url = "/Views" if session.get("role") != "member" else "/"

    if results=='success':
        print("Success")
        
        return jsonify({'success':'Made into Staff Successfully !','redirect_url':redirect_url})
    else:
        print("Already")
        return jsonify({'error':'Already a Staff !','redirect_url':redirect_url})

# @main.route('/check_fines')
# def check_fines():
#     overdue_books=check_and_apply_fines()
#     if overdue_books:
#         for copy_id in overdue_books:
#             update_book_copies(copy_id,'Available')
#     return render_template('all_fines_history.html')

# @main.route('/expire_reservations')
# def expire_reservations():
#     expired_reserve=check_and_apply_reservations()
#     if expired_reserve:
#         for copy_id in expired_reserve:
#             update_book_copies(copy_id,'Available')
#     return render_template('all_reservations.html')


@main.route('/update_fines',methods=['POST'])
def update_fines():
    data = request.get_json()
    fine_id = data['fine_id']
    action = data['action']
    print(f"The fine id from the issued book function in routes.py is {fine_id} and ")
    print(session["role"])
    if "user_name" not in session:
        flash("Please Log in first!!!","error")
        return redirect(url_for("auth_main.login"))
    
    fines_history=update_fines_status(fine_id,'True')
    if fines_history=='success':
            return jsonify({"success": True, "message": "Fine Paid  Successfully!", "redirect_url": url_for('staff_main.admin_dashboard')})
    else:
            return jsonify({"error": True, "message": "Error Encountered!", "redirect_url": url_for('staff_main.admin_dashboard')})
