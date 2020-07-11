from rest_framework import serializers

from jobs import models


class JobSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(lookup_field='job_id', view_name='job-detail')

    class Meta:
        model = models.Job
        exclude = ('job_id',)
