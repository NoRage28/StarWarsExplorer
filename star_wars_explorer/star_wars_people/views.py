from .models import Dataset
from .serializers import DatasetViewSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from .services import read_data_from_csv
from rest_framework.response import Response
from rest_framework import status
from .tasks import download_dataset_task


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetViewSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        file_name = serializer.data['name']
        file = read_data_from_csv(file_name=file_name)
        return Response(file, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def download_dataset(self, request):
        download_dataset_task.delay()
        return Response(status=status.HTTP_201_CREATED)
