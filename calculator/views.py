"""
Calculator app views.

View funksiyalari:
    - home: Bosh sahifa — kredit kalkulyator formasi va banklar ro'yxati
    - calculate: Kredit hisob-kitob natijalarini ko'rsatish
    - compare: Banklar bo'yicha taqqoslash
    - about: Loyiha haqida ma'lumot
"""

import json
from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CreditCalculatorForm
from .models import Bank
from .utils import CreditCalculator


class DecimalEncoder(json.JSONEncoder):
    """Decimal qiymatlarni JSON formatga o'tkazish uchun encoder."""

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def home(request):
    """Bosh sahifa — kredit kalkulyator formasi.

    GET: Bo'sh forma va faol banklar ro'yxatini ko'rsatadi.
    POST: Formani validatsiya qilib, calculate sahifasiga yo'naltiradi.

    Args:
        request: HTTP so'rov

    Returns:
        HttpResponse: Bosh sahifa yoki calculate sahifasiga redirect
    """
    if request.method == 'POST':
        form = CreditCalculatorForm(request.POST)
        if form.is_valid():
            # Ma'lumotlarni session'ga saqlash va calculate sahifasiga o'tish
            request.session['calc_data'] = {
                'amount': str(form.cleaned_data['amount']),
                'interest_rate': str(form.cleaned_data['interest_rate']),
                'term_months': form.cleaned_data['term_months'],
                'payment_type': form.cleaned_data['payment_type'],
            }
            return redirect('calculator:calculate')
    else:
        form = CreditCalculatorForm()

    banks = Bank.objects.filter(is_active=True)[:6]

    context = {
        'form': form,
        'banks': banks,
        'page_title': 'Kredit Kalkulyator',
    }
    return render(request, 'calculator/home.html', context)


def calculate(request):
    """Kredit hisob-kitob natijalarini ko'rsatish.

    POST so'rov orqali formadan kelgan ma'lumotlarni qayta ishlaydi
    yoki session'dan ma'lumotlarni oladi. Amortizatsiya jadvali va
    Chart.js uchun grafik ma'lumotlarini tayyorlaydi.

    Args:
        request: HTTP so'rov

    Returns:
        HttpResponse: Natijalar sahifasi yoki bosh sahifaga redirect
    """
    calc_data = None

    if request.method == 'POST':
        form = CreditCalculatorForm(request.POST)
        if form.is_valid():
            calc_data = {
                'amount': str(form.cleaned_data['amount']),
                'interest_rate': str(form.cleaned_data['interest_rate']),
                'term_months': form.cleaned_data['term_months'],
                'payment_type': form.cleaned_data['payment_type'],
            }
    else:
        # Session'dan ma'lumotlarni olish (redirect holatda)
        calc_data = request.session.get('calc_data')

    if not calc_data:
        messages.warning(request, "Iltimos, avval kredit ma'lumotlarini kiriting.")
        return redirect('calculator:home')

    # Kalkulyatorni ishga tushirish
    calculator = CreditCalculator(
        amount=calc_data['amount'],
        annual_rate=calc_data['interest_rate'],
        term_months=calc_data['term_months'],
    )

    result = calculator.calculate(payment_type=calc_data['payment_type'])
    schedule = result['schedule']

    # -----------------------------------------------------------------
    # Chart.js uchun ma'lumotlarni tayyorlash
    # -----------------------------------------------------------------

    # Oy raqamlari (labels)
    chart_labels = json.dumps([item['month'] for item in schedule])

    # Qoldiq qarz (balance) — har oy uchun
    balance_data = json.dumps(
        [item['balance'] for item in schedule],
        cls=DecimalEncoder,
    )

    # Kumulyativ foiz to'lovlari
    cumulative_interest = []
    running_interest = Decimal('0')
    for item in schedule:
        running_interest += item['interest']
        cumulative_interest.append(running_interest)

    interest_data = json.dumps(cumulative_interest, cls=DecimalEncoder)

    # Kumulyativ asosiy qarz to'lovlari
    cumulative_principal = []
    running_principal = Decimal('0')
    for item in schedule:
        running_principal += item['principal']
        cumulative_principal.append(running_principal)

    principal_data = json.dumps(cumulative_principal, cls=DecimalEncoder)

    # Forma — qayta tahrirlash imkoniyati uchun
    form = CreditCalculatorForm(initial={
        'amount': calc_data['amount'],
        'interest_rate': calc_data['interest_rate'],
        'term_months': calc_data['term_months'],
        'payment_type': calc_data['payment_type'],
    })

    context = {
        'form': form,
        'result': result,
        'schedule': schedule,
        'chart_labels': chart_labels,
        'balance_data': balance_data,
        'interest_data': interest_data,
        'principal_data': principal_data,
        'page_title': 'Hisob-kitob natijalari',
    }
    return render(request, 'calculator/results.html', context)


def compare(request):
    """Banklar bo'yicha taqqoslash.

    Barcha faol banklarni ko'rsatadi va foydalanuvchi
    kiritgan summasi / muddatiga ko'ra har bir bank uchun
    minimal foiz stavkada oylik to'lovni hisoblaydi.

    Args:
        request: HTTP so'rov

    Returns:
        HttpResponse: Banklar taqqoslash sahifasi
    """
    banks = Bank.objects.filter(is_active=True)

    # Foydalanuvchi summani va muddatni kiritishi mumkin (GET parametrlari)
    amount = request.GET.get('amount', '50000000')
    term_months = request.GET.get('term_months', '36')

    try:
        amount = Decimal(amount)
        term_months = int(term_months)
    except (ValueError, TypeError):
        amount = Decimal('50000000')
        term_months = 36

    # Har bir bank uchun minimal stavkada oylik to'lovni hisoblash
    bank_calculations = []
    for bank in banks:
        calculator = CreditCalculator(
            amount=amount,
            annual_rate=bank.min_rate,
            term_months=term_months,
        )
        result = calculator.calculate('annuity')

        bank_calculations.append({
            'bank': bank,
            'monthly_payment': result['monthly_payment'],
            'total_payment': result['total_payment'],
            'overpayment': result['overpayment'],
            'rate': bank.min_rate,
        })

    # Oylik to'lov bo'yicha saralash (eng arzondan qimmatingacha)
    bank_calculations.sort(key=lambda x: x['monthly_payment'])

    context = {
        'comparison_results': bank_calculations,
        'banks': banks,
        'amount': amount,
        'term_months': term_months,
        'page_title': 'Banklar taqqoslash',
    }
    return render(request, 'calculator/compare.html', context)


def about(request):
    """CreditSmart haqida ma'lumot sahifasi.

    Args:
        request: HTTP so'rov

    Returns:
        HttpResponse: About sahifasi
    """
    context = {
        'page_title': 'Biz haqimizda',
    }
    return render(request, 'calculator/about.html', context)
