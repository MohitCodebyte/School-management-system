from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
from models import db, Fee, Student
from datetime import datetime

fees_bp = Blueprint('fees', __name__)

@fees_bp.route('/fees')
@login_required
def fee_list():
    """List all fee records"""
    status_filter = request.args.get('status', '')
    student_filter = request.args.get('student_id', '')
    
    query = Fee.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if student_filter:
        query = query.filter_by(student_id=student_filter)
    
    fees = query.order_by(Fee.created_at.desc()).all()
    students = Student.query.all()
    
    return render_template('fees/list.html', fees=fees, students=students, 
                         status_filter=status_filter, student_filter=student_filter)

@fees_bp.route('/fees/add', methods=['GET', 'POST'])
@login_required
def fee_add():
    """Add a new fee record"""
    if request.method == 'POST':
        try:
            total_fee = float(request.form.get('total_fee'))
            paid_fee = float(request.form.get('paid_fee', 0))
            due_fee = total_fee - paid_fee
            
            status = 'Paid' if due_fee == 0 else ('Partial' if paid_fee > 0 else 'Pending')
            
            fee = Fee(
                student_id=int(request.form.get('student_id')),
                fee_type=request.form.get('fee_type'),
                total_fee=total_fee,
                paid_fee=paid_fee,
                due_fee=due_fee,
                payment_date=datetime.strptime(request.form.get('payment_date'), '%Y-%m-%d') if request.form.get('payment_date') else None,
                payment_method=request.form.get('payment_method'),
                status=status,
                academic_year=request.form.get('academic_year')
            )
            
            db.session.add(fee)
            db.session.commit()
            flash('Fee record added successfully!', 'success')
            return redirect(url_for('fees.fee_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding fee record: {str(e)}', 'danger')
    
    students = Student.query.all()
    return render_template('fees/add.html', students=students)

@fees_bp.route('/fees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def fee_edit(id):
    """Edit an existing fee record"""
    fee = Fee.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            total_fee = float(request.form.get('total_fee'))
            paid_fee = float(request.form.get('paid_fee', 0))
            due_fee = total_fee - paid_fee
            
            status = 'Paid' if due_fee == 0 else ('Partial' if paid_fee > 0 else 'Pending')
            
            fee.student_id = int(request.form.get('student_id'))
            fee.fee_type = request.form.get('fee_type')
            fee.total_fee = total_fee
            fee.paid_fee = paid_fee
            fee.due_fee = due_fee
            fee.payment_date = datetime.strptime(request.form.get('payment_date'), '%Y-%m-%d') if request.form.get('payment_date') else None
            fee.payment_method = request.form.get('payment_method')
            fee.status = status
            fee.academic_year = request.form.get('academic_year')
            
            db.session.commit()
            flash('Fee record updated successfully!', 'success')
            return redirect(url_for('fees.fee_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating fee record: {str(e)}', 'danger')
    
    students = Student.query.all()
    return render_template('fees/edit.html', fee=fee, students=students)

@fees_bp.route('/fees/delete/<int:id>', methods=['POST'])
@login_required
def fee_delete(id):
    """Delete a fee record"""
    fee = Fee.query.get_or_404(id)
    
    try:
        db.session.delete(fee)
        db.session.commit()
        flash('Fee record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting fee record: {str(e)}', 'danger')
    
    return redirect(url_for('fees.fee_list'))

@fees_bp.route('/fees/collection')
@login_required
def fee_collection():
    """View fee collection summary"""
    from sqlalchemy import func
    
    total_collected = db.session.query(func.sum(Fee.paid_fee)).scalar() or 0
    total_pending = db.session.query(func.sum(Fee.due_fee)).scalar() or 0
    total_fees = db.session.query(func.sum(Fee.total_fee)).scalar() or 0
    
    # Collection by academic year
    collection_by_year = db.session.query(
        Fee.academic_year,
        func.sum(Fee.paid_fee).label('collected')
    ).group_by(Fee.academic_year).all()
    
    return render_template('fees/collection.html',
                         total_collected=total_collected,
                         total_pending=total_pending,
                         total_fees=total_fees,
                         collection_by_year=collection_by_year)
