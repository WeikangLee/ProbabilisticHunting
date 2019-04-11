import NewBoardGen
from decimal import *
import random
import math


class MovingTarget:
    def __init__(self, board, size=50):
        self.size = size
        self.board = board.board
        self.target = board.get_target()
        self.believe_matrix = []
        initial_possibility = Decimal(Decimal(1) / Decimal(self.size * self.size))
        for i in range(self.size):
            self.believe_matrix.append([])
            for j in range(self.size):
                self.believe_matrix[i].append(initial_possibility)
        # print(self.believe_matrix)
        # print(self.board)

    def neighbor_finder(self, location):
        neighbor = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for x, y in directions:
            i = x + location[0]
            j = y + location[1]
            if i in range(0, self.size) and j in range(0, self.size):
                neighbor.append((i, j))
        return neighbor

    def target_moving(self, old_location):
        possible_location = self.neighbor_finder(old_location)
        new_location = random.sample(possible_location, 1)
        old_type = self.board[old_location[0]][old_location[1]]
        new_type = self.board[new_location[0][0]][new_location[0][1]]
        self.target = (new_location[0][0], new_location[0][1])
        return old_type, new_type

    def update_possibility(self, type1, type2):
        # find possible locations, and set impossible locations to 0
        for i in range(self.size):
            for j in range(self.size):
                _type = self.board[i][j]
                if _type == type1:
                    neighbor = self.neighbor_finder((i, j))
                    is_possible_location = False
                    for x, y in neighbor:
                        if self.board[x][y] == type2:
                            is_possible_location = True
                    if not is_possible_location:
                        self.believe_matrix[i][j] = Decimal(0)

                elif type == type2:
                    neighbor = self.neighbor_finder((i,j))
                    is_possible_location = False
                    for x,y in neighbor:
                        if self.board[x][y] == type2:
                            is_possible_location = True
                    if not is_possible_location:
                        self.believe_matrix[i][j] = Decimal(0)

                else:
                    self.believe_matrix[i][j] = Decimal(0)
        # flow the possibility
        temp_believe_matrix = []
        for i in range(self.size):
            temp_believe_matrix.append([])
            for j in range(self.size):
                temp_believe_matrix[i].append(Decimal(0))

        for i in range(self.size):
            for j in range(self.size):
                if self.believe_matrix[i][j] != 0:
                    neighbor = self.neighbor_finder((i, j))
                    counter = 0
                    for x, y in neighbor:
                        if self.board[i][j] == type1 or self.board[i][j] == type2:
                            counter += 1
                    for x, y in neighbor:
                        if self.board[i][j] == type1 or self.board[i][j] == type2:
                            temp_believe_matrix[x][y] += self.believe_matrix[i][j] / counter
        self.believe_matrix = temp_believe_matrix

        # normalization
        total_possibility = 0
        for i in range(self.size):
            for j in range(self.size):
                total_possibility += self.believe_matrix[i][j]
        try:
            temp = Decimal(1/total_possibility)
        except Exception:
            print("I don't know why total possibility is 0, I try my best to find the problem! ")

        for i in range(self.size):
            for j in range(self.size):
                self.believe_matrix[i][j] *= temp

    def distance(self,node1,node2):
        cost = 0
        x1 = node1[0]
        y1 = node1[1]
        x2 = node2[0]
        y2 = node2[1]
        cost = abs(x1 - x2) + abs(y1 - y2)
        cost = math.sqrt(cost)
        return cost

    def find_target_hct(self):
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
                            temp_prob = self.believe_matrix[i][j] / Decimal(distance)
                        if temp_prob > max_prob1:
                            max_prob1 = temp_prob
                            # max_prob2 = self.believe_matrix[i][j]
                            max_prob_node = (i, j)

            distance = self.distance(pre_node, max_prob_node)
            if distance == 0:
                count += 1
            else:
                count += int(1 + distance*distance)
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

            temp1 = (self.believe_matrix[i][j]) * Decimal(prob_of_not_found[terrain_type])

            temp2 = (self.believe_matrix[i][j]) * Decimal(1 - prob_of_not_found[terrain_type])

            for i in range(self.size):
                for j in range(self.size):
                    terrain_type = self.board[i][j]
                    if i == max_prob_node[0] and j == max_prob_node[1]:
                        self.believe_matrix[i][j] = temp1
                        # print(self.believe_matrix[i][j])
                    else:
                        self.believe_matrix[i][j] = (self.believe_matrix[i][j]) * ((1 + ((temp2) / (1 - max_prob2))))

            type1,type2 = self.target_moving(self.target)
            self.update_possibility(type1,type2)
            # print('target:', self.target)

    def find_target_hft(self):
        count = 0
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
                        terrain_type = self.board[i][j]
                        temp_prob = self.believe_matrix[i][j] * Decimal(1 - prob_of_not_found[terrain_type])
                        if temp_prob > max_prob1:
                            max_prob1 = temp_prob
                            max_prob2 = self.believe_matrix[i][j]
                            max_prob_node = (i, j)
                    else:
                        terrain_type = self.board[i][j]
                        distance = self.distance(pre_node, (i, j))
                        if distance == 0:
                            temp_prob = self.believe_matrix[i][j] * Decimal(1 - prob_of_not_found[terrain_type])
                        else:
                            temp_prob = self.believe_matrix[i][j] * Decimal((1 - prob_of_not_found[terrain_type]) / distance)
                        if temp_prob > max_prob1:
                            max_prob1 = temp_prob
                            max_prob2 = self.believe_matrix[i][j]
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
            # print(Decimal(prob_of_not_found[terrain_type]).quantize(Decimal('0.00')))
            temp1 = (self.believe_matrix[i][j]) * Decimal(prob_of_not_found[terrain_type])

            temp2 = (self.believe_matrix[i][j]) * Decimal(1 - prob_of_not_found[terrain_type])

            for i in range(self.size):
                for j in range(self.size):
                    terrain_type = self.board[i][j]
                    if i == max_prob_node[0] and j == max_prob_node[1]:
                        self.believe_matrix[i][j] = temp1
                        # print(self.believe_matrix[i][j])
                    else:
                        self.believe_matrix[i][j] = (self.believe_matrix[i][j]) * ((1 + ((temp2) / (1 - max_prob2))))

            type1,type2 = self.target_moving(self.target)
            self.update_possibility(type1,type2)
            # print('target:', self.target)




if __name__ == '__main__':
    board = NewBoardGen.Board()
    hunter = MovingTarget(board)
    hunter.find_target_hct()



