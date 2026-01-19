from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def map_variants_tavern():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="⚒️Отправиться в кузницу",
            callback_data="go_to_kuzna"
        ),
        InlineKeyboardButton(
            text="⛏️Отправиться в шахту",
            callback_data="go_to_shahta"
        ),
        InlineKeyboardButton(
            text="🎮Отправиться в данж",
            callback_data="go_to_danj"
        )
    )

    builder.adjust(1)
    return builder.as_markup()