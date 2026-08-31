from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
from models import Attendance, Student, Teacher, SchoolClass
from datetime import date, datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance')
@login_required
def attendance_list():
    """List attendance records"""
    date_filter = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    class_filter = request.args.get('class_id', '')
    
    query = Attendance.query.filter_by(date=date_filter)
    
    if class_filter:
        query = query.filter_by(class_id=class_filter)
    
    attendance = query.order_by(Attendance.date.desc()).all()
    classes = SchoolClass.query.all()
    
    return render_template('attendance/list.html', 
                         attendance=attendance, 
                         classes=classes,
                         date_filter=date_filter,
                         class_filter=class_filter)

@attendance_bp.route('/attendance/mark', methods=['GET', 'POST'])
@login_required
def attendance_mark():
    """Mark attendance for students"""
    if request.method == 'POST':
        selected_date = request.form.get('date', date.today().strftime('%Y-%m-%d'))
        class_id = request.form.get('class_id')
        
        students = Student.query.filter_by(class_name=class_id).all() if class_id else Student.query.all()
        
        for student in students:
            status = request.form.get(f'status_{student.id}', 'Present')
            remarks = request.form.get(f'remarks_{student.id}', '')
            
            # Check if attendance already exists
            existing = Attendance.query.filter_by(
                student_id=student.id,
                date=datetime.strptime(selected_date, '%Y-%m-%d').date()
            ).first()
            
            if existing:
                existing.status = status
                existing.remarks = remarks
            else:
                attendance = Attendance(
                    student_id=student.id,
                    class_id=int(class_id) if class_id else None,
                    date=datetime.strptime(selected_date, '%Y-%m-%d').date(),
                    status=status,
                    remarks=remarks
                )
                db.session.add(attendance)
        
        try:
            db.session.commit()
            flash('Attendance marked successfully!', 'success')
            return redirect(url_for('attendance.attendance_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error marking attendance: {str(e)}', 'danger')
    
    classes = SchoolClass.query.all()
    students = Student.query.all()
    
    return render_template('attendance/mark.html', 
                         classes=classes, 
                         students=students,
                         today=date.today().strftime('%Y-%m-%d'))

@attendance_bp.route('/attendance/report')
@login_required
def attendance_report():
    """Generate attendance report"""
    from_date = request.args.get('from_date', date.today().replace(day=1).strftime('%Y-%m-%d'))
    to_date = request.args.get('to_date', date.today().strftime('%Y-%m-%d'))
    student_id = request.args.get('student_id', '')
    
    query = Attendance.query.filter(
        Attendance.date >= from_date,
        Attendance.date <= to_date
    )
    
    if student_id:
        query = query.filter_by(student_id=student_id)
    
    attendance = query.order_by(Attendance.date.desc()).all()
    students = Student.query.all()
    
    # Calculate attendance percentage
    total_days = len(set(a.date for a in attendance))
    present_days = len([a for a in attendance if a.status == 'Present'])
    percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    return render_template('attendance/report.html',
                         attendance=attendance,
                         students=students,
                         from_date=from_date,
                         to_date=to_date,
                         student_id=student_id,
                         present_days=present_days,
                         total_days=total_days,
                         percentage=round(percentage, 2))
