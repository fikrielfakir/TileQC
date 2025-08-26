from models import db, ControlParameter, OptimizedMeasurement, ScheduledControl
from datetime import datetime, date, timedelta, time
import json

class MeasurementService:
    
    @staticmethod
    def record_measurement(parameter_id, operator_name, measurement_data):
        """Optimized method to record a measurement with automated conformity checking"""
        try:
            parameter = ControlParameter.query.get(parameter_id)
            if not parameter:
                raise ValueError("Parameter not found")
            
            # Determine shift based on current time
            current_time = datetime.now().time()
            shift = MeasurementService._determine_shift(current_time)
            
            # Create measurement record
            measurement = OptimizedMeasurement(
                parameter_id=parameter_id,
                operator_name=operator_name,
                measurement_date=measurement_data.get('date', date.today()),
                measurement_time=measurement_data.get('time', datetime.now().time()),
                shift=shift,
                format=measurement_data.get('format'),
                line_number=measurement_data.get('line_number'),
                oven_number=measurement_data.get('oven_number'),
                press_number=measurement_data.get('press_number'),
                sample_size=measurement_data.get('sample_size', 1),
                observations=measurement_data.get('observations')
            )
            
            # Handle different measurement types with automated validation
            if parameter.control_type == 'numeric':
                value = float(measurement_data.get('value', 0))
                measurement.numeric_value = value
                measurement.is_conforming = parameter.check_conformity(value)
                
                # Calculate deviation percentage
                if parameter.target_value:
                    deviation = ((value - float(parameter.target_value)) / float(parameter.target_value)) * 100
                    measurement.deviation_percentage = round(deviation, 2)
                    
            elif parameter.control_type == 'visual':
                defects = measurement_data.get('defects', {})
                measurement.json_values = defects
                
                # Check if all defects are within limits based on parameter specifications
                is_conforming = True
                defect_limits = parameter.defect_categories or {}
                
                for defect_name, percentage in defects.items():
                    limit = defect_limits.get(defect_name, 15)  # Default 15% limit
                    if percentage > limit:
                        is_conforming = False
                        break
                measurement.is_conforming = is_conforming
                
            elif parameter.control_type == 'boolean':
                measurement.boolean_value = measurement_data.get('value', False)
                measurement.is_conforming = measurement.boolean_value
                
            elif parameter.control_type == 'categorical':
                measurement.text_value = measurement_data.get('value')
                measurement.is_conforming = measurement_data.get('is_conforming', True)
            
            # Generate NC number if non-conforming
            if not measurement.is_conforming:
                measurement.nc_number = MeasurementService._generate_nc_number()
            
            db.session.add(measurement)
            
            # Update scheduled control if exists
            scheduled = ScheduledControl.query.filter_by(
                parameter_id=parameter_id,
                scheduled_date=measurement.measurement_date,
                status='pending'
            ).first()
            
            if scheduled:
                scheduled.status = 'completed'
                scheduled.completed_at = datetime.now()
                scheduled.measurement_id = measurement.id
            
            db.session.commit()
            
            return {
                'success': True,
                'measurement_id': measurement.id,
                'is_conforming': measurement.is_conforming,
                'nc_number': measurement.nc_number,
                'deviation_percentage': float(measurement.deviation_percentage) if measurement.deviation_percentage else None
            }
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def record_bulk_measurements(measurements_data):
        """Record multiple measurements efficiently in a single transaction"""
        results = []
        successful_count = 0
        
        try:
            for measurement_data in measurements_data:
                parameter_id = measurement_data.get('parameter_id')
                operator_name = measurement_data.get('operator_name')
                
                result = MeasurementService.record_measurement(
                    parameter_id, operator_name, measurement_data
                )
                
                results.append({
                    'parameter_id': parameter_id,
                    'result': result
                })
                
                if result.get('success'):
                    successful_count += 1
            
            return {
                'success': True,
                'total_processed': len(measurements_data),
                'successful': successful_count,
                'failed': len(measurements_data) - successful_count,
                'results': results
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'results': results
            }
    
    @staticmethod
    def _determine_shift(current_time):
        """Determine shift based on time"""
        if time(6, 0) <= current_time < time(14, 0):
            return '06H-14H'
        elif time(14, 0) <= current_time < time(22, 0):
            return '14H-22H'
        else:
            return '22H-06H'
    
    @staticmethod
    def _generate_nc_number():
        """Generate non-conformity number"""
        today = date.today()
        count = OptimizedMeasurement.query.filter(
            OptimizedMeasurement.measurement_date == today,
            OptimizedMeasurement.nc_number.isnot(None)
        ).count() + 1
        return f"NC-{today.strftime('%Y%m%d')}-{count:03d}"
    
    @staticmethod
    def get_pending_controls(operator_name=None, shift=None):
        """Get pending scheduled controls for an operator/shift"""
        query = ScheduledControl.query.filter_by(
            status='pending',
            scheduled_date=date.today()
        ).join(ControlParameter)
        
        if operator_name:
            query = query.filter(ScheduledControl.assigned_operator == operator_name)
        
        if shift:
            query = query.filter(ScheduledControl.shift == shift)
        
        return query.order_by(ScheduledControl.scheduled_time).all()
    
    @staticmethod
    def get_overdue_controls():
        """Get overdue controls that should be marked as overdue"""
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        
        # Find controls that are past their scheduled time today or from previous days
        overdue_query = ScheduledControl.query.filter(
            ScheduledControl.status == 'pending'
        ).filter(
            db.or_(
                ScheduledControl.scheduled_date < current_date,
                db.and_(
                    ScheduledControl.scheduled_date == current_date,
                    ScheduledControl.scheduled_time < current_time
                )
            )
        )
        
        return overdue_query.all()
    
    @staticmethod
    def mark_overdue_controls():
        """Mark overdue controls and return count"""
        overdue_controls = MeasurementService.get_overdue_controls()
        count = 0
        
        for control in overdue_controls:
            control.status = 'overdue'
            count += 1
        
        if count > 0:
            db.session.commit()
        
        return count