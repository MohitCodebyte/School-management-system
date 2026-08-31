from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
from models import db, Teacher, User
from datetime import datetime

teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/teachers')
@login_required
def teacher_list():
    """List all teachers"""
    teachers = Teacher.query.order_by(Teacher.created_at.desc()).all()
    return render_template('teachers/list.html', teachers=teachers)

@teachers_bp.route('/teachers/add', methods=['GET', 'POST'])
@login_required
def teacher_add():
    """Add a new teacher"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            subject = request.form.get('subject')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validation
            if not name or not email or not password:
                flash('Name, email, and password are required.', 'danger')
                return render_template('teachers/add.html')
            
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('teachers/add.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'danger')
                return render_template('teachers/add.html')
            
            # Check if email already exists in users table
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists. Please use a different email.', 'danger')
                return render_template('teachers/add.html')
            
            # Create user account first
            user = User(
                name=name,
                email=email,
                role='teacher',
                is_active=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()  # Get the user ID before committing
            
            # Create teacher record
            teacher = Teacher(
                name=name,
                subject=subject,
                qualification=request.form.get('qualification'),
                experience=int(request.form.get('experience', 0)),
                phone=phone,
                email=email,
                address=request.form.get('address'),
                date_of_birth=datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d') if request.form.get('date_of_birth') else None,
                gender=request.form.get('gender'),
                joining_date=datetime.strptime(request.form.get('joining_date'), '%Y-%m-%d') if request.form.get('joining_date') else None
            )
            
            db.session.add(teacher)
            db.session.commit()
            flash('Teacher added successfully! Login account created.', 'success')
            return redirect(url_for('teachers.teacher_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding teacher: {str(e)}', 'danger')
    
    return render_template('teachers/add.html')

@teachers_bp.route('/teachers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def teacher_edit(id):
    """Edit an existing teacher"""
    teacher = Teacher.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            teacher.name = request.form.get('name')
            teacher.subject = request.form.get('subject')
            teacher.qualification = request.form.get('qualification')
            teacher.experience = int(request.form.get('experience', 0))
            teacher.phone = request.form.get('phone')
            teacher.email = request.form.get('email')
            teacher.address = request.form.get('address')
            teacher.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d') if request.form.get('date_of_birth') else None
            teacher.gender = request.form.get('gender')
            teacher.joining_date = datetime.strptime(request.form.get('joining_date'), '%Y-%m-%d') if request.form.get('joining_date') else None
            
            db.session.commit()
            flash('Teacher updated successfully!', 'success')
            return redirect(url_for('teachers.teacher_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating teacher: {str(e)}', 'danger')
    
    return render_template('teachers/edit.html', teacher=teacher)

@teachers_bp.route('/teachers/delete/<int:id>', methods=['POST'])
@login_required
def teacher_delete(id):
    """Delete a teacher"""
    teacher = Teacher.query.get_or_404(id)
    
    try:
        db.session.delete(teacher)
        db.session.commit()
        flash('Teacher deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting teacher: {str(e)}', 'danger')
    
    return redirect(url_for('teachers.teacher_list'))
