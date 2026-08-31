from . import db
from datetime import datetime

class Notification(db.Model):
    """Notification model for centralized messaging system"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender_role = db.Column(db.Enum('admin', 'teacher', 'student'), nullable=False)
    target_role = db.Column(db.Enum('admin', 'teacher', 'student', 'all'), nullable=False)
    target_class = db.Column(db.String(50))  # For teacher targeting specific class
    target_section = db.Column(db.String(10))  # For teacher targeting specific section
    is_active = db.Column(db.Boolean, default=True)
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', back_populates='notifications_created')
    
    def __repr__(self):
        return f'<Notification {self.title} - {self.sender_role}>'
    
    def to_dict(self):
        """Convert notification object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'created_by': self.created_by,
            'sender_role': self.sender_role,
            'target_role': self.target_role,
            'target_class': self.target_class,
            'target_section': self.target_section,
            'is_active': self.is_active,
            'is_pinned': self.is_pinned,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
