import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiohttp import web

TOKEN = "8651896465:AAEYYUoxcWHBzJdk8jTwFB79yGqP3semOwY"
YOUR_ID = 1447998146

# Контакты
ADDRESS = "г. Москва, 2-й Вольный переулок, дом 11"
PHONE = "+7 960 335-66-69"

# Модели телефонов
MODELS = {
    "Apple": [
        "iPhone 7", "iPhone 7 Plus", "iPhone 8", "iPhone 8 Plus",
        "iPhone X", "iPhone XR", "iPhone XS", "iPhone XS Max",
        "iPhone 11", "iPhone 11 Pro", "iPhone 11 Pro Max",
        "iPhone SE 2020", "iPhone 12", "iPhone 12 Mini", "iPhone 12 Pro", "iPhone 12 Pro Max",
        "iPhone 13", "iPhone 13 Mini", "iPhone 13 Pro", "iPhone 13 Pro Max",
        "iPhone SE 2022", "iPhone 14", "iPhone 14 Plus", "iPhone 14 Pro", "iPhone 14 Pro Max",
        "iPhone 15", "iPhone 15 Plus", "iPhone 15 Pro", "iPhone 15 Pro Max",
        "iPhone 16", "iPhone 16 Plus", "iPhone 16 Pro", "iPhone 16 Pro Max",
        "iPhone 17", "iPhone 17 Air", "iPhone 17 Pro", "iPhone 17 Pro Max"
    ],
    "Xiaomi": ["Redmi Note 10", "Mi 11", "POCO X3", "Redmi Note 11"],
    "Samsung": ["Galaxy S21", "Galaxy S22", "Galaxy S23", "Galaxy A52"]
}

# Цены на аккумуляторы
BATTERY_PRICES = {
    "iPhone 7": {"copy": 2000, "good": 2500, "original": 3000},
    "iPhone 7 Plus": {"copy": 2200, "good": 2600, "original": 3200},
    "iPhone 8": {"copy": 2500, "good": 3000, "original": 3500},
    "iPhone 8 Plus": {"copy": 2700, "good": 3300, "original": 3700},
    "iPhone X": {"copy": 2500, "good": 3000, "original": 3760},
    "iPhone XR": {"copy": 2500, "good": 3200, "original": 4000},
    "iPhone XS": {"copy": 2500, "good": 2700, "original": 3800},
    "iPhone XS Max": {"copy": 2500, "good": 3200, "original": 4000},
    "iPhone 11": {"copy": 2500, "good": 2900, "original": 4000},
    "iPhone 11 Pro": {"copy": 3000, "good": 3600, "original": 6000},
    "iPhone 11 Pro Max": {"copy": 3200, "good": 4000, "original": 7000},
    "iPhone SE 2020": {"copy": 2500, "good": 3000, "original": 3500},
    "iPhone 12": {"copy": 3500, "good": 4600, "original": 8500},
    "iPhone 12 Mini": {"copy": 3200, "good": 4500, "original": None},
    "iPhone 12 Pro": {"copy": 3500, "good": 4600, "original": 8500},
    "iPhone 12 Pro Max": {"copy": 4000, "good": 5000, "original": 12000},
    "iPhone 13": {"copy": 4000, "good": 5500, "original": None},
    "iPhone 13 Mini": {"copy": 3200, "good": 4500, "original": None},
    "iPhone 13 Pro": {"copy": 4000, "good": 6000, "original": 10000},
    "iPhone 13 Pro Max": {"copy": 4200, "good": 6000, "original": 12000},
    "iPhone SE 2022": {"copy": 2500, "good": 2700, "original": 3200},
    "iPhone 14": {"copy": 3200, "good": 4500, "original": 10000},
    "iPhone 14 Plus": {"copy": 4000, "good": 5000, "original": 12000},
    "iPhone 14 Pro": {"copy": 3500, "good": 5000, "original": 11000},
    "iPhone 14 Pro Max": {"copy": 3500, "good": 6000, "original": 13000},
    "iPhone 15": {"copy": 4000, "good": 6500, "original": 14000},
    "iPhone 15 Plus": {"copy": 4200, "good": 6000, "original": 14000},
    "iPhone 15 Pro": {"copy": 4500, "good": 6500, "original": 15000},
    "iPhone 15 Pro Max": {"copy": 4500, "good": 7000, "original": 15990},
    "iPhone 16": {"copy": 4500, "good": 6500, "original": 15000},
    "iPhone 16 Plus": {"copy": 4500, "good": 6000, "original": 13500},
    "iPhone 16 Pro": {"copy": 5000, "good": 6000, "original": 16000},
    "iPhone 16 Pro Max": {"copy": 5000, "good": 7000, "original": 16500},
    "iPhone 17": {"copy": None, "good": 9000, "original": 18000},
    "iPhone 17 Air": {"copy": None, "good": None, "original": 18000},
    "iPhone 17 Pro": {"copy": None, "good": 15000, "original": 18000},
    "iPhone 17 Pro Max": {"copy": None, "good": 15000, "original": 18500},
}

# Цены на экраны
SCREEN_PRICES = {
    "iPhone 7": {"copy": 2500, "good": 3500, "original": None},
    "iPhone 7 Plus": {"copy": 2600, "good": 3700, "original": None},
    "iPhone 8": {"copy": 2800, "good": 3700, "original": None},
    "iPhone 8 Plus": {"copy": 3000, "good": 4000, "original": None},
    "iPhone X": {"copy": 2800, "good": 5000, "original": 7200},
    "iPhone XR": {"copy": 2800, "good": 4000, "original": 5000},
    "iPhone XS": {"copy": 3000, "good": 5000, "original": 6500},
    "iPhone XS Max": {"copy": 3500, "good": 5000, "original": 7500},
    "iPhone 11": {"copy": 3000, "good": 4500, "original": 6000},
    "iPhone 11 Pro": {"copy": 3000, "good": 5000, "original": 7000},
    "iPhone 11 Pro Max": {"copy": 3200, "good": 5500, "original": 9000},
    "iPhone SE 2020": {"copy": 2800, "good": 3700, "original": None},
    "iPhone 12": {"copy": 3500, "good": 5500, "original": 7500},
    "iPhone 12 Mini": {"copy": 4500, "good": 7000, "original": 9000},
    "iPhone 12 Pro": {"copy": 3500, "good": 5500, "original": 7500},
    "iPhone 12 Pro Max": {"copy": 3500, "good": 7000, "original": 16000},
    "iPhone 13": {"copy": 4000, "good": 6000, "original": 12000},
    "iPhone 13 Mini": {"copy": 4500, "good": 7000, "original": 14500},
    "iPhone 13 Pro": {"copy": 4500, "good": 7000, "original": 13000},
    "iPhone 13 Pro Max": {"copy": 4500, "good": 7000, "original": 15500},
    "iPhone SE 2022": {"copy": 2500, "good": 3500, "original": None},
    "iPhone 14": {"copy": 3800, "good": 5500, "original": 11000},
    "iPhone 14 Plus": {"copy": 4500, "good": 7000, "original": 15500},
    "iPhone 14 Pro": {"copy": 4500, "good": 7000, "original": 19000},
    "iPhone 14 Pro Max": {"copy": 5000, "good": 7000, "original": 21000},
    "iPhone 15": {"copy": 4500, "good": 8000, "original": 15500},
    "iPhone 15 Plus": {"copy": 4000, "good": 8000, "original": 16000},
    "iPhone 15 Pro": {"copy": 5000, "good": 8000, "original": 25000},
    "iPhone 15 Pro Max": {"copy": 5000, "good": 9000, "original": 26500},
    "iPhone 16": {"copy": 6000, "good": 9000, "original": 18000},
    "iPhone 16 Plus": {"copy": 7000, "good": 8500, "original": 16500},
    "iPhone 16 Pro": {"copy": 7500, "good": 10000, "original": 26000},
    "iPhone 16 Pro Max": {"copy": 7000, "good": 10000, "original": 28000},
    "iPhone 17": {"copy": None, "good": 12000, "original": 30000},
    "iPhone 17 Air": {"copy": None, "good": None, "original": 31000},
    "iPhone 17 Pro": {"copy": None, "good": 15000, "original": 34000},
    "iPhone 17 Pro Max": {"copy": None, "good": 15000, "original": 37000},
}

# Цены на разъемы
CHARGING_PRICES = {
    "iPhone 7": {"copy": 2500, "original": 3500},
    "iPhone 7 Plus": {"copy": 2500, "original": 3500},
    "iPhone 8": {"copy": 2500, "original": 3500},
    "iPhone 8 Plus": {"copy": 2700, "original": 3700},
    "iPhone X": {"copy": 3500, "original": 4500},
    "iPhone XR": {"copy": 3500, "original": 4500},
    "iPhone XS": {"copy": 3500, "original": 4500},
    "iPhone XS Max": {"copy": 3500, "original": 5000},
    "iPhone 11": {"copy": 3000, "original": 4500},
    "iPhone 11 Pro": {"copy": 3000, "original": 5000},
    "iPhone 11 Pro Max": {"copy": 3200, "original": 5500},
    "iPhone SE 2020": {"copy": 2800, "original": 3500},
    "iPhone 12": {"copy": 3500, "original": 5500},
    "iPhone 12 Mini": {"copy": 3500, "original": 5500},
    "iPhone 12 Pro": {"copy": 3500, "original": 5500},
    "iPhone 12 Pro Max": {"copy": 3500, "original": 5500},
    "iPhone 13": {"copy": 4000, "original": 5500},
    "iPhone 13 Mini": {"copy": 4500, "original": 5500},
    "iPhone 13 Pro": {"copy": 4500, "original": 5500},
    "iPhone 13 Pro Max": {"copy": 4500, "original": 5500},
    "iPhone SE 2022": {"copy": 2500, "original": 3500},
    "iPhone 14": {"copy": 3800, "original": 5500},
    "iPhone 14 Plus": {"copy": 4500, "original": 7000},
    "iPhone 14 Pro": {"copy": 4500, "original": 7000},
    "iPhone 14 Pro Max": {"copy": 5000, "original": 7000},
    "iPhone 15": {"copy": 4500, "original": 7000},
    "iPhone 15 Plus": {"copy": 4000, "original": 6000},
    "iPhone 15 Pro": {"copy": 5000, "original": 7000},
    "iPhone 15 Pro Max": {"copy": 5000, "original": 7000},
    "iPhone 16": {"copy": 5500, "original": 7000},
    "iPhone 16 Plus": {"copy": 5000, "original": 7000},
    "iPhone 16 Pro": {"copy": 5500, "original": 7000},
    "iPhone 16 Pro Max": {"copy": 5500, "original": 7000},
    "iPhone 17": {"copy": None, "original": 8500},
    "iPhone 17 Air": {"copy": None, "original": 8500},
    "iPhone 17 Pro": {"copy": None, "original": 8500},
    "iPhone 17 Pro Max": {"copy": None, "original": 8500},
}

class RepairState(StatesGroup):
    brand = State()
    model = State()
    service = State()
    quality = State()
    phone = State()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Заказать ремонт", callback_data="repair")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])

async def setup_bot_commands():
    commands = [
        BotCommand(command="/start", description="🏠 Главное меню"),
        BotCommand(command="/repair", description="📱 Заказать ремонт"),
        BotCommand(command="/contacts", description="📞 Наши контакты"),
        BotCommand(command="/help", description="❓ Помощь"),
    ]
    await bot.set_my_commands(commands)

# ============ КОНТАКТЫ ============
async def show_contacts(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"📞 КОНТАКТЫ\n\n📍 {ADDRESS}\n📱 {PHONE}\n⏰ Ежедневно с 10 до 20",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]])
    )
    await callback.answer()

async def show_help(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "❓ ПОМОЩЬ\n\nВыберите бренд → модель → услугу → качество → оставьте номер",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]])
    )
    await callback.answer()

async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("🔧 Главное меню\n\nВыберите действие:", reply_markup=get_main_keyboard())
    await callback.answer()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🔧 Добро пожаловать в сервис ремонта!\n\nВыберите действие:", reply_markup=get_main_keyboard())

@dp.message(Command("repair"))
async def cmd_repair(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍎 Apple", callback_data="brand_Apple")],
        [InlineKeyboardButton(text="📱 Xiaomi", callback_data="brand_Xiaomi")],
        [InlineKeyboardButton(text="🤖 Samsung", callback_data="brand_Samsung")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])
    await message.answer("Выберите бренд:", reply_markup=keyboard)
    await state.set_state(RepairState.brand)

@dp.message(Command("contacts"))
async def cmd_contacts(message: types.Message):
    await message.answer(
        f"📞 КОНТАКТЫ\n\n📍 {ADDRESS}\n📱 {PHONE}\n⏰ Ежедневно с 10 до 20",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]])
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "❓ ПОМОЩЬ\n\n📱 /repair - Заказать ремонт\n📞 /contacts - Наши контакты\n🏠 /start - Главное меню",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]])
    )

@dp.callback_query(lambda c: c.data == "contacts")
async def contacts_callback(callback: types.CallbackQuery):
    await show_contacts(callback)

@dp.callback_query(lambda c: c.data == "help")
async def help_callback(callback: types.CallbackQuery):
    await show_help(callback)

@dp.callback_query(lambda c: c.data == "main_menu")
async def main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await back_to_menu(callback, state)

@dp.callback_query(lambda c: c.data == "repair")
async def repair_callback(callback: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍎 Apple", callback_data="brand_Apple")],
        [InlineKeyboardButton(text="📱 Xiaomi", callback_data="brand_Xiaomi")],
        [InlineKeyboardButton(text="🤖 Samsung", callback_data="brand_Samsung")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])
    await callback.message.edit_text("Выберите бренд:", reply_markup=keyboard)
    await state.set_state(RepairState.brand)
    await callback.answer()

@dp.callback_query(RepairState.brand, lambda c: c.data.startswith("brand_"))
async def select_brand(callback: types.CallbackQuery, state: FSMContext):
    brand = callback.data.replace("brand_", "")
    await state.update_data(brand=brand)
    
    models = MODELS.get(brand, [])
    buttons = []
    for model in models:
        buttons.append([InlineKeyboardButton(text=model, callback_data=f"model_{model}")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="repair")])
    
    await callback.message.edit_text(f"Бренд: {brand}\n\nВыберите модель:", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.set_state(RepairState.model)
    await callback.answer()

@dp.callback_query(RepairState.model, lambda c: c.data.startswith("model_"))
async def select_model(callback: types.CallbackQuery, state: FSMContext):
    model = callback.data.replace("model_", "")
    await state.update_data(model=model)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔋 Аккумулятор", callback_data="service_battery")],
        [InlineKeyboardButton(text="📱 Экран", callback_data="service_screen")],
        [InlineKeyboardButton(text="⚡ Разъем зарядки", callback_data="service_charging")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="repair")]
    ])
    
    await callback.message.edit_text(f"Модель: {model}\n\nЧто нужно отремонтировать?", reply_markup=keyboard)
    await state.set_state(RepairState.service)
    await callback.answer()

@dp.callback_query(RepairState.service, lambda c: c.data.startswith("service_"))
async def select_service(callback: types.CallbackQuery, state: FSMContext):
    service = callback.data.replace("service_", "")
    user_data = await state.get_data()
    model = user_data.get('model')
    
    await state.update_data(service=service)
    
    if service == "battery":
        prices = BATTERY_PRICES.get(model, {})
    elif service == "screen":
        prices = SCREEN_PRICES.get(model, {})
    else:
        prices = CHARGING_PRICES.get(model, {})
    
    buttons = []
    if prices.get("copy"):
        buttons.append([InlineKeyboardButton(text=f"🔴 Копия - {prices['copy']}₽", callback_data=f"quality_copy_{prices['copy']}")])
    if prices.get("good"):
        buttons.append([InlineKeyboardButton(text=f"🟡 Хорошая - {prices['good']}₽", callback_data=f"quality_good_{prices['good']}")])
    if prices.get("original"):
        buttons.append([InlineKeyboardButton(text=f"🟢 Оригинал - {prices['original']}₽", callback_data=f"quality_original_{prices['original']}")])
    buttons.append([InlineKeyboardButton(text="🔧 Своя запчасть", callback_data="quality_own_0")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"service_back_{model}")])
    
    service_names = {"battery": "аккумулятора", "screen": "экрана", "charging": "разъема"}
    await callback.message.edit_text(f"Выберите качество для замены {service_names.get(service)}:", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.set_state(RepairState.quality)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("service_back_"))
async def back_to_services(callback: types.CallbackQuery, state: FSMContext):
    model = callback.data.replace("service_back_", "")
    await state.update_data(model=model)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔋 Аккумулятор", callback_data="service_battery")],
        [InlineKeyboardButton(text="📱 Экран", callback_data="service_screen")],
        [InlineKeyboardButton(text="⚡ Разъем зарядки", callback_data="service_charging")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="repair")]
    ])
    
    await callback.message.edit_text(f"Модель: {model}\n\nЧто нужно отремонтировать?", reply_markup=keyboard)
    await state.set_state(RepairState.service)
    await callback.answer()

@dp.callback_query(RepairState.quality, lambda c: c.data.startswith("quality_"))
async def select_quality(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    quality = parts[1]
    price = parts[2]
    user_data = await state.get_data()
    model = user_data.get('model')
    service = user_data.get('service')
    
    quality_names = {"copy": "Копия", "good": "Хорошая копия", "original": "Оригинал", "own": "Своя запчасть"}
    service_names = {"battery": "аккумулятора", "screen": "экрана", "charging": "разъема"}
    
    if quality == "own":
        text = f"📦 ЗАКАЗ\n\n📱 {model}\n🔧 Замена {service_names.get(service)}\n⭐️ Своя запчасть\n💰 Только работа"
    else:
        text = f"📦 ЗАКАЗ\n\n📱 {model}\n🔧 Замена {service_names.get(service)}\n⭐️ {quality_names.get(quality)}\n💰 {price}₽"
    
    await state.update_data(order_text=text)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Оформить заказ", callback_data="checkout")],
        [InlineKeyboardButton(text="🔄 Начать заново", callback_data="repair")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text + "\n\n👇 Нажмите кнопку:", reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "checkout")
async def checkout(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Отправить номер", callback_data="send_phone")],
        [InlineKeyboardButton(text="✍️ Ввести вручную", callback_data="manual_phone")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_order")]
    ])
    await callback.message.edit_text("📞 Укажите номер телефона:", reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "send_phone")
async def send_phone(callback: types.CallbackQuery, state: FSMContext):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]], resize_keyboard=True)
    await callback.message.answer("Нажмите кнопку:", reply_markup=kb)
    await state.set_state(RepairState.phone)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "manual_phone")
async def manual_phone(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите номер телефона:\nПример: +7 900 123-45-67")
    await state.set_state(RepairState.phone)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_to_order")
async def back_to_order(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("order_text", "Заказ")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Оформить заказ", callback_data="checkout")],
        [InlineKeyboardButton(text="🔄 Начать заново", callback_data="repair")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text + "\n\n👇 Нажмите кнопку:", reply_markup=kb)
    await callback.answer()

@dp.message(RepairState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text.strip()
    data = await state.get_data()
    
    await bot.send_message(YOUR_ID, f"🆕 НОВЫЙ ЗАКАЗ!\n\n👤 {message.from_user.full_name}\n📱 {phone}\n{data.get('order_text', '')}")
    
    await message.answer(f"✅ ЗАКАЗ ПРИНЯТ!\n\n{data.get('order_text', '')}\n\nМастер свяжется с вами.\n📍 {ADDRESS}", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Выберите действие:", reply_markup=get_main_keyboard())
    await state.clear()

# ============ ВЕБ-СЕРВЕР ДЛЯ HEALTH CHECK ============
async def health_check(request):
    return web.Response(text="Bot is running")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

# ============ ОСНОВНАЯ ФУНКЦИЯ ============
async def main():
    # Запускаем веб-сервер в фоне
    asyncio.create_task(start_web_server())
    
    await setup_bot_commands()
    print("=" * 55)
    print("🤖 БОТ ЗАПУЩЕН!")
    print("✅ Добавлена кнопка MENU внизу экрана")
    print("✅ Команды: /start, /repair, /contacts, /help")
    print("=" * 55)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
