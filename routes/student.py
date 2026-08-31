from flask import Blueprint, render_template, session
from routes.auth import student_required
from models import (
    Student,
    SchoolClass,
    Attendance,
    Fee,
    Exam,
    Notice,
    Notification
)

student_bp = Blueprint('student', __name__)


@student_bp.route('/student/dashboard')
@student_required
def student_dashboard():
    """Student dashboard"""
    student_id = session.get('student_id')
    student = Student.query.get(student_id) if student_id else None
    
    # Fallback to email-based lookup if student_id not found
    if not student and session.get('user_email'):
        student = Student.query.filter_by(email=session.get('user_email')).first()
        if student:
            session['student_id'] = student.id
    
    if not student:
        return render_template('student/dashboard.html', student=None)

    recent_attendance = Attendance.query.filter_by(
        student_id=student.id
    ).order_by(
        Attendance.date.desc()
    ).limit(5).all()

    student_fees = Fee.query.filter_by(
        student_id=student.id
    ).all()

    total_due = sum(float(fee.due_fee or 0) for fee in student_fees)
    total_paid = sum(float(fee.paid_fee or 0) for fee in student_fees)

    student_exams = Exam.query.filter_by(
        student_id=student.id
    ).order_by(
        Exam.exam_date.desc()
    ).limit(5).all()

    notifications = Notification.query.filter_by(
        is_active=True
    ).filter(
        (Notification.target_role == 'student') |
        (Notification.target_role == 'all')
    ).order_by(
        Notification.created_at.desc()
    ).limit(10).all()

    recent_notices = Notice.query.order_by(
        Notice.created_at.desc()
    ).limit(5).all()

    student_class = SchoolClass.query.filter_by(
        class_name=student.class_name,
        section=student.section
    ).first()

    return render_template(
        'student/dashboard.html',
        student=student,
        student_class=student_class,
        recent_attendance=recent_attendance,
        student_fees=student_fees,
        total_due=total_due,
        total_paid=total_paid,
        student_exams=student_exams,
        notifications=notifications,
        recent_notices=recent_notices
    )

@student_bp.route('/student/exams')
@student_required
def student_exams():
    """Student's exams page"""
    student_id = session.get('student_id')
    student = Student.query.get(student_id) if student_id else None
    
    # Fallback to email-based lookup if student_id not found
    if not student and session.get('user_email'):
        student = Student.query.filter_by(email=session.get('user_email')).first()
        if student:
            session['student_id'] = student.id
    
    if not student:
        return render_template('student/exams.html', exams=[], student=None)

    exams = Exam.query.filter_by(
        student_id=student.id
    ).order_by(
        Exam.exam_date.desc()
    ).all()

    return render_template(
        'student/exams.html',
        exams=exams,
        student=student
    )

@student_bp.route('/student/fees')
@student_required
def student_fees():
    """Student's fees page"""
    student_id = session.get('student_id')
    student = Student.query.get(student_id) if student_id else None
    
    # Fallback to email-based lookup if student_id not found
    if not student and session.get('user_email'):
        student = Student.query.filter_by(email=session.get('user_email')).first()
        if student:
            session['student_id'] = student.id
    
    if not student:
        return render_template('student/fees.html', fees=[], student=None)

    fees = Fee.query.filter_by(
        student_id=student.id
    ).all()

    return render_template(
        'student/fees.html',
        fees=fees,
        student=student
    )

@student_bp.route('/student/notices')
@student_required
def student_notices():
    """Student's notices page"""
    notices = Notice.query.order_by(
        Notice.created_at.desc()
    ).all()

    notifications = Notification.query.filter_by(
        is_active=True
    ).filter(
        (Notification.target_role == 'student') |
        (Notification.target_role == 'all')
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return render_template(
        'student/notices.html',
        notices=notices,
        notifications=notifications
    )