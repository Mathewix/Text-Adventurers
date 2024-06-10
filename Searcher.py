import Adventurers
from Items import Item
from Enums import *
import pandas as pd


class Sorter:
    def __init__(self, items: list[Item], adventurers: list[Adventurers], group):
        self.items = items
        self.adventurers = adventurers
        self.group = group

    def sort_by_items(self, ret=None, usage=None):
        df = pd.DataFrame([(item.name, item.location, item.primary, item.amount, item.price) for item in self.items],
                          columns=["Name", "Location", "Attribute", "Stat", "Price"])

        df.index = df.index + 1
        user_input = input().replace(" ", "")
        if usage == "use":
            if ":" not in user_input:
                input_parts = user_input.split("&")
                limit = 1000
            else:
                input_parts = ("!price&" + user_input.split(":")[0]).split("&")

                limit = user_input.split(":")[1]
                if not limit.isnumeric():
                    limit = 0
        elif usage == "sell":
            if ":" not in user_input:
                input_parts = user_input.split("&")
                limit = 1000
            else:
                input_parts = ("!stat&" + user_input.split(":")[0]).split("&")
                limit = user_input.split(":")[1]
                if not limit.isnumeric():
                    limit = 0
        else:
            input_parts = user_input.split("&")
            limit = 0
        filtered_input = ''.join(char.lower() for char in user_input if char.isalpha())
        print(filtered_input)

        filtered_df = df.copy()
        numeric_df = []
        for part in input_parts:
            if part.isnumeric():

                part_filtered_input = int(part) - 1
                numeric_df.append(part_filtered_input)
            else:
                part_filtered_input = ''.join(char.lower() for char in part if char.isalpha())
                ascending_value = True if "!" in part else False

                if part_filtered_input in [primary.value for primary in Primary]:
                    condition = filtered_df["Attribute"] == part_filtered_input
                    filtered_df = filtered_df[~condition] if "!" in part else filtered_df[condition]
                elif part_filtered_input in [location.value for location in Locations]:
                    condition = filtered_df["Location"] == part_filtered_input
                    filtered_df = filtered_df[~condition] if "!" in part else filtered_df[condition]
                elif part_filtered_input == "stat":
                    filtered_df = filtered_df.sort_values(by="Stat", ascending=ascending_value)
                elif part_filtered_input == "price":
                    filtered_df = filtered_df.sort_values(by="Price", ascending=ascending_value)
                else:
                    filtered_df = filtered_df[filtered_df["Name"].str.lower().str.startswith(part_filtered_input)]
        if ret is None:
            return pd.concat([filtered_df, df.iloc[numeric_df]], ignore_index=False)
        elif not filtered_df.empty and ret is not None:
            limit = int(limit)
            if usage is not None and limit != 0:
                current_amount = 0
                attribute = ""
                for index, row in filtered_df.iterrows():
                    attribute = row["Attribute"]
                    break
                if usage == "use":
                    current_amount += self.group.get_Attribute(attribute)
                to_move = []
                for index, row in filtered_df.iterrows():
                    if current_amount >= limit:
                        break
                    if usage == "use":

                        if attribute == "food" or attribute == "medicine":
                            current_amount += row["Stat"] * 2
                        else:
                            current_amount += row["Stat"]
                    else:
                        current_amount += 1
                    to_move.append(int(index) - 1)
                if usage == "use":
                    print(attribute, ": ", current_amount)
                return to_move
            else:
                return list(pd.concat([filtered_df, df.iloc[numeric_df]], ignore_index=False).index)

    def sort_by_adventurers(self):
        df = pd.DataFrame([(adventurer.name, adventurer.health, adventurer.attack, adventurer.defense, adventurer.speed,
                            adventurer.job.value.name) for adventurer in self.adventurers],
                          columns=["Name", "Health", "Attack", "Defense", "Speed", "Job"])
        df.index = df.index + 1
        filtered = df.sort_values(by="Health", ascending=True)
        print(filtered)

    def move_items(self, where: list[Item], items: list[int]):
        items_to_move = []
        for i in range(len(self.items)):
            if i in items:
                items_to_move.append(self.items[i])

        for item_to_move in items_to_move:
            self.items.remove(item_to_move)
            where.append(item_to_move)
        print(len(where))
        for item in where:
            print(item.name)
