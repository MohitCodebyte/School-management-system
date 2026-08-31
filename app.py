from flask import Flask, render_template, redirect, url_for, session
from config import config
from models import db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.students import students_bp
from routes.teachers import teachers_bp
from routes.attendance import attendance_bp
from routes.fees import fees_bp
from routes.exams import exams_bp
from routes.notices import notices_bp
from routes.reports import reports_bp
from routes.notifications import notifications_bp
from routes.admin import admin_bp
from routes.teacher import teacher_bp
from routes.student import student_bp
import sqlalchemy

def validate_database_schema(app):
    """Validate database schema on startup"""
    with app.app_context():
        try:
            inspector = sqlalchemy.inspect(db.engine)
            
            # Check if students table exists
            if 'students' not in inspector.get_table_names():
                print("ERROR: 'students' table does not exist in database")
                print("Please run the database.sql script to create the database schema")
                return False
            
            # Check students table columns
            students_columns = [col['name'] for col in inspector.get_columns('students')]
            required_columns = ['id', 'admission_number', 'name', 'class', 'section', 'parent_name', 'phone', 'email', 'address', 'date_of_birth', 'gender', 'admission_date', 'photo', 'created_at', 'updated_at']
            
            missing_columns = [col for col in required_columns if col not in students_columns]
            if missing_columns:
                print(f"ERROR: Missing columns in 'students' table: {missing_columns}")
                print(f"Current columns: {students_columns}")
                print("\nTo fix this, run the following SQL in your MySQL database:")
                for col in missing_columns:
                    if col == 'class':
                        print("ALTER TABLE students ADD COLUMN class VARCHAR(50) NOT NULL AFTER name;")
                    elif col == 'section':
                        print("ALTER TABLE students ADD COLUMN section VARCHAR(10) AFTER class;")
                    elif col == 'parent_name':
                        print("ALTER TABLE students ADD COLUMN parent_name VARCHAR(255) AFTER section;")
                    elif col == 'phone':
                        print("ALTER TABLE students ADD COLUMN phone VARCHAR(20) AFTER parent_name;")
                    elif col == 'email':
                        print("ALTER TABLE students ADD COLUMN email VARCHAR(255) AFTER phone;")
                    elif col == 'address':
                        print("ALTER TABLE students ADD COLUMN address TEXT AFTER email;")
                    elif col == 'date_of_birth':
                        print("ALTER TABLE students ADD COLUMN date_of_birth DATE AFTER address;")
                    elif col == 'gender':
                        print("ALTER TABLE students ADD COLUMN gender ENUM('Male', 'Female', 'Other') AFTER date_of_birth;")
                    elif col == 'admission_date':
                        print("ALTER TABLE students ADD COLUMN admission_date DATE AFTER gender;")
                    elif col == 'photo':
                        print("ALTER TABLE students ADD COLUMN photo VARCHAR(255) AFTER admission_date;")
                    elif col == 'created_at':
                        print("ALTER TABLE students ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER photo;")
                    elif col == 'updated_at':
                        print("ALTER TABLE students ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at;")
                return False
            
            # Check other required tables
            required_tables = ['users', 'teachers', 'classes', 'attendance', 'fees', 'exams', 'notices']
            existing_tables = inspector.get_table_names()
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                print(f"ERROR: Missing tables in database: {missing_tables}")
                print(f"Existing tables: {existing_tables}")
                print("\nPlease run the database.sql script to create all required tables")
                return False
            
            print("Database schema validation: PASSED")
            return True
            
        except Exception as e:
            print(f"ERROR: Database validation failed: {str(e)}")
            print("Please ensure your MySQL database is running and credentials are correct in config.py")
            return False

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(fees_bp)
    app.register_blueprint(exams_bp)
    app.register_blueprint(notices_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    
    # Validate database schema before creating tables
    with app.app_context():
        if not validate_database_schema(app):
            print("\nWARNING: Database schema validation failed.")
            print("Please fix the database schema issues before continuing.")
            print("The application will attempt to start, but may encounter errors.")
        
        # Create database tables
        try:
            db.create_all()
            print("Database tables created/verified successfully")
        except Exception as e:
            print(f"ERROR: Failed to create database tables: {str(e)}")
            print("Please ensure your MySQL database is running and credentials are correct in config.py")
    
    # Root route - redirect based on role or show landing page
    @app.route('/')
    def index():
        """Landing page or role-based redirect"""
        # If user is logged in, redirect to appropriate dashboard
        if 'user_id' in session:
            user_role = session.get('user_role')
            if user_role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user_role == 'teacher':
                return redirect(url_for('teacher.teacher_dashboard'))
            elif user_role == 'student':
                return redirect(url_for('student.student_dashboard'))
            else:
                return redirect(url_for('dashboard.dashboard_home'))
        
        # If not logged in, show landing page
        return render_template('index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
