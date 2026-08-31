from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

# Import all models to ensure they're registered with SQLAlchemy
from .student import Student
from .teacher import Teacher
from .school_class import SchoolClass
from .attendance import Attendance
from .fee import Fee
from .exam import Exam
from .notice import Notice
from .user import User
from .notification import Notification

__all__ = ['db', 'Student', 'Teacher', 'SchoolClass', 'Attendance', 'Fee', 'Exam', 'Notice', 'User', 'Notification']
