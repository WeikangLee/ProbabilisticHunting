import random
import numpy as np


class Board:
    def __init__(self,size=50):
        """
        Create a new board
        param size: the size of board
        param target: the position of target
        param num_flat: the number of flat
        param num_hill: the number of num_hill
        param num_forest: the number of num_forest
        param num_cave: the number of num_cave
        """
        self.size = size
        self.target = (-1,-1)
        self.num_flat = 0
        self.num_hill = 0
        self.num_forest = 0
        self.num_cave = 0
        # create a board, setting all cells 0
        self.board = []
        for i in range(self.size):
            self.board.append([])
            for j in range(self.size):
                self.board[i].append(0)
        self.assign()
        self.set_target()

    def assign(self):
        # return a board assigned with different terrain types
        self.target = (0,0)
        self.num_hill = int(self.size * self.size * 0.3)
        self.num_forest = int(self.size * self.size * 0.3)
        self.num_cave = int(self.size * self.size * 0.2)
        self.num_flat = 2500 - self.num_hill - self.num_forest - self.num_cave
        all_cell_set = []
        for i in range(self.size):
            for j in range(self.size):
                all_cell_set.append((i,j))

        hill_forest_cave_set = random.sample(all_cell_set,self.num_hill + self.num_forest + self.num_cave)
        forest_cave_set = random.sample(hill_forest_cave_set,self.num_forest + self.num_cave)
        cave_set = random.sample(forest_cave_set,self.num_cave)

        for x,y in hill_forest_cave_set:
            self.board[x][y] = 1

        for x,y in forest_cave_set:
            self.board[x][y] = 2

        for x,y in cave_set:
            self.board[x][y] = 3

    def print_board(self):
        # print the board as a matrix '0':flat '1':hill '2':forest '3':cave
        print(self.board)
        print('the number of flat:' + str(self.num_flat))
        print('the number of hilly:' + str(self.num_hill))
        print('the number of forested:' + str(self.num_forest))
        print('the number of caves:' + str(self.num_cave))

    def get_board(self):
        # return a board
        return self.board

    def set_target(self):
        # return the target
        self.target = (random.choice(range(0,self.size)),random.choice(range(0,self.size)))
        return

    def get_target(self):
        return self.target


# newboard=Board()
# newboard.print_board()

