from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from utils.db_api import database as commands
from loader import dp, bot
from keyboards.inline.menu_button import doctor_menu, confirm_keyboard
from keyboards.inline.main_inline import admin_menu, logout_keyboard
from utils.db_api.database import *


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    text = "Iltimos botdan foydalanish uchun Shaxsiy parolingizni kiriting 👇"
    markup = await logout_keyboard()
    await message.answer(f"Assalomu alaykum , {message.from_user.full_name}!\n"
                         f"{text}.", reply_markup=markup)
    await state.set_state('check_password')


@dp.message_handler(lambda message: message.text.startswith("⬅️Chiqish"), state="*")
async def logout(message: types.Message, state: FSMContext):
    await state.finish()
    text = "Iltimos botdan foydalanish uchun Shaxsiy parolingizni kiriting 👇"
    markup = await logout_keyboard()
    await message.answer(f"Assalomu alaykum , {message.from_user.full_name}!\n"
                         f"{text}.", reply_markup=markup)
    await state.set_state('check_password')


@dp.message_handler(state="check_password", content_types=types.ContentTypes.TEXT)
async def check_password(message: types.Message, state: FSMContext):
    password = message.text
    user = await commands.get_doctor(password)
    if user is not None:
        if user.is_admin:
            markup = await admin_menu()
            await bot.send_message(chat_id=message.from_user.id, text="Assalomu alaykum Admin. "
                                                                      "Kerakli bo'limni tanlang 👇",
                                   reply_markup=markup)
            await state.set_state('admin_menu')
        else:
            markup = await doctor_menu()
            await bot.send_message(chat_id=message.from_user.id, text=f"Assalomu alaykum {user.full_name}",
                                   reply_markup=markup)
            await state.set_state('doctor_menu')
            await state.update_data(doctor=password)
            await state.update_data(doctor=user.unique_password)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="❌ Ushbu parol bilan foydalanuvchi toplimadi\n"
                                                                  "🔄 Parolni qaytadan kiriting ")
        await state.set_state('check_password')


