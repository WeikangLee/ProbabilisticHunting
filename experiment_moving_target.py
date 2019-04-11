import moving_target_rule_1and2
import moving_target_distance
import NewBoardGen

# moving target with rule1 and rule2

iteration = 100
board = NewBoardGen.Board()

# rule 1 hct
print("rule 1 hct")
print("processing", end="")
step = 0
for i in range(iteration):
    board.assign()
    hunter = moving_target_rule_1and2.MovingTarget(board)
    step += hunter.find_target_hct()
    print(".", end="")
print('\nAverage cost of rule1: ', int(step/iteration))

# rule 2 hft
print("\n\nrule2 hft")
print("processing", end="")
step = 0
for i in range(iteration):
    board.assign()
    hunter = moving_target_rule_1and2.MovingTarget(board)
    step += hunter.find_target_hft()
    print(".", end="")
print('\nAverage cost of rule2: ', int(step/iteration))


# Redo Q4
# moving target  rule1 and rule2 with location based

# rule 1 hct with location based
print("\n\nrule1 hct with location based")
print("processing", end="")
step = 0
for i in range(iteration):
    board.assign()
    hunter = moving_target_distance.MovingTarget(board)
    step += hunter.find_target_hct()
    print(".", end="")
print('\nAverage cost of rule1 with location based: ', int(step / iteration))


# rule 2 hft with location based
print("\n\nrule2 hft with location based")
print("processing", end="")
step = 0
for i in range(iteration):
    board.assign()
    hunter = moving_target_distance.MovingTarget(board)
    step += hunter.find_target_hft()
    print(".", end="")
print('\nAverage cost of rule2 with location based: ', int(step / iteration))

