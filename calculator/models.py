"""
Bank modeli — O'zbekiston banklari ma'lumotlar bazasi.

Har bir bank uchun kredit shartlari, foiz stavkalari va
boshqa moliyaviy parametrlarni saqlash uchun model.
"""

from django.db import models


class Bank(models.Model):
    """O'zbekiston banklari uchun kredit ma'lumotlari modeli.

    Attributes:
        name: Bank nomi
        logo_url: Bank logotipi URL manzili
        min_rate: Minimal yillik foiz stavkasi
        max_rate: Maksimal yillik foiz stavkasi
        min_term_months: Minimal kredit muddati (oy)
        max_term_months: Maksimal kredit muddati (oy)
        min_amount: Minimal kredit summasi (so'm)
        max_amount: Maksimal kredit summasi (so'm)
        credit_type: Kredit turi (iste'mol, ipoteka, avto, biznes)
        description: Bank haqida qisqacha ma'lumot
        website: Bank veb-sayti
        is_active: Faol/nofaol holati
    """

    CREDIT_TYPE_CHOICES = [
        ('consumer', "Iste'mol krediti"),
        ('mortgage', 'Ipoteka'),
        ('auto', 'Avtokredit'),
        ('business', 'Biznes kredit'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Bank nomi',
    )
    logo_url = models.URLField(
        blank=True,
        verbose_name='Logotip URL',
    )
    min_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Minimal foiz stavkasi (%)',
    )
    max_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Maksimal foiz stavkasi (%)',
    )
    min_term_months = models.PositiveIntegerField(
        default=3,
        verbose_name='Minimal muddat (oy)',
    )
    max_term_months = models.PositiveIntegerField(
        default=360,
        verbose_name='Maksimal muddat (oy)',
    )
    min_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=1000000,
        verbose_name="Minimal kredit summasi (so'm)",
    )
    max_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=5000000000,
        verbose_name="Maksimal kredit summasi (so'm)",
    )
    credit_type = models.CharField(
        max_length=20,
        choices=CREDIT_TYPE_CHOICES,
        default='consumer',
        verbose_name='Kredit turi',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Tavsif',
    )
    website = models.URLField(
        blank=True,
        verbose_name='Veb-sayt',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Faol',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan sana',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yangilangan sana',
    )

    class Meta:
        ordering = ['min_rate']
        verbose_name = 'Bank'
        verbose_name_plural = 'Banklar'

    def __str__(self):
        return self.name

    @property
    def rate_range(self):
        """Foiz stavkalari oralig'ini chiroyli formatda qaytaradi."""
        return f"{self.min_rate}% — {self.max_rate}%"
