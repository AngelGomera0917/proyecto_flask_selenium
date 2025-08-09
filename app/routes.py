from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db, Admin

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            login_user(Admin())
            return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    users = User.query.all()
    return render_template('dashboard.html', users=users)

@main.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    user = User(name=name, email=email, phone=phone)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    user = User.query.get(id)
    user.name = request.form['name']
    user.email = request.form['email']
    user.phone = request.form['phone']
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.dashboard'))
