from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional, NumberRange
from models import Specification

class SpecificationForm(FlaskForm):
    control_type = SelectField('Control Type', 
                              choices=[('clay', 'Clay Control'),
                                     ('press', 'Press Control'),
                                     ('dryer', 'Dryer Control'),
                                     ('biscuit_kiln', 'Biscuit Kiln'),
                                     ('email_kiln', 'Email Kiln'),
                                     ('dimensional', 'Dimensional Test'),
                                     ('enamel', 'Enamel Control'),
                                     ('digital', 'Digital Decoration')],
                              validators=[DataRequired()])
    
    parameter_name = StringField('Parameter Name', validators=[DataRequired()])
    format_type = SelectField('Format Type (Optional)', 
                             choices=[('', 'All Formats'),
                                    ('20x20', '20x20'),
                                    ('25x40', '25x40'),
                                    ('25x50', '25x50')],
                             validators=[Optional()])
    
    enamel_type = SelectField('Enamel Type (Optional)',
                             choices=[('', 'All Types'),
                                    ('engobe', 'Engobe'),
                                    ('email', 'Email'),
                                    ('mate', 'Mate')],
                             validators=[Optional()])
    
    min_value = FloatField('Minimum Value', validators=[Optional()])
    max_value = FloatField('Maximum Value', validators=[Optional()])
    target_value = FloatField('Target Value (Optional)', validators=[Optional()])
    
    unit = SelectField('Unit',
                      choices=[('%', '%'),
                             ('mm', 'mm'),
                             ('g', 'g'),
                             ('N', 'N'),
                             ('N/mm²', 'N/mm²'),
                             ('g/l', 'g/l'),
                             ('seconds', 'seconds'),
                             ('lux', 'lux'),
                             ('m²', 'm²'),
                             ('pieces', 'pieces')],
                      validators=[DataRequired()])
    
    description = TextAreaField('Description', validators=[Optional()])
    is_active = BooleanField('Active', default=True)

class BulkSpecificationForm(FlaskForm):
    control_type = SelectField('Control Type', 
                              choices=[('clay', 'Clay Control'),
                                     ('press', 'Press Control'),
                                     ('dryer', 'Dryer Control'),
                                     ('biscuit_kiln', 'Biscuit Kiln'),
                                     ('email_kiln', 'Email Kiln'),
                                     ('dimensional', 'Dimensional Test'),
                                     ('enamel', 'Enamel Control'),
                                     ('digital', 'Digital Decoration')],
                              validators=[DataRequired()])
    
    action = SelectField('Action',
                        choices=[('reset_defaults', 'Reset to Default Values'),
                               ('export', 'Export Current Specifications'),
                               ('deactivate_all', 'Deactivate All')],
                        validators=[DataRequired()])