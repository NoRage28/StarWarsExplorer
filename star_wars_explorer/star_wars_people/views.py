from .models import Dataset
from rest_framework import viewsets
from rest_framework.decorators import action
from .services import CSVDataWriterAndDBSaver
from rest_framework.response import Response
from rest_framework import status


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()

    @action(detail=False, methods=['post'])
    def download_dataset(self, request):
        file_saver = CSVDataWriterAndDBSaver()
        file_saver.write_data_and_save_to_db()
        return Response(status=status.HTTP_201_CREATED)
