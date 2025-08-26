from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, ControlParameter, OptimizedMeasurement, ScheduledControl, ControlStage
from services.measurement_service import MeasurementService
from services.scheduling_service import SchedulingService
from datetime import date, datetime, time
import json

optimized_bp = Blueprint('optimized', __name__)

@optimized_bp.route('/dashboard')
@login_required
def dashboard():
    """Optimized dashboard showing scheduled controls and quick measurement entry"""
    
    # Get today's pending controls for current user
    current_shift = MeasurementService._determine_shift(datetime.now().time())
    pending_controls = MeasurementService.get_pending_controls(
        operator_name=current_user.username,
        shift=current_shift
    )
    
    # Get overdue controls
    overdue_controls = MeasurementService.get_overdue_controls()
    
    # Get schedule summary
    schedule_summary = SchedulingService.get_schedule_summary()
    
    # Recent measurements for current user
    recent_measurements = OptimizedMeasurement.query.filter_by(
        operator_name=current_user.username
    ).order_by(OptimizedMeasurement.created_at.desc()).limit(10).all()
    
    return render_template('optimized/dashboard.html',
                         pending_controls=pending_controls,
                         overdue_controls=overdue_controls,
                         schedule_summary=schedule_summary,
                         recent_measurements=recent_measurements,
                         current_shift=current_shift)

@optimized_bp.route('/quick-measurement', methods=['GET', 'POST'])
@login_required
def quick_measurement():
    """Quick single measurement entry"""
    
    if request.method == 'POST':
        parameter_id = request.form.get('parameter_id')
        measurement_data = {
            'value': request.form.get('value'),
            'format': request.form.get('format'),
            'line_number': request.form.get('line_number'),
            'oven_number': request.form.get('oven_number'),
            'press_number': request.form.get('press_number'),
            'sample_size': request.form.get('sample_size', 1),
            'observations': request.form.get('observations'),
            'defects': {}
        }
        
        # Handle visual defects
        parameter = ControlParameter.query.get(parameter_id)
        if parameter and parameter.control_type == 'visual':
            defects = {}
            for key, value in request.form.items():
                if key.startswith('defect_'):
                    defect_name = key.replace('defect_', '')
                    try:
                        defects[defect_name] = float(value) if value else 0
                    except ValueError:
                        defects[defect_name] = 0
            measurement_data['defects'] = defects
        
        # Record measurement
        result = MeasurementService.record_measurement(
            parameter_id, 
            current_user.username, 
            measurement_data
        )
        
        if result['success']:
            flash(f"Mesure enregistrée avec succès. Status: {'Conforme' if result['is_conforming'] else 'Non-conforme'}", 
                  'success' if result['is_conforming'] else 'warning')
            if result.get('nc_number'):
                flash(f"Numéro de non-conformité généré: {result['nc_number']}", 'info')
        else:
            flash(f"Erreur lors de l'enregistrement: {result['error']}", 'error')
        
        return redirect(url_for('optimized.quick_measurement'))
    
    # Get active parameters for dropdown
    parameters = ControlParameter.query.filter_by(active=True).join(ControlStage).order_by(
        ControlStage.order_sequence, ControlParameter.name
    ).all()
    
    return render_template('optimized/quick_measurement.html', parameters=parameters)

@optimized_bp.route('/bulk-measurement', methods=['GET', 'POST'])
@login_required
def bulk_measurement():
    """Bulk measurement entry for multiple parameters"""
    
    if request.method == 'POST':
        measurements_data = []
        
        # Parse form data for multiple measurements
        parameter_ids = request.form.getlist('parameter_ids[]')
        
        for i, parameter_id in enumerate(parameter_ids):
            if not parameter_id:
                continue
                
            measurement_data = {
                'parameter_id': parameter_id,
                'operator_name': current_user.username,
                'value': request.form.get(f'values[{i}]'),
                'format': request.form.get(f'formats[{i}]'),
                'line_number': request.form.get(f'line_numbers[{i}]'),
                'observations': request.form.get(f'observations[{i}]'),
                'sample_size': request.form.get(f'sample_sizes[{i}]', 1)
            }
            
            # Handle defects for visual controls
            parameter = ControlParameter.query.get(parameter_id)
            if parameter and parameter.control_type == 'visual':
                defects = {}
                defect_keys = ['grains', 'cracks', 'cleaning', 'foliage', 'chipping']
                for defect in defect_keys:
                    value = request.form.get(f'defects[{i}][{defect}]')
                    defects[defect] = float(value) if value else 0
                measurement_data['defects'] = defects
            
            measurements_data.append(measurement_data)
        
        # Record bulk measurements
        result = MeasurementService.record_bulk_measurements(measurements_data)
        
        if result['success']:
            flash(f"Enregistrement terminé: {result['successful']}/{result['total_processed']} mesures réussies", 'success')
            if result['failed'] > 0:
                flash(f"{result['failed']} mesures ont échoué", 'warning')
        else:
            flash(f"Erreur lors de l'enregistrement: {result['error']}", 'error')
        
        return redirect(url_for('optimized.bulk_measurement'))
    
    # Get scheduled controls for today
    today_controls = SchedulingService.get_daily_schedule()
    
    # Group by stage for better organization
    controls_by_stage = {}
    for control in today_controls:
        stage_name = control.parameter.stage.name
        if stage_name not in controls_by_stage:
            controls_by_stage[stage_name] = []
        controls_by_stage[stage_name].append(control)
    
    return render_template('optimized/bulk_measurement.html', 
                         controls_by_stage=controls_by_stage)

@optimized_bp.route('/scheduled-controls')
@login_required
def scheduled_controls():
    """View scheduled controls with filtering options"""
    
    target_date = request.args.get('date')
    shift = request.args.get('shift')
    
    if target_date:
        try:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()
    
    # Get scheduled controls
    controls = SchedulingService.get_daily_schedule(target_date, shift)
    
    # Get schedule summary
    summary = SchedulingService.get_schedule_summary(target_date)
    
    return render_template('optimized/scheduled_controls.html',
                         controls=controls,
                         summary=summary,
                         target_date=target_date,
                         selected_shift=shift)

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