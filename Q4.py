import NewBoardGen
import hunter_hct_4
import hunter_hft_4


board = NewBoardGen.Board(50)

# hct Location based
print('hct Location based')
step = 0
iteration = 20

for i in range(0,4):
    step = 0
    print('processing', end='')
    for j in range(iteration):
        hunter = hunter_hct_4.hunter_hct(board, 50)
        hunter.set_target(i)
        step += hunter.find_target()
        print('.', end='')
    print('\nterrain type:', i)
    print('average cost:', step/iteration)



# hft Location based
print('\n\nhft Location based')
step = 0
iteration = 20

for i in range(0,4):
    step = 0
    print('processing', end='')
    for j in range(iteration):
        hunter = hunter_hft_4.hunter_hft(board, 50)
        hunter.set_target(i)
        step += hunter.find_target()
        print('.', end='')
    print('\nterrain type:', i)
    print('average cost:', step/iteration)

