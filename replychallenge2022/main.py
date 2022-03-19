from typing import List, Dict
import os


class Demon():

    def __init__(self, index: int, stamina_to_consume: int, turn_before_stamina_gain: int, stamina_gained: int,
                 turn_collecting_fragments: int):
        self.index = index
        self.stamina_to_consume = stamina_to_consume
        self.turn_before_stamina_gain = turn_before_stamina_gain
        self.stamina_gained = stamina_gained
        self.turn_collecting_fragments = turn_collecting_fragments
        self.fragments_per_turn = {}
        self.isDefeated = False
        self.tot_fragments = 0

    def addFragmentPerTurn(self, turn: int, num_fragments: int):
        self.fragments_per_turn[turn] = num_fragments
        self.tot_fragments += num_fragments

    def setDefeated(self, isDefeated: bool):
        self.isDefeated = isDefeated

    def isAvailable(self) -> bool:
        return self.isDefeated


def parse_input(letter):
    filenames = ['data/00.txt',
                 'data/01.txt',
                 'data/02.txt',
                 'data/03.txt',
                 'data/04.txt',
                 'data/05.txt']

    int_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'f', 5: 'g'}
    letter_to_int = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}

    f = open(filenames[letter])
    # Parse input file
    print('Reading first line')
    line = f.readline()
    print('Read first line')
    stamina_initial = int(line.split(' ')[0])
    stamina_max = int(line.split(' ')[1])
    num_turns = int(line.split(' ')[2])
    num_demons = int(line.split(' ')[3])

    Si = stamina_initial
    Smax = stamina_max
    T = num_turns
    D = num_demons

    print('T ' + str(T))
    print('D ' + str(D))

    demons = []

    for d in range(D):
        line = f.readline()
        lineSplit = line.split(' ')

        stamina_to_consume = int(lineSplit[0])
        turn_before_stamina_gain = int(lineSplit[1])
        stamina_gained = int(lineSplit[2])
        turn_collecting_fragments = int(lineSplit[3])

        demon = Demon(d, stamina_to_consume, turn_before_stamina_gain, stamina_gained, turn_collecting_fragments)
        for t in range(turn_collecting_fragments):
            demon.addFragmentPerTurn(t, int(lineSplit[4 + t]))
        demons.append(demon)

    return Si, Smax, T, D, demons


class Evaluator:
    def __init__(self, Si: int, Smax: int, T: int, D: int, demons: List[Demon]):
        self.Si = Si
        self.Smax = Smax
        self.D = D
        self.T = T
        self.demons = demons
        self.fragments_collected = 0
        self.fragment_to_collect_at_turn = {k: 0 for k in range(T)}
        self.stamina_to_recover_at_turn = {k: 0 for k in range(T)}
        self.demons_fought = []
        self.last_percentage = 0

    def sortDemons(self):
        # reverse: True -> descending , False -> ascending
        percentage_of_stamina = int(self.Si * 100 / self.Smax)
        if percentage_of_stamina <= 40:
            self.demons.sort(key=lambda x: x.turn_before_stamina_gain, reverse=False)
        else:
            self.demons.sort(key=lambda x: x.tot_fragments, reverse=True)

    def isDemonFightable(self, demon: Demon):
        if not demon.isDefeated and demon.stamina_to_consume <= self.Si:
            return True
        return False

    def updateAndResortDemons(self, Ti: int):
        for demon in self.demons:
            newTotFragments = 0
            times_to_remove = []
            for time, num_fragments in demon.fragments_per_turn.items():
                if Ti + time < self.T:
                    newTotFragments += num_fragments
                else:
                    times_to_remove.append(time)

            [demon.fragments_per_turn.pop(time) for time in times_to_remove]
            demon.tot_fragments = newTotFragments
            # if demon.tot_fragments == 0:
            #     self.demons.remove(demon)
        self.sortDemons()

    def pickNextDemon(self):
        for demon in self.demons:
            if self.isDemonFightable(demon):
                return demon
        return None

    def fightDemon(self, demon: Demon, Ti: int):
        self.demons.remove(demon)
        self.Si -= demon.stamina_to_consume
        # Define when to recover stamin and collect fragments
        if Ti + demon.turn_before_stamina_gain < self.T:
            self.stamina_to_recover_at_turn[Ti + demon.turn_before_stamina_gain] += demon.stamina_gained
        for time, num_fragments in demon.fragments_per_turn.items():
            if Ti + time < self.T:
                self.fragment_to_collect_at_turn[Ti + time] += num_fragments
        self.demons_fought.append(demon.index)

    def printProgress(self, Ti: int):
        percentage_of_advancement = int(Ti * 100 / self.T)
        if percentage_of_advancement >= self.last_percentage or percentage_of_advancement == 100:
            print('Completed turns: ' + str(percentage_of_advancement) + '%\t->\tFragments collected so far: ' + str(
                self.fragments_collected))
            # let's print something every 5% of projects
            self.last_percentage += 5

    def run(self):
        Ti = 0
        while Ti < T:
            # Recover stamin
            self.Si = min(self.Smax, self.Si + self.stamina_to_recover_at_turn[Ti])
            self.updateAndResortDemons(Ti)
            nextDemon = self.pickNextDemon()
            if nextDemon is not None:
                self.fightDemon(nextDemon, Ti)
            # Collect fragments
            self.fragments_collected += self.fragment_to_collect_at_turn[Ti]
            self.printProgress(Ti)
            Ti += 1
        self.printProgress(Ti)


def write_output(letter, demons_fought: List[int]):
    filename = '' + letter + '.txt'
    with open(filename, 'w') as out:
        # print(str(len(demons_fought)), file=out)
        for d in demons_fought:
            print(str(d), file=out)


if __name__ == '__main__':
    # letters = ['a', 'b', 'c', 'd', 'e', 'f']
    # letters = [0, 1, 2, 3, 4, 5]
    letters = [5]
    for letter in letters:
        Si, Smax, T, D, demons = parse_input(letter)
        evaluator = Evaluator(Si, Smax, T, D, demons)
        evaluator.run()

        write_output(str(letter), evaluator.demons_fought)
