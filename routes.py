from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, User
import logging
import re

main = Blueprint('main', __name__)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            zip_code = request.form['zip_code']
            country = request.form['country']
            area = request.form['area']
            group = request.form['group']
            department = request.form['department']

            # Validaciones del lado del servidor
            if not first_name or not first_name.isalpha() or len(first_name) > 50:
                flash('First name is required and should only contain alphabetic characters (max 50).')
                return redirect(url_for('main.register'))

            if not last_name or not last_name.isalpha() or len(last_name) > 50:
                flash('Last name is required and should only contain alphabetic characters (max 50).')
                return redirect(url_for('main.register'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered.')
                return redirect(url_for('main.register'))

            email_pattern = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$')
            if not email_pattern.match(email):
                flash('Invalid email format.')
                return redirect(url_for('main.register'))

            if User.query.filter_by(phone=phone).first():
                flash('Phone numer already registered.')
                return redirect(url_for('main.register'))

            phone_pattern = re.compile(r'^[+]+[0-9]{10,12}$')
            if not phone_pattern.match(phone):
                flash('Invalid phone format')
                return redirect(url_for('main.register'))

            password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
            if not password_pattern.match(password):
                flash(
                    'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.')
                return redirect(url_for('main.register'))

            if address and len(address) > 200:
                flash('Address should not exceed 200 characters.')
                return redirect(url_for('main.register'))

            if city and len(city) > 100:
                flash('City should not exceed 100 characters.')
                return redirect(url_for('main.register'))

            if state and len(state) > 100:
                flash('State should not exceed 100 characters.')
                return redirect(url_for('main.register'))

            if zip_code and (not zip_code.isdigit() or len(zip_code) < 5 or len(zip_code) > 10):
                flash('Zip code should contain only numeric characters (5-10 characters).')
                return redirect(url_for('main.register'))

            if country and len(country) > 100:
                flash('Country should not exceed 100 characters.')
                return redirect(url_for('main.register'))

            if not area or len(area) > 100:
                flash('Area should not exceed 100 characters.')
                return redirect(url_for('main.register'))

            if not group or len(group) > 100:
                flash('Group should not exceed 100 characters.')
                return redirect(url_for('main.register'))

            if not department or len(department) > 100:
                flash('Department should not exceed 100 characters.')
                return redirect(url_for('main.register'))

            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country,
                area=area,
                group=group,
                department=department
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('User registered successfully!')
            logging.info(f'User registered: {email}')
            return redirect(url_for('main.login'))
        except Exception as e:
            logging.error(f'Error during user registration: {str(e)}')
            flash('An error occurred during registration. Please try again.')
            return redirect(url_for('main.register'))

    return render_template('register.html')


@main.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        try:
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.phone = request.form['phone']
            user.address = request.form['address']
            user.city = request.form['city']
            user.state = request.form['state']
            user.zip_code = request.form['zip_code']
            user.country = request.form['country']
            user.area = request.form['area']
            user.group = request.form['group']
            user.department = request.form['department']
            db.session.commit()
            flash('Profile updated successfully')
            logging.info(f'User updated profile: {user.email}')
            return redirect(url_for('main.profile', user_id=user.id))
        except Exception as e:
            logging.error(f'Error during profile update: {str(e)}')
            flash('An error occurred during profile update. Please try again.')
            return redirect(url_for('main.profile', user_id=user.id))
    return render_template('profile.html', user=user)


@main.route('/admin', methods=['GET'])
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)


@main.route('/admin/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully')
        logging.info(f'User deleted: {user.email}')
        return redirect(url_for('main.admin'))
    except Exception as e:
        logging.error(f'Error during user deletion: {str(e)}')
        flash('An error occurred during user deletion. Please try again.')
        return redirect(url_for('main.admin'))
