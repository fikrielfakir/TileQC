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

# Complete R2-F1-LABO Form
class R2F1LaboForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    
    # Humidité Trémie Générale
    humidity_before_prep = FloatField('% Humidité Trémie', validators=[Optional(), NumberRange(min=2.5, max=4.1)])
    measurement_time_1 = TimeField('Heure', validators=[Optional()])
    
    # Humidité Après Tamisage  
    humidity_after_sieving = FloatField('% Humidité Tamisage', validators=[Optional(), NumberRange(min=2.0, max=3.5)])
    measurement_time_2 = TimeField('Heure', validators=[Optional()])
    
    # Humidité Silos (4 mesures)
    silo_time_1 = TimeField('Heure Silo 1', validators=[Optional()])
    silo_number_1 = StringField('N° Silo 1', validators=[Optional()])
    silo_humidity_1 = FloatField('% Humidité Silo 1', validators=[Optional(), NumberRange(min=5.3, max=6.3)])
    
    silo_time_2 = TimeField('Heure Silo 2', validators=[Optional()])
    silo_number_2 = StringField('N° Silo 2', validators=[Optional()])
    silo_humidity_2 = FloatField('% Humidité Silo 2', validators=[Optional(), NumberRange(min=5.3, max=6.3)])
    
    silo_time_3 = TimeField('Heure Silo 3', validators=[Optional()])
    silo_number_3 = StringField('N° Silo 3', validators=[Optional()])
    silo_humidity_3 = FloatField('% Humidité Silo 3', validators=[Optional(), NumberRange(min=5.3, max=6.3)])
    
    silo_time_4 = TimeField('Heure Silo 4', validators=[Optional()])
    silo_number_4 = StringField('N° Silo 4', validators=[Optional()])
    silo_humidity_4 = FloatField('% Humidité Silo 4', validators=[Optional(), NumberRange(min=5.3, max=6.3)])
    
    # Humidité Moyenne (calculée automatiquement)
    humidity_after_prep = FloatField('Humidité Moyenne', validators=[Optional(), NumberRange(min=5.3, max=6.3)])
    
    # Humidité Argile Presse
    press_silo_number = StringField('N° Silo Presse', validators=[Optional()])
    press_humidity = FloatField('% Humidité Presse', validators=[Optional(), NumberRange(min=5.2, max=6.0)])
    press_time = TimeField('Heure Presse', validators=[Optional()])
    
    # Humidité Résiduelle Séchoir
    residual_humidity = FloatField('% Humidité Résiduelle', validators=[Optional(), NumberRange(min=0.1, max=1.5)])
    dryer_time = TimeField('Heure Séchoir', validators=[Optional()])
    
    notes = TextAreaField('Notes')

# Separate forms for each clay sub-control
class HumidityBeforePrepForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_time = TimeField('Temps de Mesure', validators=[Optional()])
    humidity_before_prep = FloatField('Humidité Trémie Générale (%)', validators=[DataRequired(), NumberRange(min=0, max=100, message="Valeur entre 0% et 100%")])
    notes = TextAreaField('Notes')

class HumidityAfterSievingForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_time = TimeField('Temps de Mesure', validators=[Optional()])
    humidity_after_sieving = FloatField('Humidité Après Tamisage (%)', validators=[DataRequired(), NumberRange(min=0, max=100, message="Valeur entre 0% et 100%")])
    notes = TextAreaField('Notes')

class HumidityAfterPrepForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_time = TimeField('Temps de Mesure', validators=[Optional()])
    humidity_after_prep = FloatField('Humidité Niveau Silo (%)', validators=[DataRequired(), NumberRange(min=0, max=100, message="Valeur entre 0% et 100%")])
    notes = TextAreaField('Notes')

class GranulometryForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_time = TimeField('Temps de Mesure', validators=[Optional()])
    granulometry_refusal = FloatField('Refus Granulométrique (%)', validators=[DataRequired(), NumberRange(min=0, max=100, message="Valeur entre 0% et 100%")])
    notes = TextAreaField('Notes')

class CalciumCarbonateForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    shift = SelectField('Équipe', choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('night', 'Nuit')])
    measurement_time = TimeField('Temps de Mesure', validators=[Optional()])
    calcium_carbonate = FloatField('% Chaux CaCO₃ (%)', validators=[DataRequired(), NumberRange(min=0, max=100, message="Valeur entre 0% et 100%")])
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
