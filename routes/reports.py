from flask import Blueprint, render_template, request, flash, send_file
from routes.auth import login_required
from models import db, Student, Teacher, Attendance, Fee, Exam, SchoolClass
from datetime import date, datetime
from sqlalchemy import func
import io
import csv

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
@login_required
def reports_home():
    """Reports home page"""
    return render_template('reports/index.html')

@reports_bp.route('/reports/students')
@login_required
def student_report():
    """Generate student report"""
    class_filter = request.args.get('class', '')
    
    query = Student.query
    
    if class_filter:
        query = query.filter_by(class_name=class_filter)
    
    students = query.order_by(Student.class_name, Student.name).all()
    classes = db.session.query(Student.class_name).distinct().all()
    
    return render_template('reports/students.html', 
                         students=students, 
                         classes=classes,
                         class_filter=class_filter)

@reports_bp.route('/reports/attendance')
@login_required
def attendance_report():
    """Generate attendance report"""
    from_date = request.args.get('from_date', date.today().replace(day=1).strftime('%Y-%m-%d'))
    to_date = request.args.get('to_date', date.today().strftime('%Y-%m-%d'))
    class_filter = request.args.get('class', '')
    
    query = Attendance.query.filter(
        Attendance.date >= from_date,
        Attendance.date <= to_date
    )
    
    if class_filter:
        query = query.join(Student).filter(Student.class_name == class_filter)
    
    attendance = query.order_by(Attendance.date, Attendance.student_id).all()
    classes = db.session.query(Student.class_name).distinct().all()
    
    # Calculate statistics
    total_records = len(attendance)
    present_count = len([a for a in attendance if a.status == 'Present'])
    absent_count = len([a for a in attendance if a.status == 'Absent'])
    late_count = len([a for a in attendance if a.status == 'Late'])
    
    return render_template('reports/attendance.html',
                         attendance=attendance,
                         classes=classes,
                         from_date=from_date,
                         to_date=to_date,
                         class_filter=class_filter,
                         total_records=total_records,
                         present_count=present_count,
                         absent_count=absent_count,
                         late_count=late_count)

@reports_bp.route('/reports/fees')
@login_required
def fee_report():
    """Generate fee report"""
    status_filter = request.args.get('status', '')
    academic_year = request.args.get('academic_year', '')
    
    query = Fee.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if academic_year:
        query = query.filter_by(academic_year=academic_year)
    
    fees = query.order_by(Fee.academic_year, Fee.student_id).all()
    
    # Calculate totals
    total_fees = sum(f.total_fee for f in fees)
    total_paid = sum(f.paid_fee for f in fees)
    total_due = sum(f.due_fee for f in fees)
    
    return render_template('reports/fees.html',
                         fees=fees,
                         status_filter=status_filter,
                         academic_year=academic_year,
                         total_fees=total_fees,
                         total_paid=total_paid,
                         total_due=total_due)

@reports_bp.route('/reports/exams')
@login_required
def exam_report():
    """Generate exam report"""
    exam_name = request.args.get('exam_name', '')
    subject = request.args.get('subject', '')
    class_filter = request.args.get('class', '')
    
    query = Exam.query
    
    if exam_name:
        query = query.filter(Exam.exam_name.ilike(f'%{exam_name}%'))
    
    if subject:
        query = query.filter(Exam.subject.ilike(f'%{subject}%'))
    
    if class_filter:
        query = query.join(Student).filter(Student.class_name == class_filter)
    
    exams = query.order_by(Exam.exam_date, Exam.subject).all()
    
    # Calculate statistics
    total_exams = len(exams)
    avg_marks = sum(e.marks_obtained or 0 for e in exams) / total_exams if total_exams > 0 else 0
    
    return render_template('reports/exams.html',
                         exams=exams,
                         exam_name=exam_name,
                         subject=subject,
                         class_filter=class_filter,
                         total_exams=total_exams,
                         avg_marks=round(avg_marks, 2))

@reports_bp.route('/reports/export/<report_type>')
@login_required
def export_report(report_type):
    """Export report to CSV"""
    if report_type == 'students':
        records = Student.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Admission No', 'Name', 'Class', 'Section', 'Parent Name', 'Phone', 'Email'])
        for r in records:
            writer.writerow([r.admission_number, r.name, r.class_name, r.section, r.parent_name, r.phone, r.email])
    
    elif report_type == 'fees':
        records = Fee.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Student ID', 'Fee Type', 'Total Fee', 'Paid Fee', 'Due Fee', 'Status', 'Academic Year'])
        for r in records:
            writer.writerow([r.student_id, r.fee_type, r.total_fee, r.paid_fee, r.due_fee, r.status, r.academic_year])
    
    else:
        flash('Invalid report type', 'danger')
        return redirect(url_for('reports.reports_home'))
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'{report_type}_report_{date.today()}.csv'
    )
