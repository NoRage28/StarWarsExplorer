from .models import Dataset
from .serializers import DatasetViewSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from .services import read_data_from_csv, start_download_dataset_task
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from rest_framework import views


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetViewSerializer

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        file_name = serializer.data['name']
        file = read_data_from_csv(file_name=file_name)
        return Response(file, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def download_dataset(self, request) -> Response:
        cache_task_key = start_download_dataset_task()
        return Response(cache_task_key, status=status.HTTP_201_CREATED)


class StatusTaskApiView(views.APIView):
    def get(self, request, format=None):
        task_id = self.request.query_params['task_id']
        task_status = cache.get(task_id)
        return Response(task_status, status=status.HTTP_200_OK)
