class Farm:
    def __init__(self, farm_name):
        self.name = farm_name
        self.animals = {}

    def add_animal(self, animal_type=None, count=1, **kwargs):
        """Add a single animal_type/count pair or multiple via kwargs."""
        if animal_type is not None:
            self.animals[animal_type] = self.animals.get(animal_type, 0) + count
        for animal, qty in kwargs.items():
            self.animals[animal] = self.animals.get(animal, 0) + qty

    def get_info(self):
        lines = [f"{self.name}'s farm", ""]
        for animal, qty in self.animals.items():
            lines.append(f"{animal} : {qty}")
        lines.append("")
        lines.append("    E-I-E-I-0!")
        return "\n".join(lines)

    def get_animal_types(self):
        return sorted(self.animals.keys())

    def get_short_info(self):
        animal_types = self.get_animal_types()
        animal_list = []
        for animal in animal_types:
            name = animal + "s" if self.animals[animal] > 1 else animal
            animal_list.append(name)
        if not animal_list:
            return f"{self.name}'s farm has no animals."
        if len(animal_list) > 1:
            short_info = ", ".join(animal_list[:-1]) + " and " + animal_list[-1]
        else:
            short_info = animal_list[0]
        return f"{self.name}'s farm has {short_info}."


# Test the code
macdonald = Farm("McDonald")
macdonald.add_animal("cow", 5)
macdonald.add_animal("sheep")
macdonald.add_animal("sheep")
macdonald.add_animal("goat", 12)
# Example of kwargs usage:
# macdonald.add_animal(cow=5, sheep=2, goat=12)
print(macdonald.get_info())
