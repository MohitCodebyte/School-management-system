from . import db
from datetime import datetime

class Teacher(db.Model):
    """Teacher model"""
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255))
    qualification = db.Column(db.String(255))
    experience = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    joining_date = db.Column(db.Date)
    photo = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    classes_taught = db.relationship('SchoolClass', back_populates='class_teacher', lazy=True)
    
    def __repr__(self):
        return f'<Teacher {self.name} - {self.subject}>'
    
    def to_dict(self):
        """Convert teacher object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'subject': self.subject,
            'qualification': self.qualification,
            'experience': self.experience,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'gender': self.gender,
            'joining_date': self.joining_date.strftime('%Y-%m-%d') if self.joining_date else None,
            'photo': self.photo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
