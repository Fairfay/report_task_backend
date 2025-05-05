from django.contrib import admin

from referential.models import (
    Delivery, File,
    Status, Service,
    Packaging, Transport
)

#Аналогично с identity/admin
class DeliveryAdmin(admin.ModelAdmin):
    search_fields = ['id']
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_display = (
        'id', 'operator',
        'transport', 'number',
        'delivery_time', 'departure_time',
        'distance', 'packaging',
        'status', 'technical_state',
        'created_at', 'updated_at',
        'services_list', 'file_list',
    )

    def services_list(self, obj):
        return ", ".join([service.name for service in obj.services.all()])
    services_list.short_description = 'Услуги'

    def file_list(self, obj):
        return ", ".join([f.file.name for f in obj.file.all()])
    file_list.short_description = 'Файлы'


class TransportAdmin(admin.ModelAdmin):
    search_fields = ['brand']
    readonly_fields = ('id',)
    list_display = ('id', 'brand')


class StatusAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'color')


class ServiceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ('id',)
    list_display = ('id', 'name')


class PackagingAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ('id',)
    list_display = ('id', 'name')


admin.site.register(File)
admin.site.register(Packaging, PackagingAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(Delivery, DeliveryAdmin)
