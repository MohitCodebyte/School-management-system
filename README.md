# School Management System

A modern, premium School ERP demo website built with Python Flask, MySQL, HTML5, CSS3, and Vanilla JavaScript. This system provides a comprehensive solution for managing students, teachers, attendance, fees, exams, and notices with a beautiful, professional UI inspired by modern SaaS products.

## Features

### Public Website
- **Hero Section** - Fullscreen with animated background blobs and statistics counter
- **About School** - Information about the institution
- **Why Choose Us** - Key features and benefits
- **Facilities** - Showcase of school infrastructure
- **School Gallery** - Visual gallery with hover effects
- **Academic Programs** - Information about different programs
- **Testimonials** - Parent and student reviews
- **School Achievements** - Awards and recognition
- **Admission Process** - Step-by-step admission guide
- **Contact Section** - Contact form and information
- **Footer** - Links and social media

### Admin Dashboard
- **Dashboard** - Overview with statistics cards, charts, and recent activities
- **Students** - Full CRUD operations with search and pagination
- **Teachers** - Manage teacher information
- **Attendance** - Mark and track student attendance
- **Fees** - Manage fee collection and payments
- **Exams** - Record exam results and grades
- **Notices** - Create and manage school notices
- **Reports** - Generate comprehensive reports

### Design Features
- **Glassmorphism** - Modern glass-like UI elements
- **Soft Shadows** - Professional depth effects
- **Gradient Backgrounds** - Beautiful color transitions
- **Animated Cards** - Smooth hover effects
- **Floating Elements** - Dynamic visual elements
- **Scroll Animations** - Intersection Observer API
- **Micro Interactions** - Subtle user feedback
- **Professional Typography** - Clean, readable fonts
- **Modern Spacing System** - Consistent layout
- **Responsive Design** - Mobile-first approach
- **60 FPS Animations** - Smooth performance

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Icons**: Bootstrap Icons
- **Charts**: Chart.js
- **Architecture**: Flask Blueprints, Jinja2 Templates

## Project Structure

```
school_management/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.sql                # Database schema and sample data
├── requirements.txt            # Python dependencies
│
├── models/                     # Database models
│   ├── __init__.py
│   ├── user.py
│   ├── student.py
│   ├── teacher.py
│   ├── class.py
│   ├── attendance.py
│   ├── fee.py
│   ├── exam.py
│   └── notice.py
│
├── routes/                     # Flask blueprints
│   ├── auth.py
│   ├── dashboard.py
│   ├── students.py
│   ├── teachers.py
│   ├── attendance.py
│   ├── fees.py
│   ├── exams.py
│   ├── notices.py
│   └── reports.py
│
├── static/                     # Static assets
│   ├── css/
│   │   ├── style.css
│   │   ├── dashboard.css
│   │   └── animations.css
│   ├── js/
│   │   ├── main.js
│   │   ├── dashboard.js
│   │   └── animations.js
│   └── images/
│
├── templates/                  # Jinja2 templates
│   ├── base.html
│   ├── index.html              # Landing page
│   ├── login.html              # Login page
│   ├── dashboard.html
│   ├── students/
│   │   ├── list.html
│   │   ├── add.html
│   │   ├── edit.html
│   │   └── profile.html
│   ├── teachers/
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── attendance/
│   │   └── list.html
│   ├── fees/
│   │   └── list.html
│   ├── exams/
│   │   └── list.html
│   ├── notices/
│   │   └── list.html
│   └── reports/
│       ├── index.html
│       ├── students.html
│       ├── attendance.html
│       ├── fees.html
│       └── exams.html
│
└── README.md                   # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd "d:/Intern Project/JUNE/School management system"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Setup MySQL Database

1. Open MySQL Workbench or Command Line
2. Run the database.sql file to create the database and tables:
```bash
mysql -u root -p < database.sql
```

Or manually execute the SQL commands in MySQL Workbench.

### Step 6: Configure Database Connection

Edit `config.py` to match your MySQL credentials:
```python
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'your_password'
DB_NAME = 'school_management_db'
```

### Step 7: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Demo Credentials

**Admin Login:**
- Email: `admin@school.com`
- Password: `123456`

## Usage

### Accessing the Application
1. Open your browser and navigate to `http://localhost:5000`
2. You'll see the beautiful landing page
3. Click "Login to Portal" to access the admin dashboard
4. Enter the demo credentials to log in

### Managing Students
- **View Students**: Navigate to Students section
- **Add Student**: Click "Add Student" button
- **Edit Student**: Click the edit icon on any student record
- **Delete Student**: Click the delete icon (with confirmation)
- **View Profile**: Click the eye icon to see detailed student information
- **Search**: Use the search bar to find students by name, admission number, or class

### Managing Teachers
- Similar CRUD operations as students
- Track subject specialization, qualification, and experience

### Attendance Management
- **Mark Attendance**: Select date and class, then mark students as Present/Absent/Late
- **View Records**: Filter by date and class
- **Generate Reports**: View attendance summaries with statistics

### Fee Management
- **Add Fee Records**: Record fee payments for students
- **Track Payments**: Monitor paid, pending, and partial payments
- **Collection Summary**: View overall fee collection statistics

### Exam Management
- **Record Results**: Add exam marks and grades
- **Automatic Grading**: System calculates grades based on marks
- **Performance Analysis**: View exam results and statistics

### Notice Management
- **Create Notices**: Add announcements for students, teachers, or parents
- **Set Priority**: Mark notices as High, Medium, or Low priority
- **Target Audience**: Specify who should see each notice

### Reports
- **Student Report**: Comprehensive student information
- **Attendance Report**: Attendance patterns and statistics
- **Fee Report**: Fee collection summaries
- **Exam Report**: Exam results and performance analysis
- **Export**: Download reports as CSV files

## Color Palette

- **Primary**: #2563EB
- **Secondary**: #3B82F6
- **Accent**: #06B6D4
- **Success**: #10B981
- **Warning**: #F59E0B
- **Danger**: #EF4444
- **Background**: #F8FAFC
- **Dark**: #0F172A
- **Cards**: #FFFFFF

## Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Laptop**: 1024px - 1440px
- **Desktop**: 1440px - 1920px
- **Ultra Wide**: > 1920px

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Optimizations

- Lazy loading for images
- Debounced search inputs
- Optimized database queries
- CSS animations with hardware acceleration
- Efficient JavaScript event handling

## Security Notes

This is a demo application. For production use:
- Implement proper password hashing (bcrypt/argon2)
- Add CSRF protection
- Implement role-based access control
- Add input validation and sanitization
- Use environment variables for sensitive data
- Enable HTTPS
- Add rate limiting
- Implement session management best practices

## Customization

### Changing the Color Scheme
Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary: #2563EB;
    --secondary: #3B82F6;
    /* ... other variables */
}
```

### Adding New Modules
1. Create a new model in `models/`
2. Create routes in `routes/`
3. Create templates in `templates/`
4. Register the blueprint in `app.py`

### Modifying the Landing Page
Edit `templates/index.html` to customize the public website sections.

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Verify credentials in `config.py`
- Check if the database exists

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility

### Template Not Found
- Verify the templates folder structure
- Check template file names match route references

## Development

### Running in Development Mode
```bash
python app.py
```

### Running in Production Mode
Set the environment variable:
```bash
set FLASK_ENV=production
python app.py
```

## License

This is a demo project for educational purposes.

## Credits

- **Design Inspiration**: Apple, Stripe, Linear, Framer, Notion
- **Icons**: Bootstrap Icons
- **Charts**: Chart.js
- **Framework**: Flask

## Support

For issues or questions, please refer to the code comments or contact the development team.

---

**Note**: This is a demonstration project. For production deployment, additional security measures and optimizations should be implemented.
