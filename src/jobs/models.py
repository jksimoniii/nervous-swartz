import os

from django.db import models
from google.cloud import bigquery


class Job(models.Model):
    job_id = models.CharField(max_length=256)
    finished = models.BooleanField(default=False)
    query = models.TextField()
    resource_url = models.URLField(blank=True, null=True)

    @classmethod
    def callback(cls, future):
        """
        When a QueryJob completes, extract the temporary table to a CSV
        stored in GCP
        """
        if future.job_type != 'query':
            return
        bucket = os.environ.get('GCP_BUCKET')
        filename = f'{future.job_id}.csv'
        client = bigquery.Client()
        extract_job = client.extract_table(
            future.destination,
            f'gs://{bucket}/{filename}',
            location='US'
        )
        extract_job.result()
        cls.objects.update_or_create(
            job_id=future.job_id,
            defaults={
                'finished': True,
                'resource_url': f'https://{bucket}.storage.googleapis.com/{filename}'
            },
        )

