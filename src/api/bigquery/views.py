from google.cloud import bigquery
from rest_framework import mixins, response, viewsets

from api.bigquery import serializers
from jobs import models


class BigQueryViewSet(viewsets.ViewSet):
    lookup_field = 'table_name'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = bigquery.Client()

    def retrieve(self, request, *args, **kwargs):
        """
        Construct a QueryJob for BigQuery and track it internally with
        the Job model. When constructing the QueryJob, we will attach a callback
        to perform post-query processing (see jobs.models.Job.Callback).
        """
        query = self.get_query()
        query_job = self.client.query(query)
        job = models.Job.objects.create(
            job_id=query_job.job_id,
            query=query_job.query
        )
        query_job.add_done_callback(models.Job.callback)
        serializer = serializers.JobSerializer(
            instance=job,
            context={
                'request': request
            }
        )
        return response.Response(serializer.data)

    """
    Helper methods for building the query
    """
    def get_query(self):
        dataset = f'{self.kwargs.get("resource")}.{self.kwargs.get("dataset")}'
        table_name = self.kwargs.get('table_name')
        query = f'SELECT * FROM {dataset}.{table_name}'
        return self.filter_query(query)

    def filter_query(self, query):
        if not self.request.query_params:
            return query
        filters = ' AND'.join([f'{k}={v}' for k, v in self.request.query_params.items()])
        return f'{query} WHERE {filters}'


class JobViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin
                 ):
    lookup_field = 'job_id'
    serializer_class = serializers.JobSerializer
    queryset = models.Job.objects.all()
