import random

from Adventurers import Group, Adventurer
from Enums import AdventurerType

merchant_names = ["Tradelock", "Bargainbeard", "Coinheart", "Wealthwind"]
warrior_names = ["Bladestorm", "Ironclad", "Thunderstrike", "Steelcrusher"]
thief_names = ["Shadowcloak", "Silversprint", "Lockpick", "Swiftshadow"]
doctor_names = ["Healwise", "Remedyhand", "Cureheart", "Lifewarden"]
guide_names = ["Pathfinder", "Trailblazer", "Wayfinder", "Eagleeye"]


adventurer_names = ["Starshard", "Evergaze", "Moonshadow", "Emberflame", "Stormwhisper", "Auroradream", "Valorstrike", "Epicblade", "Saviorheart", "Eternalsword"]

all_adventurer_names = {
    AdventurerType.MERCHANT: merchant_names,
    AdventurerType.WARRIOR: warrior_names,
    AdventurerType.THIEF: thief_names,
    AdventurerType.DOCTOR: doctor_names,
    AdventurerType.GUIDE: guide_names,
}


class Player:

    def __init__(self, name):
        self.name = name
        self.money = 500
        self.inventory = []
        self.adventurers = []
        self.group = Group()
        self.time = 0

        self.adventurers.append(Adventurer("William", AdventurerType.WARRIOR))
        self.adventurers.append(Adventurer("Gregor", AdventurerType.GUIDE))
        self.adventurers.append(Adventurer("Denis", AdventurerType.DOCTOR))
        self.adventurers.append(Adventurer("Thomas", AdventurerType.THIEF))
        for i in range(4):
            self.put_adventurer_group(self.adventurers[0])

    def have_money(self, amount):
        if self.money - amount >= 0:
            self.money -= amount
            return True
        else:
            print("poor :>")
            return False

    def buy_adventurer(self, cost, time):
        if len(self.adventurers) < 10:
            job = random.choice(list(AdventurerType)[:-1])
            random_name = random.choice(all_adventurer_names[job] + adventurer_names)
            if self.have_money(cost):
                dude = Adventurer(random_name, job)
                for i in range(int(time/2)):
                    dude.improve()
                self.adventurers.append(dude)
        else:
            print("too many adventurers")



    def adventurers_add(self, adventurer):

        self.adventurers.append(self.group.adventurers[adventurer])
        self.group.remove_adventurer(adventurer, True)

    def put_adventurer_group(self, adventurer):
        self.group.add_adventurer(adventurer)
        self.adventurers.remove(adventurer)
    def start_adventure(self, location):

        self.group.duration = int((self.group.get_adventure_delay() + location.duration) * (1.0 - (self.group.give_speed()*0.05)))
        print(self.group.duration)
        if self.group.duration > 60:
            print(self.group.duration, "We are not going for such a long quest")
        else:
            if self.group.duration < 10:
                self.group.duration = 10
            for usage in self.group.usable:

                if usage.primary == "weapon":
                    self.group.bonus_attack += usage.amount
                elif usage.primary == "equipment":
                    self.group.bonus_defense += usage.amount
                elif usage.primary == "food":

                    self.group.food += usage.amount*2
                elif usage.primary == "medicine":
                    self.group.heal += usage.amount*2
                else:
                    self.group.luck += usage.amount
                doctors = 0
                for adventurers in self.adventurers:
                    if adventurers.job == AdventurerType.DOCTOR:
                        doctors += 1
                self.group.heal = int(self.group.heal * (1 + doctors*0.5))
            self.time += self.group.duration
            print(self.group.food)
            self.group.remove_items(place="usable")
            location.adventure(self.group)
            self.end_adventure()

    def end_adventure(self):
        for loot in self.group.items:
            self.inventory.append(loot)
        self.money += self.group.money
        self.group.remove_items("inventory")
        for adventurer in self.group.adventurers:
            adventurer.improve()
        self.group.reset()

    def return_item(self, item, place):
        self.inventory.append(item)
        self.group.remove_items(item=item, place=place)
