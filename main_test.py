# ссылка на статью - https://mastergroosha.github.io/telegram-tutorial-2/quickstart/

import logging
import pandas as pd
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiogram.utils.markdown as md

storage = MemoryStorage()

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.DEBUG)

headz_link = "https://headz.io/"


# Начинаем наш диалог
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Пришли файл")


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def download_documents(message: types.Message):
    current_date = datetime.now()
    destination = f"/Users/vikentijzerebov/pythonProject/WelcomeMessageMaker/data/{current_date}.csv"
    await message.document.download(destination_file=destination)
    column_names = ["ID", "Имя Клиента", "Ник в Телеграмм без символа @", "Ссылка на IT вакансии компании"]
    df = pd.read_csv(f"/Users/vikentijzerebov/pythonProject/WelcomeMessageMaker/data/{current_date}.csv",
                     names=column_names,
                     sep=";",
                     index_col="ID")
    print(df.index)
    print("***" * 20)
    print(df.values[1][0], df.values[1][1], df.values[1][2])
    print("***" * 20)
    print(len(df.values))
    for row in range(1, len(df.values)):
        await bot.send_message(message.chat.id,
                               md.text(md.text("Кому писать - ", md.hlink(title=f"{df.values[row][0]}",
                                                                          url=f"t.me/{df.values[row][1]}")),
                                       md.text(df.values[row][0], ", добрый день.", sep=""),
                                       md.text("Меня зовут Викентий (",
                                               "<b>",
                                               md.hlink(title="Headz.io", url=f"{headz_link}"),
                                               "</b>",
                                               " - Get IT) - увидел, что у вас ",
                                               "<b>",
                                               md.hlink(title="открыты IT вакансии", url=f"{df.values[row][2]}"),
                                               "</b>",
                                               " и хочу предложить размещение на нашем портале.",
                                               sep=""),
                                       md.text("Если в двух словах - мы что-то вроде ",
                                               "<b>",
                                               md.hlink(title="тиндера в IT рекрутинге",
                                                        url="https://www.canva.com/design/DAEt1rQ6Cno/66M6aNXLNM98ABzIfjhd8w/view"),
                                               "</b>",
                                               " с машинным обучением для мэтчинга резюме и вакансий, что позволяет работать ",
                                               "<b>",
                                               md.hitalic("только с теплыми"),
                                               "</b>",
                                               " кандидатами, которые предоставляют интерес для компании.",
                                               sep=""),
                                       md.text(
                                           "Если интересно - можем согласовать встречу (20-30 минут) - расскажу как сервис работает и какие есть варианты размещения. Время для встречи ",
                                           "<b>",
                                           md.hlink(title="удобно выбрать тут",
                                                    url="https://calendly.com/vickenty/headz"),
                                           "</b>.",
                                           sep=""
                                           ),
                                       md.text(
                                           "Если данный вопрос стоит обсудить с кем-то из ваших коллег - буду признателен за контакт."),
                                       sep="\n\n"), parse_mode="HTML")
    # count += 1
    # # await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
