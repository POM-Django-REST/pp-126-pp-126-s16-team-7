from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_authors', 'count')  
    list_filter = ('authors',)
    
    readonly_fields = ('get_authors',)

    fieldsets = (
        ('Інформація про книгу (незмінна)', {
            'fields': ('name', 'get_authors')
        }),
        ('Стан (змінне)', {
            'fields': ('description', 'count')
        }),
    )

    def get_authors(self, obj):
        return ", ".join([f"{a.name} {a.surname}" for a in obj.authors.all()])
    get_authors.short_description = 'Автор(и)'
