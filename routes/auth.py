from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from models import User, Student, Teacher

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    """Decorator to require teacher role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'teacher':
            flash('Access denied. Teacher privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """Decorator to require student role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'student':
            flash('Access denied. Student privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route with role-based redirect"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        print("=================================")
        print("EMAIL ENTERED:", email)
        print("USER FOUND:", user)

        if user:
            print("DB EMAIL:", user.email)
            print("ROLE:", user.role)
            print("ACTIVE:", user.is_active)
            print("PASSWORD MATCH:", user.check_password(password))
        print("=================================")
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact administration.', 'danger')
                return render_template('login.html')
            
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash('Login successful!', 'success')
            
            if user.role == 'student':
                student = Student.query.filter_by(email=user.email).first()
                if student:
                    session['student_id'] = student.id
                else:
                    flash('Student record not found. Demo mode enabled.', 'warning')
            elif user.role == 'teacher':
                teacher = Teacher.query.filter_by(email=user.email).first()
                if teacher:
                    session['teacher_id'] = teacher.id
                else:
                    flash('Teacher record not found. Demo mode enabled.', 'warning')
            
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher.teacher_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student.student_dashboard'))
            else:
                return redirect(url_for('dashboard.dashboard_home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
