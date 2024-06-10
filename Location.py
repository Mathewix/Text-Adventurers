import math
import random
from Adventurers import Group, Adventurer
from Enums import *
from Items import Item

# Names for each primary item type
equipment_names = ["Armor", "Helmet", "Shield", "Gauntlets", "Boots"]
weapon_names = ["Sword", "Axe", "Bow", "Dagger", "Mace"]
food_names = ["Apple", "Bread", "Cheese", "Fish", "Berries"]
medicine_names = ["Ointment", "Antidote", "Herb", "Bandage", "Salve"]
accessory_names = ["Ring", "Amulet", "Neckless"]
ore_names = ["Iron", "Coal", "Gold", "Stone"]

# Combine all the names into a single list
all_item_names = {
    Primary.EQUIPMENT: equipment_names,
    Primary.WEAPON: weapon_names,
    Primary.FOOD: food_names,
    Primary.MEDICINE: medicine_names,
    Primary.ACCESSORIES: accessory_names,
    Primary.ORES: ore_names
}


class Location:
    def __init__(self, name, duration, item_price_range, damage_dealt):
        self.name = name
        self.duration = duration
        self.item_price = item_price_range
        self.damage_dealt = damage_dealt
        self.difficulty = 0
        self.lowest_item_stat = 0
        self.highest_item_stat = 0
        if name == "town":
            self.item_options = [Primary.FOOD, Primary.WEAPON, Primary.EQUIPMENT]
        elif name == "forest":
            self.item_options = [Primary.FOOD, Primary.MEDICINE, Primary.EQUIPMENT]
        elif name == "swamp":
            self.item_options = [Primary.ACCESSORIES, Primary.MEDICINE, Primary.FOOD]
        elif name == "mountain":
            self.item_options = [Primary.WEAPON, Primary.ORES, Primary.EQUIPMENT]
        elif name == "dungeon":
            self.item_options = [Primary.WEAPON, Primary.ORES, Primary.ACCESSORIES]

    def hunger_and_heal(self, food_value, guide_food, group: Group):
        if group.heal != 0:
            for adventurer in group.adventurers:
                heal_needed = 100 - adventurer.health
                if heal_needed != 0:
                    if group.heal >= heal_needed:
                        group.heal -= heal_needed
                        adventurer.health += heal_needed
                    elif group.heal < heal_needed:
                        adventurer.health += group.heal
                        group.heal = 0
        if group.food > food_value:
            group.food -= food_value
        elif 0 < group.food <= food_value:
            group.bonus_defense -= 1
            print("little hungry")
            if guide_food <= 0:
                group.food = 0
            else:
                group.food = 4
                guide_food -= 1
        elif group.food == 0:
            group.bonus_defense -= 3
            print("very hungry")
            return False
        return True

    def guide_food_calculation(self, group: Group):
        guide_food = 0
        for adventurer in group.adventurers:
            guide_food += 2 if adventurer.job == AdventurerType.GUIDE else 0
        return guide_food

    def adventure(self, group: Group):
        print(group.money)
        repetition = math.ceil(group.give_attack() / 2.5)
        food_value = math.ceil(group.duration / repetition)
        guide_food = self.guide_food_calculation(group)
        i = 0
        while i < repetition:
            if not self.hunger_and_heal(food_value, guide_food, group):
                i += 1
            i += 1
            self.give_item(group)
        self.sell_items(group)
        for adventurer in group.adventurers:
            if adventurer.job == AdventurerType.THIEF:
                self.give_item(group, True)
        if self.name != "town":
            for adventurer in group.adventurers:
                adventurer.improve()

    def give_item(self, group: Group, free=None, attribute=None, amount=None, player=None):
        if attribute is None:
            random_attribute = random.choice(self.item_options)
        else:
            random_attribute = attribute
        random_name = random.choice(all_item_names[random_attribute])
        if attribute is None:
            price = int(random.randrange(self.item_price[0], self.item_price[1]) * (1 + 0.1 * self.difficulty))
        else:
            price = 5
        if group.lucky_event():
            price = int(price * 1.5)
        if amount is None:
            value = random.randrange(2 + self.lowest_item_stat, 9 + self.highest_item_stat)
        else:
            value = amount
        if group.lucky_event():
            value = int(value * 1.5)
        damage = random.randrange(self.damage_dealt[0] + self.difficulty, self.damage_dealt[1] + self.difficulty*2)
        if group.lucky_event():
            damage = int(damage / 2)
        if player is None:
            group.add_item(Item(random_name, self.name, random_attribute.value, value, price))
        else:
            player.inventory.append(Item(random_name, self.name, random_attribute.value, value, price))
        if free is None:
            group.take_damage(damage)

    def increase_difficulty(self):
        self.difficulty += 1
        if self.difficulty % 3 == 0:
            self.lowest_item_stat += 1
        if self.difficulty % 4 ==0:
            self.highest_item_stat += 1

    def sell_items(self, group, item=None):
        group.remove_items("sell", item, 0.5)


class Town(Location):

    def __init__(self):
        super().__init__("town", 30, (15, 30), (22, 30))
    def sell_items(self, group, item=None):
        for item in group.sellable:
            if item.location == "dungeon":
                group.remove_items("sell", item, 1.5)
            elif item.location != "town":
                group.remove_items("sell", item, 0.8)
            else:
                super().sell_items(group, item)
        group.sellable.clear()

class Forest(Location):

    def __init__(self):
        super().__init__("forest", 30, (12, 34), (28, 38))

    def sell_items(self, group, item=None):
        for item in group.sellable:
            if item.location == "town":
                group.remove_items("sell", item, 1.3)
            elif item.location != "forest":
                group.remove_items("sell", item)
            else:
                super().sell_items(group, item)
        group.sellable.clear()

class Dungeon(Location):

    def __init__(self):
        super().__init__("dungeon", 40, (28, 56), (34, 46))

    def increase_difficulty(self):
        self.difficulty += 2
        if self.difficulty % 4 == 0:
            self.lowest_item_stat += 1
        if self.difficulty % 5 ==0:
            self.highest_item_stat += 1

    def sell_items(self, group, item=None):
        for item in group.sellable:
            super().sell_items(group, item)
        group.sellable.clear()

class Mountain(Location):

    def __init__(self):
        super().__init__("mountain", 35, (20, 28), (20, 44))

    def sell_items(self, group, item=None):
        for item in group.sellable:
            if item.location == "town":
                group.remove_items("sell", item, 1.3)
            elif item.location != "mountain":
                group.remove_items("sell", item)
            else:
                super().sell_items(group, item)
        group.sellable.clear()
class Swamp(Location):

    def __init__(self):
        super().__init__("swamp", 35, (8, 40), (30, 36))

    def sell_items(self, group, item=None):
        for item in group.sellable:
            if item.location == "town":
                group.remove_items("sell", item, 1.3)
            elif item.location != "swamp":
                group.remove_items("sell", item)
            else:
                super().sell_items(group, item)
        group.sellable.clear()

class Castle(Location):
    def __init__(self, level):
        super().__init__("Demon King's Castle", 45, (0, 0), (0, 0))
        self.level = level
        self.hint1 = [
            "First Boss: Castle Watch\nDecent Health with high consistent attack\n",
            "health:450\n",
            "attack:50\n",
            "specific: Defeat Boss in 12 rounds or your group retreats\n"]
        self.hint2 = [
            "Second Boss: Demon Famine\nLow Health with mediocre attack",
            "health:360\n",
            "attack:36-50\n",
            "specific: Before the fight group, has to travel 15 rounds consuming 5 food\n"]
        self.hint3 = [
            "Third Boss: Plague Lord\nA lot of health and aoe(hits all) attacks\n",
            "health:750\n",
            "attack:8 to all\n",
            "specific1:attacks ignore defense\n",
            "specific2:when below 350 health, heals from all damage he deals\n"]
        self.hint4 = [
            "Forth Boss: The Endless\nMassive health with small but growing attack\n",
            "health:1200\n",
            "attack:5+\n",
            "specific: Increases attack each round, reaching 100 attack in 13 rounds\n"]
        self.hint5 = [
            "Fifth Boss: Demon King\nA lot of health with differing attacks, you need at least 1 hero in group\n",
            "health:1000 defense:1 attack:80-120\n",
            "specifics:\n1. every 3 attacks deals 12 damage ignoring defense to all\n",
            "2. every 4 attacks deals 201 damage\n",
            "3. if any adventurer dies, Demon King's attack and defense grows,"
            " every 7 attacks heals for missing health of adventurers\n",
            "4. Yes if you beat him, you win :) good luck."
        ]


    def increase_difficulty(self):
        pass

    def make_hero(self, group):
        lowest_adventurer = Adventurer("Dummy", AdventurerType.GUIDE)
        for adventurer in group.adventurers:
            if adventurer.job.name != "hero":
                if lowest_adventurer.health >= adventurer.health:
                    lowest_adventurer = adventurer
        lowest_adventurer.become_hero()
        print(lowest_adventurer.name, "became a hero")

    def adventure(self, group: Group):
        adventure_method = getattr(self, f"adventure{self.level}", None)
        if adventure_method:
            adventure_method(group)

# First boss Royal Guard, decent health, consistent 50 damage, have to defeat it in 12 rounds
    def adventure1(self, group: Group):
        guide_food = super().guide_food_calculation(group)
        boss_health = 450
        boss_attack = 50
        repetition = 12
        food_value = math.ceil(group.duration / repetition)
        i = 0
        while i < repetition:
            super().hunger_and_heal(food_value, guide_food, group)
            boss_health -= group.give_attack()
            if boss_health <= 0:
                self.level += 1
                self.make_hero(group)
                break
            group.take_damage(boss_attack)

# Second boss Famine, low health with average damage, runs for 15 turns when group loses 5 food each round,
# after that fight starts, where group loses 1 food every round
    def adventurer2(self, group: Group):
        guide_food = super().guide_food_calculation(group)
        boss_health = 360
        boss_attack_min = 36
        boss_attack_max = 50
        repetition = 15
        food_value = 5
        i = 0
        while i < repetition:
            if super().hunger_and_heal(food_value, guide_food, group):
                guide_food -= 1
        food_value = 1
        while boss_health > 0:
            super().hunger_and_heal(food_value, guide_food, group)
            boss_health -= group.give_attack()
            if boss_health <= 0:
                self.level += 1
                self.make_hero(group)
                break
            damage = random.randrange(boss_attack_min, boss_attack_max)
            if group.lucky_event():
                damage = damage/2
            group.take_damage(damage)

# Third boss Plague Lord, a lot of health, every round deals 8 unpreventable damage to all adventurers,
# while below 50 % health, it heals from damage it deals (recommend fewer adventurers)
    def adventurer3(self, group: Group):
        guide_food = super().guide_food_calculation(group)
        boss_health = 750
        repetition = boss_health / group.give_attack()
        food_value = math.ceil(group.duration / repetition)
        while boss_health > 0:
            super().hunger_and_heal(food_value, guide_food, group)
            for adventurer in group.adventurers:
                adventurer.health -= 8
                if boss_health <= 350:
                    boss_health += 8
            boss_health -= group.give_attack()
            if boss_health <= 0:
                self.level += 1
                self.make_hero(group)
                break

# Fourth boss The Endless, has massive health with low attack, which increases every round
    def adventurer4(self, group: Group):
        guide_food = super().guide_food_calculation(group)
        boss_health = 1200
        boss_attack = 5
        repetition = boss_health / group.give_attack()
        food_value = math.ceil(group.duration / repetition)
        i = 1
        while boss_health > 0:
            super().hunger_and_heal(food_value, guide_food, group)
            boss_health -= group.give_attack()
            if boss_health <= 0:
                self.level += 1
                self.make_hero(group)
                break
            damage = boss_attack
            i += 1
            boss_attack = int(5 + 36*math.log(i) - i + i*i/10)
            if group.lucky_event():
                damage = damage/2
            group.take_damage(damage)

# Final boss Demon King, decent health and attack
    # every 3rd attack is unpreventable 12 damage to all adventurers
    # every 4th attack deals 200 damage
    # every 7th attack heals himself for the missing health of adventurers
# when he kills adventurer he gains 9 attack and 9 defense
# need at least 1 Hero in group to start this adventure
    def adventurer5(self, group: Group):
        for adventurer in group.adventurers:
            if adventurer.job == AdventurerType.HERO:
                adventurer.miracle = 1
        guide_food = super().guide_food_calculation(group)
        boss_health = 1000
        boss_defense = 1
        boss_attack_min = 80
        boss_attack_max = 120
        food_value = 0
        i = 1
        while boss_health > 0:
            super().hunger_and_heal(food_value, guide_food, group)
            boss_health -= group.give_attack()
            if boss_health <= 0:
                group.money += 1000000
                print("YIPPIEEE YOU DID IIT")
                print("And only in:")
                group.add_item(Item("Demon King's Hello Kitty Ring", "castle", Primary.ACCESSORIES, 239, 1000))
            if i % 3 == 0:
                for adventurer in group.adventurers:
                    if adventurer.get_hurt(12):
                        boss_defense += 9
                        boss_attack_max += 9
            if i % 4 == 0:
                damage = 201
                if group.lucky_event():
                    damage = damage / 2
                if group.take_damage(damage, True):
                    boss_defense += 9
                    boss_attack_max += 9
            elif i % 7 == 0:
                missing_health = 0
                for adventurer in group.adventurers:
                    missing_health += 100 - adventurer.health
            else:
                damage = random.randrange(boss_attack_min, boss_attack_max)
                if group.lucky_event():
                    damage = damage / 2
                if group.take_damage(damage, True):
                    boss_defense += 9
                    boss_attack_max += 9
            i += 1

    def get_next_info(self):
        pass

