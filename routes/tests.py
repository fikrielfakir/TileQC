from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from forms import DimensionalTestForm, DigitalDecorationForm, ExternalTestForm
from models import DimensionalTest, DigitalDecoration, ExternalTest
from app import db

tests_bp = Blueprint('tests', __name__)

@tests_bp.route('/dimensional')
@login_required
def dimensional_tests():
    page = request.args.get('page', 1, type=int)
    format_filter = request.args.get('format')
    
    query = DimensionalTest.query
    if format_filter:
        query = query.filter(DimensionalTest.format_type == format_filter)
    
    tests = query.order_by(DimensionalTest.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('tests/dimensional_tests.html', tests=tests, format_filter=format_filter)

@tests_bp.route('/dimensional/add', methods=['GET', 'POST'])
@login_required
def add_dimensional_test():
    form = DimensionalTestForm()
    
    if form.validate_on_submit():
        dimensional_test = DimensionalTest(
            date=form.date.data,
            format_type=form.format_type.data,
            central_curvature=form.central_curvature.data,
            veil=form.veil.data,
            angularity=form.angularity.data,
            edge_straightness=form.edge_straightness.data,
            lateral_curvature=form.lateral_curvature.data,
            tiles_tested=form.tiles_tested.data,
            defect_free_tiles=form.defect_free_tiles.data,
            surface_area_tested=form.surface_area_tested.data,
            lighting_level=form.lighting_level.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(dimensional_test)
        db.session.commit()
        
        flash('Enregistrement du test dimensionnel ajouté avec succès', 'success')
        return redirect(url_for('tests.dimensional_tests'))
    
    return render_template('tests/dimensional_tests.html', form=form)

@tests_bp.route('/dimensional/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dimensional_test(id):
    dimensional_test = DimensionalTest.query.get_or_404(id)
    form = DimensionalTestForm(obj=dimensional_test)
    
    if form.validate_on_submit():
        dimensional_test.date = form.date.data
        dimensional_test.format_type = form.format_type.data
        dimensional_test.central_curvature = form.central_curvature.data
        dimensional_test.veil = form.veil.data
        dimensional_test.angularity = form.angularity.data
        dimensional_test.edge_straightness = form.edge_straightness.data
        dimensional_test.lateral_curvature = form.lateral_curvature.data
        dimensional_test.tiles_tested = form.tiles_tested.data
        dimensional_test.defect_free_tiles = form.defect_free_tiles.data
        dimensional_test.surface_area_tested = form.surface_area_tested.data
        dimensional_test.lighting_level = form.lighting_level.data
        dimensional_test.notes = form.notes.data
        
        db.session.commit()
        
        flash('Enregistrement du test dimensionnel mis à jour avec succès', 'success')
        return redirect(url_for('tests.dimensional_tests'))
    
    return render_template('tests/dimensional_tests.html', form=form, edit=True, test=dimensional_test)

@tests_bp.route('/digital')
@login_required
def digital_decorations():
    page = request.args.get('page', 1, type=int)
    decorations = DigitalDecoration.query.order_by(DigitalDecoration.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('tests/digital_decoration.html', decorations=decorations)

@tests_bp.route('/digital/add', methods=['GET', 'POST'])
@login_required
def add_digital_decoration():
    form = DigitalDecorationForm()
    
    if form.validate_on_submit():
        digital_decoration = DigitalDecoration(
            date=form.date.data,
            shift=form.shift.data,
            measurement_number=form.measurement_number.data,
            sharpness=form.sharpness.data,
            offset=form.offset.data,
            tonality=form.tonality.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(digital_decoration)
        db.session.commit()
        
        flash('Enregistrement de décoration numérique ajouté avec succès', 'success')
        return redirect(url_for('tests.digital_decorations'))
    
    return render_template('tests/digital_decoration.html', form=form)

@tests_bp.route('/external')
@login_required
def external_tests():
    page = request.args.get('page', 1, type=int)
    test_filter = request.args.get('test_type')
    
    query = ExternalTest.query
    if test_filter:
        query = query.filter(ExternalTest.test_type == test_filter)
    
    tests = query.order_by(ExternalTest.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('tests/external_tests.html', tests=tests, test_filter=test_filter)

@tests_bp.route('/external/add', methods=['GET', 'POST'])
@login_required
def add_external_test():
    form = ExternalTestForm()
    
    if form.validate_on_submit():
        external_test = ExternalTest(
            date=form.date.data,
            test_type=form.test_type.data,
            iso_standard=form.iso_standard.data,
            result_value=form.result_value.data,
            result_status=form.result_status.data,
            test_report_number=form.test_report_number.data,
            laboratory=form.laboratory.data,
            notes=form.notes.data,
            controller_id=current_user.id
        )
        
        db.session.add(external_test)
        db.session.commit()
        
        flash('Enregistrement du test externe ajouté avec succès', 'success')
        return redirect(url_for('tests.external_tests'))
    
    return render_template('tests/external_tests.html', form=form)
