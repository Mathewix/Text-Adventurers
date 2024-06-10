from enum import Enum


class Primary(Enum):
    EQUIPMENT = "equipment"
    WEAPON = "weapon"
    FOOD = "food"
    ACCESSORIES = "accessory"
    MEDICINE = "medicine"
    ORES = "ore"


class Locations(Enum):
    TOWN = "town"
    FOREST = "forest"
    SWAMP = "swamp"
    MOUNTAIN = "mountain"
    DUNGEON = "dungeon"
    CASTLE = "castle"


class AType:
    def __init__(self, name, attack, defense, speed):
        self.speed = speed
        self.defense = defense
        self.attack = attack
        self.name = name


class AdventurerType(Enum):
    # merchants increase the value of sold items
    MERCHANT = AType("merchant", 3, 2, 6)
    # increases threshold for usable items by 1
    WARRIOR = AType("warrior", 5, 8, 5)
    # finds 1 item without fighting
    THIEF = AType("thief", 7, 3, 6)
    # doctors increase efficiency of medicine
    DOCTOR = AType("doctor", 1, 6, 4)
    # if food runs out guide adds 4 food twice
    GUIDE = AType("guide", 4, 5, 8)
    # hero increases morale of group (group can have only one hero)
    HERO = AType("hero", 9, 9, 1)


        
