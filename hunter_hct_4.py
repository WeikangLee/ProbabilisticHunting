import random
import NewBoardGen
import math

class hunter_hct():
    def __init__(self,board,size=50,disable_print=False):
        self.disable_print = disable_print
        self.target = (7,8)
        self.board = board.board
        self.size = size
        self.believe_matrix = []
        for i in range(self.size):
            self.believe_matrix.append([])
            for j in range(self.size):
                self.believe_matrix[i].append(((1) / (self.size * self.size)))
        # print(self.believe_matrix)

    def distance(self,node1,node2):
        cost = 0
        x1 = node1[0]
        y1 = node1[1]
        x2 = node2[0]
        y2 = node2[1]
        cost = abs(x1 - x2) + abs(y1 - y2)
        cost = math.sqrt(cost)
        return cost

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
        count = 0
        distance = 0
        prob_of_not_found = [(0.1),(0.3),(0.7),(0.9)]
        terrain_type = -1
        pre_node = (-1,-1)
        # print("target:")
        # print(self.target)
        while (1):
            max_prob1 = 0
            max_prob2 = 0
            max_prob_node = (-1,-1)

            for i in range(self.size):
                for j in range(self.size):
                    if count == 0:
                        temp_prob = self.believe_matrix[i][j]
                        if temp_prob > max_prob1:
                            max_prob1 = temp_prob
                            max_prob2 = self.believe_matrix[i][j]
                            max_prob_node = (i, j)
                    else:
                        distance = self.distance(pre_node, (i, j))
                        if distance == 0:
                            temp_prob = self.believe_matrix[i][j]
                        else:
                            temp_prob = self.believe_matrix[i][j] / distance
                        if temp_prob > max_prob1:
                            max_prob1 = temp_prob
                            # max_prob2 = self.believe_matrix[i][j]
                            max_prob_node = (i, j)

            distance = self.distance(pre_node, max_prob_node)
            if distance == 0:
                count += 1
            else:
                count += (1+distance*distance)
            pre_node = max_prob_node

            # print(max_prob_node)
            terrain_type = self.board[max_prob_node[0]][max_prob_node[1]]
            # print(count)
            if max_prob_node == self.target:
                if random.random() > prob_of_not_found[terrain_type]:
                    # print("success")
                    # print(count)
                    return count

            # update believe matrix
            i = max_prob_node[0]
            j = max_prob_node[1]

            temp1 = (self.believe_matrix[i][j]) * ((prob_of_not_found[terrain_type]))

            temp2 = (self.believe_matrix[i][j]) * ((1 - prob_of_not_found[terrain_type]))

            for i in range(self.size):
                for j in range(self.size):
                    terrain_type = self.board[i][j]
                    if i == max_prob_node[0] and j == max_prob_node[1]:
                        self.believe_matrix[i][j] = temp1
                        # print(self.believe_matrix[i][j])
                    else:
                        self.believe_matrix[i][j] = (self.believe_matrix[i][j]) * ((1 + ((temp2) / (1 - max_prob2))))


if __name__ == "__main__":
    newboard = NewBoardGen.Board(20)
    newfind = hunter_hct(newboard,20)
    newfind.set_target(3)
    newboard.print_board()
    newfind.find_target()