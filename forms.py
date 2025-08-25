from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import date

class ClayControlForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    
    # Time measurements (matching R2-F1 template)
    measurement_time_1 = TimeField('Premier Temps de Mesure', validators=[Optional()])
    measurement_time_2 = TimeField('Deuxième Temps de Mesure', validators=[Optional()])
    
    humidity_before_prep = FloatField('Humidité Avant Préparation (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    humidity_after_sieving = FloatField('Humidité Après Tamisage (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    humidity_after_prep = FloatField('Humidité Après Préparation (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    granulometry_refusal = FloatField('Refus Granulométrique (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    calcium_carbonate = FloatField('Carbonate de Calcium (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    notes = TextAreaField('Notes')

class PressControlForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_number = IntegerField('Numéro de Mesure (1-6)', validators=[DataRequired(), NumberRange(min=1, max=6)])
    measurement_time = TimeField('Temps de Mesure', validators=[Optional()])
    
    format_type = SelectField('Format', choices=[('20x20', '20x20'), ('25x40', '25x40'), ('25x50', '25x50')], validators=[DataRequired()])
    thickness = FloatField('Épaisseur (mm)', validators=[DataRequired(), NumberRange(min=0)])
    wet_weight = FloatField('Poids Humide (g)', validators=[DataRequired(), NumberRange(min=0)])
    
    # Weight measurements from different outputs (matching R2-F3 template)
    weight_output_1 = FloatField('Poids Sortie 1 (g)', validators=[Optional(), NumberRange(min=0)])
    weight_output_2 = FloatField('Poids Sortie 2 (g)', validators=[Optional(), NumberRange(min=0)])
    
    defect_grains = FloatField('Grains (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cracks = FloatField('Fissures (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cleaning = FloatField('Nettoyage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_foliage = FloatField('Feuillage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_chipping = FloatField('Ébrochage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    notes = TextAreaField('Notes')

class DryerControlForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_number = IntegerField('Numéro de Mesure (1-6)', validators=[DataRequired(), NumberRange(min=1, max=6)])
    
    residual_humidity = FloatField('Humidité Résiduelle (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    
    defect_grains = FloatField('Grains (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cracks = FloatField('Fissures (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cleaning = FloatField('Nettoyage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_foliage = FloatField('Feuillage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_chipping = FloatField('Ébrochage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    notes = TextAreaField('Notes')

class BiscuitKilnForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_number = IntegerField('Numéro de Mesure (1-6)', validators=[DataRequired(), NumberRange(min=1, max=6)])
    
    defect_cracks = FloatField('Fissures (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_chipping = FloatField('Ébrochage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_cooking = FloatField('Cuisson (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_foliage = FloatField('Feuillage (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    defect_flatness = FloatField('Planéité (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    thermal_shock = SelectField('Choc Thermique', choices=[('pass', 'Réussi'), ('fail', 'Échec')])
    shrinkage_expansion = FloatField('Retrait/Dilatation (%)', validators=[Optional(), NumberRange(min=-5, max=5)])
    fire_loss = FloatField('Perte au Feu (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    notes = TextAreaField('Notes')

class EmailKilnForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    
    thermal_shock = FloatField('Choc Thermique (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    rupture_resistance = FloatField('Résistance à la Rupture (N)', validators=[Optional(), NumberRange(min=0)])
    rupture_module = FloatField('Module de Rupture (N/mm²)', validators=[Optional(), NumberRange(min=0)])
    thickness_for_resistance = FloatField('Épaisseur pour Résistance (mm)', validators=[Optional(), NumberRange(min=0)])
    
    length_deviation = FloatField('Déviation Longueur (%)', validators=[Optional(), NumberRange(min=-100, max=100)])
    width_deviation = FloatField('Déviation Largeur (%)', validators=[Optional(), NumberRange(min=-100, max=100)])
    thickness_deviation = FloatField('Déviation Épaisseur (%)', validators=[Optional(), NumberRange(min=-100, max=100)])
    
    water_absorption = FloatField('Absorption d\'Eau (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    color_nuance = FloatField('Nuance de Couleur (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    cooking_defects = FloatField('Défauts de Cuisson (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    flatness_defects = FloatField('Défauts de Planéité (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    
    notes = TextAreaField('Notes')

class DimensionalTestForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    format_type = SelectField('Format', choices=[('20x20', '20x20'), ('25x40', '25x40'), ('25x50', '25x50')], validators=[DataRequired()])
    
    central_curvature = FloatField('Courbure Centrale (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    veil = FloatField('Voile (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    angularity = FloatField('Angularité (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    edge_straightness = FloatField('Rectitude des Arêtes (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    lateral_curvature = FloatField('Courbure Latérale (mm)', validators=[Optional(), NumberRange(min=-10, max=10)])
    
    tiles_tested = IntegerField('Carreaux Testés', validators=[Optional(), NumberRange(min=1)])
    defect_free_tiles = IntegerField('Carreaux Sans Défaut', validators=[Optional(), NumberRange(min=0)])
    surface_area_tested = FloatField('Surface Testée (m²)', validators=[Optional(), NumberRange(min=0)])
    lighting_level = FloatField('Niveau d\'Éclairage (lux)', validators=[Optional(), NumberRange(min=0)])
    
    notes = TextAreaField('Notes')

class EnamelControlForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_type = SelectField('Type de Mesure', choices=[('pde', 'PDE'), ('production_line', 'Ligne de Production')], validators=[DataRequired()])
    measurement_number = IntegerField('Numéro de Mesure', validators=[Optional(), NumberRange(min=1, max=12)])
    measurement_time = TimeField('Temps de Mesure', validators=[Optional()])
    
    enamel_type = SelectField('Type d\'Émail', choices=[('engobe', 'Engobe'), ('email', 'Émail'), ('mate', 'Mat')], validators=[DataRequired()])
    density = FloatField('Densité (g/l)', validators=[Optional(), NumberRange(min=0)])
    viscosity = FloatField('Viscosité (secondes)', validators=[Optional(), NumberRange(min=0)])
    
    format_type = SelectField('Format', choices=[('20x20', '20x20'), ('25x40', '25x40'), ('25x50', '25x50')])
    water_grammage = FloatField('Grammage Eau (g)', validators=[Optional(), NumberRange(min=0)])
    enamel_grammage = FloatField('Grammage Émail (g)', validators=[Optional(), NumberRange(min=0)])
    
    sieve_refusal = FloatField('Refus Tamis (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    notes = TextAreaField('Notes')

class DigitalDecorationForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_number = IntegerField('Numéro de Mesure (1-12)', validators=[DataRequired(), NumberRange(min=1, max=12)])
    
    sharpness = SelectField('Netteté', choices=[('pass', 'Réussi'), ('fail', 'Échec')], validators=[DataRequired()])
    offset = SelectField('Décalage', choices=[('pass', 'Réussi'), ('fail', 'Échec')], validators=[DataRequired()])
    tonality = SelectField('Tonalité', choices=[('pass', 'Réussi'), ('fail', 'Échec')], validators=[DataRequired()])
    
    notes = TextAreaField('Notes')

class ExternalTestForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    test_type = SelectField('Type de Test', 
                           choices=[('thermal_shock', 'Résistance au Choc Thermique'), 
                                   ('chemical_resistance', 'Résistance Chimique'),
                                   ('stain_resistance', 'Résistance aux Taches')], 
                           validators=[DataRequired()])
    iso_standard = StringField('Norme ISO', validators=[DataRequired()])
    
    result_value = FloatField('Valeur du Résultat', validators=[Optional()])
    result_status = SelectField('Statut du Résultat', choices=[('pass', 'Réussi'), ('fail', 'Échec'), ('pending', 'En Attente')])
    test_report_number = StringField('Numéro du Rapport de Test')
    laboratory = StringField('Laboratoire', default='CETEMCO')
    
    notes = TextAreaField('Notes')
