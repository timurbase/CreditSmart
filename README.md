# 🏦 CreditSmart — Kredit va Ipoteka Kalkulyatori

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00E5A0?style=for-the-badge)

> Kredit va ipoteka hisob-kitoblarini matematik formulalar asosida aniq hisoblab beruvchi zamonaviy fintech platforma.

---

## 📸 Skrinshotlar

<p align="center">
  <img src="docs/screenshots/home.png" alt="Bosh sahifa" width="100%">
</p>

| Kalkulyator | Natijalar | Taqqoslash |
|:-----------:|:---------:|:----------:|
| ![Calculator](docs/screenshots/calculator.png) | ![Results](docs/screenshots/results.png) | ![Compare](docs/screenshots/compare.png) |

> 💡 *Skrinshotlarni `docs/screenshots/` papkasiga joylashtiring*

---

## ✨ Xususiyatlar

| Xususiyat | Tavsif |
|-----------|--------|
| 📊 **Annuitet hisoblash** | Oylik to'lov bir xil — eng keng tarqalgan kredit turi |
| 📉 **Differensial hisoblash** | Oylik to'lov kamayib boradi — kamroq ortiqcha to'lov |
| 📋 **Amortizatsiya jadvali** | Har oylik asosiy qarz, foiz va qoldiqni ko'rish |
| 📈 **Interaktiv grafiklar** | Chart.js yordamida to'lov tarkibi va qarz kamayishini vizualizatsiya |
| 🏦 **Banklar taqqoslashi** | O'zbekiston banklari stavkalarini real vaqtda taqqoslash |
| ⭐ **Eng foydali kredit** | Eng kam ortiqcha to'lovli bankni avtomatik aniqlash |
| 🖨️ **Chop etish** | Natijalarni printer-friendly formatda chop etish |
| 📱 **Responsive dizayn** | Mobil, planshet va desktop qurilmalarda mukammal ishlaydi |
| 🌙 **Premium dark tema** | Glassmorphism effektlari bilan zamonaviy fintech dizayn |

---

## 🔢 Matematik Asos

CreditSmart quyidagi matematik modelga asoslangan:

### Differensial tenglama

```
dB/dt = rB − P
```

Bu yerda `B` — qoldiq qarz, `r` — yillik foiz stavkasi, `P` — oylik to'lov.

### Annuitet formulasi

```
PMT = P × r(1 + r)ⁿ / ((1 + r)ⁿ − 1)
```

| O'zgaruvchi | Tavsif |
|-------------|--------|
| `PMT` | Oylik to'lov summasi |
| `P` | Kredit summasi (asosiy qarz) |
| `r` | Oylik foiz stavkasi (yillik / 12) |
| `n` | To'lov muddati (oylarda) |

### Differensial formulasi

```
Asosiy qism = P / n
Foiz qism = Bₖ × r
Oylik to'lov = Asosiy qism + Foiz qism
```

Bu yerda `Bₖ` — k-oy uchun qoldiq qarz.

---

## 🚀 O'rnatish

### Talablar

- Python 3.11+
- pip (Python paket menejeri)
- Git

### Qadamlar

```bash
# 1. Repositoriyani klonlash
git clone https://github.com/yourusername/CreditSmart.git
cd CreditSmart

# 2. Virtual muhit yaratish
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Bog'liqliklarni o'rnatish
pip install -r requirements.txt

# 4. Migratsiyalarni bajarish
python manage.py migrate

# 5. Serverni ishga tushirish
python manage.py runserver
```

Brauzerda oching: **http://127.0.0.1:8000**

---

## 📦 Deploy (Joylashtirish)

### Render.com

1. [Render.com](https://render.com) da yangi **Web Service** yarating
2. GitHub repositoriyangizni ulang
3. Quyidagi sozlamalarni kiriting:

| Parametr | Qiymat |
|----------|--------|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `gunicorn creditsmart.wsgi` |

4. Environment o'zgaruvchilarni qo'shing:

```
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app.onrender.com
```

### Railway.app

```bash
# Railway CLI o'rnatish
npm install -g @railway/cli

# Login qilish
railway login

# Loyihani yaratish va deploy qilish
railway init
railway up
```

### Heroku

```bash
# Heroku CLI bilan
heroku create creditsmart-app
heroku config:set DJANGO_SECRET_KEY=<your-secret-key>
heroku config:set DJANGO_DEBUG=False
git push heroku main
heroku run python manage.py migrate
```

---

## 🛠 Texnologiyalar

### Backend

| Texnologiya | Versiya | Maqsad |
|-------------|---------|--------|
| Python | 3.11 | Asosiy dasturlash tili |
| Django | 5.0 | Web framework |
| Gunicorn | 21.2+ | WSGI HTTP server |
| WhiteNoise | 6.5+ | Statik fayllarni xizmat qilish |

### Frontend

| Texnologiya | Versiya | Maqsad |
|-------------|---------|--------|
| Bootstrap | 5.3 | Responsive grid va komponentlar |
| Chart.js | 4.x | Interaktiv grafiklar |
| Inter Font | — | Premium tipografiya |
| Custom CSS | — | Glassmorphism fintech dizayn |

### DevOps

| Texnologiya | Maqsad |
|-------------|--------|
| Git | Versiya nazorati |
| Render / Railway | Cloud deploy |
| WhiteNoise | Production static files |

---

## 📁 Loyiha Strukturasi

```
CreditSmart/
├── creditsmart/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── calculator/           # Asosiy ilova
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── calculator/
│           ├── base.html
│           ├── home.html
│           ├── calculator.html
│           ├── results.html
│           ├── compare.html
│           └── about.html
├── static/
│   ├── css/
│   │   └── style.css     # Premium fintech CSS
│   └── js/
│       └── calculator.js  # Chart.js + UI logic
├── requirements.txt
├── Procfile
├── runtime.txt
├── .gitignore
├── manage.py
└── README.md
```

---

## 🤝 Hissa qo'shish

1. Repositoriyani fork qiling
2. Yangi branch yarating (`git checkout -b feature/yangi-xususiyat`)
3. O'zgarishlarni commit qiling (`git commit -m 'Yangi xususiyat qo'shildi'`)
4. Branch-ni push qiling (`git push origin feature/yangi-xususiyat`)
5. Pull Request oching

---

## 📝 Litsenziya

Ushbu loyiha [MIT litsenziyasi](LICENSE) ostida tarqatiladi.

---

## 👨‍💻 Muallif

**CreditSmart Team**

Savollar yoki takliflar bo'lsa, Issue oching yoki Pull Request yuboring.

---

<p align="center">
  <strong>🏦 CreditSmart</strong> — Kredit hisob-kitoblarida aniqlik va shaffoflik
</p>
