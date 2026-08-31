from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from routes.auth import login_required
from models import db, Student, User
from datetime import datetime

students_bp = Blueprint('students', __name__)

@students_bp.route('/students')
@login_required
def student_list():
    """List all students with pagination and search"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    
    query = Student.query
    
    if search:
        query = query.filter(
            (Student.name.ilike(f'%{search}%')) |
            (Student.admission_number.ilike(f'%{search}%')) |
            (Student.class_name.ilike(f'%{search}%'))
        )
    
    students = query.order_by(Student.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('students/list.html', students=students, search=search)

@students_bp.route('/students/add', methods=['GET', 'POST'])
@login_required
def student_add():
    """Add a new student"""
    if request.method == 'POST':
        try:
            # Get form data
            admission_number = request.form.get('admission_number')
            name = request.form.get('name')
            class_name = request.form.get('class')
            section = request.form.get('section')
            parent_name = request.form.get('parent_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validation
            if not admission_number or not name or not email or not password:
                flash('Admission number, name, email, and password are required.', 'danger')
                return render_template('students/add.html')
            
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('students/add.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'danger')
                return render_template('students/add.html')
            
            # Check if email already exists in users table
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists. Please use a different email.', 'danger')
                return render_template('students/add.html')
            
            # Create user account first
            user = User(
                name=name,
                email=email,
                role='student',
                is_active=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()  # Get the user ID before committing
            
            # Create student record
            student = Student(
                admission_number=admission_number,
                name=name,
                class_name=class_name,
                section=section,
                parent_name=parent_name,
                phone=phone,
                email=email,
                address=request.form.get('address'),
                date_of_birth=datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d') if request.form.get('date_of_birth') else None,
                gender=request.form.get('gender'),
                admission_date=datetime.strptime(request.form.get('admission_date'), '%Y-%m-%d') if request.form.get('admission_date') else None
            )
            
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully! Login account created.', 'success')
            return redirect(url_for('students.student_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'danger')
    
    return render_template('students/add.html')

@students_bp.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def student_edit(id):
    """Edit an existing student"""
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            student.admission_number = request.form.get('admission_number')
            student.name = request.form.get('name')
            student.class_name = request.form.get('class')
            student.section = request.form.get('section')
            student.parent_name = request.form.get('parent_name')
            student.phone = request.form.get('phone')
            student.email = request.form.get('email')
            student.address = request.form.get('address')
            student.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d') if request.form.get('date_of_birth') else None
            student.gender = request.form.get('gender')
            student.admission_date = datetime.strptime(request.form.get('admission_date'), '%Y-%m-%d') if request.form.get('admission_date') else None
            
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('students.student_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'danger')
    
    return render_template('students/edit.html', student=student)

@students_bp.route('/students/delete/<int:id>', methods=['POST'])
@login_required
def student_delete(id):
    """Delete a student"""
    student = Student.query.get_or_404(id)
    
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    
    return redirect(url_for('students.student_list'))

@students_bp.route('/students/profile/<int:id>')
@login_required
def student_profile(id):
    """View student profile"""
    student = Student.query.get_or_404(id)
    return render_template('students/profile.html', student=student)
