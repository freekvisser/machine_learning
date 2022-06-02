import random


def random_letters(nr_of_notes):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    return_array = []
    for index in range(nr_of_notes):
        return_array.extend([(letters[random.randrange(0, 6)], 4)])
    return return_array


class BuildingBlock:
    def __init__(self, nr_of_notes):
        self.notes = tuple(map(tuple, random_letters(nr_of_notes)))
        print(self.notes)

    def get_notes(self):
        return self.notes


class Song(BuildingBlock):
    def __init__(self, nr_of_building_blocks, nr_of_notes):
        building_blocks = []
        for index in range(nr_of_building_blocks):
            building_blocks.append(BuildingBlock(nr_of_notes))
        super().__init__()


song = Song(8, 4)
