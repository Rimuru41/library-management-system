from flask import render_template, request, redirect, url_for,jsonify,flash,session
from ..models.model_staff import get_all_fines_history,get_members,get_staffs,get_all_issued_books
from flask import Blueprint
main = Blueprint('staff_main', __name__)
 
@main.route('/fines')
def fines():
    fines_history=get_all_fines_history()
    return render_template('all_fines_history_for_staff.html',fines_history=fines_history,role= session["role"])

@main.route('/Members')
def view_members():
    members=get_members()
    return render_template('view_members.html',books=members,role= session["role"])

@main.route('/Staffs')
def view_staffs():
    members=get_staffs()
    return render_template('view_staff.html',books=members)

@main.route('/admin_dashboard')
def admin_dashboard():
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("auth_main.login"))
    return render_template("admin_dashboard.html", user_name=session["user_name"],role= session["role"])

@main.route('/staff_dashboard')
def staff_dashboard():
    if "user_name" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("auth_main.login"))
    
    return render_template("staff_dashboard.html", user_name=session["user_name"],role= session["role"])


@main.route('/issued_books')
def issued_books():
    issued_books=get_all_issued_books()
    return render_template('all_issued_books.html',issued_books=issued_books,role= session["role"])


@main.route('/staff_Views')
def staff_Views():
    if "user_name" not in session:
        flash("please lkushinaog in first!!","error")
        return redirect(url_for('auth_main.login'))
    return render_template('staff_view.html',role= session["role"])

