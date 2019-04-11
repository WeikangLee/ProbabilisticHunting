from decimal import *
import random
import NewBoardGen

class hunter_hct():
    def __init__(self,board,size=50,disable_print=False):
        self.disable_print = disable_print
        self.target = board.get_target()
        self.board = board.board
        self.size = size
        self.believe_matrix = []
        for i in range(self.size):
            self.believe_matrix.append([])
            for j in range(self.size):
                self.believe_matrix[i].append(Decimal(Decimal(1) / Decimal(self.size * self.size)))
        # print(self.believe_matrix)

    def set_target(self, _type):
        set_terrain = _type
        terrain_list = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == set_terrain:
                    terrain_list.append((i,j))

        temp = random.sample(terrain_list,1)
        self.target = (temp[0][0],temp[0][1])
        return

    def find_target(self):
        # print(self.target)
        count = 0
        prob_of_not_found = [(0.1),(0.3),(0.7),(0.9)]
        terrain_type = -1
        while (1):
            count += 1
            max_prob = 0
            max_prob_node = (-1,-1)
            for i in range(self.size):
                for j in range(self.size):
                    if self.believe_matrix[i][j] > max_prob:
                        max_prob = self.believe_matrix[i][j]
                        max_prob_node = (i,j)

            terrain_type = self.board[max_prob_node[0]][max_prob_node[1]]
            # print(max_prob_node)
            if max_prob_node == self.target:
                if random.random() > prob_of_not_found[terrain_type]:
                    # print("success")
                    # print(count)
                    return count

            # update believe matrix
            i = max_prob_node[0]
            j = max_prob_node[1]

            temp1 = Decimal(self.believe_matrix[i][j]) * (
                Decimal(prob_of_not_found[terrain_type]).quantize(Decimal('0.00')))

            temp2 = Decimal(self.believe_matrix[i][j]) * (
                Decimal(1 - prob_of_not_found[terrain_type]).quantize(Decimal('0.00')))

            for i in range(self.size):
                for j in range(self.size):
                    if i == max_prob_node[0] and j == max_prob_node[1]:
                        self.believe_matrix[i][j] = temp1
                    else:
                        self.believe_matrix[i][j] = Decimal(self.believe_matrix[i][j]) * (
                            Decimal(1 + (temp2 / 1 - max_prob)))


if __name__ == "__main__":
    newboard = NewBoardGen.Board(50)
    newfind = hunter_hct(newboard,50)

    newboard.print_board()
    newfind.find_target()