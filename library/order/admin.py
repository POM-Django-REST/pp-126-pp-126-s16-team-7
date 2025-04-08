from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at', 'plated_end_at', 'end_at')
    list_filter = ('user', 'book', 'plated_end_at', 'end_at')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Інформація про замовлення', {
            'fields': ('user', 'book', 'plated_end_at', 'end_at')
        }),
        ('Службове', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
