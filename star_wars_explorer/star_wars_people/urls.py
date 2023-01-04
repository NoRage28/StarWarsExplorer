from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, StatusTaskApiView
from django.urls import path

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

urlpatterns = [
    path('status_task/', StatusTaskApiView.as_view())
]
urlpatterns += router.urls
