from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard():
    builder = InlineKeyboardBuilder()
    # builder.row(InlineKeyboardButton(text="Запустить приложение", url="https://t.me/srit_bot/app"))
    builder.row(InlineKeyboardButton(text="Запустить приложение", web_app=WebAppInfo(url="https://mini-app.penki.tech/")))
    builder.row(InlineKeyboardButton(text="Помощь и поддержка", url="https://google.com/"))
    return builder.as_markup()
