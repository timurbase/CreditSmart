"""
Bank modeli uchun Django Admin konfiguratsiyasi.

Professional ModelAdmin — filtrlash, qidiruv va
ro'yxatdan tahrirlash imkoniyatlari bilan.
"""

from django.contrib import admin

from .models import Bank


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    """Bank modeli uchun admin interfeys sozlamalari."""

    list_display = (
        'name',
        'credit_type',
        'min_rate',
        'max_rate',
        'min_amount',
        'max_amount',
        'is_active',
        'updated_at',
    )
    list_filter = (
        'credit_type',
        'is_active',
        'created_at',
    )
    search_fields = (
        'name',
        'description',
    )
    list_editable = (
        'min_rate',
        'max_rate',
        'is_active',
    )
    list_per_page = 20
    ordering = ('min_rate',)

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'logo_url', 'website', 'description'),
        }),
        ('Kredit shartlari', {
            'fields': (
                'credit_type',
                ('min_rate', 'max_rate'),
                ('min_term_months', 'max_term_months'),
                ('min_amount', 'max_amount'),
            ),
        }),
        ('Holat', {
            'fields': ('is_active',),
        }),
    )
