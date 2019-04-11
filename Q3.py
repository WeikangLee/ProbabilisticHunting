import NewBoardGen
import hunter_hct
import hunter_hft


board = NewBoardGen.Board(50)

# hct
print('hct')
step = 0

iteration = 20

for i in range(0,4):
    step = 0
    print('processing', end='')
    for j in range(iteration):
        hunter = hunter_hct.hunter_hct(board, 50)
        hunter.set_target(i)
        step += hunter.find_target()
        print('.', end='')
    print('\nterrain type:', i)
    print('average cost:', step/iteration)


# hft
print('\n\nhft')
step = 0

iteration = 20

for i in range(0,4):
    step = 0
    print('processing', end='')
    for j in range(iteration):
        hunter = hunter_hft.hunter_hft(board, 50)
        hunter.set_target(i)
        step += hunter.find_target()
        print('.', end='')
    print('\nterrain type:', i)
    print('average cost:', step/iteration)