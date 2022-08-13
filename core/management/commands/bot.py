from core.services import generate_password, check_field, encrypt, check_exist
from aiogram import Bot, Dispatcher, executor, types
from asgiref.sync import sync_to_async
from django.core.management import BaseCommand
from django_aiogram_airtable.settings import API_TELEGRAM_TOKEN, table

bot = Bot(token=API_TELEGRAM_TOKEN)
dp = Dispatcher(bot)


class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Welcome in the test bot. For register click /registration")


@dp.message_handler(commands=['registration'])
async def send_welcome(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="✅ Agree", callback_data="agree"),
        types.InlineKeyboardButton(text="❌ Not agree", callback_data="not agree")
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    await message.answer("You agree to the processing of personal data?", reply_markup=keyboard)


@dp.callback_query_handler()
async def get_callback_query(call: types.CallbackQuery):
    if call.data == "agree":
        try:
            password = generate_password()
            await create_user(call.message.chat, password)
            await call.message.answer(f"✅ Registration complete\n"
                                      f"Your login: <b>{call.message.chat.username}</b>\n"
                                      f"Your password: <b>{password}</b>", parse_mode="HTML")
        except Exception as e:
            print(e)
            await call.message.reply("You are already registered in the system")

    if call.data == "not agree":
        await call.message.answer("❌ Registration not complete")


@sync_to_async()
def create_user(chat, password):
    if not check_exist(chat.username):
        table.create({
            'first_name': check_field(chat.first_name),
            'last_name': check_field(chat.last_name),
            'username': chat.username,
            'password': encrypt(password),
            'external_id': str(chat.id)
        })
    else:
        raise ValueError
