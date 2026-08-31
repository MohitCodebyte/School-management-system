from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
from models import db, Notice
from datetime import datetime, date

notices_bp = Blueprint('notices', __name__)

@notices_bp.route('/notices')
@login_required
def notice_list():
    """List all notices"""
    priority_filter = request.args.get('priority', '')
    audience_filter = request.args.get('target_audience', '')
    
    query = Notice.query
    
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    
    if audience_filter:
        query = query.filter_by(target_audience=audience_filter)
    
    notices = query.order_by(Notice.date.desc()).all()
    
    return render_template('notices/list.html', notices=notices,
                         priority_filter=priority_filter, audience_filter=audience_filter)

@notices_bp.route('/notices/add', methods=['GET', 'POST'])
@login_required
def notice_add():
    """Add a new notice"""
    if request.method == 'POST':
        try:
            notice = Notice(
                title=request.form.get('title'),
                description=request.form.get('description'),
                date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
                target_audience=request.form.get('target_audience'),
                priority=request.form.get('priority'),
                created_by=1  # Will be set to current user in production
            )
            
            db.session.add(notice)
            db.session.commit()
            flash('Notice added successfully!', 'success')
            return redirect(url_for('notices.notice_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding notice: {str(e)}', 'danger')
    
    return render_template('notices/add.html')

@notices_bp.route('/notices/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def notice_edit(id):
    """Edit an existing notice"""
    notice = Notice.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            notice.title = request.form.get('title')
            notice.description = request.form.get('description')
            notice.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
            notice.target_audience = request.form.get('target_audience')
            notice.priority = request.form.get('priority')
            
            db.session.commit()
            flash('Notice updated successfully!', 'success')
            return redirect(url_for('notices.notice_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating notice: {str(e)}', 'danger')
    
    return render_template('notices/edit.html', notice=notice)

@notices_bp.route('/notices/delete/<int:id>', methods=['POST'])
@login_required
def notice_delete(id):
    """Delete a notice"""
    notice = Notice.query.get_or_404(id)
    
    try:
        db.session.delete(notice)
        db.session.commit()
        flash('Notice deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting notice: {str(e)}', 'danger')
    
    return redirect(url_for('notices.notice_list'))

@notices_bp.route('/notices/public')
def notice_public():
    """Public notices page (no login required)"""
    notices = Notice.query.filter(
        Notice.date >= date.today()
    ).order_by(Notice.date.asc()).limit(10).all()
    
    return render_template('notices/public.html', notices=notices)
