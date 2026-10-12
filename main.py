import os
import telebot
from telebot import types

# Вместо реального токена пишем вот эту команду. 
# Она будет брать токен из секретных настроек сервера Render.
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)



# ============ КЛАВИАТУРЫ ============
def main_menu_kb() -> types.InlineKeyboardMarkup:
    """Главное меню с тремя кнопками."""
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(text="👕 Каталог", callback_data="catalog"),
        types.InlineKeyboardButton(text="📦 Доставка", callback_data="delivery"),
        types.InlineKeyboardButton(text="📱 Менеджер", callback_data="manager"),
    )
    return kb


def catalog_kb() -> types.InlineKeyboardMarkup:
    """Меню категорий внутри каталога."""
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(text="🧥 Худи", callback_data="cat_hoodie"),
        types.InlineKeyboardButton(text="👕 Футболки", callback_data="cat_tshirt"),
        types.InlineKeyboardButton(text="👜 Аксессуары", callback_data="cat_accessories"),
        types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu"),
    )
    return kb


def back_kb() -> types.InlineKeyboardMarkup:
    """Кнопка 'Назад' в главное меню."""
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu"))
    return kb


# ============ ХЭНДЛЕРЫ ============
@bot.message_handler(commands=["start"])
def cmd_start(message: types.Message) -> None:
    """Реакция на команду /start."""
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в магазин корейской одежды 🇰🇷\n"
        "Выберите раздел:",
        reply_markup=main_menu_kb(),
    )


@bot.callback_query_handler(func=lambda call: call.data == "catalog")
def cb_catalog(call: types.CallbackQuery) -> None:
    """Нажатие на 'Каталог'."""
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👕 <b>Каталог товаров</b>\n\nВыберите категорию:",
        reply_markup=catalog_kb(),
    )
    bot.answer_callback_query(call.id)  # убираем "часики" на кнопке


@bot.callback_query_handler(func=lambda call: call.data == "delivery")
def cb_delivery(call: types.CallbackQuery) -> None:
    """Нажатие на 'Доставка'."""
    text = (
        "📦 <b>Условия доставки</b>\n\n"
        "🇰🇿 <b>По Казахстану:</b>\n"
        "• Срок: 3–7 рабочих дней\n"
        "• Стоимость: от 1500 ₸ (зависит от региона)\n"
        "• Отправка через Казпочту / СДЭК\n\n"
        "🏙 <b>В город Жезказган:</b>\n"
        "• Срок: 2–4 рабочих дня\n"
        "• Стоимость: 1000 ₸\n"
        "• Возможен самовывоз (адрес уточняйте у менеджера)\n\n"
        "📌 Заказ собирается в течение 1 рабочего дня после оплаты."
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=back_kb(),
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == "manager")
def cb_manager(call: types.CallbackQuery) -> None:
    """Нажатие на 'Менеджер'."""
    text = (
        "📱 <b>Связь с менеджером</b>\n\n"
        "По всем вопросам пишите напрямую:\n"
        f"👉 @{MANAGER_USERNAME}"
    )
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(
            text="💬 Написать менеджеру",
            url=f"https://t.me/{MANAGER_USERNAME}",
        ),
        types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu"),
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=kb,
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def cb_category(call: types.CallbackQuery) -> None:
    """Нажатие на конкретную категорию внутри каталога."""
    titles = {
        "cat_hoodie": "🧥 Худи",
        "cat_tshirt": "👕 Футболки",
        "cat_accessories": "👜 Аксессуары",
    }
    title = titles.get(call.data, "Категория")

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(
            f"<b>{title}</b>\n\n"
            "Здесь будет список товаров этой категории.\n"
            "(Добавим позже — подключим базу данных или JSON.)"
        ),
        reply_markup=catalog_kb(),
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def cb_back(call: types.CallbackQuery) -> None:
    """Возврат в главное меню."""
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Главное меню. Выберите раздел:",
        reply_markup=main_menu_kb(),
    )
    bot.answer_callback_query(call.id)


# ============ ЗАПУСК ============
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
