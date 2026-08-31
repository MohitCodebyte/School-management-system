from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from routes.auth import login_required, admin_required, teacher_required, student_required
from models import db, Notification, User, Student

notifications_bp = Blueprint('notifications', __name__)

@login_required
def get_notifications_for_user():
    """Get notifications based on user role"""
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    
    # Base query
    query = Notification.query.filter_by(is_active=True)
    
    # Filter based on user role
    if user_role == 'student':
        # Students see notifications targeted to students or all
        query = query.filter(
            (Notification.target_role == 'student') | 
            (Notification.target_role == 'all')
        )
    elif user_role == 'teacher':
        # Teachers see notifications targeted to teachers or all
        query = query.filter(
            (Notification.target_role == 'teacher') | 
            (Notification.target_role == 'all')
        )
    elif user_role == 'admin':
        # Admins see all notifications
        query = query
    
    # Order by pinned first, then by created_at desc
    notifications = query.order_by(Notification.is_pinned.desc(), Notification.created_at.desc()).all()
    return notifications

@login_required
@notifications_bp.route('/notifications')
def notifications_list():
    """List all notifications for the current user"""
    notifications = get_notifications_for_user()
    return render_template('notifications/list.html', notifications=notifications)

@login_required
@notifications_bp.route('/notifications/api')
def notifications_api():
    """API endpoint to get notifications for AJAX calls"""
    notifications = get_notifications_for_user()
    return jsonify([n.to_dict() for n in notifications])

@admin_required
@notifications_bp.route('/notifications/create', methods=['GET', 'POST'])
def create_notification():
    """Create a new notification (Admin only)"""
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        target_role = request.form.get('target_role')
        target_class = request.form.get('target_class')
        target_section = request.form.get('target_section')
        is_pinned = request.form.get('is_pinned') == 'on'
        
        notification = Notification(
            title=title,
            message=message,
            created_by=session.get('user_id'),
            sender_role='admin',
            target_role=target_role,
            target_class=target_class if target_class else None,
            target_section=target_section if target_section else None,
            is_pinned=is_pinned
        )
        
        db.session.add(notification)
        db.session.commit()
        
        flash('Notification created successfully!', 'success')
        return redirect(url_for('notifications.notifications_list'))
    
    return render_template('notifications/create.html')

@teacher_required
@notifications_bp.route('/notifications/create-teacher', methods=['GET', 'POST'])
def create_teacher_notification():
    """Create a new notification (Teacher only)"""
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        target_role = request.form.get('target_role', 'student')  # Teachers can only send to students
        target_class = request.form.get('target_class')
        target_section = request.form.get('target_section')
        
        notification = Notification(
            title=title,
            message=message,
            created_by=session.get('user_id'),
            sender_role='teacher',
            target_role=target_role,
            target_class=target_class if target_class else None,
            target_section=target_section if target_section else None,
            is_pinned=False  # Teachers cannot pin notifications
        )
        
        db.session.add(notification)
        db.session.commit()
        
        flash('Notification created successfully!', 'success')
        return redirect(url_for('notifications.notifications_list'))
    
    # Get available classes for targeting
    from models import SchoolClass
    classes = SchoolClass.query.all()
    return render_template('notifications/create_teacher.html', classes=classes)

@login_required
@notifications_bp.route('/notifications/<int:id>/edit', methods=['GET', 'POST'])
def edit_notification(id):
    """Edit a notification"""
    notification = Notification.query.get_or_404(id)
    user_role = session.get('user_role')
    
    # Check permissions
    if user_role == 'student':
        flash('Students cannot edit notifications.', 'danger')
        return redirect(url_for('notifications.notifications_list'))
    
    if user_role == 'teacher' and notification.sender_role != 'teacher':
        flash('Teachers can only edit their own notifications.', 'danger')
        return redirect(url_for('notifications.notifications_list'))
    
    if request.method == 'POST':
        notification.title = request.form.get('title')
        notification.message = request.form.get('message')
        notification.target_role = request.form.get('target_role')
        notification.target_class = request.form.get('target_class') if request.form.get('target_class') else None
        notification.target_section = request.form.get('target_section') if request.form.get('target_section') else None
        
        if user_role == 'admin':
            notification.is_pinned = request.form.get('is_pinned') == 'on'
        
        db.session.commit()
        
        flash('Notification updated successfully!', 'success')
        return redirect(url_for('notifications.notifications_list'))
    
    return render_template('notifications/edit.html', notification=notification)

@login_required
@notifications_bp.route('/notifications/<int:id>/delete', methods=['POST'])
def delete_notification(id):
    """Delete a notification"""
    notification = Notification.query.get_or_404(id)
    user_role = session.get('user_role')
    
    # Check permissions
    if user_role == 'student':
        flash('Students cannot delete notifications.', 'danger')
        return redirect(url_for('notifications.notifications_list'))
    
    if user_role == 'teacher' and notification.sender_role != 'teacher':
        flash('Teachers can only delete their own notifications.', 'danger')
        return redirect(url_for('notifications.notifications_list'))
    
    # Soft delete by setting is_active to False
    notification.is_active = False
    db.session.commit()
    
    flash('Notification deleted successfully!', 'success')
    return redirect(url_for('notifications.notifications_list'))

@admin_required
@notifications_bp.route('/notifications/<int:id>/pin', methods=['POST'])
def pin_notification(id):
    """Pin/Unpin a notification (Admin only)"""
    notification = Notification.query.get_or_404(id)
    notification.is_pinned = not notification.is_pinned
    db.session.commit()
    
    status = 'pinned' if notification.is_pinned else 'unpinned'
    flash(f'Notification {status} successfully!', 'success')
    return redirect(url_for('notifications.notifications_list'))
