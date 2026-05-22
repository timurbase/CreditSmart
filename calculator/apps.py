"""Calculator app configuration."""

from django.apps import AppConfig


class CalculatorConfig(AppConfig):
    """Kredit kalkulyator ilovasining konfiguratsiyasi."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calculator'
    verbose_name = 'Kredit Kalkulyator'
