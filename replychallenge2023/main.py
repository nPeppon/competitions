from typing import List, Dict, Tuple, Set, Optional
import os
import random

# TODO: 1 snake at a time
# TODO: Order snakes by length
# TODO: Retry init position N times
# TODO: 

filenames = ['data\\00.txt',
             'data\\01.txt',
             'data\\02.txt',
             'data\\03.txt',
             'data\\04.txt',
             'data\\05.txt',
             'data\\06.txt']

abs_path = 'c:\\Users\\arufo\\Desktop\\Competitions\\competitions\\replychallenge2023\\'

def parse_input(letter):
    f = open(abs_path + filenames[letter])
    # Parse input file
    # print('Reading first line')
    line = f.readline()
    columns = int(line.split(' ')[0])
    rows = int(line.split(' ')[1])
    num_snakes = int(line.split(' ')[2])

    C = columns
    R = rows
    S = num_snakes

    # print('C ' + str(C))
    # print('R ' + str(R))
    # print('S ' + str(S))

    # print('Reading Second line')
    line = f.readline()
    snakes = [ Snake(int(x), i) for i,x in enumerate(line.split(" "))]
    # for s in snakes:
    #     print(s.to_string()) 
        
    matrix = []
    wormholes = []
    
    for r in range(R):
        row = f.readline().replace("\n", "").split(' ')
        matrix.append(row)
        wormholes.extend([(r, i) for i, x in enumerate(row) if x == "*"])
            
    matrix = Matrix(matrix, wormholes) 
    # [print(row) for row in matrix.matrix]
    # print(matrix.wormholes)
    return C, R, S, snakes, matrix


class Matrix:
    def __init__(self, matrix: List[List[str]], wormholes_coord:List[Tuple[int, int]]):
        self.matrix = matrix
        self.wormholes = wormholes_coord

class Snake:
    def __init__(self, size: int, id: int):
        self.id = id
        self.size = size
        self.score = 0
        self.move_list = []
        self.current_position = (-1,-1)
        self.all_positions = []

    def increase_score(self, score: int):
        self.score += score
    
    def add_move(self, move: str, coord: Tuple[int, int], score:int):
        self.move_list.append(move)
        self.current_position = coord
        self.all_positions.append((coord[0], coord[1], score))
        
    def current_position(self, position: Tuple[int, int]):
        self.current_position = position
        
    def to_string(self):
        return "Snake - Size: " + str(self.size)
        
    def kill_me(self):
        self.size = 0

class Evaluator:
    def __init__(self, C: int, R: int, S: int, snakes: List[Snake], matrix: Matrix):
        self.C = C
        self.R = R
        self.S = S
        self.snakes = snakes
        self.matrix = matrix
        self.total_score = 0
        self.killed_at_init = 0
        self.killed_no_move = 0
        self.killed_neg_score = 0
        self.last_percentage = 0
        self.completed_snakes = 0

    def to_string(self) -> str:
        return 'completed_snakes: ' + str(self.completed_snakes) + '\tkilled_at_init: ' + str(self.killed_at_init) + '\tkilled_neg_score: ' + str(self.killed_neg_score) + '\tkilled_no_move: ' + str(self.killed_no_move) + '\tScore: ' + str(self.total_score)

    def printProgress(self, Ti: int):
        percentage_of_advancement = int(Ti * 100 / self.S)
        if percentage_of_advancement >= self.last_percentage or percentage_of_advancement == 100:
            print('Snake advance: ' + str(percentage_of_advancement) + '\t' + self.to_string())
            # let's print something every 10% of projects
            self.last_percentage += 10

    def add_move(self, s:Snake, coord: Tuple[int, int], direction:str):
        if not self.matrix.matrix[coord[0]][coord[1]] == '*' and not self.matrix.matrix[coord[0]][coord[1]] == '#':
            score = self.matrix.matrix[coord[0]][coord[1]]
            s.add_move(direction, coord, score)
            # replace the cell of matrix with a #
            self.matrix.matrix[coord[0]][coord[1]] = "#" 
            s.increase_score(int(score))

    def initialize_positions(self):
        if R >= C:      
            distance = int(R/S)
            for i, s in enumerate(self.snakes):
                tupla = (i*distance, 0)
                self.add_move(s, tupla, str(tupla[1]) + " " + str(tupla[0]))
        else:
            distance = int(C/S)
            for i, s in enumerate(self.snakes):
                tupla = (0, i*distance)
                self.add_move(s, tupla, str(tupla[1]) + " " + str(tupla[0]))
    # initialize_random_positions
    def initialize_random_positions(self):
        for i, s in enumerate(self.snakes):
            self.initialize_random_position(s)

    def initialize_random_position(self, snake: Snake):
        tupla = (-1, -1)
        while tupla == (-1, -1):
            temp_tupla = (random.randint(0, R-1), random.randint(0, C-1))
            if not self.matrix.matrix[temp_tupla[0]][temp_tupla[1]] == '#' and not self.matrix.matrix[temp_tupla[0]][temp_tupla[1]] == '*':
                tupla = temp_tupla
        self.add_move(snake, tupla, str(tupla[1]) + " " + str(tupla[0]))
        
    def clean_snake(self, snake:Snake):
        snake.move_list = []
        for tupla in snake.all_positions:
            self.matrix.matrix[tupla[0]][tupla[1]] = tupla[2]
        snake.all_positions = []
        
    def choose_next_move_for_snake(self, current_position: Tuple[int, int], is_wormohole:bool = False):
        best_direction = ''
        best_position = current_position
        best_score = -100001
        
        possibilities = [(0,-1), (0, 1), (1,0), (-1,0)]
        directions = ['L', 'R', 'D', 'U']
        
        for _i, p in enumerate(possibilities):
            next_position = ((current_position[0] + p[0]) % self.R, (current_position[1] + p[1]) % self.C)
            next_score = self.matrix.matrix[next_position[0]][next_position[1]]
            if not next_score == "#":
                if next_score == "*" and not is_wormohole:
                    for worm in self.matrix.wormholes:
                        w_position, w_direction, w_score = self.choose_next_move_for_snake(worm, True)
                        if w_score >= best_score:
                            best_score = w_score
                            best_position = w_position
                            best_direction = str(w_position[1]) + " " + str(w_position[0])
                elif not next_score == "*" and (int(next_score) >= best_score):
                    best_score = int(next_score)
                    best_position = next_position
                    best_direction = directions[_i]
        if best_direction == '':
            best_direction =  '.'
        return best_position, best_direction, best_score
        
    def run_all_snakes_together(self):
        self.initialize_random_positions()
        iteration = 0
        while len(self.snakes) > 0:
            for snake in self.snakes:
                if snake.current_position == (-1, -1):
                    self.snakes.remove(snake)
                    self.killed_at_init += 1
                else:
                    position, direction, score = self.choose_next_move_for_snake(snake.current_position)
                    if direction == '.':
                        self.snakes.remove(snake)
                        self.clean_snake(snake)
                        self.killed_no_move += 1
                    else:
                        self.add_move(snake, position, direction)
                    if len(snake.move_list) == snake.size:
                        self.snakes.remove(snake)
                        if snake.score > 0:
                            self.total_score += snake.score
                        else:
                            self.killed_neg_score += 1
                            self.clean_snake(snake)
            iteration += 1
        print('killed_at_init: ' + str(self.killed_at_init) +
              '\tkilled_neg_score: ' + str(self.killed_neg_score) + '\tkilled_no_move: ' + str(self.killed_no_move))

    def run_one_snake_at_time(self):
        # reverse: True -> descending , False -> ascending
        self.snakes.sort(
            key=lambda x: x.size, reverse=True)
        for i,snake in enumerate(self.snakes):
            self.printProgress(i)
            self.run_single_snake(snake)

        # reverse: True -> descending , False -> ascending
        self.snakes.sort(key=lambda x: x.id, reverse=False)
        print(self.to_string())

    def run_single_snake(self, snake: Snake, retry_left: int = 10):
        retry_left -= 1
        if retry_left == -1:
            return
        self.initialize_random_position(snake)
        if snake.current_position == (-1, -1):
            if retry_left == 0:
                self.killed_at_init += 1
            self.run_single_snake(snake, retry_left)
            return
        while len(snake.move_list) < snake.size:
            position, direction, score = self.choose_next_move_for_snake(snake.current_position)
            if direction == '.':
                if retry_left == 0:
                    self.killed_no_move += 1
                self.clean_snake(snake)
                self.run_single_snake(snake, retry_left)
                return
            else:
                self.add_move(snake, position, direction)
            if len(snake.move_list) == snake.size:
                if snake.score > 0:
                    self.total_score += snake.score
                    self.completed_snakes += 1
                    return
                else:
                    if retry_left == 0:
                        self.killed_neg_score += 1
                    self.clean_snake(snake)
                    self.run_single_snake(snake, retry_left)
                    return
    
def write_output(letter, demons_fought: List[int]):
    filename = '' + letter + '.txt'
    with open(filename, 'w') as out:
        for s in snakes:
            print(" ".join(s.move_list), file=out)


if __name__ == '__main__':
    # letters = ['a', 'b', 'c', 'd', 'e', 'f']
    input_files = [0, 1, 2, 3, 4, 5, 6]
    # input_files = [6]
    for file in input_files:
        print('File: ' + str(file))
        C, R, S, snakes, matrix = parse_input(file)
        evaluator = Evaluator(C, R, S, snakes.copy(), matrix)
        # evaluator.run_all_snakes_together()
        evaluator.run_one_snake_at_time()
        print('Score: ' + str(evaluator.total_score))
        write_output(str(file), evaluator.snakes)
