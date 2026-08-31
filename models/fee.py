from . import db
from datetime import datetime

class Fee(db.Model):
    """Fee model"""
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    fee_type = db.Column(db.String(100), nullable=False)
    total_fee = db.Column(db.DECIMAL(10, 2), nullable=False)
    paid_fee = db.Column(db.DECIMAL(10, 2), default=0.00)
    due_fee = db.Column(db.DECIMAL(10, 2), nullable=False)
    payment_date = db.Column(db.Date)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.Enum('Paid', 'Pending', 'Partial'), default='Pending')
    academic_year = db.Column(db.String(20))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', back_populates='fees')
    
    def __repr__(self):
        return f'<Fee Student {self.student_id} - {self.fee_type} - {self.status}>'
    
    def to_dict(self):
        """Convert fee object to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'fee_type': self.fee_type,
            'total_fee': float(self.total_fee),
            'paid_fee': float(self.paid_fee),
            'due_fee': float(self.due_fee),
            'payment_date': self.payment_date.strftime('%Y-%m-%d') if self.payment_date else None,
            'payment_method': self.payment_method,
            'status': self.status,
            'academic_year': self.academic_year,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
