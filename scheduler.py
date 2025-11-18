"""
Scheduler Module
Schedule recordings to run at specific times
"""

import schedule
import time
import threading
import json
import os
from datetime import datetime


class AutomationScheduler:
    def __init__(self, player, recording_manager):
        self.player = player
        self.recording_manager = recording_manager
        self.jobs = []
        self.running = False
        self.scheduler_thread = None
        self.schedule_file = "schedule_config.json"

    def add_job(self, job_id, slot_name, schedule_type, schedule_value, enabled=True):
        """
        Add a scheduled job

        Args:
            job_id: Unique job identifier
            slot_name: Recording slot to play
            schedule_type: Type of schedule ('time', 'interval', 'daily', 'hourly')
            schedule_value: Value for schedule (e.g., "14:30", "30" for minutes)
            enabled: Whether job is enabled
        """
        job = {
            'id': job_id,
            'slot_name': slot_name,
            'schedule_type': schedule_type,
            'schedule_value': schedule_value,
            'enabled': enabled,
            'last_run': None,
            'run_count': 0
        }

        # Remove existing job with same ID
        self.jobs = [j for j in self.jobs if j['id'] != job_id]

        self.jobs.append(job)
        self._schedule_job(job)

        print(f"Job '{job_id}' scheduled: {schedule_type} {schedule_value}")
        return job

    def _schedule_job(self, job):
        """Internal method to schedule a job"""
        if not job['enabled']:
            return

        slot_name = job['slot_name']
        schedule_type = job['schedule_type']
        schedule_value = job['schedule_value']

        def job_func():
            self._execute_job(job)

        if schedule_type == 'time':
            # Run at specific time daily (e.g., "14:30")
            schedule.every().day.at(schedule_value).do(job_func).tag(job['id'])

        elif schedule_type == 'interval':
            # Run every X minutes
            minutes = int(schedule_value)
            schedule.every(minutes).minutes.do(job_func).tag(job['id'])

        elif schedule_type == 'hourly':
            # Run every hour at specific minute (e.g., ":30")
            schedule.every().hour.at(schedule_value).do(job_func).tag(job['id'])

        elif schedule_type == 'daily':
            # Run daily at specific time
            schedule.every().day.at(schedule_value).do(job_func).tag(job['id'])

        elif schedule_type == 'weekday':
            # Run on specific weekday (e.g., "monday" at "14:30")
            weekday, time_str = schedule_value.split('@')
            getattr(schedule.every(), weekday.lower()).at(time_str).do(job_func).tag(job['id'])

    def _execute_job(self, job):
        """Execute a scheduled job"""
        print(f"\n[SCHEDULER] Executing job '{job['id']}'")
        print(f"[SCHEDULER] Slot: {job['slot_name']}")

        try:
            actions = self.recording_manager.load_recording(job['slot_name'])
            if actions:
                self.player.load_actions(actions)
                self.player.play()

                # Update job stats
                job['last_run'] = datetime.now().isoformat()
                job['run_count'] += 1

                print(f"[SCHEDULER] Job completed successfully")
                self.save_schedule()
            else:
                print(f"[SCHEDULER] Error: Could not load recording '{job['slot_name']}'")

        except Exception as e:
            print(f"[SCHEDULER] Error executing job: {e}")

    def remove_job(self, job_id):
        """Remove a scheduled job"""
        self.jobs = [j for j in self.jobs if j['id'] != job_id]
        schedule.clear(job_id)
        print(f"Job '{job_id}' removed")
        self.save_schedule()

    def enable_job(self, job_id):
        """Enable a job"""
        for job in self.jobs:
            if job['id'] == job_id:
                job['enabled'] = True
                self._schedule_job(job)
                print(f"Job '{job_id}' enabled")
                self.save_schedule()
                return True
        return False

    def disable_job(self, job_id):
        """Disable a job"""
        for job in self.jobs:
            if job['id'] == job_id:
                job['enabled'] = False
                schedule.clear(job_id)
                print(f"Job '{job_id}' disabled")
                self.save_schedule()
                return True
        return False

    def list_jobs(self):
        """List all scheduled jobs"""
        return self.jobs.copy()

    def start(self):
        """Start the scheduler"""
        if self.running:
            print("Scheduler is already running")
            return

        self.running = True

        def run_scheduler():
            print("\n[SCHEDULER] Started")
            while self.running:
                schedule.run_pending()
                time.sleep(1)
            print("\n[SCHEDULER] Stopped")

        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        print("Stopping scheduler...")

    def save_schedule(self, filename=None):
        """Save schedule configuration to file"""
        if filename is None:
            filename = self.schedule_file

        with open(filename, 'w') as f:
            json.dump(self.jobs, f, indent=2)

        print(f"Schedule saved to {filename}")

    def load_schedule(self, filename=None):
        """Load schedule configuration from file"""
        if filename is None:
            filename = self.schedule_file

        if not os.path.exists(filename):
            print(f"No schedule file found at {filename}")
            return

        try:
            with open(filename, 'r') as f:
                self.jobs = json.load(f)

            # Re-schedule all enabled jobs
            schedule.clear()
            for job in self.jobs:
                if job['enabled']:
                    self._schedule_job(job)

            print(f"Schedule loaded from {filename}")
            print(f"Loaded {len(self.jobs)} jobs")

        except Exception as e:
            print(f"Error loading schedule: {e}")

    def get_next_run_times(self):
        """Get next run times for all scheduled jobs"""
        next_runs = []

        for job in schedule.get_jobs():
            next_run = schedule.idle_seconds()
            if next_run is not None:
                next_runs.append({
                    'job_id': list(job.tags)[0] if job.tags else 'unknown',
                    'next_run_seconds': next_run
                })

        return next_runs

    def clear_all(self):
        """Clear all scheduled jobs"""
        self.jobs = []
        schedule.clear()
        print("All scheduled jobs cleared")
        self.save_schedule()


class ScheduleBuilder:
    """Helper class to build schedules easily"""

    @staticmethod
    def every_n_minutes(n):
        """Schedule every N minutes"""
        return ('interval', str(n))

    @staticmethod
    def daily_at(time_str):
        """Schedule daily at specific time (e.g., "14:30")"""
        return ('daily', time_str)

    @staticmethod
    def hourly_at(minute):
        """Schedule hourly at specific minute (e.g., ":30")"""
        return ('hourly', f":{minute:02d}")

    @staticmethod
    def on_weekday_at(weekday, time_str):
        """Schedule on specific weekday (e.g., "monday", "14:30")"""
        return ('weekday', f"{weekday}@{time_str}")

    @staticmethod
    def at_time(time_str):
        """Schedule at specific time daily (e.g., "14:30")"""
        return ('time', time_str)
