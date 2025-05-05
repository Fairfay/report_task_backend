from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from django.db.models.functions import ExtractYear, ExtractDay, ExtractMonth

from referential.models import Delivery, Transport, File, Service, Status, Packaging
from referential.serializers import (
    DeliverySerializer, TransportSerializer,
    FileSerializer, ServiceSerializer, 
    StatusSerializer, PackagingSerializer
)


class DeliveryViewSet(viewsets.ModelViewSet):
    '''Основной CRUD для доставок'''

    # Оптимизация запросов:
    # - select_related для ForeignKey
    # - prefetch_related для ManyToMany
    queryset = Delivery.objects.select_related(
        'transport',
        'operator',
        'packaging',
    ).prefetch_related(
        'file',
        'services',
    ).all()
    serializer_class = DeliverySerializer
    permission_classes = [
        IsAuthenticated,
    ]
    pagination_class = PageNumberPagination 

    def list(self, request):
        queryset = self.get_queryset()
        transport_id = self.request.query_params.get('transport')
        service_id = self.request.query_params.get('service')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        # Фильтрация по параметрам запроса
        if transport_id:
            queryset = queryset.filter(transport=transport_id)
        if service_id:
            queryset = queryset.filter(services=service_id)
        if date_from and date_to:
            if date_from != date_to:
                queryset = queryset.filter(delivery_time__gte=date_from, delivery_time__lte=date_to)
            else:
                queryset = queryset.filter(delivery_time__date=date_from)
        # Пагинация
        page = self.paginate_queryset(queryset)
        serializer = DeliverySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    def perform_create(self, serializer):
        '''Автоматическое проставление оператора при создании'''
        serializer.save(operator=self.request.user)

class StatisticsViewSet(viewsets.ModelViewSet):
    """
    Генерация статистики по доставкам
    Пример ответа: [{"year": 2023, "month": 9, "day": 15, "count": 25}]
    """
    pagination_class = None
    queryset = Delivery.objects.select_related(
        'transport',
        'operator',
        'packaging',
    ).prefetch_related(
        'file',
        'services',
    ).all()
    permission_classes = [
        IsAuthenticated,
    ]

    def list(self, request):
        '''Статистика по дням с фильтрацией'''
        queryset = self.get_queryset()
        transport_id = self.request.query_params.get('transport')
        service_id = self.request.query_params.get('service')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if transport_id:
            queryset = queryset.filter(transport=transport_id)
        if service_id:
            queryset = queryset.filter(services=service_id)
        if date_from and date_to:
            if date_from != date_to:
                queryset = queryset.filter(delivery_time__gte=date_from, delivery_time__lte=date_to)
            else:
                queryset = queryset.filter(delivery_time__date=date_from)
        # Группировка по дате и подсчет
        stats = (
            queryset
            .annotate(year=ExtractYear('delivery_time'))
            .annotate(month=ExtractMonth('delivery_time'))
            .annotate(day=ExtractDay('delivery_time'))
            .values('year', 'month', 'day')
            .annotate(count=Count('id'))
            .order_by('year', 'month', 'day')
        )

        response_data = [
            {
                'year': item['year'],
                'month': item['month'],
                'day': item['day'],
                'count': item['count']
            }
            for item in stats
        ]
        return Response(response_data)


class TransportViewSet(viewsets.ReadOnlyModelViewSet):
    '''Предоставляет список транспорта'''
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class ServiceViewSet(viewsets.ModelViewSet):
    '''CRUD для дополнительных услуг'''
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class StatusViewSet(viewsets.ModelViewSet):
    '''CRUD для статусов доставки'''
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class PackagingViewSet(viewsets.ModelViewSet):
    '''CRUD для типов упаковки'''
    queryset = Packaging.objects.all()
    serializer_class = PackagingSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class FileUploadAPIView(APIView):
    '''Загрузка файлов (одного или нескольких)'''
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        '''Обработка множественной загрузки файлов'''
        files = request.FILES.getlist('file')
        response_data = []

        for file in files:
            data = {'file': file}
            serializer = FileSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data.append(serializer.data)

        return Response(response_data, status=status.HTTP_201_CREATED)


class FileViewSet(viewsets.ModelViewSet):
    '''
    Используется для вывода и удаления файлов - модель 'File'.
    '''
    http_method_names = ['get', 'delete']
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def destroy(self, request, *args, **kwargs):
        '''Удаление файла'''
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
