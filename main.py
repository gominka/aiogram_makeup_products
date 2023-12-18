from aiogram import types, executor

from loader import dp


@dp.message_handler()
async def echo_upper(message: types.Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    executor.start_polling(dp)