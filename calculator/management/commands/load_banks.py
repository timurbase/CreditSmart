"""
O'zbekiston banklari ma'lumotlarini yuklash uchun management command.

Foydalanish:
    python manage.py load_banks

Bu buyruq O'zbekistonning 10 ta yirik bankining kredit
ma'lumotlarini ma'lumotlar bazasiga yuklaydi. Mavjud
banklar yangilanadi (update_or_create).
"""

from django.core.management.base import BaseCommand

from calculator.models import Bank


class Command(BaseCommand):
    """O'zbekiston banklari ma'lumotlarini bazaga yuklash."""

    help = "O'zbekiston banklari kredit ma'lumotlarini yuklash"

    # Banklar ma'lumotlari
    BANKS_DATA = [
        # -----------------------------------------------------------------
        # IST'MOL KREDITLARI
        # -----------------------------------------------------------------
        {
            'name': 'Agrobank',
            'min_rate': 14,
            'max_rate': 20,
            'min_term_months': 3,
            'max_term_months': 60,
            'min_amount': 1000000,
            'max_amount': 500000000,
            'credit_type': 'consumer',
            'description': (
                "Agrobank — O'zbekistonning yirik davlat banki. "
                "Qishloq xo'jaligi va agrosanoat sohasiga ixtisoslashgan. "
                "Arzon foiz stavkalari va qulay kredit shartlari bilan "
                "ajralib turadi."
            ),
            'website': 'https://agrobank.uz',
        },
        {
            'name': 'Xalq Banki',
            'min_rate': 15,
            'max_rate': 22,
            'min_term_months': 6,
            'max_term_months': 84,
            'min_amount': 2000000,
            'max_amount': 1000000000,
            'credit_type': 'consumer',
            'description': (
                "Xalq Banki — O'zbekiston xalq banki. "
                "Aholining keng qatlamlariga kredit xizmatlarini "
                "ko'rsatish bo'yicha yetakchi bank. "
                "Ijtimoiy yo'naltirilgan kredit mahsulotlari."
            ),
            'website': 'https://xb.uz',
        },
        {
            'name': "O'zbekiston Milliy Banki (NBU)",
            'min_rate': 16,
            'max_rate': 24,
            'min_term_months': 6,
            'max_term_months': 120,
            'min_amount': 5000000,
            'max_amount': 2000000000,
            'credit_type': 'consumer',
            'description': (
                "O'zbekiston Milliy Banki (NBU) — mamlakatning "
                "eng yirik tijorat banki. Universal bank xizmatlari "
                "va keng tarmoq infrastrukturasi."
            ),
            'website': 'https://nbu.uz',
        },
        # -----------------------------------------------------------------
        # IPOTEKA KREDITLARI
        # -----------------------------------------------------------------
        {
            'name': 'Ipoteka Bank',
            'min_rate': 16,
            'max_rate': 22,
            'min_term_months': 12,
            'max_term_months': 240,
            'min_amount': 10000000,
            'max_amount': 5000000000,
            'credit_type': 'mortgage',
            'description': (
                "Ipoteka Bank — O'zbekistonning ipoteka kreditlash "
                "bo'yicha yetakchi banki. Uy-joy olish uchun eng qulay "
                "shartlar va uzoq muddatli kreditlar. Davlat dasturlari "
                "bo'yicha imtiyozli ipoteka kreditlari."
            ),
            'website': 'https://ipotekabank.uz',
        },
        {
            'name': 'Aloqa Bank',
            'min_rate': 17,
            'max_rate': 24,
            'min_term_months': 12,
            'max_term_months': 180,
            'min_amount': 10000000,
            'max_amount': 3000000000,
            'credit_type': 'mortgage',
            'description': (
                "Aloqa Bank — zamonaviy raqamli bank xizmatlari. "
                "Ipoteka va iste'mol kreditlari bo'yicha qulay shartlar. "
                "Tezkor onlayn ariza berish imkoniyati."
            ),
            'website': 'https://aloqabank.uz',
        },
        # -----------------------------------------------------------------
        # AVTO KREDITLAR
        # -----------------------------------------------------------------
        {
            'name': 'Kapitalbank',
            'min_rate': 18,
            'max_rate': 28,
            'min_term_months': 6,
            'max_term_months': 60,
            'min_amount': 5000000,
            'max_amount': 1000000000,
            'credit_type': 'auto',
            'description': (
                "Kapitalbank — O'zbekistonning yirik xususiy banki. "
                "Avtokredit va iste'mol kreditlari bo'yicha keng tanlov. "
                "Tez tasdiqlash va onlayn xizmatlar."
            ),
            'website': 'https://kapitalbank.uz',
        },
        {
            'name': 'Turonbank',
            'min_rate': 19,
            'max_rate': 27,
            'min_term_months': 6,
            'max_term_months': 48,
            'min_amount': 5000000,
            'max_amount': 800000000,
            'credit_type': 'auto',
            'description': (
                "Turonbank — ishonchli tijorat banki. Avtomobil "
                "sotib olish uchun maqbul kredit shartlari va "
                "avtodilerlar bilan hamkorlik dasturlari."
            ),
            'website': 'https://turonbank.uz',
        },
        # -----------------------------------------------------------------
        # BIZNES KREDITLAR
        # -----------------------------------------------------------------
        {
            'name': 'Hamkorbank',
            'min_rate': 20,
            'max_rate': 30,
            'min_term_months': 3,
            'max_term_months': 60,
            'min_amount': 10000000,
            'max_amount': 5000000000,
            'credit_type': 'business',
            'description': (
                "Hamkorbank — kichik va o'rta biznes uchun yetakchi bank. "
                "Biznes kreditlari, aylanma mablag'lar va "
                "investitsion loyihalar uchun moliyalashtirish."
            ),
            'website': 'https://hamkorbank.uz',
        },
        {
            'name': 'Davr Bank',
            'min_rate': 21,
            'max_rate': 29,
            'min_term_months': 6,
            'max_term_months': 48,
            'min_amount': 5000000,
            'max_amount': 2000000000,
            'credit_type': 'business',
            'description': (
                "Davr Bank — zamonaviy biznes yechimlar. "
                "Tadbirkorlik faoliyatini moliyalashtirish, "
                "lizing va faktoring xizmatlari."
            ),
            'website': 'https://davrbank.uz',
        },
        {
            'name': 'Uzum Bank',
            'min_rate': 22,
            'max_rate': 32,
            'min_term_months': 1,
            'max_term_months': 36,
            'min_amount': 500000,
            'max_amount': 100000000,
            'credit_type': 'consumer',
            'description': (
                "Uzum Bank — O'zbekistonning neobanki. "
                "To'liq raqamli bank xizmatlari, mobil ilova "
                "orqali boshqarish, tezkor mikrokreditlar va "
                "bo'lib to'lash xizmatlari."
            ),
            'website': 'https://uzumbank.uz',
        },
    ]

    def handle(self, *args, **options):
        """Banklar ma'lumotlarini bazaga yuklash yoki yangilash."""
        self.stdout.write(
            self.style.NOTICE("O'zbekiston banklari ma'lumotlari yuklanmoqda...")
        )

        created_count = 0
        updated_count = 0

        for bank_data in self.BANKS_DATA:
            bank_name = bank_data.pop('name')
            bank, created = Bank.objects.update_or_create(
                name=bank_name,
                defaults=bank_data,
            )
            # Nomni qaytarish (pop olib tashlagani uchun)
            bank_data['name'] = bank_name

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"  [+] {bank.name} - yaratildi")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"  [~] {bank.name} - yangilandi")
                )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f"Tayyor! Jami: {len(self.BANKS_DATA)} ta bank. "
                f"Yangi: {created_count}, Yangilangan: {updated_count}."
            )
        )
