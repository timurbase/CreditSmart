"""
Kredit kalkulyator formasi.

Foydalanuvchidan kredit summasi, foiz stavkasi, muddat va
to'lov turini qabul qilish uchun forma.
"""

from django import forms


class CreditCalculatorForm(forms.Form):
    """Kredit hisob-kitob formasi.

    Fields:
        amount: Kredit summasi (so'm)
        interest_rate: Yillik foiz stavkasi (%)
        term_months: Kredit muddati (oy)
        payment_type: To'lov turi (annuitet yoki differensial)
    """

    PAYMENT_CHOICES = [
        ('annuity', "Annuitet (teng to'lov)"),
        ('differential', 'Differensial (kamayuvchi)'),
    ]

    amount = forms.DecimalField(
        min_value=100000,
        max_value=10000000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Masalan: 50 000 000',
            'id': 'amount',
        }),
        label="Kredit summasi (so'm)",
    )

    interest_rate = forms.DecimalField(
        min_value=0.1,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Masalan: 24',
            'id': 'interest_rate',
            'step': '0.1',
        }),
        label='Yillik foiz stavkasi (%)',
    )

    term_months = forms.IntegerField(
        min_value=1,
        max_value=360,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Masalan: 36',
            'id': 'term_months',
        }),
        label='Muddat (oy)',
    )

    payment_type = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='annuity',
        label="To'lov turi",
    )
