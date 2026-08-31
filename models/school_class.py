from . import db
from datetime import datetime

class SchoolClass(db.Model):
    """SchoolClass model"""
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(10))
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='SET NULL'))
    room_number = db.Column(db.String(20))
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    class_teacher = db.relationship('Teacher', back_populates='classes_taught', lazy=True)
    attendance_records = db.relationship('Attendance', back_populates='class_info', lazy=True)
    
    def __repr__(self):
        return f'<SchoolClass {self.class_name} - {self.section}>'
    
    def to_dict(self):
        """Convert class object to dictionary"""
        return {
            'id': self.id,
            'class_name': self.class_name,
            'section': self.section,
            'class_teacher_id': self.class_teacher_id,
            'room_number': self.room_number,
            'capacity': self.capacity,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
