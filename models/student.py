from . import db
from datetime import datetime

class Student(db.Model):
    """Student model"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    admission_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    class_name = db.Column('class', db.String(50), nullable=False)
    section = db.Column(db.String(10))
    parent_name = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    admission_date = db.Column(db.Date)
    photo = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendance = db.relationship('Attendance', back_populates='student', lazy=True, cascade='all, delete-orphan')
    fees = db.relationship('Fee', back_populates='student', lazy=True, cascade='all, delete-orphan')
    exams = db.relationship('Exam', back_populates='student', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.admission_number} - {self.name}>'
    
    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            'id': self.id,
            'admission_number': self.admission_number,
            'name': self.name,
            'class': self.class_name,
            'section': self.section,
            'parent_name': self.parent_name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'gender': self.gender,
            'admission_date': self.admission_date.strftime('%Y-%m-%d') if self.admission_date else None,
            'photo': self.photo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
