import math
import random

from Enums import AdventurerType
from Items import Item


class Adventurer:
    def __init__(self, name, job):
        self.name = name
        self.job = job
        self.attack = job.value.attack
        self.defense = job.value.defense
        self.speed = job.value.speed
        self.health = 100
        self.miracle = 0
        self.trained = 0



    def get_hurt(self, damage):
        if damage > 0:
            self.health -= damage
        if self.health <= 0:
            if self.miracle == 1:
                self.health = 50
                return False
            return True
        return False

    def improve(self, train=None):
        stats = self.attack + self.defense + self.speed
        speed_threshold = int(self.attack + self.defense) + self.speed
        r = random.randrange(stats)
        if r <= speed_threshold:
            r = random.random()
            if r <= 0.5 - (self.attack - self.defense)/10:
                self.attack += 1
            else:
                self.defense += 1
        else:
            self.speed += 1
        if train:
            self.trained += 1

    def become_hero(self):
        self.attack = self.attack - self.job.value.attack + 9
        self.defense = self.defense - self.job.value.defense + 9
        self.speed = self.speed - self.job.value.speed + 1
        self.health = 100
        self.job = AdventurerType.HERO

    def info(self):
        print(self.name + '\t', self.job.value.name, str(self.health) + "❤️", str(self.attack) + "⚔️", str(self.defense) + "🛡️", str(self.speed) + "⚡️", sep='\t')


class Group:

    def __init__(self):
        self.duration = 0
        self.bonus_defense = 0
        self.bonus_attack = 0
        self.adventurers = []
        self.items = []
        self.usable = []
        self.sellable = []
        self.money = 0
        self.attack = 0
        self.defense = 0
        self.food = 0
        self.luck = 0
        self.heal = 0
        self.speed = 0

    def add_adventurer(self, a: Adventurer):
        if len(self.adventurers) < 4:
            self.adventurers.append(a)
            self.defense += a.defense
            self.attack += a.attack

    def add_item(self, i: Item, place=None):
        if place is None:
            self.items.append(i)
        else:
            if place == "get":
                self.items.append(i)
            elif place == "sell":
                self.sellable.append(i)
            elif place == "use":
                self.usable.append(i)

    def take_damage(self, damage, ret=None):
        if self.adventurers:
            adventurer = random.choice(self.adventurers)
            if adventurer.get_hurt(damage - self.give_defense()):
                if self.lucky_event():
                    adventurer.health = 1
                else:
                    self.remove_adventurer(adventurer, False)
                    if ret is not None:
                        return True
            if ret is not None:
                return False
        else:
            print("The group has been wiped out")
            self.items = [Item("Bones", "town", "accessory", "4", "44")]

    def remove_adventurer(self, adventurer, lives):
        self.defense -= self.adventurers[adventurer].defense
        self.attack -= self.adventurers[adventurer].attack
        if lives:
            self.adventurers.pop(adventurer)
            return adventurer
        else:
            print(self.adventurers[adventurer].job.value.name, adventurer.name + " has died")
            self.adventurers.pop(adventurer)


    def remove_items(self, place=None, item=None, bonus=None):
        money = 0
        if item is None:
            if place == "usable":
                self.usable.clear()
            elif place == "sell":
                for sellable in self.sellable:
                    money = sellable.price if sellable.primary != "ore" else (sellable.price*(1 + sellable.amount*0.2))
                    for adventurer in self.adventurers:
                        if adventurer.job.value.name == "merchant":
                            money = money * 1.4
                        print("burh")
                    self.money += int(money)
                self.sellable.clear()
            elif place == "inventory":
                self.items.clear()
        else:
            if place == "sell":
                money = item.price if item.primary != "ore" else (item.price * (1 + item.amount * 0.2))
                for adventurer in self.adventurers:
                    if adventurer.job.value.name == "merchant":
                        money = money * 1.4
                if bonus is not None:
                    money = money * bonus
                    print(money)
                self.money += int(money)

            elif place == "usable":
                self.usable.remove(item)
            elif place == "inventory":
                self.items.remove(item)

    def give_speed(self):
        if self.alive():
            return sorted(self.adventurers, key=lambda x: x.speed)[0].speed
        else:
            return 0

    def give_defense(self):
        self.defense = 0
        for adventurer in self.adventurers:
            self.defense += adventurer.defense
        return self.defense + self.bonus_defense

    def give_attack(self):
        self.attack = 0
        for adventurer in self.adventurers:
            self.attack += adventurer.attack
        return self.attack + self.bonus_attack

    def give_food(self):
        food = self.food
        for item in self.usable:
            if item.primary == "food":
                food += item.amount * 2
        return food

    def give_heal(self):
        heal = self.heal
        for item in self.usable:
            if item.primary == "medicine":
                heal += item.amount*2
        return heal

    def give_luck(self):
        luck = self.luck
        for item in self.usable:
            if item.primary == "accessory":
                luck += item.amount
        return luck

    def info(self):
        print("defense:", self.give_defense(), "attack:", self.give_attack(), "food:", self.give_food(), "medicine:"
              , self.give_heal(),"speed:", self.give_speed(), "luck:", self.give_luck())
        for adventurer in self.adventurers:
            adventurer.info()
        print()

    def alive(self):
        if self.adventurers:
            return True
        return False

    def lucky_event(self):
        if self.luck <= 100:
            lucky = (1 + self.luck * (0.95 - (self.luck * 0.004)))/100
        else:
            lucky = (56 + (self.luck - 100)*0.1)/100
        chance = random.random()
        return lucky >= chance

    def get_adventure_delay(self):
        delay = math.ceil(sum(5 + item.amount if item.primary == "ore" else 5 for item in self.sellable)/2)
        threshold = 40 + sum(5 if adventurer.job.value.name == "warrior" else 0 for adventurer in self.adventurers)
        usable = 0
        for item in self.usable:
            if item.primary == "ore":
                usable += 5 + item.amount
            elif item.primary == "medicine":
                usable += 3
            elif item.primary == "food":
                usable += 3
            else:
                usable += 5
        if usable < threshold:
            delay -= math.ceil((usable-threshold)*(usable-threshold)/40)
        else:
            delay += math.ceil((usable - threshold) * (usable - threshold) / 40)
        return math.floor(delay/4)

    def get_Attribute(self, string):
        if string == "food":
            return self.food
        elif string == "medicine":
            return self.heal
        elif string == "weapon":
            return self.attack
        elif string == "equipment":
            return self.defense


    def reset(self):
        self.bonus_defense = 0
        self.bonus_attack = 0
        self.money = 0
        self.food = 0
        self.luck = 0
        self.heal = 0
        self.duration = 0
