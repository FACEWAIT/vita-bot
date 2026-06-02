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
            "• Suli (овёс)\n"
            "• Lavlagi (свёкла)\n"
            "• Yalpiz (мята)\n\n"
            "✅ 100% tabiiy mahsulot. Hech qanday kimyoviy qo'shimchalar yo'q."
        ),
        "faq_usage": (
            "📋 *Qanday ichish kerak:*\n\n"
            "• Har kuni ichish tavsiya etiladi\n"
            "• Minimum: kuniga 1 shisha\n"
            "• Tavsiya etilgan miqdor: kuniga 500 ml\n\n"
            "⏰ *Qachon ichish yaxshi?*\n\n"
            "🌙 *Kechqurun* — uxlashdan 30 daqiqa oldin\n"
            "🌅 *Ertalab* — faqat ishga chiqsangiz yoki uyda bo'lsangiz\n\n"
            "🫙 Ichishdan oldin yaxshilab chayqating!"
        ),
        "faq_benefits": (
            "✅ *Foydasi:*\n\n"
            "• Tabiiy energiya va tetiklik beradi ⚡\n"
            "• Umumiy ahvolni yaxshilaydi\n"
            "• Ishtahani nazorat qilishga yordam beradi\n"
            "• Og'irlik his-tuyg'usini kamaytiradi\n"
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
            "📌 *Minimum:* kuniga 1 shisha, keyin almashtirib\n"
            "_(1-kun 200 ml, 2-kun 300 ml — 3 oy davomida)_\n\n"
            "⭐ *Tavsiya etilgan:* kuniga 500 ml\n"
            "_(bu to'liq kurs — eng yaxshi natija)_\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🚚 *Yetkazib berish:*\n"
            "• Toshkent shahrida — *bepul*\n"
            "• Toshkent viloyatida — alohida to'lanadi"
        ),
        "faq_certificate": (
            "📄 *Sertifikat:*\n\n"
            "Hozirda sertifikat rasmiylashtirish jarayonida.\n\n"
            "Savollar bo'lsa:\n"
            "📞 +998 33 854 34 34\n"
            "💬 @Muzaffar3790"
        ),
        "faq_where": (
            "📍 *Qayerdan sotib olish:*\n\n"
            "📱 Instagram: @vita\\_deluxe.uz\n"
            "🌐 Sayt: vitadeluxe.taplink.ws\n"
            "📞 Tel: +998 33 854 34 34\n"
            "💬 Telegram: @Muzaffar3790\n\n"
            "Yoki quyida buyurtma bering 👇"
        ),
        "order_ask_name": "🛒 *Buyurtma berish*\n\nIsmingizni yozing 👇",
        "order_ask_phone": "Rahmat, *{name}*! 👍\n\nTelefon raqamingizni yozing:\n_Misol: +998901234567_",
        "order_ask_package": (
            "📦 *Qaysi paketni tanlaysiz?*\n\n"
            "🧪 *Sinov paketi* — mahsulotni sinab ko'rish uchun\n"
            "5 ta × 200 ml + 5 ta × 300 ml\n\n"
            "📦 *To'liq kurs (3 oy)* — eng yaxshi natija uchun\n"
            "45 ta × 200 ml + 45 ta × 300 ml\n"
            "_Kuniga 1 shisha almashtirib (minimum)\n"
            "yoki kuniga 500 ml (tavsiya etilgan)_"
        ),
        "btn_trial": "🧪 Sinov paketi — 116 000 so'm (−20%)",
        "btn_course": "📦 To'liq kurs 3 oy — 1 305 000 so'm",
        "order_confirm_text": (
            "✅ *Buyurtmangizni tekshiring:*\n\n"
            "👤 Ism: {name}\n"
            "📞 Telefon: {phone}\n"
            "📦 Paket: {package}\n\n"
            "Tasdiqlaysizmi?"
        ),
        "order_success": (
            "🎉 *Buyurtmangiz qabul qilindi!*\n\n"
            "Tez orada @Muzaffar3790 siz bilan bog'lanadi. 📞\n\n"
            "Boshqa savol bo'lsa: /start"
        ),
        "order_cancelled": "❌ Buyurtma bekor qilindi.\n\n/start — bosh menuga qaytish",
        "admin_notify": (
            "🔔 *YANGI BUYURTMA!*\n\n"
            "👤 Ism: {name}\n"
            "📞 Telefon: {phone}\n"
            "📦 Paket: {package}\n"
            "📱 Telegram: {username}\n"
            "🆔 User ID: {user_id}"
        ),
    },

    "ru": {
        "welcome": (
            "Привет! 👋\n\n"
            "⚡ *VITA DELUXE* — натуральный энергетический напиток "
            "из овса, свёклы и мяты!\n\n"
            "Даёт энергию, контролирует аппетит и поддерживает "
            "здоровый образ жизни 🌿\n\n"
            "Выберите одно из следующего:"
        ),
        "choose_section": "Выберите одно из следующего:",
        "faq_title": "❓ *Частые вопросы*\n\nВыберите интересующий вопрос:",
        "btn_faq": "❓ Частые вопросы",
        "btn_order": "🛒 Сделать заказ",
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
            "• Овёс\n"
            "• Свёкла\n"
            "• Мята\n\n"
            "✅ 100% натуральный продукт. Никаких химических добавок."
        ),
        "faq_usage": (
            "📋 *Как принимать:*\n\n"
            "• Рекомендуется пить ежедневно\n"
            "• Минимум: 1 бутылка в день\n"
            "• Рекомендуемая норма: 500 мл в день\n\n"
            "⏰ *Когда лучше пить?*\n\n"
            "🌙 *Вечером* — за 30 минут до сна\n"
            "🌅 *Утром* — только если работаете или сидите дома\n\n"
            "🫙 Перед употреблением хорошо взболтать!"
        ),
        "faq_benefits": (
            "✅ *Польза:*\n\n"
            "• Даёт натуральную энергию и бодрость ⚡\n"
            "• Улучшает общее самочувствие\n"
            "• Помогает контролировать аппетит\n"
            "• Уменьшает чувство тяжести\n"
            "• Поддерживает здоровый образ жизни\n"
            "• При правильном питании и активности помогает снизить вес"
        ),
        "faq_price": (
            "💰 *Цены:*\n\n"
            "🧪 *Пробный пакет* _(10 бутылок)_\n"
            "5 × 200 мл + 5 × 300 мл\n"
            "~~145 000~~ → *116 000 сум* _(скидка −20%)_\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "📦 *Полный курс — 3 месяца* _(90 бутылок)_\n"
            "45 × 200 мл + 45 × 300 мл\n"
            "*1 305 000 сум*\n\n"
            "📌 *Минимум:* 1 бутылка в день, чередуя\n"
            "_(1-й день 200 мл, 2-й день 300 мл — 3 месяца)_\n\n"
            "⭐ *Рекомендуется:* 500 мл в день\n"
            "_(полноценный курс — лучший результат)_\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "🚚 *Доставка:*\n"
            "• По Ташкенту — *бесплатно*\n"
            "• По Ташкентской области — оплачивается отдельно"
        ),
        "faq_certificate": (
            "📄 *Сертификат:*\n\n"
            "На данный момент сертификат в процессе оформления.\n\n"
            "По вопросам:\n"
            "📞 +998 33 854 34 34\n"
            "💬 @Muzaffar3790"
        ),
        "faq_where": (
            "📍 *Где купить:*\n\n"
            "📱 Instagram: @vita\\_deluxe.uz\n"
            "🌐 Сайт: vitadeluxe.taplink.ws\n"
            "📞 Тел: +998 33 854 34 34\n"
            "💬 Telegram: @Muzaffar3790\n\n"
            "Или сделайте заказ прямо здесь 👇"
        ),
        "order_ask_name": "🛒 *Оформление заказа*\n\nНапишите ваше имя 👇",
        "order_ask_phone": "Спасибо, *{name}*! 👍\n\nНапишите ваш номер телефона:\n_Пример: +998901234567_",
        "order_ask_package": (
            "📦 *Какой пакет выбираете?*\n\n"
            "🧪 *Пробный пакет* — попробовать продукт\n"
            "5 × 200 мл + 5 × 300 мл\n\n"
            "📦 *Полный курс (3 месяца)* — для лучшего результата\n"
            "45 × 200 мл + 45 × 300 мл\n"
            "_Минимум: 1 бутылка в день, чередуя\n"
            "Рекомендуется: 500 мл в день_"
        ),
        "btn_trial": "🧪 Пробный пакет — 116 000 сум (−20%)",
        "btn_course": "📦 Полный курс 3 мес — 1 305 000 сум",
        "order_confirm_text": (
            "✅ *Проверьте ваш заказ:*\n\n"
            "👤 Имя: {name}\n"
            "📞 Телефон: {phone}\n"
            "📦 Пакет: {package}\n\n"
            "Подтверждаете?"
        ),
        "order_success": (
            "🎉 *Ваш заказ принят!*\n\n"
            "Скоро @Muzaffar3790 свяжется с вами. 📞\n\n"
            "Другие вопросы: /start"
        ),
        "order_cancelled": "❌ Заказ отменён.\n\n/start — вернуться в главное меню",
        "admin_notify": (
            "🔔 *НОВЫЙ ЗАКАЗ!*\n\n"
            "👤 Имя: {name}\n"
            "📞 Телефон: {phone}\n"
            "📦 Пакет: {package}\n"
            "📱 Telegram: {username}\n"
            "🆔 User ID: {user_id}"
        ),
    },
}

def t(context, key):
    lang = context.user_data.get("lang", "uz")
    return T[lang][key]

LANG, NAME, PHONE, PACKAGE, CONFIRM = range(5)

def lang_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
         InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
    ])

def main_menu(context):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(context, "btn_faq"), callback_data="faq")],
        [InlineKeyboardButton(t(context, "btn_order"), callback_data="order_start")],
        [InlineKeyboardButton(t(context, "btn_where"), callback_data="faq_where")],
    ])

def faq_menu(context):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(context, "btn_ingredients"), callback_data="faq_ingredients")],
        [InlineKeyboardButton(t(context, "btn_usage"), callback_data="faq_usage")],
        [InlineKeyboardButton(t(context, "btn_benefits"), callback_data="faq_benefits")],
        [InlineKeyboardButton(t(context, "btn_price"), callback_data="faq_price")],
        [InlineKeyboardButton(t(context, "btn_certificate"), callback_data="faq_certificate")],
        [InlineKeyboardButton(t(context, "btn_where"), callback_data="faq_where")],
        [InlineKeyboardButton(t(context, "btn_back_main"), callback_data="back_main")],
    ])

def back_faq_kb(context):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(context, "btn_back_faq"), callback_data="faq")],
        [InlineKeyboardButton(t(context, "btn_back_main"), callback_data="back_main")],
    ])

def cancel_kb(context):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(context, "btn_cancel"), callback_data="cancel_order")],
    ])

def package_kb(context):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(context, "btn_trial"), callback_data="pkg_trial")],
        [InlineKeyboardButton(t(context, "btn_course"), callback_data="pkg_course")],
        [InlineKeyboardButton(t(context, "btn_cancel"), callback_data="cancel_order")],
    ])

def confirm_kb(context):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(context, "btn_confirm"), callback_data="confirm_yes")],
        [InlineKeyboardButton(t(context, "btn_cancel"), callback_data="cancel_order")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 *VITA DELUXE*\n\nTilni tanlang / Выберите язык:",
        parse_mode="Markdown",
        reply_markup=lang_kb(),
    )
    return LANG

async def choose_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["lang"] = "uz" if query.data == "lang_uz" else "ru"
    await query.edit_message_text(
        t(context, "welcome"),
        parse_mode="Markdown",
        reply_markup=main_menu(context),
    )
    return ConversationHandler.END

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_main":
        await query.edit_message_text(
            t(context, "choose_section"),
            reply_markup=main_menu(context),
        )
    elif data == "faq":
        await query.edit_message_text(
            t(context, "faq_title"),
            parse_mode="Markdown",
            reply_markup=faq_menu(context),
        )
    elif data.startswith("faq_"):
        await query.edit_message_text(
            t(context, data),
            parse_mode="Markdown",
            reply_markup=back_faq_kb(context),
        )

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        t(context, "order_ask_name"),
        parse_mode="Markdown",
        reply_markup=cancel_kb(context),
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        t(context, "order_ask_phone").format(name=update.message.text),
        parse_mode="Markdown",
        reply_markup=cancel_kb(context),
    )
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text(
        t(context, "order_ask_package"),
        parse_mode="Markdown",
        reply_markup=package_kb(context),
    )
    return PACKAGE

async def get_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "uz")
    packages = {
        "pkg_trial": T[lang]["btn_trial"],
        "pkg_course": T[lang]["btn_course"],
    }
    context.user_data["package"] = packages[query.data]
    await query.edit_message_text(
        t(context, "order_confirm_text").format(
            name=context.user_data["name"],
            phone=context.user_data["phone"],
            package=context.user_data["package"],
        ),
        parse_mode="Markdown",
        reply_markup=confirm_kb(context),
    )
    return CONFIRM

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm_yes":
        name = context.user_data["name"]
        phone = context.user_data["phone"]
        package = context.user_data["package"]
        user = query.from_user
        username = f"@{user.username}" if user.username else "—"
        await query.edit_message_text(
            t(context, "order_success"), parse_mode="Markdown"
        )
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=t(context, "admin_notify").format(
                name=name, phone=phone, package=package,
                username=username, user_id=user.id,
            ),
            parse_mode="Markdown",
        )
    else:
        await query.edit_message_text(t(context, "order_cancelled"))
    return ConversationHandler.END

async def cancel_mid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(t(context, "order_cancelled"))
    return ConversationHandler.END

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
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PACKAGE: [CallbackQueryHandler(get_package, pattern="^pkg_")],
            CONFIRM: [CallbackQueryHandler(confirm_order, pattern="^(confirm_yes|cancel_order)$")],
        },
        fallbacks=[
            CallbackQueryHandler(cancel_mid, pattern="^cancel_order$"),
            CommandHandler("start", start),
        ],
        per_message=False,
    )

    app.add_handler(lang_conv)
    app.add_handler(order_conv)
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot ishlamoqda... (To'xtatish uchun Ctrl+C)")
    async with app:
        await app.start()
        await app.updater.start_polling()
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run_bot())
