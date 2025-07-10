from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from common.models import APILog


class Command(BaseCommand):
    help = 'Clean up old API logs from the database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete logs older than this many days (default: 30)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Get logs to delete
        logs_to_delete = APILog.objects.filter(
            request_timestamp__lt=cutoff_date
        )
        
        count = logs_to_delete.count()
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} API logs older than {days} days'
                )
            )
            if count > 0:
                self.stdout.write(
                    f'Oldest log: {logs_to_delete.earliest("request_timestamp").request_timestamp}'
                )
                self.stdout.write(
                    f'Newest log to delete: {logs_to_delete.latest("request_timestamp").request_timestamp}'
                )
        else:
            if count > 0:
                logs_to_delete.delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully deleted {count} API logs older than {days} days'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'No API logs older than {days} days found'
                    )
                ) 