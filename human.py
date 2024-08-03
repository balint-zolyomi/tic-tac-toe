class Human:
    def __init__(self, board):
        self.board = board

    def move(self):
        while True:
            move = input("Enter coordinates (i,j): ")
            i, j = move.split()
            i = int(i)
            j = int(j)
            action = (i, j)

            if self.board.state[i, j] == 0:
                self.board.move(action)
                break
