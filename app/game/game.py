import random
import sqlite3


def get_ran(first, second):
    random_number = random.randint(first, second)
    return random_number

def matching(item, slot_type):
    if slot_type == "head" and item == "leather":
        return "Шапочка из фольги"
    elif slot_type == "body" and item == "leather":
        return "Куртка Levi's"
    elif slot_type == "boots" and item == "leather":                    # тут будет много вариантов, и другой способ подбора
        return "Бархатные тяги"
    elif slot_type == "weapon" and item == "kinjal":
        return "Короткий кинжал"
    else:
        return item

class Inventory:
    def __init__(self, user):
        connection = sqlite3.connect("players.db")
        cursor = connection.cursor()
        cursor.execute("SELECT head, body, boots, weapon FROM Players WHERE userid = ?", (user,))
        self.equipment = cursor.fetchone()
        connection.close()
        
    def check_equip(self):
        if self.equipment:
            head, body, boots, weapon = self.equipment
            return [head, body, boots, weapon]
        else:
            return None
    