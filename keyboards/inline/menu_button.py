from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from backend.models import *


async def doctor_menu():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🆕 Bir martalik keshbek kodini kiritish", callback_data="add_kash")],
            [InlineKeyboardButton(text="🗓 Bugungi kungi keshbekni ko'rish", callback_data="kash_today")],
            [InlineKeyboardButton(text="📆 Alohida kun uchun keshbekni ko'rish", callback_data="kash_day")],
            [InlineKeyboardButton(text="🗓 Shu oy uchun keshbekni ko'rish", callback_data="kash_this_month")],
            [InlineKeyboardButton(text="📆 Alohida oy uchun keshbekni ko'rish", callback_data="kash_month")],
        ]
    )
    return markup


async def confirm_keyboard():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Yo'q", callback_data=f"cancel"),
                InlineKeyboardButton(text="✅ Ha", callback_data=f"confirm"),
            ],
        ]
    )
    return markup


async def get_or_back():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back"),
                InlineKeyboardButton(text="📑 Excell hujjatni yuklash", callback_data=f"get"),
            ],
        ]
    )
    return markup


async def moth_by_doctor(doctor):
    orders = Order.objects.filter(doctor__unique_password=doctor)
    inline_keyboard = []
    for i in orders:
        inline_keyboard.append([InlineKeyboardButton(text=i.category_name, callback_data=i.id)])
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


async def back_to():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_to_menu"),
            ],
        ]
    )
    return markup


async def year_keyboard(years):
    inline_keyboard = []
    for i in years:
        inline_keyboard.append([InlineKeyboardButton(text=f"{i}", callback_data=i)])
    inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


Moths = {1: 'Yanvar', 2: 'Fevral', 3: 'Mart', 4: 'Aprel', 5: 'May', 6: 'Iyun', 7: 'Iyul', 8: 'Avgust', 9: 'Sentabr',
         10: 'Oktyabr', 11: 'Noyabr', 12: 'Dekabr', }


async def month_keyboard(date):
    inline_keyboard = []
    for i in date:
        inline_keyboard.append([InlineKeyboardButton(text=f"{Moths[i]}", callback_data=i)])
    inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup
