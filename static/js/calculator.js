/* ============================================================
   CreditSmart — Calculator JavaScript
   Form Enhancements • Animations • Navbar • Utilities
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
    initPresetButtons();
    initFormValidation();
    initShowMoreSchedule();
    initNavbar();
    initBackToTop();
    initAnimations();
    initSmoothScroll();
});

/* ==========================================================
   PRESET BUTTONS (10M, 30M, 50M ... / 12 oy, 24 oy ...)
   ========================================================== */
function initPresetButtons() {
    // All preset buttons have: data-target="id_amount" data-value="50000000"
    const presetBtns = document.querySelectorAll('.btn-preset[data-target]');

    presetBtns.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('data-target');
            const value = this.getAttribute('data-value');
            const targetInput = document.getElementById(targetId);

            if (targetInput && value) {
                targetInput.value = value;
                targetInput.focus();

                // Highlight active preset in this group
                const siblings = this.parentElement.querySelectorAll('.btn-preset');
                siblings.forEach(function (s) { s.classList.remove('active'); });
                this.classList.add('active');

                // Trigger input event for any listeners
                targetInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        });
    });
}

/* ==========================================================
   FORM VALIDATION
   ========================================================== */
function initFormValidation() {
    const form = document.getElementById('creditForm');
    if (!form) return;

    const amountInput = document.getElementById('id_amount');
    const rateInput = document.getElementById('id_interest_rate');
    const termInput = document.getElementById('id_term_months');

    form.addEventListener('submit', function (e) {
        let valid = true;

        // Validate amount
        if (amountInput) {
            const val = parseFloat(amountInput.value);
            if (!val || val < 100000) {
                showError(amountInput, 'Minimal summa: 100,000 so\'m');
                valid = false;
            } else {
                clearError(amountInput);
            }
        }

        // Validate interest rate
        if (rateInput) {
            const val = parseFloat(rateInput.value);
            if (!val || val <= 0 || val > 100) {
                showError(rateInput, 'Foiz stavkasini kiriting (0.1 — 100)');
                valid = false;
            } else {
                clearError(rateInput);
            }
        }

        // Validate term
        if (termInput) {
            const val = parseInt(termInput.value);
            if (!val || val < 1 || val > 360) {
                showError(termInput, 'Muddatni kiriting (1 — 360 oy)');
                valid = false;
            } else {
                clearError(termInput);
            }
        }

        if (!valid) {
            e.preventDefault();
        }
    });
}

function showError(input, message) {
    if (!input) return;
    // Add error styling
    input.classList.add('is-invalid');

    // Find or create error message
    const wrapper = input.closest('.mb-4') || input.parentElement;
    let errorEl = wrapper.querySelector('.js-field-error');
    if (!errorEl) {
        errorEl = document.createElement('div');
        errorEl.className = 'js-field-error text-danger small mt-1';
        wrapper.appendChild(errorEl);
    }
    errorEl.textContent = message;
}

function clearError(input) {
    if (!input) return;
    input.classList.remove('is-invalid');
    const wrapper = input.closest('.mb-4') || input.parentElement;
    const errorEl = wrapper.querySelector('.js-field-error');
    if (errorEl) errorEl.remove();
}

/* ==========================================================
   SHOW MORE SCHEDULE ROWS (Results page)
   ========================================================== */
function initShowMoreSchedule() {
    const btn = document.getElementById('showMoreScheduleBtn');
    if (!btn) return;

    btn.addEventListener('click', function () {
        const hiddenRows = document.querySelectorAll('.schedule-hidden-row');
        let isExpanded = !hiddenRows[0]?.classList.contains('d-none');

        hiddenRows.forEach(function (row) {
            row.classList.toggle('d-none');
        });

        if (!isExpanded) {
            // Now showing all
            this.innerHTML = '<i class="bi bi-chevron-up me-1"></i> Kamroq ko\'rsatish';
        } else {
            // Now hiding
            const count = hiddenRows.length;
            this.innerHTML = '<i class="bi bi-chevron-down me-1"></i> Ko\'proq ko\'rsatish <span class="badge bg-primary ms-1">' + count + '</span>';

            // Scroll to table top
            const table = document.getElementById('amortizationSection');
            if (table) {
                table.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
}

/* ==========================================================
   NAVBAR — scroll effect
   ========================================================== */
function initNavbar() {
    const navbar = document.getElementById('mainNavbar');
    if (!navbar) return;

    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }, { passive: true });
}

/* ==========================================================
   BACK TO TOP BUTTON
   ========================================================== */
function initBackToTop() {
    // Create back-to-top button if not in DOM
    let btn = document.querySelector('.back-to-top');
    if (!btn) {
        btn = document.createElement('button');
        btn.className = 'back-to-top';
        btn.setAttribute('aria-label', 'Yuqoriga qaytish');
        btn.innerHTML = '<i class="bi bi-chevron-up"></i>';
        document.body.appendChild(btn);
    }

    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 400) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    }, { passive: true });

    btn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

/* ==========================================================
   SCROLL ANIMATIONS (fade-in, slide-up)
   ========================================================== */
function initAnimations() {
    const els = document.querySelectorAll('.fade-in, .slide-up');
    if (els.length === 0 || !('IntersectionObserver' in window)) {
        // Fallback: show everything
        els.forEach(function (el) { el.style.opacity = '1'; });
        return;
    }

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -30px 0px'
    });

    els.forEach(function (el) {
        observer.observe(el);
    });
}

/* ==========================================================
   SMOOTH SCROLL for anchor links
   ========================================================== */
function initSmoothScroll() {
    document.querySelectorAll('a[href*="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Only handle same-page anchors
            const hashIndex = href.indexOf('#');
            if (hashIndex === -1) return;

            const hash = href.substring(hashIndex);
            if (hash === '#' || hash === '') return;

            // If it's a different page link with hash, let browser handle
            const path = href.substring(0, hashIndex);
            if (path && path !== '' && !path.endsWith(window.location.pathname)) return;

            const target = document.querySelector(hash);
            if (target) {
                e.preventDefault();
                const offset = 80;
                const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top: top, behavior: 'smooth' });
            }
        });
    });
}

/* ==========================================================
   UTILITY: Currency formatter
   ========================================================== */
function formatCurrency(number) {
    if (number == null || isNaN(number)) return "0 so'm";
    return Math.round(number)
        .toString()
        .replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + " so'm";
}
