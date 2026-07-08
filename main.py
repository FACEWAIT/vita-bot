#!/usr/bin/env python3
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, filters, ContextTypes,
)

BOT_TOKEN = "7661533612:AAFtifXuZP5IkTzdZvwK1O_MmF408Rs7XxY"
ADMIN_ID = 940613012

# ─── ТЕКСТ (UZ / RU) ──────────────────────────────────────────────────────────
T = {
    "uz": {
        "welcome": (
            "Salom! 👋\n\n"
            "⚡ *VITA DELUXE* — suli, lavlagi va yalpizdan tayyorlangan "
            "*tabiiy energiya ichimligi!*\n\n"
            "Energiya beradi, ishtahani nazorat qiladi va sog'lom "
            "turmush tarzini qo'llab-quvvatlaydi 🌿\n\n"
            "Quyidagilardan birini tanlang:"
        ),
        "choose_section": "Quyidagilardan birini tanlang:",
        "faq_title": "❓ *Ko'p so'raladigan savollar*\n\nQuyidagilardan birini tanlang:",
        "btn_faq": "❓ Ko'p so'raladigan savollar",
        "btn_order": "🛒 Buyurtma berish",
        "btn_ugc": "🤝 Blogger/UGC hamkorlik",
        "btn_where": "📍 Qayerdan sotib olish",
        "btn_ingredients": "🌿 Tarkibi",
        "btn_usage": "📋 Qanday ichish kerak",
        "btn_benefits": "✅ Foydasi",
        "btn_price": "💰 Narxlar",
        "btn_certificate": "📄 Sertifikat bormi?",
        "btn_back_faq": "⬅️ FAQ ga qaytish",
        "btn_back_main": "🏠 Bosh menu",
        "btn_cancel": "❌ Bekor qilish",
        "btn_confirm": "✅ Ha, tasdiqlyman",
        "faq_ingredients": (
            "🌿 *Tarkibi:*\n\n"
            "• Suli (овёс)\n• Lavlagi (свёкла)\n• Yalpiz (мята)\n\n"
            "✅ 100% tabiiy mahsulot. Hech qanday kimyoviy qo'shimchalar yo'q."
        ),
        "faq_usage": (
            "📋 *Qanday ichish kerak:*\n\n"
            "• Har kuni ichish tavsiya etiladi\n"
            "• Minimum: kuniga 1 shisha\n"
            "• Tavsiya etilgan miqdor: kuniga 500 ml\n\n"
            "⏰ *Qachon ichish yaxshi?*\n\n"
            "🌙 *Kechqurun* — uxlashdan 30 daqiqa oldin\n"
            "🌅 *Ertalab* — faqat uydan ishlasangiz (remote)\n\n"
            "🫙 Ichishdan oldin yaxshilab chayqating!"
        ),
        "faq_benefits": (
            "✅ *Foydasi:*\n\n"
            "• Tabiiy energiya va tetiklik beradi ⚡\n"
            "• Jigarni tozalashga yordam beradi 🫁\n"
            "• Alzheimer kasalligining oldini olishga yordam beradi 🧠\n"
            "• Umumiy ahvolni yaxshilaydi\n"
            "• Ishtahani nazorat qilishga yordam beradi\n"
            "• Og'irlik his-tuyg'usini kamaytiradi\n"
            "• Immunitetni mustahkamlaydi 💪\n"
            "• Sog'lom turmush tarzini qo'llab-quvvatlaydi\n"
            "• To'g'ri ovqatlanish va faollik bilan vazn yo'qotishga yordam beradi"
        ),
        "faq_price": (
            "💰 *Narxlar:*\n\n"
            "🧪 *Sinov paketi* _(10 ta shisha)_\n"
            "5 ta × 200 ml + 5 ta × 300 ml\n"
            "~~145 000~~ → *116 000 so'm* _(−20% chegirma)_\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "📦 *To'liq kurs — 3 oy* _(90 ta shisha)_\n"
            "45 ta × 200 ml + 45 ta × 300 ml\n"
            "*1 305 000 so'm*\n\n"
            "📌 *Minimum:* kuniga 1 shisha, almashtirib\n"
            "⭐ *Tavsiya:* kuniga 500 ml\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🚚 Toshkent — *bepul* | Viloyat — alohida"
        ),
        "faq_certificate": (
            "📄 *Sertifikat:*\n\n"
            "Hozirda rasmiylashtirish jarayonida.\n\n"
            "📞 +998 33 128 34 34\n💬 @vita_deluxe"
        ),
        "faq_where": (
            "📍 *Qayerdan sotib olish:*\n\n"
            "📱 Instagram: @vita\\_deluxe.uz\n"
            "🌐 vitadeluxe.taplink.ws\n"
            "📞 +998 33 128 34 34\n"
            "💬 @vita_deluxe\n\n"
            "Yoki quyida buyurtma bering 👇"
        ),
        # --- ORDER ---
        "order_ask_name": "🛒 *Buyurtma berish*\n\nIsmingizni yozing 👇",
        "order_ask_phone": "Rahmat, *{name}*! 👍\n\nTelefon raqamingizni yozing:\n_Misol: +998901234567_",
        "order_ask_package": (
            "📦 *Qaysi paketni tanlaysiz?*\n\n"
            "🧪 *Sinov paketi* — 5×200ml + 5×300ml\n\n"
            "📦 *To'liq kurs (3 oy)* — 45×200ml + 45×300ml\n"
            "_Kuniga 1 shisha (min) yoki 500 ml (tavsiya)_"
        ),
        "btn_trial": "🧪 Sinov paketi — 119 000 so'm (7 ta × 300 ml)",
        "btn_course": "📦 To'liq kurs 3 oy — 1 305 000 so'm",
        "order_confirm_text": (
            "✅ *Buyurtmangizni tekshiring:*\n\n"
            "👤 Ism: {name}\n📞 Telefon: {phone}\n📦 Paket: {package}\n\nTasdiqlaysizmi?"
        ),
        "order_success": (
            "🎉 *Buyurtmangiz qabul qilindi!*\n\n"
            "Tez orada @vita_deluxe bog'lanadi. 📞\n\nBoshqa savol: /start"
        ),
        "order_cancelled": "❌ Buyurtma bekor qilindi.\n\n/start — bosh menu",
        # --- UGC ---
        "ugc_welcome": (
            "🤝 *Blogger/UGC hamkorlik*\n\n"
            "Assalomu alaykum! Mahsulotimizga qiziqish bildirganingiz uchun rahmat 😊\n\n"
            "Siz *VITA DELUXE* ni bepul olasiz va o'z izohingizni ulashasiz.\n\n"
            "📋 *Shartlar:*\n"
            "• Mahsulotni qabul qiling va halol fikr bildiring\n"
            "• Oyiga *3–5 reels* va *5–8 stories* chiqaring\n"
            "• Bizni hammuallif sifatida belgilang\n"
            "• Mahsulot har hafta etkazib beriladi\n\n"
            "📦 *To'liq 3 oylik kurs bepul beriladi!*\n\n"
            "Shartlar sizga mos bo'lsa — anketani to'ldiring 👇"
        ),
        "ugc_ask_name": "📝 Ismingiz va familiyangizni yozing:",
        "ugc_ask_age": "🎂 Yoshingizni yozing:\n_Misol: 23_",
        "ugc_ask_city": "🏙️ Qaysi shahardasiz?\n_Misol: Toshkent_",
        "ugc_ask_instagram": "📱 Instagram akkauntingizni yozing:\n_Misol: @username_",
        "ugc_ask_phone": "📞 Telefon raqamingizni yozing:\n_Misol: +998901234567_",
        "ugc_confirm": (
            "✅ *Anketangizni tekshiring:*\n\n"
            "👤 Ism: {name}\n"
            "🎂 Yosh: {age}\n"
            "🏙️ Shahar: {city}\n"
            "📱 Instagram: {instagram}\n"
            "📞 Telefon: {phone}\n\n"
            "Yuborasizmi?"
        ),
        "ugc_success": (
            "🎉 *Arizangiz qabul qilindi!*\n\n"
            "Tez orada @vita_deluxe siz bilan bog'lanadi.\n\n"
            "Boshqa savol: /start"
        ),
        "ugc_cancelled": "❌ Ariza bekor qilindi.\n\n/start — bosh menu",
    },

    "ru": {
        "welcome": (
            "Привет! 👋\n\n"
            "⚡ *VITA DELUXE* — натуральный энергетический напиток "
            "из овса, свёклы и мяты!\n\n"
            "Даёт энергию, контролирует аппетит и поддерживает ЗОЖ 🌿\n\n"
            "Выберите одно из следующего:"
        ),
        "choose_section": "Выберите одно из следующего:",
        "faq_title": "❓ *Частые вопросы*\n\nВыберите интересующий вопрос:",
        "btn_faq": "❓ Частые вопросы",
        "btn_order": "🛒 Сделать заказ",
        "btn_ugc": "🤝 Сотрудничество Blogger/UGC",
        "btn_where": "📍 Где купить",
        "btn_ingredients": "🌿 Состав",
        "btn_usage": "📋 Как принимать",
        "btn_benefits": "✅ Польза",
        "btn_price": "💰 Цены",
        "btn_certificate": "📄 Есть ли сертификат?",
        "btn_back_faq": "⬅️ Назад к FAQ",
        "btn_back_main": "🏠 Главное меню",
        "btn_cancel": "❌ Отмена",
        "btn_confirm": "✅ Да, подтверждаю",
        "faq_ingredients": (
            "🌿 *Состав:*\n\n"
            "• Овёс\n• Свёкла\n• Мята\n\n"
            "✅ 100% натуральный. Без химических добавок."
        ),
        "faq_usage": (
            "📋 *Как принимать:*\n\n"
            "• Ежедневно\n• Минимум: 1 бутылка в день\n"
            "• Рекомендуется: 500 мл в день\n\n"
            "⏰ *Когда пить?*\n\n"
            "🌙 *Вечером* — за 30 минут до сна\n"
            "🌅 *Утром* — только если работаете из дома\n\n"
            "🫙 Перед употреблением взболтать!"
        ),
        "faq_benefits": (
            "✅ *Польза:*\n\n"
            "• Натуральная энергия и бодрость ⚡\n"
            "• Очищение печени 🫁\n"
            "• Профилактика болезни Альцгеймера 🧠\n"
            "• Улучшает самочувствие\n"
            "• Контроль аппетита\n"
            "• Уменьшает чувство тяжести\n"
            "• Укрепляет иммунитет 💪\n"
            "• Поддерживает ЗОЖ\n"
            "• Помогает снизить вес при правильном питании"
        ),
        "faq_price": (
            "💰 *Цены:*\n\n"
            "🧪 *Пробный пакет* _(10 бутылок)_\n"
            "5×200 мл + 5×300 мл\n"
            "~~145 000~~ → *116 000 сум* _(−20%)_\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "📦 *Полный курс — 3 месяца* _(90 бутылок)_\n"
            "45×200 мл + 45×300 мл\n"
            "*1 305 000 сум*\n\n"
            "📌 Минимум: 1 бутылка/день\n"
            "⭐ Рекомендуется: 500 мл/день\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🚚 Ташкент — *бесплатно* | Область — отдельно"
        ),
        "faq_certificate": (
            "📄 *Сертификат:*\n\n"
            "В процессе оформления.\n\n"
            "📞 +998 33 128 34 34\n💬 @vita_deluxe"
        ),
        "faq_where": (
            "📍 *Где купить:*\n\n"
            "📱 Instagram: @vita\\_deluxe.uz\n"
            "🌐 vitadeluxe.taplink.ws\n"
            "📞 +998 33 128 34 34\n"
            "💬 @vita_deluxe\n\n"
            "Или оформите заказ здесь 👇"
        ),
        # --- ORDER ---
        "order_ask_name": "🛒 *Оформление заказа*\n\nНапишите ваше имя 👇",
        "order_ask_phone": "Спасибо, *{name}*! 👍\n\nНомер телефона:\n_Пример: +998901234567_",
        "order_ask_package": (
            "📦 *Какой пакет выбираете?*\n\n"
            "🧪 *Пробный* — 5×200мл + 5×300мл\n\n"
            "📦 *Полный курс (3 мес)* — 45×200мл + 45×300мл\n"
            "_Минимум: 1 бутылка/день; рекомендуется: 500 мл_"
        ),
        "btn_trial": "🧪 Пробный пакет — 119 000 сум (7×300 мл)",
        "btn_course": "📦 Полный курс 3 мес — 1 305 000 сум",
        "order_confirm_text": (
            "✅ *Проверьте заказ:*\n\n"
            "👤 Имя: {name}\n📞 Телефон: {phone}\n📦 Пакет: {package}\n\nПодтверждаете?"
        ),
        "order_success": (
            "🎉 *Заказ принят!*\n\n"
            "@vita_deluxe свяжется с вами. 📞\n\nДругие вопросы: /start"
        ),
        "order_cancelled": "❌ Заказ отменён.\n\n/start — главное меню",
        # --- UGC ---
        "ugc_welcome": (
            "🤝 *Сотрудничество Blogger/UGC*\n\n"
            "Ассалому алейкум! Спасибо за интерес к нашему продукту 😊\n\n"
            "Вы получаете *VITA DELUXE* бесплатно и делитесь честным отзывом.\n\n"
            "📋 *Условия:*\n"
            "• Распакуйте продукт и поделитесь честным мнением\n"
            "• В месяц: *3–5 reels* и *5–8 stories* с продуктом\n"
            "• Отметьте нас как соавтора\n"
            "• Продукт поставляется еженедельно\n\n"
            "📦 *Полный 3-месячный курс — бесплатно!*\n\n"
            "Если условия подходят — заполните анкету 👇"
        ),
        "ugc_ask_name": "📝 Напишите ваше имя и фамилию:",
        "ugc_ask_age": "🎂 Ваш возраст:\n_Пример: 23_",
        "ugc_ask_city": "🏙️ Из какого вы города?\n_Пример: Ташкент_",
        "ugc_ask_instagram": "📱 Ваш Instagram аккаунт:\n_Пример: @username_",
        "ugc_ask_phone": "📞 Номер телефона:\n_Пример: +998901234567_",
        "ugc_confirm": (
            "✅ *Проверьте анкету:*\n\n"
            "👤 Имя: {name}\n"
            "🎂 Возраст: {age}\n"
            "🏙️ Город: {city}\n"
            "📱 Instagram: {instagram}\n"
            "📞 Телефон: {phone}\n\n"
            "Отправить?"
        ),
        "ugc_success": (
            "🎉 *Заявка принята!*\n\n"
            "@vita_deluxe свяжется с вами.\n\nДругие вопросы: /start"
        ),
        "ugc_cancelled": "❌ Заявка отменена.\n\n/start — главное меню",
    },
}

def t(context, key):
    lang = context.user_data.get("lang", "uz")
    return T[lang][key]

# ─── STATES ───────────────────────────────────────────────────────────────────
LANG = 0
NAME, PHONE, PACKAGE, CONFIRM = range(1, 5)
UGC_NAME, UGC_AGE, UGC_CITY, UGC_INSTAGRAM, UGC_PHONE, UGC_CONFIRM = range(10, 16)

# ─── KEYBOARDS ────────────────────────────────────────────────────────────────

def lang_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
         InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
    ])

def main_menu(ctx):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, "btn_faq"), callback_data="faq")],
        [InlineKeyboardButton(t(ctx, "btn_order"), callback_data="order_start")],
        [InlineKeyboardButton(t(ctx, "btn_ugc"), callback_data="ugc_start")],
        [InlineKeyboardButton(t(ctx, "btn_where"), callback_data="faq_where")],
    ])

def faq_menu(ctx):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, "btn_ingredients"), callback_data="faq_ingredients")],
        [InlineKeyboardButton(t(ctx, "btn_usage"), callback_data="faq_usage")],
        [InlineKeyboardButton(t(ctx, "btn_benefits"), callback_data="faq_benefits")],
        [InlineKeyboardButton(t(ctx, "btn_price"), callback_data="faq_price")],
        [InlineKeyboardButton(t(ctx, "btn_certificate"), callback_data="faq_certificate")],
        [InlineKeyboardButton(t(ctx, "btn_where"), callback_data="faq_where")],
        [InlineKeyboardButton(t(ctx, "btn_back_main"), callback_data="back_main")],
    ])

def back_faq_kb(ctx):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, "btn_back_faq"), callback_data="faq")],
        [InlineKeyboardButton(t(ctx, "btn_back_main"), callback_data="back_main")],
    ])

def cancel_kb(ctx):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, "btn_cancel"), callback_data="cancel_order")],
    ])

def ugc_start_kb(ctx):
    lang = ctx.user_data.get("lang", "uz")
    label = "✅ Anketani to'ldirish" if lang == "uz" else "✅ Заполнить анкету"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data="ugc_begin")],
        [InlineKeyboardButton(t(ctx, "btn_cancel"), callback_data="cancel_ugc")],
    ])

def ugc_cancel_kb(ctx):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, "btn_cancel"), callback_data="cancel_ugc")],
    ])

def package_kb(ctx):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, "btn_trial"), callback_data="pkg_trial")],
        [InlineKeyboardButton(t(ctx, "btn_course"), callback_data="pkg_course")],
        [InlineKeyboardButton(t(ctx, "btn_cancel"), callback_data="cancel_order")],
    ])

def confirm_kb(ctx):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, "btn_confirm"), callback_data="confirm_yes")],
        [InlineKeyboardButton(t(ctx, "btn_cancel"), callback_data="cancel_order")],
    ])

def ugc_confirm_kb(ctx):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, "btn_confirm"), callback_data="ugc_confirm_yes")],
        [InlineKeyboardButton(t(ctx, "btn_cancel"), callback_data="cancel_ugc")],
    ])

# ─── START / LANG ─────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 *VITA DELUXE*\n\nTilni tanlang / Выберите язык:",
        parse_mode="Markdown", reply_markup=lang_kb(),
    )
    return LANG

async def choose_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["lang"] = "uz" if query.data == "lang_uz" else "ru"
    await query.edit_message_text(
        t(context, "welcome"), parse_mode="Markdown", reply_markup=main_menu(context),
    )
    return ConversationHandler.END

# ─── FAQ / MENU BUTTONS ───────────────────────────────────────────────────────

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_main":
        await query.edit_message_text(
            t(context, "choose_section"), reply_markup=main_menu(context),
        )
    elif data == "faq":
        await query.edit_message_text(
            t(context, "faq_title"), parse_mode="Markdown", reply_markup=faq_menu(context),
        )
    elif data.startswith("faq_"):
        await query.edit_message_text(
            t(context, data), parse_mode="Markdown", reply_markup=back_faq_kb(context),
        )

# ─── ORDER FLOW ───────────────────────────────────────────────────────────────

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        t(context, "order_ask_name"), parse_mode="Markdown", reply_markup=cancel_kb(context),
    )
    return NAME

async def order_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        t(context, "order_ask_phone").format(name=update.message.text),
        parse_mode="Markdown", reply_markup=cancel_kb(context),
    )
    return PHONE

async def order_get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text(
        t(context, "order_ask_package"), parse_mode="Markdown", reply_markup=package_kb(context),
    )
    return PACKAGE

async def order_get_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "uz")
    context.user_data["package"] = T[lang]["btn_trial"] if query.data == "pkg_trial" else T[lang]["btn_course"]
    await query.edit_message_text(
        t(context, "order_confirm_text").format(
            name=context.user_data["name"],
            phone=context.user_data["phone"],
            package=context.user_data["package"],
        ),
        parse_mode="Markdown", reply_markup=confirm_kb(context),
    )
    return CONFIRM

async def order_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm_yes":
        name = context.user_data["name"]
        phone = context.user_data["phone"]
        package = context.user_data["package"]
        user = query.from_user
        username = f"@{user.username}" if user.username else "—"
        await query.edit_message_text(t(context, "order_success"), parse_mode="Markdown")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🛒 YANGI BUYURTMA!\n\n"
                f"👤 Ism: {name}\n"
                f"📞 Tel: {phone}\n"
                f"📦 Paket: {package}\n"
                f"📱 Telegram: {username}\n"
                f"🆔 ID: {user.id}"
            ),
        )
    else:
        await query.edit_message_text(t(context, "order_cancelled"))
    return ConversationHandler.END

async def order_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(t(context, "order_cancelled"))
    return ConversationHandler.END

# ─── UGC FLOW ─────────────────────────────────────────────────────────────────

async def ugc_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        t(context, "ugc_welcome"), parse_mode="Markdown", reply_markup=ugc_start_kb(context),
    )
    return UGC_NAME

async def ugc_begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        t(context, "ugc_ask_name"), parse_mode="Markdown", reply_markup=ugc_cancel_kb(context),
    )
    return UGC_NAME

async def ugc_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ugc_name"] = update.message.text
    await update.message.reply_text(
        t(context, "ugc_ask_age"), parse_mode="Markdown", reply_markup=ugc_cancel_kb(context),
    )
    return UGC_AGE

async def ugc_get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ugc_age"] = update.message.text
    await update.message.reply_text(
        t(context, "ugc_ask_city"), parse_mode="Markdown", reply_markup=ugc_cancel_kb(context),
    )
    return UGC_CITY

async def ugc_get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ugc_city"] = update.message.text
    await update.message.reply_text(
        t(context, "ugc_ask_instagram"), parse_mode="Markdown", reply_markup=ugc_cancel_kb(context),
    )
    return UGC_INSTAGRAM

async def ugc_get_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ugc_instagram"] = update.message.text
    await update.message.reply_text(
        t(context, "ugc_ask_phone"), parse_mode="Markdown", reply_markup=ugc_cancel_kb(context),
    )
    return UGC_PHONE

async def ugc_get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ugc_phone"] = update.message.text
    await update.message.reply_text(
        t(context, "ugc_confirm").format(
            name=context.user_data["ugc_name"],
            age=context.user_data["ugc_age"],
            city=context.user_data["ugc_city"],
            instagram=context.user_data["ugc_instagram"],
            phone=context.user_data["ugc_phone"],
        ),
        parse_mode="Markdown", reply_markup=ugc_confirm_kb(context),
    )
    return UGC_CONFIRM

async def ugc_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "ugc_confirm_yes":
        name = context.user_data["ugc_name"]
        age = context.user_data["ugc_age"]
        city = context.user_data["ugc_city"]
        instagram = context.user_data["ugc_instagram"]
        phone = context.user_data["ugc_phone"]
        user = query.from_user
        username = f"@{user.username}" if user.username else "—"
        await query.edit_message_text(t(context, "ugc_success"), parse_mode="Markdown")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🤝 YANGI UGC ARIZA!\n\n"
                f"👤 Ism: {name}\n"
                f"🎂 Yosh: {age}\n"
                f"🏙️ Shahar: {city}\n"
                f"📱 Instagram: {instagram}\n"
                f"📞 Tel: {phone}\n"
                f"💬 Telegram: {username}\n"
                f"🆔 ID: {user.id}"
            ),
        )
    else:
        await query.edit_message_text(t(context, "ugc_cancelled"))
    return ConversationHandler.END

async def ugc_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(t(context, "ugc_cancelled"))
    return ConversationHandler.END

# ─── MAIN ─────────────────────────────────────────────────────────────────────

async def run_bot():
    logging.basicConfig(level=logging.WARNING)
    app = Application.builder().token(BOT_TOKEN).build()

    lang_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={LANG: [CallbackQueryHandler(choose_lang, pattern="^lang_")]},
        fallbacks=[CommandHandler("start", start)],
        per_message=False,
    )

    order_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(order_start, pattern="^order_start$")],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_get_phone)],
            PACKAGE: [CallbackQueryHandler(order_get_package, pattern="^pkg_")],
            CONFIRM: [CallbackQueryHandler(order_confirm, pattern="^(confirm_yes|cancel_order)$")],
        },
        fallbacks=[
            CallbackQueryHandler(order_cancel, pattern="^cancel_order$"),
            CommandHandler("start", start),
        ],
        per_message=False,
    )

    ugc_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(ugc_start, pattern="^ugc_start$")],
        states={
            UGC_NAME: [
                CallbackQueryHandler(ugc_begin, pattern="^ugc_begin$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, ugc_get_name),
            ],
            UGC_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ugc_get_age)],
            UGC_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ugc_get_city)],
            UGC_INSTAGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ugc_get_instagram)],
            UGC_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ugc_get_phone)],
            UGC_CONFIRM: [CallbackQueryHandler(ugc_confirm, pattern="^(ugc_confirm_yes|cancel_ugc)$")],
        },
        fallbacks=[
            CallbackQueryHandler(ugc_cancel, pattern="^cancel_ugc$"),
            CommandHandler("start", start),
        ],
        per_message=False,
    )

    app.add_handler(lang_conv)
    app.add_handler(order_conv)
    app.add_handler(ugc_conv)
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot ishlamoqda...")
    async with app:
        await app.start()
        await app.updater.start_polling()
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run_bot())
