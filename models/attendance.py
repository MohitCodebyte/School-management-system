from . import db
from datetime import datetime

class Attendance(db.Model):
    """Attendance model"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='SET NULL'))
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Present', 'Absent', 'Late'), default='Present')
    remarks = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate attendance records
    __table_args__ = (db.UniqueConstraint('student_id', 'date', name='unique_attendance'),)
    
    # Relationships
    student = db.relationship('Student', back_populates='attendance')
    class_info = db.relationship('SchoolClass', back_populates='attendance_records')
    
    def __repr__(self):
        return f'<Attendance Student {self.student_id} - {self.date} - {self.status}>'
    
    def to_dict(self):
        """Convert attendance object to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'class_id': self.class_id,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'status': self.status,
            'remarks': self.remarks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
