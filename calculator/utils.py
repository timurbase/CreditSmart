"""
CreditSmart — Kredit va Ipoteka hisob-kitob kalkulyatori.

Matematik asos:
    Kredit qoldiq balansining differensial tenglamasi:
    dB/dt = rB - P

    Bu yerda:
        B(t) = qoldiq qarz vaqt t da
        r    = oylik foiz stavkasi (yillik / 12 / 100)
        P    = oylik to'lov summasi

Annuitet formulasi:
    PMT = P × r(1+r)^n / ((1+r)^n - 1)

    Bu yerda:
        P = asosiy qarz summasi
        r = oylik foiz stavkasi
        n = to'lov oylari soni

Differensial formulasi:
    D_k = P/n + B_k × r

    Bu yerda:
        P   = asosiy qarz summasi
        n   = to'lov oylari soni
        B_k = k-oy uchun qoldiq qarz
        r   = oylik foiz stavkasi
"""

from decimal import Decimal, ROUND_HALF_UP


class CreditCalculator:
    """Kredit va ipoteka hisob-kitob kalkulyatori.

    Ushbu klass annuitet va differensial to'lov turlarini
    qo'llab-quvvatlaydi. Barcha hisob-kitoblar Decimal
    tipida amalga oshiriladi — floating point xatoliklarini
    oldini olish uchun.

    Args:
        amount: Kredit summasi (so'm)
        annual_rate: Yillik foiz stavkasi (%)
        term_months: Kredit muddati (oy)

    Usage:
        >>> calc = CreditCalculator(50_000_000, 24, 36)
        >>> result = calc.calculate('annuity')
        >>> print(result['monthly_payment'])
    """

    # Rounding precision for currency values
    CURRENCY_PRECISION = Decimal('0.01')

    def __init__(self, amount, annual_rate, term_months):
        self.amount = Decimal(str(amount))
        self.annual_rate = Decimal(str(annual_rate))
        self.term_months = int(term_months)
        self.monthly_rate = self.annual_rate / Decimal('12') / Decimal('100')

    def _quantize(self, value):
        """Qiymatni 2 ta o'nlik kasrgacha yaxlitlash."""
        return value.quantize(self.CURRENCY_PRECISION, rounding=ROUND_HALF_UP)

    # =========================================================================
    # ANNUITET HISOB-KITOBLARI
    # =========================================================================

    def annuity_payment(self):
        """Oylik annuitet to'lovni hisoblash.

        Formula: PMT = P × r(1+r)^n / ((1+r)^n - 1)

        Agar foiz stavkasi 0 bo'lsa, oddiy bo'linma qaytariladi.

        Returns:
            Decimal: Oylik to'lov summasi (so'm)
        """
        r = self.monthly_rate
        n = self.term_months
        P = self.amount

        if r == 0:
            return self._quantize(P / n)

        factor = (1 + r) ** n
        pmt = P * (r * factor) / (factor - 1)
        return self._quantize(pmt)

    def annuity_schedule(self):
        """Annuitet amortizatsiya jadvalini yaratish.

        Har bir oy uchun to'lov tarkibi (asosiy qarz + foiz),
        qoldiq balans va boshqa ko'rsatkichlarni hisoblaydi.
        Oxirgi oyda qoldiq balans nolga keltiriladi.

        Returns:
            list[dict]: Har bir oy uchun to'lov ma'lumotlari:
                - month (int): Oy tartib raqami
                - payment (Decimal): Jami to'lov
                - principal (Decimal): Asosiy qarz to'lovi
                - interest (Decimal): Foiz to'lovi
                - balance (Decimal): Qoldiq qarz
        """
        schedule = []
        balance = self.amount
        monthly_payment = self.annuity_payment()

        for month in range(1, self.term_months + 1):
            interest = self._quantize(balance * self.monthly_rate)
            principal = monthly_payment - interest

            # Oxirgi oyda qoldiq balansni to'liq yopish
            if month == self.term_months:
                principal = balance
                monthly_payment = principal + interest

            balance -= principal
            if balance < 0:
                balance = Decimal('0')

            schedule.append({
                'month': month,
                'payment': monthly_payment,
                'principal': principal,
                'interest': interest,
                'balance': self._quantize(balance),
            })

        return schedule

    # =========================================================================
    # DIFFERENSIAL HISOB-KITOBLARI
    # =========================================================================

    def differential_payment(self, month):
        """Berilgan oy uchun differensial to'lovni hisoblash.

        Formula: D_k = P/n + B_k × r

        Args:
            month: Oy tartib raqami (1-indexed)

        Returns:
            Decimal: Berilgan oy uchun to'lov summasi (so'm)
        """
        principal_part = self.amount / self.term_months
        remaining = self.amount - principal_part * (month - 1)
        interest_part = remaining * self.monthly_rate
        return self._quantize(principal_part + interest_part)

    def differential_schedule(self):
        """Differensial amortizatsiya jadvalini yaratish.

        Har oyda asosiy qarz to'lovi teng, foiz qismi esa
        qoldiq qarzga qarab kamayib boradi.

        Returns:
            list[dict]: Har bir oy uchun to'lov ma'lumotlari
        """
        schedule = []
        balance = self.amount
        principal_part = self._quantize(self.amount / self.term_months)

        for month in range(1, self.term_months + 1):
            interest = self._quantize(balance * self.monthly_rate)

            # Oxirgi oyda qoldiq balansni to'liq yopish
            if month == self.term_months:
                principal_part = balance

            payment = principal_part + interest
            balance -= principal_part
            if balance < 0:
                balance = Decimal('0')

            schedule.append({
                'month': month,
                'payment': payment,
                'principal': principal_part,
                'interest': interest,
                'balance': self._quantize(balance),
            })

        return schedule

    # =========================================================================
    # TO'LIQ HISOB-KITOB
    # =========================================================================

    def calculate(self, payment_type='annuity'):
        """To'liq kredit hisob-kitobini amalga oshirish.

        Tanlangan to'lov turiga ko'ra amortizatsiya jadvalini yaratadi
        va umumiy statistikani hisoblaydi.

        Args:
            payment_type: 'annuity' yoki 'differential'

        Returns:
            dict: Hisob-kitob natijalari:
                - amount (Decimal): Kredit summasi
                - rate (Decimal): Yillik foiz stavkasi
                - term_months (int): Muddat (oy)
                - monthly_payment (Decimal): Oylik to'lov (1-oy uchun)
                - total_payment (Decimal): Jami to'lov
                - overpayment (Decimal): Ortiqcha to'lov
                - overpayment_percent (Decimal): Ortiqcha to'lov (%)
                - schedule (list): Amortizatsiya jadvali
                - payment_type (str): To'lov turi kodi
                - payment_type_display (str): To'lov turi nomi
        """
        if payment_type == 'annuity':
            monthly_payment = self.annuity_payment()
            schedule = self.annuity_schedule()
        else:
            monthly_payment = self.differential_payment(1)
            schedule = self.differential_schedule()

        total_payment = sum(item['payment'] for item in schedule)
        overpayment = total_payment - self.amount

        return {
            'amount': self.amount,
            'rate': self.annual_rate,
            'term_months': self.term_months,
            'monthly_payment': monthly_payment,
            'total_payment': self._quantize(total_payment),
            'overpayment': self._quantize(overpayment),
            'overpayment_percent': self._quantize(
                (overpayment / self.amount) * 100
            ),
            'schedule': schedule,
            'payment_type': payment_type,
            'payment_type_display': (
                'Annuitet' if payment_type == 'annuity' else 'Differensial'
            ),
        }
