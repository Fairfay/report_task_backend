from rest_framework import serializers

from server.settings import DATETIME_FORMAT
from referential.models import (
    Delivery, Transport,
    Packaging, Service,
    Status, File,
)


class FileSerializer(serializers.ModelSerializer):
    '''
    Обслуживает модель "File",
    используется при работе с файлами.
    '''

    created_at = serializers.DateTimeField(
        read_only=True,
        format=DATETIME_FORMAT
    )

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('created_at')


class TransportSerializer(serializers.ModelSerializer):
    '''Обслуживает модель "Transport".'''

    class Meta:
        model = Transport
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    '''Обслуживает модель "Delivery".'''

    created_at = serializers.DateTimeField(
        read_only=True,
        format=DATETIME_FORMAT
    )
    file = FileSerializer(
        many=True,
        read_only=True
    )
    transport = serializers.StringRelatedField()
    services = serializers.StringRelatedField(
        many=True,
    )

    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class StatusSerializer(serializers.ModelSerializer):
    '''Обслуживает модель "Status".'''

    class Meta:
        model = Status
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    '''Обслуживает модель "Service".'''

    class Meta:
        model = Service
        fields = '__all__'


class PackagingSerializer(serializers.ModelSerializer):
    '''Обслуживает модель "Packaging".'''

    class Meta:
        model = Packaging
        fields = '__all__'
