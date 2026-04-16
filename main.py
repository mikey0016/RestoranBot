import asyncio
import logging
import sys
from os import getenv

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy import DECIMAL, create_engine, ForeignKey, select, desc
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from streamlit import title

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton
from aiogram.utils.i18n import gettext as _, I18n, FSMI18nMiddleware
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
load_dotenv()

TOKEN = getenv("BOT_TOKEN")
engine = create_engine('postgresql+psycopg2://postgres:Faxa2000@localhost/postgres')
session = Session(engine)


class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    price: Mapped[float] = mapped_column(DECIMAL)


class AddTask(StatesGroup):
    main_menu = State()
    restoran_menu = State()
    salat_menu = State()
    fast_food_menu = State()
    hot_dish_menu = State()



dp = Dispatcher()

def language_menu_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="🇺🇿Uzbek"),
        KeyboardButton(text="🇺🇸English")
    ])
    rkb.adjust(2, repeat=True)
    markup = rkb.as_markup(resize_keyboard=True)
    return markup

def uz_menu_contact_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="🍽Restoran menyusi"),
        KeyboardButton(text="📞Biz bilan bog'lanish"),
    ])
    rkb.adjust(2, repeat=True)
    markup = rkb.as_markup(resize_keyboard=True)
    return markup

def uz_restoran_menu_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="🥗Salatlar"),
        KeyboardButton(text="🍕FastFood"),
        KeyboardButton(text="🍜Issiq taomlar"),
        KeyboardButton(text="⬅️Orqaga"),
    ])
    rkb.adjust(2, repeat=True)
    markup = rkb.as_markup(resize_keyboard=True)
    return markup

def uz_salat_menu_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="🥗Sezar salati",),
        KeyboardButton(text="🥗Olivye salati"),
        KeyboardButton(text="⬅️Orqaga")
    ])
    rkb.adjust(2, repeat=True)
    markup = rkb.as_markup(resize_keyboard=True)
    return markup


def uz_fast_food_menu_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="🍔Burger"),
        KeyboardButton(text="🌭Hot-dog"),
        KeyboardButton(text="⬅️Orqaga")
    ])
    rkb.adjust(2, repeat=True)
    markup = rkb.as_markup(resize_keyboard=True)
    return markup

def uz_hot_food_menu_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="🍛Osh"),
        KeyboardButton(text="🥘Sho'rva"),
        KeyboardButton(text="⬅️Orqaga")
    ])
    rkb.adjust(2, repeat=True)
    markup = rkb.as_markup(resize_keyboard=True)
    return markup



@dp.message(CommandStart())
async def command_start_handler(message: Message, state:FSMContext, i18n:I18n) -> None:
    markup = language_menu_button()
    username = message.from_user.first_name
    await message.answer(f"Assalomu alaykum hurmatli mijoz {username}\n\nBizning RestoranBotimizga xush kelibsiz!\n\n"
                         f"Siz bu bot orqali o'zingiz yoqtirgan taomlarni buyurtma qilishingiz mumkun!\n\n"
                         f"Bizning sayt: evos.uz\n"
                         f"Boshlash uchun tilni tanlang:\n\n\n\n"
                         f"Hello, dear customer {username}\n\nWelcome to our RestaurantBot!\n\n"
                         f"You can order your favorite dishes through this bot!\n\n"
                         f"Our website: evos.uz\n"
                         f"Select a language to get started!", reply_markup=markup)

# @dp.message(F.text == 'Uzbek')
# async def uzb_handler(message:Message, state:FSMContext, i18n: I18n):
#     await state.update_data({'locale':'uz'})
#     i18n.current_locale = 'uz'
#     await message.answer(_('Hello'), reply_markup= language())

@dp.message(F.text == "🇺🇿Uzbek")
async def restoran_menu_handler(message:Message, state:FSMContext, i18n:I18n):
    markup = uz_menu_contact_button()
    await state.update_data(({'locale':'uz'}))
    i18n.current_locale = 'uz'
    await message.reply(f"Hurmatli mijoz siz Uzbek tilini tanladingiz!")
    await message.reply(_("Asosiy Menyu"), reply_markup=markup())

@dp.message(F.text == "⬅️Orqaga")
async def back_main_handler(message:Message, state:FSMContext, i18n:I18n):
    await message.reply("Main menuga qaytish tanlandi!",reply_markup=uz_menu_contact_button())


@dp.message(F.text == "🥗Salatlar")
async def restoran_menu_handler(message:Message,  state:FSMContext, i18n:I18n):
    markup = uz_salat_menu_button()
    await state.update_data(({'locale': 'uz'}))
    i18n.current_locale = 'uz'
    await message.reply(_("Salatlar menusi:"), reply_markup=markup)

@dp.message(F.text == "🥗Sezar salati")
async def salat_info_handler(message:Message,  state:FSMContext, i18n:I18n):
    caption = (f"Salat nomi: Sezar\n"
               f"Salat tarkibi: Matyonez, no'xat va ketchup\n"
               f"Malumot izlashga qoyishmadi shu bor holos!")
    await message.answer_photo("https://www.youtube.com/watch?v=mOGA_tnfZB0", caption=caption)

@dp.message(F.text == "🥗Olivye salati")
async def salat_info_handler(message:Message,  state:FSMContext, i18n:I18n):
    caption = (f"Salat nomi: Olivye\n"
               f"Salat tarkibi: Matyonez, no'xat va ketchup\n"
               f"Malumot izlashga qoyishmadi shu bor holos!")
    await message.answer_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_HkQX3QBM5aUhaxvTcIv5ZCwrHRYrGE8elozGjBofAe6DaRiVdgPGVNgYhTZuMtimtv934eAEoRsT5nlA-QT3vayAa94wodORYKe556Vn4Q&s=10", caption=caption)


@dp.message(F.text == "🔙Orqaga")
async def back_resto_handler(message:Message, state:FSMContext, i18n:I18n):
    await message.reply("Restoran menuga qaytish tanlandi!",reply_markup=uz_restoran_menu_button())

@dp.message(F.text == "🍕FastFood")
async def restoran_menu_handler(message:Message, state:FSMContext, i18n:I18n):
    markup = uz_fast_food_menu_button()
    await state.update_data(({'locale': 'uz'}))
    i18n.current_locale = 'uz'
    await message.reply(_("FastFood menusi:"), reply_markup=markup)

@dp.message(F.text == "🍔Burger")
async def fast_food_info_handler(message:Message,  state:FSMContext, i18n:I18n):
    caption = (f"FastFood nomi: Burger\n"
               f"Burger tarkibi: Go'sht, pomidor, bodring, ketshup va mayonez\n"
               f"Malumot izlashga qoyishmadi shu bor holos!")
    await message.answer_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzJnmtwDHHhuzJCW_4SCJwwc3vnbk0qU-NocB32Dleoc7kNSXjtSgtTsNewxPePl3Jdn86t2Dd3OcZffc2YWbkr6a2BOicdkr1hsvv8kphTA&s=10", caption=caption)

@dp.message(F.text == "🌭Hot-dog")
async def fast_food_info_handler(message:Message,  state:FSMContext, i18n:I18n):
    caption = (f"FastFood nomi: Hot-dog\n"
               f"Hot-dog tarkibi: Sosiska, chimchi, ketshup va mayonez\n"
               f"Malumot izlashga qoyishmadi shu bor holos!")
    await message.answer_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWdd5PXtc1otdQymI70qQlfenwekV15ZBoNsu5UDulnJhzgFs31660A55e3-ZVVuSXvuXfmRsdjBnJ-YigCLgg1RBQSlBYDZPD1IwPjFev&s=10", caption=caption)


@dp.message(F.text == "🔙Orqaga")
async def back_resto_handler(message:Message, state:FSMContext, i18n:I18n):
    await message.reply("Restoran menuga qaytish tanlandi!",reply_markup=uz_restoran_menu_button())


@dp.message(F.text == "🍜Issiq taomlar")
async def restoran_menu_handler(message: Message, state:FSMContext, i18n:I18n):
    markup = uz_hot_food_menu_button()
    await state.update_data(({'locale': 'uz'}))
    i18n.current_locale = 'uz'
    await message.reply(_("Issiq taomlar menusi:"), reply_markup=markup)

@dp.message(F.text == "🍛Osh")
async def hot_dish_info_handler(message:Message,  state:FSMContext, i18n:I18n):
    caption = (f"Issiq taom nomi: Osh\n"
               f"Osh tarkibi: Go'sht, gurush, sabsi, mayiz, piyoz va no'xat\n"
               f"Malumot izlashga qoyishmadi shu bor holos!")
    await message.answer_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSObW99u4f5TOj_tzTWPIgFt7pmfu8NkW1tDQanyqw42e4ecWmde5yj6bVnJMvoYPWAKaMNF8Gih0TNzUavU48W3QkfsV4CrZ_fNdJSDYNa7A&s=10", caption=caption)

@dp.message(F.text == "🥘Sho'rva")
async def hot_dish_info_handler(message:Message,  state:FSMContext, i18n:I18n):
    caption = (f"Issiq taom nomi: Sho'rva\n"
               f"Sho'rva tarkibi: Go'sht, suv, yog, sabzi, piyoz va no'xat\n"
               f"Malumot izlashga qoyishmadi shu bor holos!")
    await message.answer_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIV6OwqULkjMtkzQ4TL-o7UzI9dw9nxYiciGgQXAxp3ZTT54fsnSrZib0UEVAnCmKzosp1xm9ofm7YFwjVcDTlRaN_7bADtAly9lBFilpuHA&s=10", caption=caption)


@dp.message(F.text == "🔙Orqaga")
async def back_resto_handler(message:Message, state:FSMContext, i18n:I18n):
    await message.reply("Restoran menuga qaytish tanlandi!",reply_markup=uz_restoran_menu_button())

@dp.message(F.text == "📞Biz bilan bog'lanish")
async def contact_menu_handler(message: Message, state:FSMContext, i18n:I18n):
    await message.reply("Assalomu alaykum hurmatli mijoz!\n\nBiz bilan bog'lanish uchun adminlarga murojat qiling!\n\n"
                        "Telegram:@zen1n_xz\nTelefon raqam:+998 95 098 99 50\nGitHub:https://github.com/mikey0016")

async def main() -> None:
    Base.metadata.create_all(engine)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    i18n = I18n(path="locales", default_locale="en", domain="messages")
    middleware = FSMI18nMiddleware(i18n)
    dp.message.outer_middleware(middleware)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())