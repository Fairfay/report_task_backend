from rest_framework import serializers

from server.settings import DATETIME_FORMAT
from referential.models import (
    Delivery, Transport,
    Packaging, Service,
    Status, File,
)
from identity.models import User


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
        read_only_fields = ('created_at', 'id')


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
    transport = serializers.PrimaryKeyRelatedField(queryset=Transport.objects.all())
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
    packaging = serializers.PrimaryKeyRelatedField(queryset=Packaging.objects.all())
    file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), many=True)
    operator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

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
