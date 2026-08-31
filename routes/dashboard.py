from flask import Blueprint, render_template, session
from routes.auth import login_required
from models import db, Student, Teacher, SchoolClass, Attendance, Fee, Exam, Notice
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard_home():
    """Dashboard home route"""
    # Get statistics
    total_students = Student.query.count()
    total_teachers = Teacher.query.count()
    total_classes = SchoolClass.query.count()
    
    # Today's attendance
    from datetime import date
    today = date.today()
    today_attendance = Attendance.query.filter_by(date=today).count()
    
    # Collected fees (sum of paid fees)
    collected_fees = db.session.query(func.sum(Fee.paid_fee)).scalar() or 0
    
    # Upcoming exams (exams with future dates)
    upcoming_exams = Exam.query.filter(Exam.exam_date >= today).count()
    
    # Recent activities (last 5 notices)
    recent_notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()
    
    # Get recent students
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    
    # Get attendance data for chart (last 7 days)
    from datetime import timedelta
    attendance_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        present_count = Attendance.query.filter_by(date=day, status='Present').count()
        absent_count = Attendance.query.filter_by(date=day, status='Absent').count()
        attendance_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'present': present_count,
            'absent': absent_count
        })
    
    return render_template('dashboard.html',
                         total_students=total_students,
                         total_teachers=total_teachers,
                         total_classes=total_classes,
                         today_attendance=today_attendance,
                         collected_fees=collected_fees,
                         upcoming_exams=upcoming_exams,
                         recent_notices=recent_notices,
                         recent_students=recent_students,
                         attendance_data=attendance_data)
