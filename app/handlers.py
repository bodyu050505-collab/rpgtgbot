from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.keyboards.keyboards import map_variants_tavern
from app.game.game import Inventory, matching

import sqlite3


router = Router()

TYPES = ["head", "body", "boots", "weapon"]

def init_db():
    connection = sqlite3.connect("players.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Players (
            userid PRIMARY KEY NOT NULL,
            level INTEGER NOT NULL DEFAULT 1,
            location NOT NULL DEFAULT tavern,
            money INTEGER NOT NULL DEFAULT 0,
            head NOT NULL DEFAULT leather,
            body NOT NULL DEFAULT leather,
            boots NOT NULL DEFAULT leather,
            weapon NOT NULL DEFAULT kinjal
        )
    ''')
    connection.commit()
    connection.close()

init_db()


@router.message(CommandStart())
async def cmd_start(message: Message):
    print(message.from_user.first_name, message.from_user.id)
    await message.answer("дароу, что бы начать игру пропиши 'Создать персонажа'")


@router.message(F.text == "Создать персонажа")
async def create_player(message: Message):
    print("zafiksiroval!")
    user_id = message.from_user.id
    connection = sqlite3.connect("players.db", timeout=10.0)
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Players WHERE userid = ?", (user_id,))
    player_exists = cursor.fetchone()
    if player_exists:
        await message.answer("❌ У тебя уже есть персонаж!")
        connection.close()
        return
    cursor.execute("INSERT INTO Players (userid) VALUES (?)", (user_id,))
    connection.commit()
    connection.close()
    await message.answer("Ты создал персонажа, пропиши Карта для того чтобы узнать где ты")


@router.message(F.text == "Инвентарь")
async def check_inventory(message: Message):
    print("proveril inv")
    user_id = message.from_user.id
    connection = sqlite3.connect("players.db")
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Players WHERE userid = ?", (user_id,))
    player_exists = cursor.fetchone()
    if not player_exists:
        await message.answer("❌ У тебя нет персонажа!")
        connection.close()
        return
    cursor.execute("SELECT level FROM Players WHERE userid = ?", (user_id,))
    level = cursor.fetchone()[0]
    inv = Inventory(user_id)
    equipment = inv.check_equip()
    spisok = []
    for i in range(len(equipment)):
        item = equipment[i]
        item_type = TYPES[i]
        spisok.append(matching(item, item_type))
    await message.answer(f"<b>@{message.from_user.username}, твой инвентарь:</b>\n\nУровень: {level}\n\nДеньги: ...\n\nСнаряжение:\nГолова - {spisok[0]}\nТело - {spisok[1]}\nНоги - {spisok[2]}\nОружие - {spisok[3]}", parse_mode="HTML")

@router.message(F.text == "Карта")
async def map(message: Message):
    print("map check")
    user_id = message.from_user.id
    connection = sqlite3.connect("players.db", timeout=10.0)
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Players WHERE userid = ?", (user_id,))
    player_exists = cursor.fetchone()
    if not player_exists:
        await message.answer("❌ У тебя нет персонажа!")
        connection.close()
        return
    cursor.execute("SELECT location FROM Players WHERE userid = ?", (user_id,))
    location = cursor.fetchone()[0]
    if location == "tavern":
        photo = FSInputFile("img/карта_таверна.jpg")
        await message.answer_photo(photo=photo, caption="карта ты щас в таверне", reply_markup=map_variants_tavern())

# тут нужен инлайн кейборд с вариантами куда отправиться