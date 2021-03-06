from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *
from utils.db_api.database import *


async def admin_menu():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="β Yangi keshbeklar ro'yxatini kiritish", callback_data="add_kash_list")],
            [InlineKeyboardButton(text="π¨ββοΈAlohida doktor uchun hisobotlar", callback_data="kash_by_doctor")],
            [InlineKeyboardButton(text="π Umimiy keshbeklar", callback_data="all_kash")],
            [InlineKeyboardButton(text="π Sohalar bo'yicha keshbeklar", callback_data="kash_by_category")],
            [InlineKeyboardButton(text="π Bugungi keshbekni ko'rish", callback_data="kash_this_day")],
            [InlineKeyboardButton(text="π Tanlangan kun uchun keshbekni ko'rish", callback_data="kash_in_day")],
            [InlineKeyboardButton(text="π Shu oy uchun keshbekni ko'rish", callback_data="kash_this_month")],
            [InlineKeyboardButton(text="π Tanlangan oy uchun keshbekni ko'rish", callback_data="kash_in_month")],
            [InlineKeyboardButton(text="ποΈAlohida preparat bo'yicha keshbeklar", callback_data="kash_by_product")],
        ]
    )
    return markup


async def back_admin_menu():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="π Orqaga", callback_data=f"back_admin"),
            ],
        ]
    )
    return markup


async def doctor_in_admin():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="π Bugungi kungi keshbekni ko'rish", callback_data="kash_today")],
            [InlineKeyboardButton(text="π Alohida kun uchun keshbekni ko'rish", callback_data="kash_day")],
            [InlineKeyboardButton(text="π Shu oy uchun keshbekni ko'rish", callback_data="kash_this_month")],
            [InlineKeyboardButton(text="π Alohida oy uchun keshbekni ko'rish", callback_data="kash_month")],
            [InlineKeyboardButton(text="π Orqaga", callback_data=f"back_admin")],
        ]
    )
    return markup


async def category_keyboard():
    categories = await get_categories()
    inline_keyboard = []
    for i in categories:
        inline_keyboard.append([InlineKeyboardButton(text=i.category_name, callback_data=i.id)])
    inline_keyboard.append([InlineKeyboardButton(text="π Orqaga", callback_data=f"back_menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


async def logout_keyboard():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text="β¬οΈChiqish")
    keyboard.add(key1)
    keyboard.resize_keyboard = True
    return keyboard
