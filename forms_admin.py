from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional, NumberRange
from models import Specification

class SpecificationForm(FlaskForm):
    control_type = SelectField('Type de Contrôle', 
                              choices=[('clay', 'Contrôle Argile'),
                                     ('press', 'Contrôle Presse'),
                                     ('dryer', 'Contrôle Séchoir'),
                                     ('biscuit_kiln', 'Four Biscuit'),
                                     ('email_kiln', 'Four Émail'),
                                     ('dimensional', 'Test Dimensionnel'),
                                     ('enamel', 'Contrôle Émail'),
                                     ('digital', 'Décoration Numérique')],
                              validators=[DataRequired()])
    
    parameter_name = StringField('Nom du Paramètre', validators=[DataRequired()])
    format_type = SelectField('Type de Format (Optionnel)', 
                             choices=[('', 'Tous les Formats'),
                                    ('20x20', '20x20'),
                                    ('25x40', '25x40'),
                                    ('25x50', '25x50')],
                             validators=[Optional()])
    
    enamel_type = SelectField('Type d\'Émail (Optionnel)',
                             choices=[('', 'Tous les Types'),
                                    ('engobe', 'Engobe'),
                                    ('email', 'Émail'),
                                    ('mate', 'Mat')],
                             validators=[Optional()])
    
    min_value = FloatField('Valeur Minimale', validators=[Optional()])
    max_value = FloatField('Valeur Maximale', validators=[Optional()])
    target_value = FloatField('Valeur Cible (Optionnelle)', validators=[Optional()])
    
    unit = SelectField('Unité',
                      choices=[('%', '%'),
                             ('mm', 'mm'),
                             ('g', 'g'),
                             ('N', 'N'),
                             ('N/mm²', 'N/mm²'),
                             ('g/l', 'g/l'),
                             ('seconds', 'secondes'),
                             ('lux', 'lux'),
                             ('m²', 'm²'),
                             ('pieces', 'pièces')],
                      validators=[DataRequired()])
    
    description = TextAreaField('Description', validators=[Optional()])
    is_active = BooleanField('Actif', default=True)

class BulkSpecificationForm(FlaskForm):
    control_type = SelectField('Type de Contrôle', 
                              choices=[('clay', 'Contrôle Argile'),
                                     ('press', 'Contrôle Presse'),
                                     ('dryer', 'Contrôle Séchoir'),
                                     ('biscuit_kiln', 'Four Biscuit'),
                                     ('email_kiln', 'Four Émail'),
                                     ('dimensional', 'Test Dimensionnel'),
                                     ('enamel', 'Contrôle Émail'),
                                     ('digital', 'Décoration Numérique')],
                              validators=[DataRequired()])
    
    action = SelectField('Action',
                        choices=[('reset_defaults', 'Réinitialiser aux Valeurs par Défaut'),
                               ('export', 'Exporter les Spécifications Actuelles'),
                               ('deactivate_all', 'Désactiver Tout')],
                        validators=[DataRequired()])