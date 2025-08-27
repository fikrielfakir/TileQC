from app import db
from flask_login import UserMixin
from datetime import datetime, date, time
from sqlalchemy import event
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='controller')  # controller, quality_manager, admin
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ClayControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    shift = db.Column(db.String(20))  # morning, afternoon, night
    
    # Time measurements (from R2-F1 template)
    measurement_time_1 = db.Column(db.Time)  # First measurement time
    measurement_time_2 = db.Column(db.Time)  # Second measurement time
    
    # Humidity measurements
    humidity_before_prep = db.Column(db.Float)  # 2.5-4.1%
    humidity_after_sieving = db.Column(db.Float)  # 2-3.5%
    humidity_after_prep = db.Column(db.Float)  # 5.3-6.3%
    
    # Weekly measurements
    granulometry_refusal = db.Column(db.Float)  # 10-20%
    calcium_carbonate = db.Column(db.Float)  # 15-25%
    
    # Metadata
    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compliance_status = db.Column(db.String(20))  # compliant, non_compliant, partial
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    controller = db.relationship('User', backref='clay_controls')

class PressControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    shift = db.Column(db.String(20))
    measurement_number = db.Column(db.Integer)  # 1-6 daily measurements
    measurement_time = db.Column(db.Time)  # Time of measurement (from R2-F3 template)
    
    # Format and dimensions
    format_type = db.Column(db.String(10))  # 20x20, 25x40, 25x50
    thickness = db.Column(db.Float)  # mm
    wet_weight = db.Column(db.Float)  # g
    
    # Weight measurements from different outputs (from R2-F3 template)
    weight_output_1 = db.Column(db.Float)  # g
    weight_output_2 = db.Column(db.Float)  # g
    
    # Surface defects (percentages)
    defect_grains = db.Column(db.Float, default=0)  # ≤15%
    defect_cracks = db.Column(db.Float, default=0)  # ≤1%
    defect_cleaning = db.Column(db.Float, default=0)  # ≤1%
    defect_foliage = db.Column(db.Float, default=0)  # ≤1%
    defect_chipping = db.Column(db.Float, default=0)  # ≤1%
    
    # Clay humidity for press (from R2-F3 template)
    clay_humidity = db.Column(db.Float)  # 5.2-6.0%
    
    # Metadata
    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compliance_status = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    controller = db.relationship('User', backref='press_controls')

class DryerControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    shift = db.Column(db.String(20))
    measurement_number = db.Column(db.Integer)
    
    # Measurements
    residual_humidity = db.Column(db.Float)  # 0.1-1.5%
    
    # Surface defects (same as press)
    defect_grains = db.Column(db.Float, default=0)
    defect_cracks = db.Column(db.Float, default=0)
    defect_cleaning = db.Column(db.Float, default=0)
    defect_foliage = db.Column(db.Float, default=0)
    defect_chipping = db.Column(db.Float, default=0)
    
    # Metadata
    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compliance_status = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    controller = db.relationship('User', backref='dryer_controls')

class BiscuitKilnControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    shift = db.Column(db.String(20))
    measurement_number = db.Column(db.Integer)
    
    # Defect percentages
    defect_cracks = db.Column(db.Float, default=0)  # ≤5%
    defect_chipping = db.Column(db.Float, default=0)  # ≤5%
    defect_cooking = db.Column(db.Float, default=0)  # ≤1%
    defect_foliage = db.Column(db.Float, default=0)  # ≤1%
    defect_flatness = db.Column(db.Float, default=0)  # ≤5%
    
    # Tests
    thermal_shock = db.Column(db.String(10))  # pass/fail
    shrinkage_expansion = db.Column(db.Float)  # -0.2% to +0.4%
    fire_loss = db.Column(db.Float)  # 10-19%
    
    # Metadata
    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compliance_status = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    controller = db.relationship('User', backref='biscuit_kiln_controls')

class EmailKilnControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    shift = db.Column(db.String(20))
    
    # Defects
    thermal_shock = db.Column(db.Float, default=0)  # ≤5%
    
    # Mechanical properties
    rupture_resistance = db.Column(db.Float)  # N
    rupture_module = db.Column(db.Float)  # N/mm²
    thickness_for_resistance = db.Column(db.Float)  # mm (for resistance calculation)
    
    # Dimensional deviations
    length_deviation = db.Column(db.Float)  # %
    width_deviation = db.Column(db.Float)  # %
    thickness_deviation = db.Column(db.Float)  # %
    
    # Water absorption
    water_absorption = db.Column(db.Float)  # %
    
    # Quality parameters
    color_nuance = db.Column(db.Float, default=0)  # ≤1%
    cooking_defects = db.Column(db.Float, default=0)  # ≤1%
    flatness_defects = db.Column(db.Float, default=0)  # ≤5%
    
    # Dimensional test results (daily)
    central_curvature = db.Column(db.Float)  # mm (±0.5% / ±2mm)
    veil = db.Column(db.Float)  # mm (±0.5% / ±2mm)
    angularity = db.Column(db.Float)  # mm (±0.5% / ±2mm)
    edge_straightness = db.Column(db.Float)  # mm (±0.3% / ±1.5mm)
    lateral_curvature = db.Column(db.Float)  # mm (±0.5% / ±2mm)
    
    # Surface quality testing
    surface_quality_area = db.Column(db.Float)  # m² (min 1m²)
    surface_quality_tiles = db.Column(db.Integer)  # number (min 30 tiles)
    defect_free_percentage = db.Column(db.Float)  # % (>=95%)
    
    # Metadata
    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compliance_status = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    controller = db.relationship('User', backref='email_kiln_controls')

class DimensionalTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    format_type = db.Column(db.String(10))
    
    # Dimensional measurements (±0.5% ±2mm except edge straightness)
    central_curvature = db.Column(db.Float)  # mm
    veil = db.Column(db.Float)  # mm
    angularity = db.Column(db.Float)  # mm
    edge_straightness = db.Column(db.Float)  # mm (±0.3% ±1.5mm)
    lateral_curvature = db.Column(db.Float)  # mm
    
    # Surface quality
    tiles_tested = db.Column(db.Integer)  # min 30 tiles
    defect_free_tiles = db.Column(db.Integer)
    surface_area_tested = db.Column(db.Float)  # min 1m²
    lighting_level = db.Column(db.Float)  # 300 lux
    
    # Metadata
    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compliance_status = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    controller = db.relationship('User', backref='dimensional_tests')

class EnamelControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    shift = db.Column(db.String(20))
    measurement_type = db.Column(db.String(20))  # pde, production_line
    measurement_number = db.Column(db.Integer)  # 1-12 for production line
    measurement_time = db.Column(db.Time)  # Time of measurement (from R2-F9 template)
    
    # Enamel type and properties
    enamel_type = db.Column(db.String(20))  # engobe, email, mate
    density = db.Column(db.Float)  # g/l
    viscosity = db.Column(db.Float)  # seconds (25-55)
    
    # Grammage by format
    format_type = db.Column(db.String(10))
    water_grammage = db.Column(db.Float)  # g
    enamel_grammage = db.Column(db.Float)  # g
    
    # Sieve refusal
    sieve_refusal = db.Column(db.Float)  # %
    
    # Metadata
    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compliance_status = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    controller = db.relationship('User', backref='enamel_controls')

class DigitalDecoration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    shift = db.Column(db.String(20))
    measurement_number = db.Column(db.Integer)  # 1-12 daily
    
    # Visual inspection parameters
    sharpness = db.Column(db.String(10))  # pass/fail
    offset = db.Column(db.String(10))  # pass/fail
    tonality = db.Column(db.String(10))  # pass/fail
    
    # Metadata
    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compliance_status = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    controller = db.relationship('User', backref='digital_decorations')

class ExternalTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    test_type = db.Column(db.String(50))  # thermal_shock, chemical_resistance, stain_resistance
    iso_standard = db.Column(db.String(50))  # ISO reference
    
    # Test results
    result_value = db.Column(db.Float)
    result_status = db.Column(db.String(20))  # pass/fail/pending
    test_report_number = db.Column(db.String(50))
    laboratory = db.Column(db.String(100), default='CETEMCO')
    
    # Metadata
    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    controller = db.relationship('User', backref='external_tests')

class Specification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    control_type = db.Column(db.String(50), nullable=False)  # clay, press, dryer, etc.
    parameter_name = db.Column(db.String(100), nullable=False)  # humidity_before_prep, thickness, etc.
    format_type = db.Column(db.String(20))  # For format-specific specs (20x20, 25x40, etc.)
    enamel_type = db.Column(db.String(20))  # For enamel-specific specs
    
    # Specification limits
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    target_value = db.Column(db.Float)
    unit = db.Column(db.String(20))  # %, mm, g, N, etc.
    
    # Additional constraints
    constraints = db.Column(db.Text)  # JSON for complex rules
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', backref='created_specifications')
    
    def get_constraints(self):
        """Parse JSON constraints"""
        if self.constraints:
            try:
                return json.loads(self.constraints)
            except:
                return {}
        return {}
    
    def set_constraints(self, constraints_dict):
        """Set JSON constraints"""
        self.constraints = json.dumps(constraints_dict) if constraints_dict else None
    
    @staticmethod
    def get_spec(control_type, parameter_name, format_type=None, enamel_type=None):
        """Get specification for a parameter"""
        query = Specification.query.filter(
            Specification.control_type == control_type,
            Specification.parameter_name == parameter_name,
            Specification.is_active == True
        )
        
        if format_type:
            query = query.filter(Specification.format_type == format_type)
        if enamel_type:
            query = query.filter(Specification.enamel_type == enamel_type)
            
        return query.first()
    
    def __repr__(self):
        return f'<Specification {self.control_type}.{self.parameter_name}: {self.min_value}-{self.max_value} {self.unit}>'

# Event listeners for automatic compliance calculation
@event.listens_for(ClayControl, 'before_insert')
@event.listens_for(ClayControl, 'before_update')
def calculate_clay_compliance(mapper, connection, target):
    from utils.validators import validate_clay_control
    target.compliance_status = validate_clay_control(target)

@event.listens_for(PressControl, 'before_insert')
@event.listens_for(PressControl, 'before_update')
def calculate_press_compliance(mapper, connection, target):
    from utils.validators import validate_press_control
    target.compliance_status = validate_press_control(target)

@event.listens_for(DryerControl, 'before_insert')
@event.listens_for(DryerControl, 'before_update')
def calculate_dryer_compliance(mapper, connection, target):
    from utils.validators import validate_dryer_control
    target.compliance_status = validate_dryer_control(target)

@event.listens_for(BiscuitKilnControl, 'before_insert')
@event.listens_for(BiscuitKilnControl, 'before_update')
def calculate_biscuit_compliance(mapper, connection, target):
    from utils.validators import validate_biscuit_kiln_control
    target.compliance_status = validate_biscuit_kiln_control(target)

@event.listens_for(EmailKilnControl, 'before_insert')
@event.listens_for(EmailKilnControl, 'before_update')
def calculate_email_compliance(mapper, connection, target):
    from utils.validators import validate_email_kiln_control
    target.compliance_status = validate_email_kiln_control(target)

@event.listens_for(DimensionalTest, 'before_insert')
@event.listens_for(DimensionalTest, 'before_update')
def calculate_dimensional_compliance(mapper, connection, target):
    from utils.validators import validate_dimensional_test
    target.compliance_status = validate_dimensional_test(target)

@event.listens_for(EnamelControl, 'before_insert')
@event.listens_for(EnamelControl, 'before_update')
def calculate_enamel_compliance(mapper, connection, target):
    from utils.validators import validate_enamel_control
    target.compliance_status = validate_enamel_control(target)

@event.listens_for(DigitalDecoration, 'before_insert')
@event.listens_for(DigitalDecoration, 'before_update')
def calculate_digital_compliance(mapper, connection, target):
    from utils.validators import validate_digital_decoration
    target.compliance_status = validate_digital_decoration(target)

# New Optimized Models for Automated Scheduling System

class ControlStage(db.Model):
    __tablename__ = 'control_stages'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order_sequence = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    
    parameters = db.relationship('ControlParameter', backref='stage', lazy=True)
    
    def __repr__(self):
        return f'<ControlStage {self.code}: {self.name}>'

class ControlParameter(db.Model):
    __tablename__ = 'control_parameters'
    id = db.Column(db.Integer, primary_key=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('control_stages.id'), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    specification = db.Column(db.Text, nullable=False)
    unit = db.Column(db.String(20))
    frequency_per_day = db.Column(db.Integer)
    frequency_description = db.Column(db.String(50))
    method_reference = db.Column(db.String(50))
    form_reference = db.Column(db.String(50))
    min_value = db.Column(db.Numeric(10,3))
    max_value = db.Column(db.Numeric(10,3))
    target_value = db.Column(db.Numeric(10,3))
    control_type = db.Column(db.Enum('numeric', 'visual', 'categorical', 'boolean', name='control_types'))
    defect_categories = db.Column(db.JSON)
    formats = db.Column(db.JSON)
    active = db.Column(db.Boolean, default=True)
    
    measurements = db.relationship('OptimizedMeasurement', backref='parameter', lazy=True)
    
    def check_conformity(self, value):
        """Check if a measured value is within specifications"""
        if self.control_type == 'numeric' and value is not None:
            if self.min_value is not None and float(value) < float(self.min_value):
                return False
            if self.max_value is not None and float(value) > float(self.max_value):
                return False
            return True
        return None
    
    def __repr__(self):
        return f'<ControlParameter {self.code}: {self.name}>'

class OptimizedMeasurement(db.Model):
    __tablename__ = 'optimized_measurements'
    id = db.Column(db.Integer, primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey('control_parameters.id'), nullable=False)
    operator_name = db.Column(db.String(100), nullable=False)
    measurement_date = db.Column(db.Date, nullable=False)
    measurement_time = db.Column(db.Time, nullable=False)
    shift = db.Column(db.Enum('06H-14H', '14H-22H', '22H-06H', name='shift_types'))
    format = db.Column(db.String(20))
    line_number = db.Column(db.Integer)
    oven_number = db.Column(db.Integer)
    press_number = db.Column(db.Integer)
    
    # Values
    numeric_value = db.Column(db.Numeric(10,3))
    text_value = db.Column(db.Text)
    boolean_value = db.Column(db.Boolean)
    json_values = db.Column(db.JSON)
    
    # Status
    is_conforming = db.Column(db.Boolean)
    deviation_percentage = db.Column(db.Numeric(5,2))
    
    # References
    sample_size = db.Column(db.Integer, default=1)
    nc_number = db.Column(db.String(50))
    observations = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<OptimizedMeasurement {self.id} - {self.measurement_date}>'

class ScheduledControl(db.Model):
    __tablename__ = 'scheduled_controls'
    id = db.Column(db.Integer, primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey('control_parameters.id'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    scheduled_time = db.Column(db.Time, nullable=False)
    shift = db.Column(db.Enum('06H-14H', '14H-22H', '22H-06H', name='shift_types_scheduled'))
    status = db.Column(db.Enum('pending', 'completed', 'skipped', 'overdue', name='control_status'), default='pending')
    assigned_operator = db.Column(db.String(100))
    completed_at = db.Column(db.DateTime)
    measurement_id = db.Column(db.Integer, db.ForeignKey('optimized_measurements.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    parameter = db.relationship('ControlParameter', backref='scheduled_controls')
    measurement = db.relationship('OptimizedMeasurement', backref='scheduled_control')
    
    def __repr__(self):
        return f'<ScheduledControl {self.id} - {self.scheduled_date} - {self.status}>'

class ControlSheet(db.Model):
    __tablename__ = 'control_sheets'
    id = db.Column(db.Integer, primary_key=True)
    sheet_type = db.Column(db.Enum('daily', 'weekly', 'shift', 'stage', name='sheet_types'))
    reference_date = db.Column(db.Date, nullable=False)
    shift = db.Column(db.String(10))
    stage_id = db.Column(db.Integer, db.ForeignKey('control_stages.id'))
    generated_by = db.Column(db.String(100))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(500))
    status = db.Column(db.Enum('draft', 'final', 'archived', name='sheet_status'), default='draft')
    
    stage = db.relationship('ControlStage', backref='control_sheets')
    
    def __repr__(self):
        return f'<ControlSheet {self.id}: {self.sheet_type} - {self.reference_date}>'
