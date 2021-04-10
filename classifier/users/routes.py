from flask import flash, render_template, request, Blueprint, redirect, url_for, current_app
from sqlalchemy import func, and_
from flask_login import current_user,logout_user, login_user, login_required
from classifier.models import User
from classifier.users.forms import RegistrationForm, RegistrationFormEdit, LogInForm
from classifier import db, bcrypt

users = Blueprint("users", __name__)

@users.route("/user/new", methods=['GET', 'POST'])
def create_new():
    if current_user.is_authenticated:
        flash("you are already registered", 'secondary')
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        temp= 'password'
        user=User(email=form.email.data, qualifications=form.qualifications.data,
                  expertise=form.expertise.data, password=temp)
        db.session.add(user)
        db.session.commit()
        flash("your registration was successful. you may now log in.", 'secondary')
        return redirect(url_for("users.login_page"))
    return render_template("new.html", form=form)



@users.route("/user/<int:id>")
@login_required
def user_page(id):
    user = User.query.filter(User.id==id).first()
    num = len(user.images)
    arg_dict={
        "number_classified":num,
        "user":user,
        "id":id,
        "title":"User Page" }
    return render_template("user_page.html", data=arg_dict)


@users.route("/logout")
def logout():
    logout_user()
    flash("logged out successfully")
    return redirect(url_for("main.index"))


@users.route("/login", methods=['GET',"POST"])
def login_page():
    form = LogInForm()
    if current_user.is_authenticated:
        flash("You are already logged in", "info")
        return redirect(url_for("users.user_page",id=current_user.id))

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        print('--------------------------------------------------------')
        print("user pass = {}".format(user.password))
        print(f"is true--------->{bcrypt.check_password_hash(user.password,form.password.data)}")
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash('login successful',"success")
            return redirect(url_for('users.user_page', id=user.id))
        else:
            flash("unsuccessful login! Please try again.", "danger")
        return render_template("login.html", form=form)
    arg_dict = {
        "title":"Log In",
        "legend":"ready to review birds?",
        "msg":"Please try again"}
    return render_template("login.html", form=form, data=arg_dict)


@users.route("/user/<int:id>/edit", methods=['POST', 'GET'])
@login_required
def edit_user(id):
    form = RegistrationFormEdit()
    user = User.query.filter(User.id == id).first()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.expertise = form.expertise.data
        current_user.qualifications = form.qualifications.data
        if form.password.data.strip() == "":
            current_user.password = bcrypt.generate_password_hash("password")
        else:
            current_user.password = form.password.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.user_page', id=current_user.id))
    elif request.method == "GET":
        flash("change your user profile","info")
        form.email = current_user.email
        form.qualifications = current_user.qualifications
        default_ex = current_user.expertise
        #form.expertise = current_user.expertise
        form.expertise.default = default_ex
        #form.password = current_user.password
        form.process()
    data = {
        "title":"update your profile",
        "user":user}
    return render_template("user_edit.html", form=form, data=data)
