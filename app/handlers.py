from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
import sqlite3

router = Router()


def init_db():
    connection = sqlite3.connect("players.db", timeout=20.0)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Players (
            userid PRIMARY KEY NOT NULL,
            level INTEGER NOT NULL DEFAULT 1
        )
    ''')
    connection.commit()
    connection.close()

init_db()


@router.message(CommandStart())
async def cmd_start(message: Message):
    print(message.from_user.first_name, message.from_user.id)
    await message.answer("дароу, что бы начать игру пропиши 'В приключение!'")


@router.message(F.text == "В приключение!")
async def create_player(message: Message):
    print("zafiksiroval!")