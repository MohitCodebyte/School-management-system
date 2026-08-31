from . import db
from datetime import datetime

class Exam(db.Model):
    """Exam model"""
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    marks_obtained = db.Column(db.DECIMAL(5, 2))
    total_marks = db.Column(db.DECIMAL(5, 2), nullable=False)
    grade = db.Column(db.String(10))
    exam_date = db.Column(db.Date)
    academic_year = db.Column(db.String(20))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', back_populates='exams')
    
    def __repr__(self):
        return f'<Exam {self.exam_name} - Student {self.student_id} - {self.subject}>'
    
    def to_dict(self):
        """Convert exam object to dictionary"""
        return {
            'id': self.id,
            'exam_name': self.exam_name,
            'student_id': self.student_id,
            'subject': self.subject,
            'marks_obtained': float(self.marks_obtained) if self.marks_obtained else None,
            'total_marks': float(self.total_marks),
            'grade': self.grade,
            'exam_date': self.exam_date.strftime('%Y-%m-%d') if self.exam_date else None,
            'academic_year': self.academic_year,
            'remarks': self.remarks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
