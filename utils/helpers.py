from datetime import datetime, date, timedelta
from models import *
from app import db
import json

def get_dashboard_stats(date_filter=None):
    """Get dashboard statistics for the specified date range"""
    if date_filter is None:
        date_filter = date.today()
    
    stats = {}
    
    # Clay controls
    clay_query = ClayControl.query.filter(ClayControl.date == date_filter)
    stats['clay'] = {
        'total': clay_query.count(),
        'compliant': clay_query.filter(ClayControl.compliance_status == 'compliant').count(),
        'non_compliant': clay_query.filter(ClayControl.compliance_status == 'non_compliant').count()
    }
    
    # Press controls
    press_query = PressControl.query.filter(PressControl.date == date_filter)
    stats['press'] = {
        'total': press_query.count(),
        'compliant': press_query.filter(PressControl.compliance_status == 'compliant').count(),
        'non_compliant': press_query.filter(PressControl.compliance_status == 'non_compliant').count()
    }
    
    # Dryer controls
    dryer_query = DryerControl.query.filter(DryerControl.date == date_filter)
    stats['dryer'] = {
        'total': dryer_query.count(),
        'compliant': dryer_query.filter(DryerControl.compliance_status == 'compliant').count(),
        'non_compliant': dryer_query.filter(DryerControl.compliance_status == 'non_compliant').count()
    }
    
    # Kiln controls
    biscuit_query = BiscuitKilnControl.query.filter(BiscuitKilnControl.date == date_filter)
    email_query = EmailKilnControl.query.filter(EmailKilnControl.date == date_filter)
    
    stats['biscuit_kiln'] = {
        'total': biscuit_query.count(),
        'compliant': biscuit_query.filter(BiscuitKilnControl.compliance_status == 'compliant').count(),
        'non_compliant': biscuit_query.filter(BiscuitKilnControl.compliance_status == 'non_compliant').count()
    }
    
    stats['email_kiln'] = {
        'total': email_query.count(),
        'compliant': email_query.filter(EmailKilnControl.compliance_status == 'compliant').count(),
        'non_compliant': email_query.filter(EmailKilnControl.compliance_status == 'non_compliant').count()
    }
    
    # Enamel controls
    enamel_query = EnamelControl.query.filter(EnamelControl.date == date_filter)
    stats['enamel'] = {
        'total': enamel_query.count(),
        'compliant': enamel_query.filter(EnamelControl.compliance_status == 'compliant').count(),
        'non_compliant': enamel_query.filter(EnamelControl.compliance_status == 'non_compliant').count()
    }
    
    # Calculate overall compliance rate
    total_tests = sum(stage['total'] for stage in stats.values())
    total_compliant = sum(stage['compliant'] for stage in stats.values())
    
    stats['overall'] = {
        'total': total_tests,
        'compliant': total_compliant,
        'non_compliant': total_tests - total_compliant,
        'compliance_rate': round((total_compliant / total_tests * 100) if total_tests > 0 else 0, 1)
    }
    
    return stats

def get_recent_non_conformities(limit=10):
    """Get recent non-conformities across all stages"""
    non_conformities = []
    
    # Clay controls
    clay_nc = ClayControl.query.filter(
        ClayControl.compliance_status == 'non_compliant'
    ).order_by(ClayControl.created_at.desc()).limit(limit).all()
    
    for nc in clay_nc:
        non_conformities.append({
            'type': 'Clay Control',
            'date': nc.date,
            'controller': nc.controller.full_name if nc.controller else 'Unknown',
            'status': nc.compliance_status,
            'created_at': nc.created_at
        })
    
    # Press controls
    press_nc = PressControl.query.filter(
        PressControl.compliance_status == 'non_compliant'
    ).order_by(PressControl.created_at.desc()).limit(limit).all()
    
    for nc in press_nc:
        non_conformities.append({
            'type': f'Press Control ({nc.format_type})',
            'date': nc.date,
            'controller': nc.controller.full_name if nc.controller else 'Unknown',
            'status': nc.compliance_status,
            'created_at': nc.created_at
        })
    
    # Sort by creation time and limit
    non_conformities.sort(key=lambda x: x['created_at'], reverse=True)
    return non_conformities[:limit]

def get_weekly_trend_data():
    """Get compliance trend data for the past 7 days"""
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    
    trend_data = []
    current_date = start_date
    
    while current_date <= end_date:
        stats = get_dashboard_stats(current_date)
        trend_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'compliance_rate': stats['overall']['compliance_rate']
        })
        current_date += timedelta(days=1)
    
    return trend_data

def get_format_distribution():
    """Get distribution of tests by tile format"""
    formats = {}
    
    # Press controls by format
    press_formats = db.session.query(
        PressControl.format_type,
        db.func.count(PressControl.id).label('count')
    ).group_by(PressControl.format_type).all()
    
    for format_type, count in press_formats:
        if format_type:
            formats[format_type] = formats.get(format_type, 0) + count
    
    # Dimensional tests by format
    dim_formats = db.session.query(
        DimensionalTest.format_type,
        db.func.count(DimensionalTest.id).label('count')
    ).group_by(DimensionalTest.format_type).all()
    
    for format_type, count in dim_formats:
        if format_type:
            formats[format_type] = formats.get(format_type, 0) + count
    
    return formats

def get_defect_analysis():
    """Get analysis of defect types across production stages"""
    defects = {}
    
    # Press defects
    press_defects = PressControl.query.all()
    defects['press'] = {
        'grains': sum(p.defect_grains or 0 for p in press_defects) / len(press_defects) if press_defects else 0,
        'cracks': sum(p.defect_cracks or 0 for p in press_defects) / len(press_defects) if press_defects else 0,
        'cleaning': sum(p.defect_cleaning or 0 for p in press_defects) / len(press_defects) if press_defects else 0,
        'foliage': sum(p.defect_foliage or 0 for p in press_defects) / len(press_defects) if press_defects else 0,
        'chipping': sum(p.defect_chipping or 0 for p in press_defects) / len(press_defects) if press_defects else 0,
    }
    
    # Biscuit kiln defects
    biscuit_defects = BiscuitKilnControl.query.all()
    defects['biscuit_kiln'] = {
        'cracks': sum(b.defect_cracks or 0 for b in biscuit_defects) / len(biscuit_defects) if biscuit_defects else 0,
        'chipping': sum(b.defect_chipping or 0 for b in biscuit_defects) / len(biscuit_defects) if biscuit_defects else 0,
        'cooking': sum(b.defect_cooking or 0 for b in biscuit_defects) / len(biscuit_defects) if biscuit_defects else 0,
        'foliage': sum(b.defect_foliage or 0 for b in biscuit_defects) / len(biscuit_defects) if biscuit_defects else 0,
        'flatness': sum(b.defect_flatness or 0 for b in biscuit_defects) / len(biscuit_defects) if biscuit_defects else 0,
    }
    
    return defects

def export_daily_report(report_date):
    """Export daily report data for specified date"""
    report_data = {
        'date': report_date.strftime('%Y-%m-%d'),
        'stats': get_dashboard_stats(report_date),
        'clay_controls': [],
        'press_controls': [],
        'dryer_controls': [],
        'biscuit_kiln_controls': [],
        'email_kiln_controls': [],
        'enamel_controls': [],
        'dimensional_tests': [],
        'digital_decorations': [],
        'external_tests': []
    }
    
    # Get all controls for the date
    clay_controls = ClayControl.query.filter(ClayControl.date == report_date).all()
    for control in clay_controls:
        report_data['clay_controls'].append({
            'id': control.id,
            'shift': control.shift,
            'humidity_before_prep': control.humidity_before_prep,
            'humidity_after_sieving': control.humidity_after_sieving,
            'humidity_after_prep': control.humidity_after_prep,
            'granulometry_refusal': control.granulometry_refusal,
            'calcium_carbonate': control.calcium_carbonate,
            'compliance_status': control.compliance_status,
            'controller': control.controller.full_name if control.controller else 'Unknown'
        })
    
    # Similar for other control types...
    
    return report_data

def calculate_process_capability(measurements, lower_limit, upper_limit):
    """Calculate process capability indices (Cp, Cpk)"""
    if not measurements or len(measurements) < 2:
        return None
    
    import statistics
    
    mean = statistics.mean(measurements)
    std_dev = statistics.stdev(measurements)
    
    if std_dev == 0:
        return None
    
    # Cp = (USL - LSL) / (6 * σ)
    cp = (upper_limit - lower_limit) / (6 * std_dev)
    
    # Cpk = min((USL - μ) / (3 * σ), (μ - LSL) / (3 * σ))
    cpk_upper = (upper_limit - mean) / (3 * std_dev)
    cpk_lower = (mean - lower_limit) / (3 * std_dev)
    cpk = min(cpk_upper, cpk_lower)
    
    return {
        'cp': round(cp, 3),
        'cpk': round(cpk, 3),
        'mean': round(mean, 3),
        'std_dev': round(std_dev, 3)
    }

def get_control_chart_data(model_class, parameter, days=30):
    """Get control chart data for a specific parameter"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    query = model_class.query.filter(
        model_class.date.between(start_date, end_date)
    ).order_by(model_class.date)
    
    data = []
    for record in query:
        value = getattr(record, parameter, None)
        if value is not None:
            data.append({
                'date': record.date.strftime('%Y-%m-%d'),
                'value': value,
                'compliance': record.compliance_status
            })
    
    return data
