from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message

from database import Database
from scraping import main, create
from set_bot_commands import set_default_commands
from states import Form

storage = MemoryStorage()
BOT_TOKEN = 'Your Bot Token'

bot = Bot(BOT_TOKEN)

dp = Dispatcher(bot, storage=storage)
db = Database('Url for db')


# main menu
@dp.message_handler(commands=["start"])
async def main_menu(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(-1001550159719,
                               f"<b><i>🔔 Новый пользователь!\n👤Username: @{message.from_user.username}\n"
                               f"🆔 Telegram ID: {message.from_user.id}</i></b>", parse_mode='HTML')
        await message.answer('/create - Чтобы создать QR-код\n'
                             '/upload - Читать qr-код или просто отправь мне Qr код!')
    else:
        await message.answer('/create - Чтобы создать QR-код\n'
                             '/upload - Читать qr-код или просто отправь мне Qr код!')


@dp.message_handler(commands=["stats"], commands_prefix='!?./')
async def stats(message):
    users = db.all_users()
    await message.reply(f'👤 Пользователей в боте: {str(len(users))}')


@dp.message_handler(commands=["userpost"], commands_prefix='!?./')
async def userpost(message):
    '''
    Example:
    /userpost Hello world.
    '''
    if message.from_user.id == 'Admin id':
        userpost_text = " ".join(message.text.split()[1:])
        db.cursor.execute(f"SELECT user_id FROM users")
        users_query = db.cursor.fetchall()
        user_ids = [user[0] for user in users_query]
        confirm = []
        decline = []
        await message.reply('Рассылка юзерпоста началась...')
        for user_send in user_ids:
            try:
                await bot.send_message(user_send, userpost_text)
                confirm.append(user_send)
            except:
                decline.append(user_send)
        await message.answer(
            f'📣 Рассылка юзерпоста завершена!\n\n✅ Успешно: {len(confirm)}\n❌ Неуспешно: {len(decline)}')
    else:
        await message.reply("Недостаточно прав!")


@dp.message_handler(commands=["upload"])
async def command_upload(message: types.Message):
    await message.answer('Отправь мне свой QR код.')
    await Form.Image.set()


@dp.message_handler(commands=["create"])
async def command_create(message: Message):
    await message.answer('Отправьте текст, который вы хотите сгенерировать QR-код.')
    await Form.Text.set()


@dp.message_handler(content_types=ContentType.ANY)
async def error(message: types.Message):
    if message.content_type == 'photo':
        file = f"qrcode-bot/qr_code_photo/{id}.png"
        await message.photo[-1].download(file)
        text = main(file)
        await message.answer(text)
    elif message.text == "/create":
        await message.answer('Отправьте текст, который вы хотите сгенерировать QR-код.')
        await Form.Text.set()
    elif message.text != "/upload":
        await message.answer('/create - Чтобы создать QR-код\n'
                             '/upload - Читать qr-код или просто отправь мне Qr код!')
    else:
        await message.answer('/create - Чтобы создать QR-код\n'
                             '/upload - Читать qr-код или просто отправь мне Qr код!')


@dp.message_handler(state=Form.Text, content_types=ContentType.ANY)
async def create_qr_code(message: Message, state: FSMContext):
    if message.content_type == 'text':
        await state.finish()
        await state.update_data(text=message.text)
        datanvalid = await state.get_data()
        data = datanvalid['text']
        file = f"qrcode-bot/qr_code_photo/{id}.png"
        create(data, file)
        await bot.send_photo(message.from_user.id, types.InputFile(file),
                             caption="Код qr был создан с помощью t.me/MavQrCodeBot.")
    else:
        await message.answer("Вы можете только кодировать текст!")


@dp.message_handler(content_types=ContentType.ANY, state=Form.Image)
async def read_qr_code(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        file = f"qrcode-bot/qr_code_photo/{id}.png"
        await state.finish()
        await message.photo[-1].download(file)
        text = main(file)
        await message.answer(text)
    else:
        await message.answer("Просто пришлите картинку с qr кодом.")


async def on_startup(dp):
    await set_default_commands(dp)
    print("Бот запущен!")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
