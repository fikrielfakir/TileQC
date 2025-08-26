from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from services.scheduling_service import SchedulingService
from services.measurement_service import MeasurementService
from datetime import datetime, date
import logging

class AutomationService:
    """Background automation service using APScheduler"""
    
    def __init__(self, app=None):
        self.scheduler = None
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the automation service with Flask app"""
        self.app = app
        
        # Configure scheduler
        self.scheduler = BackgroundScheduler()
        
        # Add scheduled jobs
        self._add_scheduled_jobs()
        
        # Start scheduler
        try:
            self.scheduler.start()
            app.logger.info("Automation scheduler started successfully")
        except Exception as e:
            app.logger.error(f"Failed to start automation scheduler: {e}")
    
    def _add_scheduled_jobs(self):
        """Add all scheduled automation jobs"""
        
        # Generate tomorrow's schedule at midnight
        self.scheduler.add_job(
            func=self._generate_daily_schedule_job,
            trigger=CronTrigger(hour=0, minute=1),  # 00:01 every day
            id='generate_daily_schedule',
            name='Generate Daily Schedule',
            replace_existing=True
        )
        
        # Mark overdue controls every hour
        self.scheduler.add_job(
            func=self._mark_overdue_controls_job,
            trigger=CronTrigger(minute=0),  # Every hour at minute 0
            id='mark_overdue_controls',
            name='Mark Overdue Controls',
            replace_existing=True
        )
        
        # Generate weekly schedule on Sunday night
        self.scheduler.add_job(
            func=self._generate_weekly_schedule_job,
            trigger=CronTrigger(day_of_week=6, hour=23, minute=30),  # Sunday 23:30
            id='generate_weekly_schedule',
            name='Generate Weekly Schedule',
            replace_existing=True
        )
        
        # Cleanup old records monthly
        self.scheduler.add_job(
            func=self._cleanup_old_records_job,
            trigger=CronTrigger(day=1, hour=2, minute=0),  # 1st of month at 02:00
            id='cleanup_old_records',
            name='Cleanup Old Records',
            replace_existing=True
        )
    
    def _generate_daily_schedule_job(self):
        """Job to generate tomorrow's schedule"""
        with self.app.app_context():
            try:
                result = SchedulingService.generate_daily_schedule()
                self.app.logger.info(f"Daily schedule generated: {result['scheduled_count']} controls for {result['date']}")
            except Exception as e:
                self.app.logger.error(f"Failed to generate daily schedule: {e}")
    
    def _mark_overdue_controls_job(self):
        """Job to mark overdue controls"""
        with self.app.app_context():
            try:
                count = MeasurementService.mark_overdue_controls()
                if count > 0:
                    self.app.logger.info(f"Marked {count} controls as overdue")
            except Exception as e:
                self.app.logger.error(f"Failed to mark overdue controls: {e}")
    
    def _generate_weekly_schedule_job(self):
        """Job to generate weekly schedule"""
        with self.app.app_context():
            try:
                result = SchedulingService.generate_weekly_schedule()
                self.app.logger.info(f"Weekly schedule generated: {result['scheduled_count']} controls for week starting {result['date']}")
            except Exception as e:
                self.app.logger.error(f"Failed to generate weekly schedule: {e}")
    
    def _cleanup_old_records_job(self):
        """Job to cleanup old records (implement as needed)"""
        with self.app.app_context():
            try:
                # Implement cleanup logic here
                # For example, archive measurements older than 1 year
                self.app.logger.info("Old records cleanup completed")
            except Exception as e:
                self.app.logger.error(f"Failed to cleanup old records: {e}")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()
    
    def get_job_status(self):
        """Get status of all scheduled jobs"""
        if not self.scheduler:
            return {'status': 'not_initialized'}
        
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        
        return {
            'status': 'running' if self.scheduler.running else 'stopped',
            'jobs': jobs
        }
    
    def trigger_job_manually(self, job_id):
        """Manually trigger a scheduled job"""
        try:
            job = self.scheduler.get_job(job_id)
            if job:
                job.modify(next_run_time=datetime.now())
                return {'success': True, 'message': f'Job {job_id} triggered'}
            else:
                return {'success': False, 'error': f'Job {job_id} not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Global automation service instance
automation_service = AutomationService()