from flask import render_template, request, redirect, url_for,flash,session,jsonify
from ..models.model_authentication import register_members,login_member,create_tables
import bcrypt
from flask import Blueprint
main = Blueprint('auth_main', __name__)

# @main.route('/initialize-db')
# def initialize_db():
    
#     result=create_tables()
#     if result=='success':
#         return jsonify({'error':'Database Successfully Created!'}), 201
#     else:
#         return jsonify({'message':'Some Erroe encountered!!!'}),409
@main.route("/")
def home():
    print(session)
    return render_template("home.html")


@main.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #getting form details from frontend
        data = request.form
        Member_Name = request.form.get('Member_Name')
        Email=request.form.get('Email')
        Phone_Number=request.form.get('Phone_Number')
        Address = request.form.get('Address')
        Join_Date=request.form.get('join_date')        
        password = data.get('password')

        #checking if the they filled main parts
        if not Member_Name or not Email or not password:
            flash("'error': 'All fields are required'}")

        # Hashing the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        result = register_members(Member_Name,Email,Phone_Number,Address,Join_Date,hashed_password)
        
        #Checking
        print(f"Register {result}")
        if result == 'already_registered':
            flash('Already Registered!', 'message')        
        elif result == 'success':
            return redirect(url_for('auth_main.login'))
        else:
            flash(f"'error': 'An error occurred during registration {result}'")
    return render_template('register.html')

#Commenting it so that other can't get access to it and be admins so it was just to make a admin and then commenting it 

# @main.route('/register_staff',methods=['GET','POST'])
# def register_staffs():
#     if request.method == 'POST':
            #Getting Data from frontend
#         data = request.form
#         Member_Name = request.form.get('Member_Name')
#         Email=request.form.get('Email')
#         Phone_Number=request.form.get('Phone_Number')
#         Address = request.form.get('Address')
#         role=request.form.get('role')
#         Join_Date=request.form.get('join_date')        
#         password = data.get('password')

#         if not Member_Name or not Email or not password:
#             flash("'error': 'All fields are required'}")

#         # Hashing the password
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#         result = register_staff(Member_Name,Email,Phone_Number,Address,role,Join_Date,hashed_password)

#         #Checking 
#         print("now in the register staff function")
#         if result == 'already_registered':
#             flash('Already Registered!', 'message')        
#         elif result == 'success':
#             return redirect(url_for('main.login'))
#         else:
#             flash(f"'error': 'An error occurred during registration {result}'")
#     return render_template('register_staff.html')

@main.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #Getting Data from Frontend
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
            return redirect(url_for('members_main.members_dashboard'))
        elif result[0]=='staff':
            session["user_name"] = result[1]
            session["email"] = Email
            session["role"]=result[2]
            if result[2]=='admin':
                return redirect(url_for('staff_main.admin_dashboard'))
            return redirect(url_for('staff_main.staff_dashboard'))
        elif result[0] == 'Twin':
            session["user_name"] = user
            session["email"] = Email
            return render_template('choose_role.html', role=result[2])
        else:
          flash(f"The error Encountered is {result}")
    return render_template('login.html')

#setting role if anyone has both account in staff and member
@main.route('/set_role', methods=['POST'])
def set_role():
    data = request.json
    session["role"] = data["role"]

    # Redirect based on role
    if data["role"].lower() == "member":
        return jsonify({"redirect": url_for('members_main.members_dashboard')})
    elif data["role"].lower() == "admin":
        return jsonify({"redirect": url_for('staff_main.admin_dashboard')})
    else:  # Default for Staff or others
        return jsonify({"redirect": url_for('staff_main.staff_dashboard')})

# Logout route
@main.route("/logout")
def logout():
    session.clear()  # Clears all session data
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth_main.login"))
