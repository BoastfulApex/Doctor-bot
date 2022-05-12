from aiogram import types
import pandas as pd
import datetime
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from utils.db_api import database as commands
from loader import dp, bot
from keyboards.inline.menu_button import doctor_menu, confirm_keyboard, get_or_back, back_to, year_keyboard, \
    month_keyboard
from keyboards.inline.main_inline import admin_menu, back_admin_menu, doctor_in_admin, category_keyboard
from utils.db_api.database import *


@dp.callback_query_handler(state='doctor_menu_admin')
async def get_command(call: types.CallbackQuery, state: FSMContext):
    command = call.data
    data = await state.get_data()
    if command == 'back_admin':
        markup = await admin_menu()
        await call.message.edit_text(text="Kerakli bo'limni tanlang 👇",
                                     reply_markup=markup)
        await state.set_state('admin_menu')
    elif command == "kash_today":
        orders = await get_orders()
        doctor = await get_doctor(data['doctor'])
        keshbek = []
        summa = 0
        sana = []
        preparat = []
        kod = []
        kesh = []
        for i in orders:
            if i.doctor == doctor and i.date.day == datetime.datetime.now().day:
                keshbek.append(i)
                summa += i.summa
                sana.append(f"{i.date}")
                preparat.append(i.product.product_name)
                kod.append(i.product.kod)
                kesh.append(i.product.keshbek)

        text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
               f"💸 Jami keshbeklar summasi: {summa}\n\n" \
               f"To'liq ma'lumot olish uchun xujjatni yuklab oling 👇"
        sana.append('Umumiy')
        preparat.append(f'{len(keshbek)}')
        kod.append(f'{len(keshbek)}')
        kesh.append(summa)
        df = pd.DataFrame({'Sana': sana,
                           'Preparat': preparat,
                           'Kod': kod,
                           'Keshbek': kesh, })
        df.to_excel('./xisobot.xlsx')
        markup = await get_or_back()
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state('get_or_back_doctor')
    elif command == "kash_this_month":
        orders = await get_orders()
        doctor = await get_doctor(data['doctor'])
        keshbek = []
        summa = 0
        sana = []
        preparat = []
        kod = []
        kesh = []
        for i in orders:
            if i.doctor == doctor and i.date.month == datetime.datetime.now().month:
                keshbek.append(i)
                summa += i.summa
                sana.append(f"{i.date}")
                preparat.append(i.product.product_name)
                kod.append(i.product.kod)
                kesh.append(i.product.keshbek)

        text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
               f"💸 Jami keshbeklar summasi: {summa}\n\n" \
               f"To'liq ma'lumot olish uchun xujjatni yuklab oling 👇"
        sana.append('Umumiy')
        preparat.append(f'{len(keshbek)}')
        kod.append(f'{len(keshbek)}')
        kesh.append(summa)
        df = pd.DataFrame({'Sana': sana,
                           'Preparat': preparat,
                           'Kod': kod,
                           'Keshbek': kesh, })
        df.to_excel('./xisobot.xlsx')
        markup = await get_or_back()
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state('get_or_back_doctor')
    elif command == 'kash_day':
        years = []
        orders = await get_orders()
        doctor = await get_doctor(data['doctor'])
        for order in orders:
            if order.doctor.id == doctor.id:
                years.append(order.date.year)
        years = list(dict.fromkeys(years))
        markup = await year_keyboard(years)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_admin')
    elif command == 'kash_month':
        years = []
        orders = await get_orders()
        doctor = await get_doctor(data['doctor'])
        for order in orders:
            if order.doctor.id == doctor.id:
                years.append(order.date.year)
        years = list(dict.fromkeys(years))
        markup = await year_keyboard(years)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_month_admin')


@dp.callback_query_handler(state="get_year_month_admin")
async def get_year(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data == 'back_menu':
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        doctor = await get_doctor(state_data['doctor'])
        for order in orders:
            if order.doctor.id == doctor.id and order.date.year == int(data):
                date.append(order.date.month)
        date = list(dict.fromkeys(date))
        markup = await month_keyboard(date)
        await call.message.edit_text(text='Kerakli oyni tanlang 👇', reply_markup=markup)
        await state.update_data(year=data)
        await state.set_state('get_month_month_admin')
    else:
        markup = await doctor_in_admin()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('doctor_menu_admin')


@dp.callback_query_handler(state="get_month_month_admin")
async def get_year(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data != 'back_menu':
        date = []
        keshbek = []
        summa = 0
        sana = []
        preparat = []
        kod = []
        kesh = []
        state_data = await state.get_data()
        orders = await get_orders()
        doctor = await get_doctor(state_data['doctor'])
        for order in orders:
            if order.doctor.id == doctor.id and order.date.year == int(state_data['year']) and order.date.month == int(
                    data):
                keshbek.append(order)
                summa += order.summa
                sana.append(f"{order.date}")
                preparat.append(order.product.product_name)
                kod.append(order.product.kod)
                kesh.append(order.product.keshbek)
        text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
               f"💸 Jami keshbeklar summasi: {summa}\n\n" \
               f"To'liq ma'lumot olish uchun xujjatni yuklab oling 👇"
        sana.append('Umumiy')
        preparat.append(f'{len(keshbek)}')
        kod.append(f'{len(keshbek)}')
        kesh.append(summa)
        df = pd.DataFrame({'Sana': sana,
                           'Preparat': preparat,
                           'Kod': kod,
                           'Keshbek': kesh, })
        df.to_excel('./xisobot.xlsx')
        markup = await get_or_back()
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state('get_or_back_doctor')
    else:
        markup = await doctor_in_admin()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('doctor_menu_admin')


@dp.callback_query_handler(state="get_year_admin")
async def get_year(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data != 'back_menu':
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        doctor = await get_doctor(state_data['doctor'])
        for order in orders:
            if order.doctor.id == doctor.id and order.date.year == int(data):
                date.append(order.date.month)
        date = list(dict.fromkeys(date))
        markup = await month_keyboard(date)
        await call.message.edit_text(text='Kerakli oyni tanlang 👇', reply_markup=markup)
        await state.update_data(year=data)
        await state.set_state('get_month_admin')
    else:
        markup = await doctor_in_admin()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('doctor_menu_admin')


@dp.callback_query_handler(state="get_month_admin")
async def get_year(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data != 'back_menu':
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        doctor = await get_doctor(state_data['doctor'])
        for order in orders:
            if order.doctor.id == doctor.id and order.date.year == int(state_data['year']) and order.date.month == int(
                    data):
                date.append(order.date.day)
        date = list(dict.fromkeys(date))
        markup = await year_keyboard(date)
        await call.message.edit_text(text='Kerakli kunnni tanlang 👇', reply_markup=markup)
        await state.update_data(month=data)
        await state.set_state('get_day_admin')
    else:
        markup = await doctor_in_admin()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('doctor_menu_admin')


@dp.callback_query_handler(state='get_day_admin')
async def get_day(call: types.CallbackQuery, state: FSMContext):
    day = call.data
    if day != 'back_menu':
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        doctor = await get_doctor(state_data['doctor'])
        keshbek = []
        summa = 0
        sana = []
        preparat = []
        kod = []
        kesh = []
        for order in orders:
            if order.doctor.id == doctor.id and order.date.year == int(state_data['year']) and order.date.month == int(
                    state_data['month']) and order.date.day == int(day):
                date.append(order)
                keshbek.append(order)
                summa += order.summa
                sana.append(f"{order.date}")
                preparat.append(order.product.product_name)
                kod.append(order.product.kod)
                kesh.append(order.product.keshbek)
        await state.update_data(day=day)

        text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
               f"💸 Jami keshbeklar summasi: {summa}\n\n" \
               f"To'liq ma'lumot olish uchun xujjatni yuklab oling 👇"
        sana.append('Umumiy')
        preparat.append(f'{len(keshbek)}')
        kod.append(f'{len(keshbek)}')
        kesh.append(summa)
        df = pd.DataFrame({'Sana': sana,
                           'Preparat': preparat,
                           'Kod': kod,
                           'Keshbek': kesh, })
        df.to_excel('./xisobot.xlsx')
        markup = await get_or_back()
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state('get_or_back_doctor')
    else:
        markup = await doctor_in_admin()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('doctor_menu_admin')


@dp.callback_query_handler(state="get_or_back_doctor")
async def get_file(call: types.CallbackQuery, state: FSMContext):
    command = call.data
    if command == 'get':
        file = open('./xisobot.xlsx', 'rb')
        markup = await back_to()
        await call.message.delete()
        await bot.send_document(chat_id=call.from_user.id, document=file, reply_markup=markup, caption="📊 Hisobot")
        await state.set_state('back_doctor_menu_admin')
    else:
        markup = await doctor_in_admin()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('doctor_menu_admin')


@dp.callback_query_handler(state="back_doctor_menu_admin")
async def back_to_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    markup = await doctor_in_admin()
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
    await state.set_state("doctor_menu_admin")
