from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'запустить бота'),
            types.BotCommand('create', 'Создать Qr код'),
            types.BotCommand('upload', 'Добавить Qr код'),
        ]
    )
