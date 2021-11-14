# ссылка на статью - https://mastergroosha.github.io/telegram-tutorial-2/quickstart/

# !venv/bin/python
import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit

from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode

storage = MemoryStorage()

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
# Диспетчер для бота
dp = Dispatcher(bot, storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.DEBUG)
headz_link = "https://headz.io/"


# создаём форму и указываем поля
class Form(StatesGroup):
    customer_name = State()
    company_url = State()


# Начинаем наш диалог
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await Form.customer_name.set()
    await message.reply("Привет! Как зовут клиента?")


# Сюда приходит ответ с именем
@dp.message_handler(state=Form.customer_name)
async def process_customer_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['customer_name'] = message.text

    await Form.next()
    await message.reply("Скинь ссылку на вакансии")


@dp.message_handler(state=Form.company_url)
async def process_company_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company_url'] = message.text

    await bot.send_message(message.chat.id,
                           md.text(md.text(md.text(data['customer_name']), ", добрый день.", sep=""),
                                   md.text("Меня зовут Викентий (",
                                           "<b>",
                                           md.hlink(title="Headz.io", url=f"{headz_link}"),
                                           "</b>",
                                           " - Get IT) - увидел, что у вас ",
                                           "<b>",
                                           md.hlink(title="открыты IT вакансии", url=data['company_url']),
                                           "</b>",
                                           " и хочу предложить размещение на нашем портале.",
                                           sep=""),
                                   md.text("Если в двух словах - мы что-то вроде ",
                                           "<b>",
                                           md.hlink(title="тиндера в IT рекрутинге", url="https://www.canva.com/design/DAEt1rQ6Cno/66M6aNXLNM98ABzIfjhd8w/view"),
                                           "</b>",
                                           " с машинным обучением для мэтчинга резюме и вакансий, что позволяет работать ",
                                           "<b>",
                                           md.hitalic("только с теплыми"),
                                           "</b>",
                                           " кандидатами, которые предоставляют интерес для компании.",
                                           sep=""),
                                   md.text("Если интересно - можем согласовать встречу (20-30 минут) - расскажу как сервис работает и какие есть варианты размещения. Время для встречи ",
                                           "<b>",
                                           md.hlink(title="удобно выбрать тут",
                                                    url="https://calendly.com/vickenty/headz"),
                                           "</b>",
                                           ".",
                                           sep=""
                                           ),
                                   md.text("Если данный вопрос стоит обсудить с кем-то из ваших коллег - буду признателен за контакт."),
                                   sep="\n\n"), parse_mode="HTML")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

#
headz_link = "<b><a href='https://headz.io/'>Headz.io</a></b>"
tinder_link = "<b><a href='https://drive.google.com/file/d/1WsOT2Y_YLYtWVuiPgiAzsDCr_0WytwN4/view?usp=sharing'>тиндер в IT рекрутинге</a></b>"
calendly = "<b><a href='https://calendly.com/vickenty/headz'>Calendly</a></b>"
