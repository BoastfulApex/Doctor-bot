import datetime
import pandas as pd
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from utils.db_api import database as commands
from loader import dp, bot
from keyboards.inline.menu_button import *
from utils.db_api.database import *


@dp.callback_query_handler(state='doctor_menu')
async def menu_commands(call: types.CallbackQuery, state: FSMContext):
    command = call.data
    data = await state.get_data()
    if command == 'add_kash':
        await call.message.edit_text("🔖 Biri martalik keshbek kodini kiriting")
        await state.set_state("get_kash_kode")
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
                sana.append(f"{datetime.datetime.today()}")
                preparat.append(i.product.product_name)
                kod.append(i.product.kod)
                kesh.append(i.product.keshbek)

        text = f"🚛 Jami keshbaklar: {len(keshbek)}\n" \
               f"💸 Jami summa {summa}\n\n" \
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
        await state.set_state('get_or_back')
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

        text = f"🚛 Jami keshbaklar: {len(keshbek)}\n" \
               f"💸 Jami summa {summa}\n\n" \
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
        await state.set_state('get_or_back')
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
        await state.set_state('get_year')
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
        await state.set_state('get_year_month')


@dp.callback_query_handler(state="get_year")
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
        await state.set_state('get_month')
    else:
        markup = await doctor_menu()
        await call.message.edit_text(text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('doctor_menu')


@dp.callback_query_handler(state="get_year_month")
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
        await state.set_state('get_month_month')
    else:
        markup = await doctor_menu()
        await call.message.edit_text(text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('doctor_menu')


@dp.callback_query_handler(state="get_month")
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
        await call.message.edit_text(text='Kerakli kunni tanlang 👇', reply_markup=markup)
        await state.update_data(month=data)
        await state.set_state('get_day')
    else:
        years = []
        orders = await get_orders()
        state_data = await state.get_data()
        doctor = await get_doctor(state_data['doctor'])
        for order in orders:
            if order.doctor.id == doctor.id:
                years.append(order.date.year)
        years = list(dict.fromkeys(years))
        markup = await year_keyboard(years)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year')


@dp.callback_query_handler(state="get_month_month")
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
        text = f"🚛 Jami keshbaklar: {len(keshbek)}\n" \
               f"💸 Jami summa {summa}\n\n" \
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
        await state.set_state('get_or_back')
    else:
        years = []
        orders = await get_orders()
        state_data = await state.get_data()
        doctor = await get_doctor(state_data['doctor'])
        for order in orders:
            if order.doctor.id == doctor.id:
                years.append(order.date.year)
        years = list(dict.fromkeys(years))
        markup = await year_keyboard(years)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_month')


@dp.callback_query_handler(state='get_day')
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

        text = f"🚛 Jami keshbaklar: {len(keshbek)}\n" \
               f"💸 Jami summa {summa}\n\n" \
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
        await state.set_state('get_or_back')
    else:
        date = []
        state_data = await state.get_data()
        orders = await get_orders()
        doctor = await get_doctor(state_data['doctor'])
        for order in orders:
            if order.doctor.id == doctor.id and order.date.year == int(state_data['year']):
                date.append(order.date.month)
        date = list(dict.fromkeys(date))
        markup = await month_keyboard(date)
        await call.message.edit_text(text='Kerakli oyni tanlang 👇', reply_markup=markup)
        await state.set_state('get_month')


@dp.message_handler(state="get_kash_kode")
async def get_kash_kode(message: types.Message, state: FSMContext):
    if message.text:
        kod = message.text
        product = await get_product(kod)
        if product is not None:
            orders = await get_orders()
            check = True
            for i in orders:
                if i.product.kod == product.kod:
                    check = False
            if check:
                text = f'💊 Maxsulot: {product.product_name}\n' \
                       f'💸 Keshbek: {product.keshbek}\n\n' \
                       f'Keshbekni qo\'shishni istaysizmi?'
                markup = await confirm_keyboard()
                await state.update_data(product_kod=kod)
                await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
                await state.set_state('confirm_add_kash')
            else:
                await bot.send_message(chat_id=message.from_user.id, text="⚠️Uhbu kod avval foydalanilgan\n"
                                                                          "🔄 Boshqa koq kiriting.")
                await state.set_state('get_kash_kode')

        else:
            await bot.send_message(chat_id=message.from_user.id, text="⚠️Ushbu kod bilan maxsulot topilmadi\n"
                                                                      "🔄 Kodni qaytadan kiriting ")
            await state.set_state('get_kash_kode')


@dp.callback_query_handler(state='confirm_add_kash')
async def confirm_add_kash(call: types.CallbackQuery, state: FSMContext):
    command = call.data
    if command == "confirm":
        data = await state.get_data()
        await add_order(data['product_kod'], doctor=data['doctor'])
        markup = await doctor_menu()
        await call.message.edit_text(text='✅ Keshbek qo\'shildi.\n'
                                          'Kerakli bo\'limni talnang 👇', reply_markup=markup)
        await state.set_state('doctor_menu')
    else:
        markup = await doctor_menu()
        await call.message.edit_text(text='❌ Keshbekni qo\'shish bekor qilindi.\n'
                                          'Kerakli bo\'limni talnang 👇', reply_markup=markup)
        await state.set_state('doctor_menu')


@dp.callback_query_handler(state="get_or_back")
async def get_file(call: types.CallbackQuery, state: FSMContext):
    command = call.data
    if command == 'get':
        file = open('./xisobot.xlsx', 'rb')
        markup = await back_to()
        await call.message.delete()
        await bot.send_document(chat_id=call.from_user.id, document=file, reply_markup=markup, caption="Xisobot")
        await state.set_state('back_doctor_menu')
    else:
        markup = await doctor_menu()
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('doctor_menu')


@dp.callback_query_handler(state="back_doctor_menu")
async def back_to_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    markup = await doctor_menu()
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text="Kerakli buyruqni tanlang 👇", reply_markup=markup)
    await state.set_state("doctor_menu")
