from Location import *
from Searcher import Sorter
from Player import Player
import os

name = input("Enter you Name:")

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    DEFAULT = '\033[0m'

    def print_colored(text, color):
        colored_text = f"{color}{text}{Color.DEFAULT}"
        print(colored_text)

commands = "sell | use | search | adventure | buy adventurer | adventurers | atg (add to group) | rfg (remove from group)"
usable_commands = " | ".join(f"{Color.GREEN}{cmd}{Color.DEFAULT}" for cmd in commands.split(" | "))
print(f"Usable commands: {usable_commands}")

player = Player(name)
town = Town()
forest = Forest()
swamp = Swamp()
mountain = Mountain()
dungeon = Dungeon()
castle = Castle(level=1)
sorter = Sorter(player.inventory, player.adventurers, player.group)
locations = [town, forest, swamp, mountain, dungeon]
bought_adventurers = 0
bought_items = 0
time = 0
# give some starting items and reasonable adventurers
for i in range(5):
    town.give_item(player.group, free=True, attribute=Primary.FOOD, amount=i+1, player=player)
for i in range(2):
    town.give_item(player.group,  free=True, attribute=Primary.MEDICINE, amount=5, player=player)
town.give_item(player.group,  free=True, attribute=Primary.WEAPON, amount=4, player=player)
town.give_item(player.group,  free=True, attribute=Primary.EQUIPMENT, amount=6, player=player)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Usable commands: {usable_commands}")

def print_Line():
    print("---------------------------------------------")

def buy_food(repetition):
    money = 0
    for i in range(repetition):
        money += 30
    if player.have_money(money):
        town.give_item(player.group,  free=True, attribute=Primary.FOOD, amount=5, player=player)


def sell_items():
    print("What should we sell?")
    for i in player.inventory:
        i.info()
    sell = sorter.sort_by_items(ret=True, usage="sell")
    sorter.move_items(player.group.sellable, sell)

def remove_item_from(where, which = None):
    if which is not None:
        if where == "sell":
            player.inventory.append(player.group.sellable.pop(which))
        else:
            player.inventory.append(player.group.usable.pop(which))
    else:
        if where == "sell":
            player.inventory.append(player.group.sellable.pop())
        else:
            player.inventory.append(player.group.usable.pop())

def use_items():
    print("What should we use?")
    use = sorter.sort_by_items(ret=True, usage="use")
    sorter.move_items(player.group.usable, use)

def remove_adventurer_from_group():
    print("Who do we remove? (1,2,3,4)")
    while True:
        inp = int(input())
        if 1 <= inp <= 4:
            if player.group.adventurers[inp-1]:
                player.adventurers_add(inp-1)
                break
        else:
            print("try again...")


def improve_adventurer(whom, repetition):
    price = 0
    for i in range(repetition):
        price += 25 + (player.adventurers[whom].trained + i) * 10
    if player.have_money(price):
        player.adventurers[whom].improve(True)


def add_adventurer_to_group():
    print("Who do we add? (one of adventurers indexes)")
    add = int(input())
    if add <= len(player.adventurers):
        a = player.adventurers[add - 1]
        player.put_adventurer_group(a)

    else:
        print("adventurer does not exist")

def heal_group():
    cost = 40
    for adventurer in player.group.adventurers:
        if adventurer.health != 100:
            cost += 10
    if player.have_money(cost):
        for adventurer in player.group.adventurers:
            adventurer.health = 100

def get_boss_info():
    castle.get_next_info()

player_input = ""
while player_input != "end":

    if player.time >= 35:
        player.time -= 35
        for loc in locations:
            loc.increase_difficulty()
            time += 1
    print("What to do?")
    player_input = input().lower()

    if player_input == "adventurers":
        new = sorter.sort_by_adventurers()
        print(new)

    elif player_input == "sell":
        sell_items()

    elif player_input == "use":
        use_items()

    elif player_input == "search":
        print("You can sort by using key words 'price'/'stat' or use '!' as negation or '&' to combine more "
              "requirements. Other than that you can write indexes or starting letter of items.")
        new = sorter.sort_by_items()
        print(new)

    elif player_input == "adventure":
        cycle = True

        while cycle:
            print("Locations: town, forest, swamp, mountain, dungeon")
            place = input().lower()
            for location in locations:
                if place == location.name:
                    player.start_adventure(location)
                    cycle = False
                elif place == "castle":
                    player.start_adventure(castle)
                    cycle = False
                elif place == "exit":
                    cycle = False
    elif player_input == "buy adventurer":
        player.buy_adventurer(100 + 50*bought_adventurers, time)
        bought_adventurers += 1
    elif player_input == "atg":
        if len(player.adventurers) > 0:
            add_adventurer_to_group()
        else:
            print("There are no available adventurers")
    elif player_input == "rfg":
        if len(player.group.adventurers) > 0:
            remove_adventurer_from_group()
        else:
            print("There are no adventurers in the group")
    elif player_input == "rsi":
        which = input("Which item to remove? (number of item in order 1,2,3... or press enter to remove last one) ")
        if which != "":
            if which.isnumeric():
                which = int(which)
                if which < len(player.group.sellable):
                    remove_item_from("sell", which+1)
        else:
            remove_item_from("sell")
    elif player_input == "rui":
        which = input("Which item to remove? (number of item in order 1,2,3... or press enter to remove last one) ")
        if which != "":
            if which.isnumeric():
                which = int(which)
                if which < len(player.group.usable):
                    remove_item_from("use", which+1)
        else:
            remove_item_from("use")
    elif player_input == "heal":
        heal_group()
    elif player_input == "improve":
        cycle = True
        while cycle:
            who = input("Who are we improving? (1,2,3,4)")
            if who.isnumeric():
                how_much = input("How many times?")
                if how_much.isnumeric():
                    improve_adventurer(player.group.adventurers[who], how_much)
                    cycle = False
    elif player_input == "buy food":
        cycle = True
        while cycle:
            how_much = input("how much food you want to buy? 5 food for 30")
            if how_much.isnumeric():
                buy_food(how_much)
                cycle = False
    elif player_input == "clear":
        clear_console()
    elif player_input == "help":
        print("Welcome to the Game Help Menu!")
        print("Usable commands:")
        print(f"-{Color.GREEN}'sell':{Color.DEFAULT} Add items from your inventory to sellable inventory of your group."
              f"Example: Dungeon & Ore:5 will try to add 5 ores from dungeon to sellable")
        print(f"- {Color.GREEN}'use':{Color.DEFAULT} Add items from your inventory to usable inventory of your group. "
              f"Add items based on their type example: food: 30, will try to "
              f"add food items with smallest price until group has 30 food")
        print(f"- {Color.GREEN}'search':{Color.DEFAULT} Search through your inventory using keywords to "
              f"find only specific ones. Example: town&price&weapon - will show only weapons from town sorted by price")
        print(f"- {Color.GREEN}'adventure':{Color.DEFAULT} Embark on an adventure with your group.")
        print(f"- {Color.GREEN}'buy adventurer':{Color.DEFAULT} Purchase a new adventurer to join your group."
              f" Price 100 + 50 for each bought adventurer")
        print(f"- {Color.GREEN}'adventurers':{Color.DEFAULT} Display information about your current adventurers.")
        print(f"- {Color.GREEN}'atg':{Color.DEFAULT} Add an adventurer to your group.")
        print(f"- {Color.GREEN}'rfg':{Color.DEFAULT} Remove an adventurer from your group.")
        print(f"- {Color.GREEN}'rui':{Color.DEFAULT} Remove an usable item from your group.")
        print(f"- {Color.GREEN}'rsi':{Color.DEFAULT} Remove a sellable item from your group.")
        print(f"- {Color.GREEN}'heal':{Color.DEFAULT} Heal your group of adventurers. "
              f"Price 40 + 10 for each injured adventurer")
        print(f"- {Color.GREEN}'improve':{Color.DEFAULT} Enhance the skills of one of adventurers inside the group."
              f" Price 25 + 10 for each time the adventurer was improved")
        print(f"- {Color.GREEN}'buy food':{Color.DEFAULT} Purchase food for your group. "
              f"Price 30 for food from Town with quality 5")
        print(f"- {Color.GREEN}'end':{Color.DEFAULT} End the game.")
        print("Remember, you can always type 'help' to access this menu.")
    elif player_input == "end":
        break
    else:
        print("Usable commands: sell, use, search, adventure, buy adventurer, adventurers, atg (add to group), "
              "rfg (remove from group)")
        print("If you want to end write: end")
    player.group.info()
    print(str(player.money) + "💰")
# got to show things

for i in player.inventory:
    i.info()
