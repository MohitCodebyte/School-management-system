from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
from models import db, Exam, Student
from datetime import datetime

exams_bp = Blueprint('exams', __name__)

@exams_bp.route('/exams')
@login_required
def exam_list():
    """List all exam records"""
    exam_filter = request.args.get('exam_name', '')
    student_filter = request.args.get('student_id', '')
    
    query = Exam.query
    
    if exam_filter:
        query = query.filter(Exam.exam_name.ilike(f'%{exam_filter}%'))
    
    if student_filter:
        query = query.filter_by(student_id=student_filter)
    
    exams = query.order_by(Exam.exam_date.desc()).all()
    students = Student.query.all()
    
    return render_template('exams/list.html', exams=exams, students=students,
                         exam_filter=exam_filter, student_filter=student_filter)

@exams_bp.route('/exams/add', methods=['GET', 'POST'])
@login_required
def exam_add():
    """Add a new exam record"""
    if request.method == 'POST':
        try:
            marks_obtained = float(request.form.get('marks_obtained')) if request.form.get('marks_obtained') else None
            total_marks = float(request.form.get('total_marks'))
            
            # Calculate grade
            grade = None
            if marks_obtained is not None:
                percentage = (marks_obtained / total_marks) * 100
                if percentage >= 90:
                    grade = 'A+'
                elif percentage >= 80:
                    grade = 'A'
                elif percentage >= 70:
                    grade = 'B+'
                elif percentage >= 60:
                    grade = 'B'
                elif percentage >= 50:
                    grade = 'C'
                else:
                    grade = 'F'
            
            exam = Exam(
                exam_name=request.form.get('exam_name'),
                student_id=int(request.form.get('student_id')),
                subject=request.form.get('subject'),
                marks_obtained=marks_obtained,
                total_marks=total_marks,
                grade=grade,
                exam_date=datetime.strptime(request.form.get('exam_date'), '%Y-%m-%d') if request.form.get('exam_date') else None,
                academic_year=request.form.get('academic_year'),
                remarks=request.form.get('remarks')
            )
            
            db.session.add(exam)
            db.session.commit()
            flash('Exam record added successfully!', 'success')
            return redirect(url_for('exams.exam_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding exam record: {str(e)}', 'danger')
    
    students = Student.query.all()
    return render_template('exams/add.html', students=students)

@exams_bp.route('/exams/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def exam_edit(id):
    """Edit an existing exam record"""
    exam = Exam.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            marks_obtained = float(request.form.get('marks_obtained')) if request.form.get('marks_obtained') else None
            total_marks = float(request.form.get('total_marks'))
            
            # Calculate grade
            grade = None
            if marks_obtained is not None:
                percentage = (marks_obtained / total_marks) * 100
                if percentage >= 90:
                    grade = 'A+'
                elif percentage >= 80:
                    grade = 'A'
                elif percentage >= 70:
                    grade = 'B+'
                elif percentage >= 60:
                    grade = 'B'
                elif percentage >= 50:
                    grade = 'C'
                else:
                    grade = 'F'
            
            exam.exam_name = request.form.get('exam_name')
            exam.student_id = int(request.form.get('student_id'))
            exam.subject = request.form.get('subject')
            exam.marks_obtained = marks_obtained
            exam.total_marks = total_marks
            exam.grade = grade
            exam.exam_date = datetime.strptime(request.form.get('exam_date'), '%Y-%m-%d') if request.form.get('exam_date') else None
            exam.academic_year = request.form.get('academic_year')
            exam.remarks = request.form.get('remarks')
            
            db.session.commit()
            flash('Exam record updated successfully!', 'success')
            return redirect(url_for('exams.exam_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating exam record: {str(e)}', 'danger')
    
    students = Student.query.all()
    return render_template('exams/edit.html', exam=exam, students=students)

@exams_bp.route('/exams/delete/<int:id>', methods=['POST'])
@login_required
def exam_delete(id):
    """Delete an exam record"""
    exam = Exam.query.get_or_404(id)
    
    try:
        db.session.delete(exam)
        db.session.commit()
        flash('Exam record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting exam record: {str(e)}', 'danger')
    
    return redirect(url_for('exams.exam_list'))

@exams_bp.route('/exams/results')
@login_required
def exam_results():
    """View exam results summary"""
    from sqlalchemy import func
    
    # Average marks by subject
    subject_avg = db.session.query(
        Exam.subject,
        func.avg(Exam.marks_obtained).label('avg_marks')
    ).group_by(Exam.subject).all()
    
    # Pass percentage
    total_exams = Exam.query.count()
    passed_exams = Exam.query.filter(Exam.grade.in_(['A+', 'A', 'B+', 'B', 'C'])).count()
    pass_percentage = (passed_exams / total_exams * 100) if total_exams > 0 else 0
    
    return render_template('exams/results.html',
                         subject_avg=subject_avg,
                         total_exams=total_exams,
                         passed_exams=passed_exams,
                         pass_percentage=round(pass_percentage, 2))
