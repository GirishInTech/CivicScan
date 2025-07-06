from django.core.management.base import BaseCommand
from reports.models import Report, Hotspot
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Detects hotspots from dirty cleanliness reports and updates the Hotspot model.'

    def handle(self, *args, **kwargs):
        # Step 1: Filter dirty reports
        reports = Report.objects.filter(status='dirty')

        if not reports.exists():
            self.stdout.write(self.style.WARNING("No dirty reports found."))
            return

        # Step 2: Parse lat/long from location string
        records = []
        for report in reports:
            try:
                lat, lng = map(float, report.location.split(','))
                records.append({
                    'latitude': lat,
                    'longitude': lng,
                    'address': report.address,
                    'submitted_at': report.submitted_at
                })
            except ValueError:
                continue  # skip invalid location

        if not records:
            self.stdout.write(self.style.WARNING("No valid lat/lng data found."))
            return

        df = pd.DataFrame(records)

        # Step 3: DBSCAN clustering
        coords = np.radians(df[['latitude', 'longitude']])
        kms_per_radian = 6371.0088
        epsilon = 2 / kms_per_radian  # 500 meters

        db = DBSCAN(eps=epsilon, min_samples=2, algorithm='ball_tree', metric='haversine')
        df['cluster'] = db.fit_predict(coords)

        # Step 4: Clean existing hotspots
        Hotspot.objects.all().delete()

        # Step 5: Save new hotspots
        grouped = df[df['cluster'] != -1].groupby('cluster')

        for cluster_id, group in grouped:
            Hotspot.objects.create(
                cluster_id=cluster_id,
                latitude=group['latitude'].mean(),
                longitude=group['longitude'].mean(),
                report_count=len(group),
                address=group['address'].iloc[0]
            )

        self.stdout.write(self.style.SUCCESS(f"{len(grouped)} hotspot(s) detected and saved."))
