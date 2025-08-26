from models import db, ControlParameter, ScheduledControl, ControlStage
from datetime import datetime, date, timedelta, time
import random

class SchedulingService:
    
    @staticmethod
    def generate_daily_schedule(target_date=None):
        """Generate scheduled controls for a specific date based on frequencies"""
        if not target_date:
            target_date = date.today() + timedelta(days=1)  # Generate for tomorrow
        
        # Clear existing schedule for the date
        ScheduledControl.query.filter_by(scheduled_date=target_date).delete()
        
        # Get all active parameters that require daily controls
        parameters = ControlParameter.query.filter(
            ControlParameter.active == True,
            ControlParameter.frequency_per_day > 0
        ).all()
        
        scheduled_count = 0
        
        for parameter in parameters:
            frequency = parameter.frequency_per_day
            
            # Generate scheduled times based on frequency
            scheduled_times = SchedulingService._generate_scheduled_times(frequency)
            
            for scheduled_time in scheduled_times:
                # Determine shift
                shift = SchedulingService._determine_shift(scheduled_time)
                
                # Create scheduled control
                scheduled_control = ScheduledControl(
                    parameter_id=parameter.id,
                    scheduled_date=target_date,
                    scheduled_time=scheduled_time,
                    shift=shift,
                    status='pending'
                )
                
                db.session.add(scheduled_control)
                scheduled_count += 1
        
        # Generate weekly controls if it's Monday
        if target_date.weekday() == 0:  # Monday
            weekly_count = SchedulingService._generate_weekly_controls(target_date)
            scheduled_count += weekly_count
        
        db.session.commit()
        
        return {
            'success': True,
            'date': target_date,
            'scheduled_count': scheduled_count
        }
    
    @staticmethod
    def generate_weekly_schedule():
        """Generate weekly controls for the upcoming week"""
        monday = date.today() + timedelta(days=(7 - date.today().weekday()))
        return SchedulingService.generate_daily_schedule(monday)
    
    @staticmethod
    def _generate_scheduled_times(frequency):
        """Generate scheduled times based on frequency per day"""
        if frequency == 1:
            # Once per day - middle of main shift
            return [time(10, 0)]
        elif frequency == 4:
            # 4 times per day - distributed across shifts
            return [time(8, 0), time(12, 0), time(16, 0), time(20, 0)]
        elif frequency == 6:
            # 6 times per day - every 4 hours
            return [time(6, 0), time(10, 0), time(14, 0), time(18, 0), time(22, 0), time(2, 0)]
        elif frequency == 12:
            # 12 times per day - every 2 hours
            return [time(h, 0) for h in [6, 8, 10, 12, 14, 16, 18, 20, 22, 0, 2, 4]]
        else:
            # Custom frequency - distribute evenly across 24 hours
            interval = 24 / frequency
            return [time(int((i * interval) % 24), 0) for i in range(frequency)]
    
    @staticmethod
    def _generate_weekly_controls(target_date):
        """Generate weekly controls for Monday"""
        # Get parameters that require weekly controls
        weekly_parameters = ControlParameter.query.filter(
            ControlParameter.active == True,
            ControlParameter.frequency_description.like('%weekly%')
        ).all()
        
        count = 0
        for parameter in weekly_parameters:
            scheduled_control = ScheduledControl(
                parameter_id=parameter.id,
                scheduled_date=target_date,
                scheduled_time=time(9, 0),  # Monday morning
                shift='06H-14H',
                status='pending'
            )
            db.session.add(scheduled_control)
            count += 1
        
        return count
    
    @staticmethod
    def _determine_shift(scheduled_time):
        """Determine shift based on scheduled time"""
        if time(6, 0) <= scheduled_time < time(14, 0):
            return '06H-14H'
        elif time(14, 0) <= scheduled_time < time(22, 0):
            return '14H-22H'
        else:
            return '22H-06H'
    
    @staticmethod
    def get_daily_schedule(target_date=None, shift=None):
        """Get scheduled controls for a specific date and optional shift"""
        if not target_date:
            target_date = date.today()
        
        query = ScheduledControl.query.filter_by(scheduled_date=target_date)
        
        if shift:
            query = query.filter_by(shift=shift)
        
        return query.join(ControlParameter).order_by(
            ScheduledControl.scheduled_time,
            ControlParameter.code
        ).all()
    
    @staticmethod
    def assign_operator_to_controls(control_ids, operator_name):
        """Assign an operator to multiple scheduled controls"""
        updated_count = ScheduledControl.query.filter(
            ScheduledControl.id.in_(control_ids),
            ScheduledControl.status == 'pending'
        ).update({
            'assigned_operator': operator_name
        }, synchronize_session=False)
        
        db.session.commit()
        return updated_count
    
    @staticmethod
    def get_schedule_summary(target_date=None):
        """Get schedule summary with counts by shift and status"""
        if not target_date:
            target_date = date.today()
        
        # Get all scheduled controls for the date
        controls = ScheduledControl.query.filter_by(scheduled_date=target_date).all()
        
        summary = {
            'date': target_date,
            'total': len(controls),
            'by_shift': {'06H-14H': 0, '14H-22H': 0, '22H-06H': 0},
            'by_status': {'pending': 0, 'completed': 0, 'overdue': 0, 'skipped': 0}
        }
        
        for control in controls:
            if control.shift:
                summary['by_shift'][control.shift] += 1
            summary['by_status'][control.status] += 1
        
        return summary
    
    @staticmethod
    def initialize_default_parameters():
        """Initialize default control parameters based on existing system"""
        # Create default stages
        stages_data = [
            {'code': 'CLAY', 'name': 'Contrôle Argile', 'order_sequence': 1},
            {'code': 'PRESS', 'name': 'Contrôle Presse', 'order_sequence': 2},
            {'code': 'DRYER', 'name': 'Contrôle Séchoir', 'order_sequence': 3},
            {'code': 'BISCUIT', 'name': 'Contrôle Four Biscuit', 'order_sequence': 4},
            {'code': 'EMAIL', 'name': 'Contrôle Four Email', 'order_sequence': 5},
            {'code': 'ENAMEL', 'name': 'Contrôle Email', 'order_sequence': 6},
            {'code': 'TESTS', 'name': 'Tests et Contrôles', 'order_sequence': 7},
        ]
        
        for stage_data in stages_data:
            stage = ControlStage.query.filter_by(code=stage_data['code']).first()
            if not stage:
                stage = ControlStage(**stage_data)
                db.session.add(stage)
        
        db.session.commit()
        
        # Create default parameters
        parameters_data = [
            {
                'code': 'CLAY_HUM_BEFORE',
                'name': 'Humidité avant préparation',
                'stage_code': 'CLAY',
                'specification': '2.5% - 4.1%',
                'unit': '%',
                'frequency_per_day': 6,
                'control_type': 'numeric',
                'min_value': 2.5,
                'max_value': 4.1,
                'target_value': 3.3
            },
            {
                'code': 'CLAY_HUM_AFTER_SIEVE',
                'name': 'Humidité après tamisage',
                'stage_code': 'CLAY',
                'specification': '2% - 3.5%',
                'unit': '%',
                'frequency_per_day': 6,
                'control_type': 'numeric',
                'min_value': 2.0,
                'max_value': 3.5,
                'target_value': 2.75
            },
            {
                'code': 'DRYER_RESIDUAL_HUM',
                'name': 'Humidité résiduelle séchoir',
                'stage_code': 'DRYER',
                'specification': '0.1% - 1.5%',
                'unit': '%',
                'frequency_per_day': 4,
                'control_type': 'numeric',
                'min_value': 0.1,
                'max_value': 1.5,
                'target_value': 0.8,
                'method_reference': 'R2-MA-LABO-02'
            },
            {
                'code': 'PRESS_DEFECTS',
                'name': 'Défauts surface presse',
                'stage_code': 'PRESS',
                'specification': 'Grains ≤15%, autres ≤1%',
                'unit': '%',
                'frequency_per_day': 12,
                'control_type': 'visual',
                'defect_categories': {
                    'grains': 15,
                    'cracks': 1,
                    'cleaning': 1,
                    'foliage': 1,
                    'chipping': 1
                }
            }
        ]
        
        for param_data in parameters_data:
            stage = ControlStage.query.filter_by(code=param_data['stage_code']).first()
            if stage and not ControlParameter.query.filter_by(code=param_data['code']).first():
                param = ControlParameter(
                    stage_id=stage.id,
                    code=param_data['code'],
                    name=param_data['name'],
                    specification=param_data['specification'],
                    unit=param_data.get('unit'),
                    frequency_per_day=param_data['frequency_per_day'],
                    control_type=param_data['control_type'],
                    min_value=param_data.get('min_value'),
                    max_value=param_data.get('max_value'),
                    target_value=param_data.get('target_value'),
                    method_reference=param_data.get('method_reference'),
                    defect_categories=param_data.get('defect_categories')
                )
                db.session.add(param)
        
        db.session.commit()
        
        return {
            'success': True,
            'stages_created': len(stages_data),
            'parameters_created': len(parameters_data)
        }