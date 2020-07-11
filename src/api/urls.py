from django.urls import include, path
from rest_framework import routers

from api.bigquery import views


router = routers.DefaultRouter()
router.register(r'bigquery/jobs', views.JobViewSet, basename='job')
urlpatterns = router.urls + [
    path('bigquery/<str:resource>/<str:dataset>/', include('api.bigquery.urls'))
]
