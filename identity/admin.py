from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from identity.models import User


# Кастомная админка для модели User
# Расширяет стандартный UserAdmin для поддержки дополнительных полей и кастомного поиска
class UserAdmin(BaseUserAdmin):
    # Поле ID доступно только для чтения (неизменяемое)
    readonly_fields = ('id',)
    # Отображаемые поля в списке пользователей
    list_display = ('id', 'username', 'email', 'last_name')
    # Поля для поиска через стандартную панель поиска
    search_fields = ('username', 'last_name', 'email')
    # Группировка полей при редактировании пользователя
    fieldsets = (
        (None, {'fields': ('id', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'patronymic')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )
    # Группировка полей при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'patronymic')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        })
    )

    # Расширенный поиск с поддержкой префиксов (user:/last_name:/email:/id:)
    def get_search_results(self, request, queryset, search_term):
        if search_term:
            if search_term.startswith('user:'):
                search_term = search_term[5:]
                queryset = queryset.filter(username__icontains=search_term)
            elif search_term.startswith('last_name:'):
                search_term = search_term[10:]
                queryset = queryset.filter(last_name__icontains=search_term)
            elif search_term.startswith('email:'):
                search_term = search_term[6:]
                queryset = queryset.filter(email__icontains=search_term)
            elif search_term.startswith('id:'):
                search_term = search_term[3:]
                queryset = queryset.filter(id__icontains=search_term)
            else:
                queryset = super().get_search_results(request, queryset, search_term)[0]
        # Возвращаем отфильтрованный queryset и его количество
        return queryset, queryset.count()


# Регистрация кастомной админки для модели User
admin.site.register(User, UserAdmin)
