from . import db
from datetime import datetime

class Notice(db.Model):
    """Notice model"""
    __tablename__ = 'notices'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    target_audience = db.Column(db.Enum('All', 'Students', 'Teachers', 'Parents'), default='All')
    priority = db.Column(db.Enum('Low', 'Medium', 'High'), default='Medium')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', back_populates='notices_created')
    
    def __repr__(self):
        return f'<Notice {self.title} - {self.date}>'
    
    def to_dict(self):
        """Convert notice object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'target_audience': self.target_audience,
            'priority': self.priority,
            'created_by': self.created_by,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
