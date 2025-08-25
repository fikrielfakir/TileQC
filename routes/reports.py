from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from utils.helpers import get_dashboard_stats, export_daily_report, get_defect_analysis
from datetime import date, timedelta
import json

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
def reports_dashboard():
    return render_template('reports/daily_report.html')

@reports_bp.route('/daily')
@login_required
def daily_report():
    report_date = request.args.get('date')
    if report_date:
        try:
            selected_date = date.fromisoformat(report_date)
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()
    
    # Get comprehensive report data
    report_data = export_daily_report(selected_date)
    
    return render_template('reports/daily_report.html', 
                         report_data=report_data, 
                         selected_date=selected_date)

@reports_bp.route('/weekly')
@login_required
def weekly_report():
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    
    weekly_stats = []
    current_date = start_date
    
    while current_date <= end_date:
        daily_stats = get_dashboard_stats(current_date)
        weekly_stats.append({
            'date': current_date,
            'stats': daily_stats
        })
        current_date += timedelta(days=1)
    
    return render_template('reports/weekly_report.html', weekly_stats=weekly_stats)

@reports_bp.route('/monthly')
@login_required
def monthly_report():
    end_date = date.today()
    start_date = end_date.replace(day=1)
    
    monthly_stats = get_dashboard_stats()  # Will need to modify helper for date range
    defect_analysis = get_defect_analysis()
    
    return render_template('reports/monthly_report.html', 
                         monthly_stats=monthly_stats,
                         defect_analysis=defect_analysis,
                         start_date=start_date,
                         end_date=end_date)

@reports_bp.route('/non_conformities')
@login_required
def non_conformities():
    from utils.helpers import get_recent_non_conformities
    
    limit = request.args.get('limit', 50, type=int)
    non_conformities = get_recent_non_conformities(limit)
    
    return render_template('reports/non_conformities.html', 
                         non_conformities=non_conformities)

@reports_bp.route('/api/export/daily/<date_str>')
@login_required
def export_daily_json(date_str):
    try:
        report_date = date.fromisoformat(date_str)
        report_data = export_daily_report(report_date)
        return jsonify(report_data)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

@reports_bp.route('/spc_charts')
@login_required
def spc_charts():
    from utils.helpers import get_control_chart_data
    from models import ClayControl, PressControl, DryerControl
    
    # Get SPC data for key parameters
    clay_humidity = get_control_chart_data(ClayControl, 'humidity_after_prep', days=30)
    press_thickness = get_control_chart_data(PressControl, 'thickness', days=30)
    dryer_humidity = get_control_chart_data(DryerControl, 'residual_humidity', days=30)
    
    return render_template('reports/spc_charts.html',
                         clay_humidity=json.dumps(clay_humidity),
                         press_thickness=json.dumps(press_thickness),
                         dryer_humidity=json.dumps(dryer_humidity))
