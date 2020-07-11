from rest_framework import routers

from api.bigquery import views

router = routers.DefaultRouter()
router.register(r'tables', views.BigQueryViewSet, basename='table')
urlpatterns = router.urls
