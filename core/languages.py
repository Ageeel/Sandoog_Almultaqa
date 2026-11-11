WORDS = {
# ================= ENGLISH =================
"en": {
    "app_name": "Sandoog Al-Multaqa",
    "subscribers": "Subscribers",
    "retracted": "Withdrawn",
    "dunnes": "Pending",
    "payers": "Paid",
    "fridays": "Fridays",
    "loading": "Loading...",
    "search": "Type to find a subscriber",
    "no_subs": "No subscribers yet",
    "no_pending": "No one is pending — everyone is paid up",
    "no_retracted": "No withdrawn members",
    "get_started": "Get Started",
    "donations": "Donations",
    "sub_funds": "Fund Balance",
    "£": "SDG",

    "withdrawn_status": "Withdrawn",
    "unknown_name": "Unknown",
    "paid_status": "Paid up",
    "late_status": "Late {n} week(s)",
    "advance_status": "Ahead {n} week(s)",

    "onboarding_title": "Sandoog Al-Multaqa",
    "onboarding_text": "Easily organize your weekly contributions. Pay 1,000 pounds every week, and track contributions and schedules with full transparency and regularity—no need for paper notes",
    "onboarding_sub": "Secure and protected data, safe from loss or tampering",
    "plasma_label":"Plasma",

    "settings": "Settings",
    "language": "Language",
    "choose_language": "Choose language",
    "arabic": "العربية",
    "english": "English",
    "close": "Close",

    "notif_withdraw": "Withdrawal of {amount}",
    "notif_deposit": "Deposit of {amount}",
    "notif_donation": "Donation of {amount}",
    "notif_new_sub": "New subscriber",
    "notif_unsub": "Member withdrawn",
    "notif_general": "General notification",
    "bank_notif": "Bank receipt",
    "view_image": "View image",
    "on_day": "On {date}",
    "total_deposits": "Total Deposits",
    "total_withdrawals": "Total Withdrawals",
    "notifications": "Notifications",

    "progress": "Payment progress",
},

# ================= ARABIC =================
"ar": {
    "app_name": "صندوق الملتقى",
    "subscribers": "المشتركين",
    "retracted": "المنسحبين",
    "dunnes": "المطالبين",
    "payers": "المسددين",
    "fridays": "الجمعات",
    "loading": "جار التحميل...",
    "search": "ابحث عن اسم المشترك...",
    "no_subs": "لا يوجد مشتركين بعد",
    "no_pending": "لا يوجد مطالبين، المشتركين سددوا ما عليهم",
    "no_retracted": "لا يوجد منسحبين",
    "get_started": "أبدأ الإستخدام",
    "donations": "التبرعات",
    "sub_funds": "رصيد الصندوق",
    "£": "جنيه",

    "withdrawn_status": "منسحب",
    "unknown_name": "مجهول",
    "paid_status": "تم الدفع",
    "late_status": "متأخر {n} جمعة",
    "advance_status": "مقدم {n} جمعة",

    "onboarding_title": "صندوق الملتقى",
    "onboarding_text":"نظّموا مساهماتكم الأسبوعية بسهولة. ادفع 1,000 جنيه كل أسبوع، وتابع المساهمات والمواعيد بكل شفافية وانتظام، حيث لا حاجة للملاحظات الورقية",
    "onboarding_sub": "بيانات آمنة ومحمية من الضياع والتلاعب ",
    "plasma_label":"بلازما",

    "settings": "الإعدادات",
    "language": "اللغة",
    "choose_language": "اختر اللغة",
    "arabic": "العربية",
    "english": "English",
    "close": "إغلاق",

    "notif_withdraw": "سحب {amount}",
    "notif_deposit": "إيداع {amount}",
    "notif_donation": "تبرع بمبلغ {amount}",
    "notif_new_sub": "مشترك جديد",
    "notif_unsub": "إنسحاب مشترك",
    "notif_general": "إشعار عام",
    "bank_notif": "إشعار بنكك",
    "view_image": "عرض الصورة",
    "on_day": "في يوم {date}",
    "total_deposits": "إجمالي الودائع",
    "total_withdrawals": "إجمالي السحب",
    "notifications": "الإشعارات",

    "progress": "نسبة السداد",
},
}


class Language:
    def __init__(self, lang: str = "ar"):
        self.lang = lang if lang in WORDS else "ar"

    @property
    def rtl(self) -> bool:
        return self.lang == "ar"

    def t(self, key: str, **kwargs) -> str:
        text = WORDS.get(self.lang, {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def set_lang(self, lang: str):
        if lang in WORDS:
            self.lang = lang

    def toggle(self):
        # Was always resetting to "ar" — now actually flips between languages.
        self.set_lang("en" if self.lang == "ar" else "ar")
