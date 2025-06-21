from django.core.management.base import BaseCommand
from reports.models import Report
from reports.views import get_address  # reuse your existing function

class Command(BaseCommand):
    help = 'Update the address field for all existing reports'

    def handle(self, *args, **kwargs):
        reports = Report.objects.all()
        total = reports.count()
        self.stdout.write(f'Starting update for {total} reports...')

        updated_count = 0
        for report in reports:
            if report.location:
                try:
                    lat_str, lng_str = report.location.split(',')
                    lat = float(lat_str.strip())
                    lng = float(lng_str.strip())

                    address = get_address(lat, lng)
                    report.address = address
                    report.save()
                    updated_count += 1
                    self.stdout.write(f'Updated report ID {report.id}')
                except Exception as e:
                    self.stderr.write(f'Error updating report ID {report.id}: {e}')
            else:
                self.stderr.write(f'Report ID {report.id} has no location')

        self.stdout.write(self.style.SUCCESS(f'Finished updating {updated_count} reports out of {total}'))
