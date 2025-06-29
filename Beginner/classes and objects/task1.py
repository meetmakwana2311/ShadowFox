class Avenger:
    def __init__(self, name, age, gender, super_power, weapon):
        self.name = name
        self.age = age
        self.gender = gender
        self.super_power = super_power
        self.weapon = weapon

    def get_info(self):
        print(f"Name       : {self.name}")
        print(f"Age        : {self.age}")
        print(f"Gender     : {self.gender}")
        print(f"Super Power: {self.super_power}")
        print(f"Weapon     : {self.weapon}")
        print()

    def is_leader(self):
        return self.name == "Captain America"

super_heroes_data = [
    ("Captain America", 105, "Male", "Super strength", "Shield"),
    ("Iron Man", 48, "Male", "Technology", "Armor"),
    ("Black Widow", 34, "Female", "Superhuman", "Batons"),
    ("Hulk", 49, "Male", "Unlimited Strength", "No Weapon"),
    ("Thor", 1500, "Male", "Super Energy", "Mjölnir"),
    ("Hawkeye", 41, "Male", "Fighting Skills", "Bow and Arrows"),
]

avengers = []
for hero in super_heroes_data:
    avengers.append(Avenger(*hero))

for avenger in avengers:
    avenger.get_info()
    if avenger.is_leader():
        print(f"{avenger.name} is the leader of the Avengers.\n")
    else:
        print(f"{avenger.name} is not the leader.\n")
