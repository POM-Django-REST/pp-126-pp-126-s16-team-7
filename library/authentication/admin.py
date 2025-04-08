from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from rest_framework.authtoken.models import Token 

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'middle_name', 'last_name', 'is_staff', 'role')  # Додали 'role' у список
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Role'), {'fields': ['role']}),  # Використовуємо список для 'role'
        (_('Token'), {'fields': ['token_key']}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser', 'role'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'token_key') 

    def token_key(self, obj):
        """
        Функція для отримання токену користувача.
        """
        token, created = Token.objects.get_or_create(user=obj)  # Створюємо токен, якщо він не існує
        return token.key  # Повертаємо токен як значення
    token_key.short_description = 'Token'

    def generate_token(self, request, queryset):
        """Метод для генерації токену для вибраних користувачів."""
        for user in queryset:
            token, created = Token.objects.get_or_create(user=user)
            self.message_user(request, f'Token для користувача {user.email} згенеровано: {token.key}')
        self.save_model(request, queryset)

    generate_token.short_description = 'Generate Token for selected users'
    actions = ['generate_token']
    