from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from routes.auth import teacher_required, login_required
from models import db, Student, Teacher, SchoolClass, Attendance, Fee, Exam, Notice, Notification
from sqlalchemy import func
from datetime import date, datetime

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/teacher/dashboard')
@teacher_required
def teacher_dashboard():
    """Teacher dashboard with role-based access"""
    teacher_id = session.get('teacher_id')
    
    # Get teacher's assigned classes
    teacher_classes = SchoolClass.query.filter_by(class_teacher_id=teacher_id).all()
    
    # Get students in teacher's classes
    teacher_students = []

    for cls in teacher_classes:
        teacher_students.extend(
            Student.query.filter_by(
                class_name=cls.class_name,
                section=cls.section
            ).all()
        )

    teacher_students = list({s.id: s for s in teacher_students}.values())
    # Statistics
    total_students = len(teacher_students)
    total_classes = len(teacher_classes)
    
    # Today's attendance for teacher's students
    today = date.today()
    student_ids = [s.id for s in teacher_students]
    today_attendance = Attendance.query.filter(
        Attendance.student_id.in_(student_ids),
        Attendance.date == today
    ).count()
    
    # Calculate attendance percentage
    attendance_percentage = 0
    if total_students > 0:
        attendance_percentage = round((today_attendance / total_students) * 100, 1)
    
    # Recent notifications
    notifications = Notification.query.filter_by(is_active=True).filter(
        (Notification.target_role == 'teacher') | 
        (Notification.target_role == 'all')
    ).order_by(Notification.is_pinned.desc(), Notification.created_at.desc()).limit(5).all()
    
    # Upcoming exams for teacher's students
    upcoming_exams = Exam.query.filter(
        Exam.student_id.in_(student_ids),
        Exam.exam_date >= today
    ).order_by(Exam.exam_date).limit(5).all()
    
    # Recent notices
    recent_notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()
    
    return render_template('teacher/dashboard.html',
                         total_students=total_students,
                         total_classes=total_classes,
                         today_attendance=today_attendance,
                         attendance_percentage=attendance_percentage,
                         teacher_classes=teacher_classes,
                         teacher_students=teacher_students,
                         notifications=notifications,
                         upcoming_exams=upcoming_exams,
                         recent_notices=recent_notices)

@teacher_bp.route('/teacher/students')
@teacher_required
def teacher_students():
    """Teacher's students page"""
    teacher_id = session.get('teacher_id')
    
    # Get teacher's assigned classes
    teacher_classes = SchoolClass.query.filter_by(class_teacher_id=teacher_id).all()
    
    # Get students in teacher's classes
    teacher_students = []

    for cls in teacher_classes:
        teacher_students.extend(
            Student.query.filter_by(
                class_name=cls.class_name,
                section=cls.section
            ).all()
        )

    teacher_students = list({s.id: s for s in teacher_students}.values())
    
    return render_template('teacher/students.html', students=teacher_students)

@teacher_bp.route('/teacher/students/add', methods=['GET', 'POST'])
@teacher_required
def teacher_students_add():
    """Add student page"""
    if request.method == 'POST':
        # Get form data
        admission_number = request.form.get('admission_number')
        name = request.form.get('name')
        class_name = request.form.get('class_name')
        section = request.form.get('section')
        parent_name = request.form.get('parent_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        
        # Create new student
        new_student = Student(
            admission_number=admission_number,
            name=name,
            class_name=class_name,
            section=section,
            parent_name=parent_name,
            phone=phone,
            email=email,
            address=address,
            created_at=datetime.now()
        )
        
        db.session.add(new_student)
        db.session.commit()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('teacher.teacher_students'))
    
    return render_template('teacher/students_add.html')

@teacher_bp.route('/teacher/students/edit/<int:id>', methods=['GET', 'POST'])
@teacher_required
def teacher_students_edit(id):
    """Edit student page"""
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        # Update student
        student.name = request.form.get('name')
        student.class_name = request.form.get('class_name')
        student.section = request.form.get('section')
        student.parent_name = request.form.get('parent_name')
        student.phone = request.form.get('phone')
        student.email = request.form.get('email')
        student.address = request.form.get('address')
        
        db.session.commit()
        
        flash('Student updated successfully!', 'success')
        return redirect(url_for('teacher.teacher_students'))
    
    return render_template('teacher/students_edit.html', student=student)

@teacher_bp.route('/teacher/students/delete/<int:id>', methods=['POST'])
@teacher_required
def teacher_students_delete(id):
    """Delete student"""
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('teacher.teacher_students'))

@teacher_bp.route('/teacher/attendance')
@teacher_required
def teacher_attendance():
    """Teacher's attendance page"""
    teacher_id = session.get('teacher_id')
    
    # Get teacher's assigned classes
    teacher_classes = SchoolClass.query.filter_by(class_teacher_id=teacher_id).all()
    
    # Get students in teacher's classes
    teacher_students = []

    for cls in teacher_classes:
        teacher_students.extend(
            Student.query.filter_by(
                class_name=cls.class_name,
                section=cls.section
            ).all()
        )

    teacher_students = list({s.id: s for s in teacher_students}.values())
    
    # Get today's date
    today = date.today()
    
    # Get today's attendance records
    student_ids = [s.id for s in teacher_students]
    attendance_records = Attendance.query.filter(
        Attendance.student_id.in_(student_ids),
        Attendance.date == today
    ).all()
    
    # Create a dictionary of attendance status for each student
    attendance_status = {record.student_id: record.status for record in attendance_records}
    
    return render_template('teacher/attendance.html', 
                         students=teacher_students,
                         today=today,
                         attendance_status=attendance_status)

@teacher_bp.route('/teacher/attendance/mark', methods=['POST'])
@teacher_required
def teacher_attendance_mark():
    """Mark attendance for students"""
    teacher_id = session.get('teacher_id')
    
    # Get teacher's assigned classes
    teacher_classes = SchoolClass.query.filter_by(class_teacher_id=teacher_id).all()
    
    # Get students in teacher's classes
    teacher_students = []

    for cls in teacher_classes:
        teacher_students.extend(
            Student.query.filter_by(
                class_name=cls.class_name,
                section=cls.section
            ).all()
        )

    teacher_students = list({s.id: s for s in teacher_students}.values())
    
    # Get today's date
    today = date.today()
    
    # Get attendance data from form
    for student in teacher_students:
        status = request.form.get(f'status_{student.id}')
        
        if status:
            # Check if attendance record already exists
            existing_record = Attendance.query.filter_by(
                student_id=student.id,
                date=today
            ).first()
            
            if existing_record:
                # Update existing record
                existing_record.status = status
            else:
                # Create new attendance record
                new_attendance = Attendance(
                    student_id=student.id,
                    date=today,
                    status=status,
                    marked_by=teacher_id
                )
                db.session.add(new_attendance)
    
    db.session.commit()
    
    flash('Attendance marked successfully!', 'success')
    return redirect(url_for('teacher.teacher_attendance'))

@teacher_bp.route('/teacher/exams')
@teacher_required
def teacher_exams():
    """Teacher's exams page"""
    teacher_id = session.get('teacher_id')
    
    # Get teacher's assigned classes
    teacher_classes = SchoolClass.query.filter_by(class_teacher_id=teacher_id).all()
    
    # Get students in teacher's classes
    teacher_students = []

    for cls in teacher_classes:
        teacher_students.extend(
            Student.query.filter_by(
                class_name=cls.class_name,
                section=cls.section
            ).all()
        )

    teacher_students = list({s.id: s for s in teacher_students}.values())
    student_ids = [s.id for s in teacher_students]
    
    # Get exams for teacher's students
    exams = Exam.query.filter(
        Exam.student_id.in_(student_ids)
    ).order_by(Exam.exam_date.desc()).all()
    
    return render_template('teacher/exams.html', exams=exams, students=teacher_students)

@teacher_bp.route('/teacher/exams/add', methods=['GET', 'POST'])
@teacher_required
def teacher_exams_add():
    """Add exam page"""
    teacher_id = session.get('teacher_id')
    
    # Get teacher's assigned classes
    teacher_classes = SchoolClass.query.filter_by(class_teacher_id=teacher_id).all()
    
    # Get students in teacher's classes
    teacher_students = []

    for cls in teacher_classes:
        teacher_students.extend(
            Student.query.filter_by(
                class_name=cls.class_name,
                section=cls.section
            ).all()
        )

    teacher_students = list({s.id: s for s in teacher_students}.values())
    
    if request.method == 'POST':
        # Get form data
        exam_name = request.form.get('exam_name')
        subject = request.form.get('subject')
        exam_date = datetime.strptime(request.form.get('exam_date'), '%Y-%m-%d').date()
        total_marks = request.form.get('total_marks')
        student_id = request.form.get('student_id')
        
        # Create new exam
        new_exam = Exam(
            exam_name=exam_name,
            subject=subject,
            exam_date=exam_date,
            total_marks=total_marks,
            student_id=student_id,
            created_at=datetime.now()
        )
        
        db.session.add(new_exam)
        db.session.commit()
        
        flash('Exam added successfully!', 'success')
        return redirect(url_for('teacher.teacher_exams'))
    
    return render_template('teacher/exams_add.html', students=teacher_students)

@teacher_bp.route('/teacher/exams/edit/<int:id>', methods=['GET', 'POST'])
@teacher_required
def teacher_exams_edit(id):
    """Edit exam page"""
    exam = Exam.query.get_or_404(id)
    
    teacher_id = session.get('teacher_id')
    
    # Get teacher's assigned classes
    teacher_classes = SchoolClass.query.filter_by(class_teacher_id=teacher_id).all()
    
    # Get students in teacher's classes
    teacher_students = []

    for cls in teacher_classes:
        teacher_students.extend(
            Student.query.filter_by(
                class_name=cls.class_name,
                section=cls.section
            ).all()
        )

    teacher_students = list({s.id: s for s in teacher_students}.values())
    
    if request.method == 'POST':
        # Update exam
        exam.exam_name = request.form.get('exam_name')
        exam.subject = request.form.get('subject')
        exam.exam_date = datetime.strptime(request.form.get('exam_date'), '%Y-%m-%d').date()
        exam.total_marks = request.form.get('total_marks')
        exam.student_id = request.form.get('student_id')
        
        db.session.commit()
        
        flash('Exam updated successfully!', 'success')
        return redirect(url_for('teacher.teacher_exams'))
    
    return render_template('teacher/exams_edit.html', exam=exam, students=teacher_students)

@teacher_bp.route('/teacher/exams/delete/<int:id>', methods=['POST'])
@teacher_required
def teacher_exams_delete(id):
    """Delete exam"""
    exam = Exam.query.get_or_404(id)
    db.session.delete(exam)
    db.session.commit()
    
    flash('Exam deleted successfully!', 'success')
    return redirect(url_for('teacher.teacher_exams'))

@teacher_bp.route('/teacher/notices')
@teacher_required
def teacher_notices():
    """Teacher's notices page"""
    # Get notices created by teacher
    teacher_id = session.get('teacher_id')
    notices = Notice.query.filter_by(created_by=teacher_id).order_by(Notice.created_at.desc()).all()
    
    return render_template('teacher/notices.html', notices=notices)

@teacher_bp.route('/teacher/notices/add', methods=['GET', 'POST'])
@teacher_required
def teacher_notices_add():
    """Add notice page"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        target_audience = request.form.get('target_audience')
        
        teacher_id = session.get('teacher_id')
        
        # Create new notice
        new_notice = Notice(
            title=title,
            description=description,
            target_audience=target_audience,
            created_by=teacher_id,
            created_at=datetime.now()
        )
        
        db.session.add(new_notice)
        db.session.commit()
        
        flash('Notice created successfully!', 'success')
        return redirect(url_for('teacher.teacher_notices'))
    
    return render_template('teacher/notices_add.html')

@teacher_bp.route('/teacher/notices/edit/<int:id>', methods=['GET', 'POST'])
@teacher_required
def teacher_notices_edit(id):
    """Edit notice page"""
    notice = Notice.query.get_or_404(id)
    
    if request.method == 'POST':
        # Update notice
        notice.title = request.form.get('title')
        notice.description = request.form.get('description')
        notice.target_audience = request.form.get('target_audience')
        
        db.session.commit()
        
        flash('Notice updated successfully!', 'success')
        return redirect(url_for('teacher.teacher_notices'))
    
    return render_template('teacher/notices_edit.html', notice=notice)

@teacher_bp.route('/teacher/notices/delete/<int:id>', methods=['POST'])
@teacher_required
def teacher_notices_delete(id):
    """Delete notice"""
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    
    flash('Notice deleted successfully!', 'success')
    return redirect(url_for('teacher.teacher_notices'))

@teacher_bp.route('/teacher/reports')
@teacher_required
def teacher_reports():
    """Teacher's reports page"""
    teacher_id = session.get('teacher_id')
    
    # Get teacher's assigned classes
    teacher_classes = SchoolClass.query.filter_by(class_teacher_id=teacher_id).all()
    
    # Get students in teacher's classes
    teacher_students = []

    for cls in teacher_classes:
        teacher_students.extend(
            Student.query.filter_by(
                class_name=cls.class_name,
                section=cls.section
            ).all()
        )

    teacher_students = list({s.id: s for s in teacher_students}.values())
    student_ids = [s.id for s in teacher_students]
    
    # Calculate attendance summary
    from datetime import date, timedelta
    today = date.today()
    last_30_days = today - timedelta(days=30)
    
    attendance_records = Attendance.query.filter(
        Attendance.student_id.in_(student_ids),
        Attendance.date >= last_30_days
    ).all()
    
    total_attendance_records = len(attendance_records)
    present_count = len([r for r in attendance_records if r.status == 'present'])
    absent_count = len([r for r in attendance_records if r.status == 'absent'])
    late_count = len([r for r in attendance_records if r.status == 'late'])
    
    # Get exam summary
    exams = Exam.query.filter(
        Exam.student_id.in_(student_ids)
    ).all()
    
    total_exams = len(exams)
    
    # Calculate average marks
    total_marks_obtained = sum([exam.marks_obtained for exam in exams if exam.marks_obtained])
    total_total_marks = sum([exam.total_marks for exam in exams if exam.total_marks])
    
    average_percentage = 0
    if total_total_marks > 0:
        average_percentage = round((total_marks_obtained / total_total_marks) * 100, 1)
    
    return render_template('teacher/reports.html',
                         total_students=len(teacher_students),
                         total_classes=len(teacher_classes),
                         total_attendance_records=total_attendance_records,
                         present_count=present_count,
                         absent_count=absent_count,
                         late_count=late_count,
                         total_exams=total_exams,
                         average_percentage=average_percentage)
