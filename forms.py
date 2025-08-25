from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import date

class ClayControlForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Shift', choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')])
    
    humidity_before_prep = FloatField('Humidity Before Prep (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    humidity_after_sieving = FloatField('Humidity After Sieving (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    humidity_after_prep = FloatField('Humidity After Prep (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    granulometry_refusal = FloatField('Granulometry Refusal (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    calcium_carbonate = FloatField('Calcium Carbonate (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    notes = TextAreaField('Notes')

class PressControlForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Shift', choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')])
    measurement_number = IntegerField('Measurement Number (1-6)', validators=[DataRequired(), NumberRange(min=1, max=6)])
    
    format_type = SelectField('Format', choices=[('20x20', '20x20'), ('25x40', '25x40'), ('25x50', '25x50')], validators=[DataRequired()])
    thickness = FloatField('Thickness (mm)', validators=[DataRequired(), NumberRange(min=0)])
    wet_weight = FloatField('Wet Weight (g)', validators=[DataRequired(), NumberRange(min=0)])
    
    defect_grains = FloatField('Grains (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cracks = FloatField('Cracks (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cleaning = FloatField('Cleaning (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_foliage = FloatField('Foliage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_chipping = FloatField('Chipping (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    notes = TextAreaField('Notes')

class DryerControlForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Shift', choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')])
    measurement_number = IntegerField('Measurement Number (1-6)', validators=[DataRequired(), NumberRange(min=1, max=6)])
    
    residual_humidity = FloatField('Residual Humidity (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    
    defect_grains = FloatField('Grains (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cracks = FloatField('Cracks (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cleaning = FloatField('Cleaning (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_foliage = FloatField('Foliage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_chipping = FloatField('Chipping (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    notes = TextAreaField('Notes')

class BiscuitKilnForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Shift', choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')])
    measurement_number = IntegerField('Measurement Number (1-6)', validators=[DataRequired(), NumberRange(min=1, max=6)])
    
    defect_cracks = FloatField('Cracks (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_chipping = FloatField('Chipping (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cooking = FloatField('Cooking (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_foliage = FloatField('Foliage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_flatness = FloatField('Flatness (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    thermal_shock = SelectField('Thermal Shock', choices=[('pass', 'Pass'), ('fail', 'Fail')])
    shrinkage_expansion = FloatField('Shrinkage/Expansion (%)', validators=[Optional(), NumberRange(min=-5, max=5)])
    fire_loss = FloatField('Fire Loss (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    notes = TextAreaField('Notes')

class EmailKilnForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Shift', choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')])
    
    thermal_shock = FloatField('Thermal Shock (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    rupture_resistance = FloatField('Rupture Resistance (N)', validators=[Optional(), NumberRange(min=0)])
    rupture_module = FloatField('Rupture Module (N/mm²)', validators=[Optional(), NumberRange(min=0)])
    thickness_for_resistance = FloatField('Thickness for Resistance (mm)', validators=[Optional(), NumberRange(min=0)])
    
    length_deviation = FloatField('Length Deviation (%)', validators=[Optional(), NumberRange(min=-100, max=100)])
    width_deviation = FloatField('Width Deviation (%)', validators=[Optional(), NumberRange(min=-100, max=100)])
    thickness_deviation = FloatField('Thickness Deviation (%)', validators=[Optional(), NumberRange(min=-100, max=100)])
    
    water_absorption = FloatField('Water Absorption (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    color_nuance = FloatField('Color Nuance (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    cooking_defects = FloatField('Cooking Defects (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    flatness_defects = FloatField('Flatness Defects (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    notes = TextAreaField('Notes')

class DimensionalTestForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    format_type = SelectField('Format', choices=[('20x20', '20x20'), ('25x40', '25x40'), ('25x50', '25x50')], validators=[DataRequired()])
    
    central_curvature = FloatField('Central Curvature (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    veil = FloatField('Veil (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    angularity = FloatField('Angularity (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    edge_straightness = FloatField('Edge Straightness (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    lateral_curvature = FloatField('Lateral Curvature (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    
    tiles_tested = IntegerField('Tiles Tested', validators=[Optional(), NumberRange(min=1)])
    defect_free_tiles = IntegerField('Defect-Free Tiles', validators=[Optional(), NumberRange(min=0)])
    surface_area_tested = FloatField('Surface Area Tested (m²)', validators=[Optional(), NumberRange(min=0)])
    lighting_level = FloatField('Lighting Level (lux)', validators=[Optional(), NumberRange(min=0)])
    
    notes = TextAreaField('Notes')

class EnamelControlForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Shift', choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')])
    measurement_type = SelectField('Measurement Type', choices=[('pde', 'PDE'), ('production_line', 'Production Line')], validators=[DataRequired()])
    measurement_number = IntegerField('Measurement Number', validators=[Optional(), NumberRange(min=1, max=12)])
    
    enamel_type = SelectField('Enamel Type', choices=[('engobe', 'Engobe'), ('email', 'Email'), ('mate', 'Mate')], validators=[DataRequired()])
    density = FloatField('Density (g/l)', validators=[Optional(), NumberRange(min=0)])
    viscosity = FloatField('Viscosity (seconds)', validators=[Optional(), NumberRange(min=0)])
    
    format_type = SelectField('Format', choices=[('20x20', '20x20'), ('25x40', '25x40'), ('25x50', '25x50')])
    water_grammage = FloatField('Water Grammage (g)', validators=[Optional(), NumberRange(min=0)])
    enamel_grammage = FloatField('Enamel Grammage (g)', validators=[Optional(), NumberRange(min=0)])
    
    sieve_refusal = FloatField('Sieve Refusal (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    notes = TextAreaField('Notes')

class DigitalDecorationForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Shift', choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')])
    measurement_number = IntegerField('Measurement Number (1-12)', validators=[DataRequired(), NumberRange(min=1, max=12)])
    
    sharpness = SelectField('Sharpness', choices=[('pass', 'Pass'), ('fail', 'Fail')], validators=[DataRequired()])
    offset = SelectField('Offset', choices=[('pass', 'Pass'), ('fail', 'Fail')], validators=[DataRequired()])
    tonality = SelectField('Tonality', choices=[('pass', 'Pass'), ('fail', 'Fail')], validators=[DataRequired()])
    
    notes = TextAreaField('Notes')

class ExternalTestForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    test_type = SelectField('Test Type', 
                           choices=[('thermal_shock', 'Thermal Shock Resistance'), 
                                   ('chemical_resistance', 'Chemical Resistance'),
                                   ('stain_resistance', 'Stain Resistance')], 
                           validators=[DataRequired()])
    iso_standard = StringField('ISO Standard', validators=[DataRequired()])
    
    result_value = FloatField('Result Value', validators=[Optional()])
    result_status = SelectField('Result Status', choices=[('pass', 'Pass'), ('fail', 'Fail'), ('pending', 'Pending')])
    test_report_number = StringField('Test Report Number')
    laboratory = StringField('Laboratory', default='CETEMCO')
    
    notes = TextAreaField('Notes')
