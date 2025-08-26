from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from forms import ClayControlForm, HumidityBeforePrepForm, HumidityAfterSievingForm, HumidityAfterPrepForm, GranulometryForm, CalciumCarbonateForm, CombinedHumidityForm, CombinedAnalysisForm
from models import ClayControl
from app import db
from datetime import date
from excel_export import ExcelExporter
import os

clay_bp = Blueprint('clay', __name__)

@clay_bp.route('/')
@login_required
def clay_controls():
    page = request.args.get('page', 1, type=int)
    controls = ClayControl.query.order_by(ClayControl.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('clay/clay_control.html', controls=controls)

@clay_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_clay_control():
    form = ClayControlForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl()
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.measurement_time_1 = form.measurement_time_1.data
        clay_control.measurement_time_2 = form.measurement_time_2.data
        clay_control.humidity_before_prep = form.humidity_before_prep.data
        clay_control.humidity_after_sieving = form.humidity_after_sieving.data
        clay_control.humidity_after_prep = form.humidity_after_prep.data
        clay_control.granulometry_refusal = form.granulometry_refusal.data
        clay_control.calcium_carbonate = form.calcium_carbonate.data
        clay_control.notes = form.notes.data
        clay_control.controller_id = current_user.id
        clay_control.compliance_status = 'compliant'  # Default
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Enregistrement du contrôle argile ajouté avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/clay_control.html', form=form)

@clay_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_clay_control(id):
    clay_control = ClayControl.query.get_or_404(id)
    form = ClayControlForm(obj=clay_control)
    
    if form.validate_on_submit():
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.measurement_time_1 = form.measurement_time_1.data
        clay_control.measurement_time_2 = form.measurement_time_2.data
        clay_control.humidity_before_prep = form.humidity_before_prep.data
        clay_control.humidity_after_sieving = form.humidity_after_sieving.data
        clay_control.humidity_after_prep = form.humidity_after_prep.data
        clay_control.granulometry_refusal = form.granulometry_refusal.data
        clay_control.calcium_carbonate = form.calcium_carbonate.data
        clay_control.notes = form.notes.data
        
        db.session.commit()
        
        flash('Enregistrement du contrôle argile mis à jour avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/clay_control.html', form=form, edit=True, control=clay_control)

@clay_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_clay_control(id):
    if current_user.role not in ['admin', 'quality_manager']:
        flash('Permissions insuffisantes', 'error')
        return redirect(url_for('clay.clay_controls'))
    
    clay_control = ClayControl.query.get_or_404(id)
    db.session.delete(clay_control)
    db.session.commit()
    
    flash('Enregistrement du contrôle argile supprimé avec succès', 'success')
    return redirect(url_for('clay.clay_controls'))

@clay_bp.route('/api/trend/<parameter>')
@login_required
def clay_trend_api(parameter):
    from utils.helpers import get_control_chart_data
    data = get_control_chart_data(ClayControl, parameter, days=30)
    return jsonify(data)

# Separate routes for each clay sub-control

@clay_bp.route('/humidity-before-prep', methods=['GET', 'POST'])
@login_required
def humidity_before_prep():
    form = HumidityBeforePrepForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl()
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.measurement_time_1 = form.measurement_time.data
        clay_control.humidity_before_prep = form.humidity_before_prep.data
        clay_control.notes = form.notes.data
        clay_control.controller_id = current_user.id
        
        # Check compliance
        humidity_value = form.humidity_before_prep.data
        if humidity_value is not None and (humidity_value < 2.5 or humidity_value > 4.1):
            clay_control.compliance_status = 'non_compliant'
            flash(f'⚠️ Valeur hors spécification ({humidity_value}%) - F.N.C. requis (Spéc: 2.5%-4.1%)', 'warning')
        else:
            clay_control.compliance_status = 'compliant'
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Humidité trémie générale enregistrée avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/humidity_before_prep.html', form=form)

@clay_bp.route('/humidity-after-sieving', methods=['GET', 'POST'])
@login_required
def humidity_after_sieving():
    form = HumidityAfterSievingForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl()
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.measurement_time_1 = form.measurement_time.data
        clay_control.humidity_after_sieving = form.humidity_after_sieving.data
        clay_control.notes = form.notes.data
        clay_control.controller_id = current_user.id
        
        # Check compliance
        humidity_value = form.humidity_after_sieving.data
        if humidity_value is not None and (humidity_value < 2.0 or humidity_value > 3.5):
            clay_control.compliance_status = 'non_compliant'
            flash(f'⚠️ Valeur hors spécification ({humidity_value}%) - F.N.C. requis (Spéc: 2%-3.5%)', 'warning')
        else:
            clay_control.compliance_status = 'compliant'
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Humidité après tamisage enregistrée avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/humidity_after_sieving.html', form=form)

@clay_bp.route('/humidity-after-prep', methods=['GET', 'POST'])
@login_required
def humidity_after_prep():
    form = HumidityAfterPrepForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl()
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.measurement_time_1 = form.measurement_time.data
        clay_control.humidity_after_prep = form.humidity_after_prep.data
        clay_control.notes = form.notes.data
        clay_control.controller_id = current_user.id
        
        # Check compliance
        humidity_value = form.humidity_after_prep.data
        if humidity_value is not None and (humidity_value < 5.3 or humidity_value > 6.3):
            clay_control.compliance_status = 'non_compliant'
            flash(f'⚠️ Valeur hors spécification ({humidity_value}%) - F.N.C. requis (Spéc: 5.3%-6.3%)', 'warning')
        else:
            clay_control.compliance_status = 'compliant'
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Humidité niveau silo enregistrée avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/humidity_after_prep.html', form=form)

@clay_bp.route('/granulometry', methods=['GET', 'POST'])
@login_required
def granulometry():
    form = GranulometryForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl()
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.measurement_time_1 = form.measurement_time.data
        clay_control.granulometry_refusal = form.granulometry_refusal.data
        clay_control.notes = form.notes.data
        clay_control.controller_id = current_user.id
        
        # Check compliance
        granulo_value = form.granulometry_refusal.data
        if granulo_value is not None and (granulo_value < 10 or granulo_value > 20):
            clay_control.compliance_status = 'non_compliant'
            flash(f'⚠️ Valeur hors spécification ({granulo_value}%) - F.N.C. requis (Spéc: 10%-20%)', 'warning')
        else:
            clay_control.compliance_status = 'compliant'
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('Granulométrie enregistrée avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/granulometry.html', form=form)

@clay_bp.route('/calcium-carbonate', methods=['GET', 'POST'])
@login_required
def calcium_carbonate():
    form = CalciumCarbonateForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl()
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.measurement_time_1 = form.measurement_time.data
        clay_control.calcium_carbonate = form.calcium_carbonate.data
        clay_control.notes = form.notes.data
        clay_control.controller_id = current_user.id
        
        # Check compliance
        calcium_value = form.calcium_carbonate.data
        if calcium_value is not None and (calcium_value < 15 or calcium_value > 25):
            clay_control.compliance_status = 'non_compliant'
            flash(f'⚠️ Valeur hors spécification ({calcium_value}%) - F.N.C. requis (Spéc: 15%-25%)', 'warning')
        else:
            clay_control.compliance_status = 'compliant'
        
        db.session.add(clay_control)
        db.session.commit()
        
        flash('% Chaux CaCO₃ enregistré avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/calcium_carbonate.html', form=form)

# Combined forms routes as requested by user
@clay_bp.route('/combined-humidity', methods=['GET', 'POST'])
@login_required
def combined_humidity():
    form = CombinedHumidityForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl()
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.measurement_time_1 = form.measurement_time_1.data
        clay_control.measurement_time_2 = form.measurement_time_2.data
        clay_control.humidity_before_prep = form.humidity_before_prep.data
        clay_control.humidity_after_sieving = form.humidity_after_sieving.data
        clay_control.humidity_after_prep = form.humidity_after_prep.data
        clay_control.notes = form.notes.data
        clay_control.controller_id = current_user.id
        
        # Check compliance for all humidity values
        compliance_issues = []
        overall_compliance = 'compliant'
        
        if form.humidity_before_prep.data:
            if form.humidity_before_prep.data < 2.5 or form.humidity_before_prep.data > 4.1:
                compliance_issues.append(f'Trémie générale ({form.humidity_before_prep.data}%) - Spéc: 2.5%-4.1%')
                overall_compliance = 'non_compliant'
                
        if form.humidity_after_sieving.data:
            if form.humidity_after_sieving.data < 2.0 or form.humidity_after_sieving.data > 3.5:
                compliance_issues.append(f'Après tamisage ({form.humidity_after_sieving.data}%) - Spéc: 2%-3.5%')
                overall_compliance = 'non_compliant'
                
        if form.humidity_after_prep.data:
            if form.humidity_after_prep.data < 5.3 or form.humidity_after_prep.data > 6.3:
                compliance_issues.append(f'Niveau silo ({form.humidity_after_prep.data}%) - Spéc: 5.3%-6.3%')
                overall_compliance = 'non_compliant'
        
        clay_control.compliance_status = overall_compliance
        
        db.session.add(clay_control)
        db.session.commit()
        
        if compliance_issues:
            flash(f'⚠️ Valeurs hors spécification: {", ".join(compliance_issues)} - F.N.C. requis', 'warning')
        
        # Check if export to Excel was requested
        if request.form.get('export_excel'):
            try:
                exporter = ExcelExporter()
                export_data = {
                    'date': form.date.data,
                    'shift': form.shift.data,
                    'controller': current_user.username,
                    'humidity_before_prep': form.humidity_before_prep.data,
                    'humidity_after_sieving': form.humidity_after_sieving.data,
                    'humidity_after_prep': form.humidity_after_prep.data,
                    'measurement_time_1': form.measurement_time_1.data,
                    'measurement_time_2': form.measurement_time_2.data,
                    'measurement_time_3': form.measurement_time_3.data,
                    'notes': form.notes.data
                }
                file_path, filename = exporter.export_humidity_data(export_data)
                flash(f'✅ Données exportées vers Excel: {filename}', 'success')
                return send_file(file_path, as_attachment=True, download_name=filename)
            except Exception as e:
                flash(f'❌ Erreur lors de l\'export Excel: {str(e)}', 'error')
        
        flash('Contrôles d\'humidité enregistrés avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/combined_humidity.html', form=form)

@clay_bp.route('/combined-analysis', methods=['GET', 'POST'])
@login_required
def combined_analysis():
    form = CombinedAnalysisForm()
    
    if form.validate_on_submit():
        clay_control = ClayControl()
        clay_control.date = form.date.data
        clay_control.shift = form.shift.data
        clay_control.granulometry_refusal = form.granulometry_refusal.data
        clay_control.calcium_carbonate = form.calcium_carbonate.data
        clay_control.notes = form.notes.data
        clay_control.controller_id = current_user.id
        
        # Check compliance for both analysis values
        compliance_issues = []
        overall_compliance = 'compliant'
        
        if form.granulometry_refusal.data:
            if form.granulometry_refusal.data < 10 or form.granulometry_refusal.data > 20:
                compliance_issues.append(f'Granulométrie ({form.granulometry_refusal.data}%) - Spéc: 10%-20%')
                overall_compliance = 'non_compliant'
                
        if form.calcium_carbonate.data:
            if form.calcium_carbonate.data < 15 or form.calcium_carbonate.data > 25:
                compliance_issues.append(f'CaCO₃ ({form.calcium_carbonate.data}%) - Spéc: 15%-25%')
                overall_compliance = 'non_compliant'
        
        clay_control.compliance_status = overall_compliance
        
        db.session.add(clay_control)
        db.session.commit()
        
        if compliance_issues:
            flash(f'⚠️ Valeurs hors spécification: {", ".join(compliance_issues)} - F.N.C. requis', 'warning')
        
        # Check if export to Excel was requested
        if request.form.get('export_excel'):
            try:
                exporter = ExcelExporter()
                export_data = {
                    'date': form.date.data,
                    'shift': form.shift.data,
                    'controller': current_user.username,
                    'granulometry_refusal': form.granulometry_refusal.data,
                    'calcium_carbonate': form.calcium_carbonate.data,
                    'granulometry_time': form.granulometry_time.data,
                    'calcium_time': form.calcium_time.data,
                    'notes': form.notes.data
                }
                file_path, filename = exporter.export_analysis_data(export_data)
                flash(f'✅ Données exportées vers Excel: {filename}', 'success')
                return send_file(file_path, as_attachment=True, download_name=filename)
            except Exception as e:
                flash(f'❌ Erreur lors de l\'export Excel: {str(e)}', 'error')
        
        flash('Analyses enregistrées avec succès', 'success')
        return redirect(url_for('clay.clay_controls'))
    
    return render_template('clay/combined_analysis.html', form=form)

# Control Sheet Generation Routes
@clay_bp.route('/generate-humidity-sheet')
@login_required
def generate_humidity_sheet():
    """Generate Fiche Contrôle Humidité"""
    return render_template('clay/humidity_control_sheet.html')

@clay_bp.route('/generate-clay-sheet') 
@login_required
def generate_clay_sheet():
    """Generate Fiche de Contrôle Argile"""
    return render_template('clay/clay_control_sheet.html')

