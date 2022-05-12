import datetime
from itertools import product

from aiogram import types
import pandas as pd
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from utils.db_api import database as commands
from loader import dp, bot
from keyboards.inline.menu_button import doctor_menu, confirm_keyboard, get_or_back, back_to, year_keyboard, \
    month_keyboard
from keyboards.inline.main_inline import admin_menu, back_admin_menu, doctor_in_admin, category_keyboard
from utils.db_api.database import *


@dp.callback_query_handler(state="admin_menu")
async def get_admin_command(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data == "add_kash_list":
        markup = await back_admin_menu()
        await call.message.edit_text(text="📊 Ro'yxatni yuklang.", reply_markup=markup)
        await state.set_state('get_file')
    elif data == 'kash_by_doctor':
        await call.message.edit_text(text="Tanlamoxchi bo'lgan 👨‍⚕️Doktorning ID sini kiriting")
        await state.set_state('get_doctor_id')
    elif data == 'kash_by_category':
        if data != 'back_menu':
            orders = await get_orders()
            categories = await get_categories()
            soha = []
            all = []
            jami = 0
            for category in categories:
                summa = 0
                for i in orders:
                    if i.product.category.id == category.id:
                        summa += i.summa
                all.append(summa)
                jami += summa
                soha.append(category.speciality)
            df = pd.DataFrame({'Soha': soha,
                               'Keshbek': all, })
            df.to_excel('./xisobot.xlsx')
            text = f"📈 Jami sohalar: {len(categories)}\n" \
                   f"🚛 Jami keshbek summasi: {jami}"
            markup = await get_or_back()
            await call.message.edit_text(text=text, reply_markup=markup)
            await state.set_state('get_or_back_admin')
    elif data == 'all_kash':
        orders = await get_orders()
        keshbek = []
        summa = 0
        sana = []
        preparat = []
        kod = []
        doctors = []
        kesh = []
        for i in orders:
            keshbek.append(i)
            summa += i.summa
            sana.append(f"{i.date}")
            preparat.append(i.product.product_name)
            kod.append(i.product.kod)
            kesh.append(i.product.keshbek)
            doctors.append(i.doctor.full_name)
        text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
               f"💸 Jami keshbek summasi: {summa}\n\n" \
               f"To'liq ma'lumot olish uchun xujjatni yuklab oling 👇"
        sana.append('Umumiy')
        preparat.append(f'{len(keshbek)}')
        kod.append(f'{len(keshbek)}')
        doctors.append(f'{len(keshbek)}')
        kesh.append(summa)
        df = pd.DataFrame({'Sana': sana,
                           'Doktor': doctors,
                           'Preparat': preparat,
                           'Kod': kod,
                           'Keshbek': kesh, })
        df.to_excel('./xisobot.xlsx')
        markup = await get_or_back()
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state('get_or_back_admin')
    elif data == "kash_this_day":
        orders = await get_orders()
        keshbek = []
        summa = 0
        sana = []
        doctors = []
        preparat = []
        kod = []
        kesh = []
        for i in orders:
            if i.date.day == datetime.datetime.now().day:
                keshbek.append(i)
                summa += i.summa
                sana.append(f"{i.date}")
                preparat.append(i.product.product_name)
                kod.append(i.product.kod)
                kesh.append(i.product.keshbek)
                doctors.append(i.doctor.full_name)
        text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
               f"💸 Jami keshbeklar summasi {summa}\n\n" \
               f"To'liq ma'lumot olish uchun xujjatni yuklab oling 👇"
        sana.append('Umumiy')
        preparat.append(f'{len(keshbek)}')
        kod.append(f'{len(keshbek)}')
        doctors.append(f'{len(keshbek)}')
        kesh.append(summa)
        df = pd.DataFrame({'Sana': sana,
                           'Doktor': doctors,
                           'Preparat': preparat,
                           'Kod': kod,
                           'Keshbek': kesh, })
        df.to_excel('./xisobot.xlsx')
        markup = await get_or_back()
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state('get_or_back_admin')
    elif data == "kash_this_month":
        orders = await get_orders()
        keshbek = []
        summa = 0
        sana = []
        doctors = []
        preparat = []
        kod = []
        kesh = []
        for i in orders:
            if i.date.day == datetime.datetime.now().day:
                keshbek.append(i)
                summa += i.summa
                sana.append(f"{i.date}")
                preparat.append(i.product.product_name)
                kod.append(i.product.kod)
                kesh.append(i.product.keshbek)
                doctors.append(i.doctor.full_name)
        text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
               f"💸 Jami keshbeklar summasi {summa}\n\n" \
               f"To'liq ma'lumot olish uchun xujjatni yuklab oling"
        sana.append('Umumiy')
        preparat.append(f'{len(keshbek)}')
        kod.append(f'{len(keshbek)}')
        doctors.append(f'{len(keshbek)}')
        kesh.append(summa)
        df = pd.DataFrame({'Sana': sana,
                           'Doktor': doctors,
                           'Preparat': preparat,
                           'Kod': kod,
                           'Keshbek': kesh, })
        df.to_excel('./xisobot.xlsx')
        markup = await get_or_back()
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state('get_or_back_admin')
    elif data == 'kash_in_day':
        years = []
        orders = await get_orders()
        for order in orders:
            years.append(order.date.year)
        years = list(dict.fromkeys(years))
        markup = await year_keyboard(years)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_')
    elif data == 'kash_in_month':
        years = []
        orders = await get_orders()
        for order in orders:
            years.append(order.date.year)
        years = list(dict.fromkeys(years))
        markup = await year_keyboard(years)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_month_')
    elif data == 'kash_by_product':
        markup = await back_admin_menu()
        await call.message.edit_text(text="💊 Preparat nomini kiriting 👇", reply_markup=markup)
        await state.set_state('get_kod_admin')


@dp.message_handler(content_types=types.ContentType.TEXT, state='get_kod_admin')
async def get_kod(message: types.Message, state: FSMContext):
    if message.text:
        name = message.text
        orders = await get_order_by_product(name)
        if orders is not None:
            keshbek = []
            summa = 0
            sana = []
            preparat = []
            kod = []
            kesh = []
            doctors = []
            for order in orders:
                keshbek.append(order)
                summa += order.summa
                sana.append(f"{order.date}")
                preparat.append(order.product.product_name)
                kod.append(order.product.kod)
                doctors.append(order.doctor.full_name)
                kesh.append(order.product.keshbek)
            text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
                   f"💸 Jami summa {summa}\n\n" \
                   f"To'liq ma'lumot olish uchun xujjatni yuklab oling 👇"
            sana.append('Umumiy')
            preparat.append(f'{len(keshbek)}')
            kod.append(f'{len(keshbek)}')
            doctors.append(f'{len(keshbek)}')
            kesh.append(summa)
            df = pd.DataFrame({'Sana': sana,
                               'Doctor': doctors,
                               'Preparat': preparat,
                               'Kod': kod,
                               'Keshbek': kesh, })
            df.to_excel('./xisobot.xlsx')
            markup = await get_or_back()
            await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
            await state.set_state('get_or_back_admin')
        else:
            markup = await back_admin_menu()
            await bot.send_message(chat_id=message.from_user.id, text="❌ Ushbu nom bilan preparat topilmadi.\n"
                                                                      "🔄 Iltimos qayta kiriting.",
                                   reply_markup=markup)
            await state.set_state('get_kod_admin')


@dp.callback_query_handler(state="get_kod_admin")
async def back(call: types.CallbackQuery, state: FSMContext):
    markup = await admin_menu()
    await call.message.edit_text(text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
    await state.set_state('admin_menu')


@dp.callback_query_handler(state="get_year_month_")
async def get_year(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data != 'back_menu':
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        for order in orders:
            if order.date.year == int(data):
                date.append(order.date.month)
        date = list(dict.fromkeys(date))
        markup = await month_keyboard(date)
        await call.message.edit_text(text='Kerakli oyni tanlang 👇', reply_markup=markup)
        await state.update_data(year=data)
        await state.set_state('get_month_month_')
    else:
        markup = await admin_menu()
        await call.message.edit_text(text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
        await state.set_state('admin_menu')


@dp.callback_query_handler(state="get_month_month_")
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
        doctors = []
        state_data = await state.get_data()
        orders = await get_orders()
        for order in orders:
            if order.date.year == int(state_data['year']) and order.date.month == int(data):
                keshbek.append(order)
                summa += order.summa
                sana.append(f"{order.date}")
                preparat.append(order.product.product_name)
                kod.append(order.product.kod)
                doctors.append(order.doctor.full_name)
                kesh.append(order.product.keshbek)
        text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
               f"💸 Jami keshbeklar summasi: {summa}\n\n" \
               f"To'liq ma'lumot olish uchun xujjatni yuklab oling 👇"
        sana.append('Umumiy')
        preparat.append(f'{len(keshbek)}')
        kod.append(f'{len(keshbek)}')
        doctors.append(f'{len(keshbek)}')
        kesh.append(summa)
        df = pd.DataFrame({'Sana': sana,
                           'Doctor': doctors,
                           'Preparat': preparat,
                           'Kod': kod,
                           'Keshbek': kesh, })
        df.to_excel('./xisobot.xlsx')
        markup = await get_or_back()
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state('get_or_back_admin')
    else:
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        for order in orders:
            if order.date.year == int(state_data['year']):
                date.append(order.date.year)
        date = list(dict.fromkeys(date))
        markup = await year_keyboard(date)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.update_data(year=data)
        await state.set_state('get_year_month_')


@dp.callback_query_handler(state="get_year_")
async def get_year(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data != 'back_menu':
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        for order in orders:
            if order.date.year == int(data):
                date.append(order.date.month)
        date = list(dict.fromkeys(date))
        markup = await month_keyboard(date)
        await call.message.edit_text(text='Kerakli oyni tanlang 👇', reply_markup=markup)
        await state.update_data(year=data)
        await state.set_state('get_month_')
    else:
        markup = await admin_menu()
        await call.message.edit_text(text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
        await state.set_state('admin_menu')


@dp.callback_query_handler(state="get_month_")
async def get_year(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data != 'back_menu':
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        for order in orders:
            if order.date.year == int(state_data['year']) and order.date.month == int(
                    data):
                date.append(order.date.day)
        date = list(dict.fromkeys(date))
        markup = await year_keyboard(date)
        await call.message.edit_text(text='Kerakli kunnni tanlang 👇', reply_markup=markup)
        await state.update_data(month=data)
        await state.set_state('get_day_')
    else:
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        for order in orders:
            if order.date.year == int(state_data['year']):
                date.append(order.date.year)
        date = list(dict.fromkeys(date))
        markup = await year_keyboard(date)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.update_data(year=data)
        await state.set_state('get_year_month_')


@dp.callback_query_handler(state='get_day_')
async def get_day(call: types.CallbackQuery, state: FSMContext):
    day = call.data
    if day != 'back_menu':
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        keshbek = []
        summa = 0
        sana = []
        doctors = []
        preparat = []
        kod = []
        kesh = []
        for order in orders:
            if order.date.year == int(state_data['year']) and order.date.month == int(
                    state_data['month']) and order.date.day == int(day):
                date.append(order)
                keshbek.append(order)
                summa += order.summa
                doctors.append(order.doctor.full_name)
                sana.append(f"{order.date}")
                preparat.append(order.product.product_name)
                kod.append(order.product.kod)
                kesh.append(order.product.keshbek)
        await state.update_data(day=day)

        text = f"🚛 Jami keshbeklar: {len(keshbek)}\n" \
               f"💸 Jami summa {summa}\n\n" \
               f"To'liq ma'lumot olish uchun xujjatni yuklab oling 👇"
        sana.append('Umumiy')
        preparat.append(f'{len(keshbek)}')
        kod.append(f'{len(keshbek)}')
        doctors.append(f'{len(keshbek)}')
        kesh.append(summa)
        df = pd.DataFrame({'Sana': sana,
                           'Doktor': doctors,
                           'Preparat': preparat,
                           'Kod': kod,
                           'Keshbek': kesh, })
        df.to_excel('./xisobot.xlsx')
        markup = await get_or_back()
        await call.message.edit_text(text=text, reply_markup=markup)
        await state.set_state('get_or_back_admin')
    else:
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        for order in orders:
            if order.date.year == int(state_data['year']):
                date.append(order.date.month)
        date = list(dict.fromkeys(date))
        markup = await month_keyboard(date)
        await call.message.edit_text(text='Kerakli oyni tanlang 👇', reply_markup=markup)
        await state.set_state('get_month_')


@dp.message_handler(state='get_doctor_id')
async def get_id(message: types.Message, state: FSMContext):
    password = message.text
    user = await get_doctor(password)
    if user is not None:
        markup = await doctor_in_admin()
        await bot.send_message(chat_id=message.from_user.id, text=f"{user.full_name}ning shaxsiy kabineti",
                               reply_markup=markup)
        await state.set_state('doctor_menu_admin')
        await state.update_data(doctor=password)
        await state.update_data(doctor=user.unique_password)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="❌ Ushbu parol bilan foydalanuvchi toplimadi\n"
                                                                  "🔄 Parolni qaytadan kiriting ")
        await state.set_state('get_doctor_id')


@dp.callback_query_handler(state='get_file')
async def get_file_command(call: types.CallbackQuery, state: FSMContext):
    markup = await admin_menu()
    await call.message.edit_text(text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
    await state.set_state('admin_menu')


@dp.message_handler(state='get_file', content_types=types.ContentTypes.DOCUMENT)
async def get_file(message: types.Message, state: FSMContext):
    await message.document.download('new_file.xlsx')
    df = pd.read_excel('new_file.xlsx')
    for i in df.index:
        await add_product(product_name=df['Preparat'][i], category1=df['Soha'][i], kod=df['Kod'][i],
                          keshbek=df['Keshbek'][i])
    markup = await admin_menu()
    await bot.send_message(chat_id=message.from_user.id, text="✅ Yangi maxsulotlar ro'yxati qo'shildinn\n\n"
                                                              "   Kerakli buyruqni tanlang 👇",
                           reply_markup=markup)
    await state.set_state('admin_menu')


@dp.callback_query_handler(state="get_or_back_admin")
async def get_file(call: types.CallbackQuery, state: FSMContext):
    command = call.data
    if command == 'get':
        file = open('./xisobot.xlsx', 'rb')
        markup = await back_admin_menu()
        await call.message.delete()
        await bot.send_document(chat_id=call.from_user.id, document=file, reply_markup=markup, caption="Xisobot")
        await state.set_state('back_admin_menu')
    else:
        markup = await admin_menu()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('admin_menu')


@dp.callback_query_handler(state="back_admin_menu")
async def back_to_admin(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    markup = await admin_menu()
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
    await state.set_state("admin_menu")
