from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, ControlParameter, OptimizedMeasurement, ScheduledControl, ControlStage
from services.measurement_service import MeasurementService
from services.scheduling_service import SchedulingService
from datetime import date, datetime, time
import json

optimized_bp = Blueprint('optimized', __name__)

# @optimized_bp.route('/dashboard')
# @login_required
# def dashboard():
#     """Optimized dashboard showing scheduled controls and quick measurement entry"""
#     return redirect(url_for('main.dashboard'))

# @optimized_bp.route('/quick-measurement', methods=['GET', 'POST'])
# @login_required
# def quick_measurement():
#     """Quick single measurement entry"""
#     return redirect(url_for('main.dashboard'))

# @optimized_bp.route('/bulk-measurement', methods=['GET', 'POST'])
# @login_required
# def bulk_measurement():
#     """Bulk measurement entry for multiple parameters"""
#     return redirect(url_for('main.dashboard'))

# @optimized_bp.route('/scheduled-controls')
# @login_required
# def scheduled_controls():
#     """View scheduled controls with filtering options"""
#     return redirect(url_for('main.dashboard'))

@optimized_bp.route('/api/record-measurement', methods=['POST'])
@login_required
def api_record_measurement():
    """API endpoint for recording measurements via AJAX"""
    
    try:
        data = request.get_json()
        parameter_id = data.get('parameter_id')
        measurement_data = data.get('measurement_data', {})
        
        result = MeasurementService.record_measurement(
            parameter_id,
            current_user.username,
            measurement_data
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@optimized_bp.route('/api/get-parameter-details/<int:parameter_id>')
@login_required
def api_get_parameter_details(parameter_id):
    """API endpoint to get parameter details for dynamic forms"""
    
    parameter = ControlParameter.query.get_or_404(parameter_id)
    
    return jsonify({
        'id': parameter.id,
        'code': parameter.code,
        'name': parameter.name,
        'specification': parameter.specification,
        'unit': parameter.unit,
        'control_type': parameter.control_type,
        'min_value': float(parameter.min_value) if parameter.min_value else None,
        'max_value': float(parameter.max_value) if parameter.max_value else None,
        'target_value': float(parameter.target_value) if parameter.target_value else None,
        'defect_categories': parameter.defect_categories,
        'formats': parameter.formats
    })

@optimized_bp.route('/api/assign-operator', methods=['POST'])
@login_required
def api_assign_operator():
    """API endpoint to assign operator to scheduled controls"""
    
    if current_user.role not in ['quality_manager', 'admin']:
        return jsonify({'success': False, 'error': 'Permission denied'}), 403
    
    try:
        data = request.get_json()
        control_ids = data.get('control_ids', [])
        operator_name = data.get('operator_name')
        
        updated_count = SchedulingService.assign_operator_to_controls(control_ids, operator_name)
        
        return jsonify({
            'success': True,
            'updated_count': updated_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@optimized_bp.route('/generate-schedule', methods=['POST'])
@login_required
def generate_schedule():
    """Generate tomorrow's schedule (admin/quality manager only)"""
    
    if current_user.role not in ['quality_manager', 'admin']:
        flash('Permission denied', 'error')
        return redirect(url_for('optimized.dashboard'))
    
    try:
        target_date = request.form.get('target_date')
        if target_date:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        else:
            target_date = None
        
        result = SchedulingService.generate_daily_schedule(target_date)
        
        if result['success']:
            flash(f"Planning généré pour {result['date']}: {result['scheduled_count']} contrôles programmés", 'success')
        else:
            flash('Erreur lors de la génération du planning', 'error')
            
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    
    return redirect(url_for('optimized.scheduled_controls'))

@optimized_bp.route('/initialize-parameters', methods=['POST'])
@login_required
def initialize_parameters():
    """Initialize default control parameters (admin only)"""
    
    if current_user.role != 'admin':
        flash('Permission denied', 'error')
        return redirect(url_for('optimized.dashboard'))
    
    try:
        result = SchedulingService.initialize_default_parameters()
        
        if result['success']:
            flash(f"Paramètres initialisés: {result['stages_created']} étapes, {result['parameters_created']} paramètres", 'success')
        else:
            flash('Erreur lors de l\'initialisation', 'error')
            
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    
    return redirect(url_for('optimized.dashboard'))