#!/bin/env python3

from Piece import Piece
from MtSquare import MtSquare

# Two x Two Square piece
class TxTPiece(Piece):
    def __init__(self, piece_name, start_x, start_y): 
        super().__init__(piece_name, 'TxT', start_x, start_y)
    
    # find array of possible moves given two empty space coordinates
    # @return empty array if no moves found or array of tuples of possible positions
    def find_moves(self, mt1, mt2):
        rv = []
        if (mt1.x != mt2.x and mt1.y != mt2.y):
            return rv
        # spaces vertically left of square
        if (mt1.x == mt2.x and mt1.x == self.x-1):
            if ((mt1.y == self.y and mt2.y == self.y+1)
                or (mt1.y == self.y+1 and mt2.y == self.y)):
                edge = self.make_edge(self.x-1, self.y, 'L')
                rv.append(edge)
        # spaces vertically right of square
        if (mt1.x == mt2.x and mt1.x == self.x+2):
            if ((mt1.y == self.y and mt2.y == self.y+1)
                or (mt1.y == self.y+1 and mt2.y == self.y)):
                edge = self.make_edge(self.x+1, self.y, 'R')
                rv.append(edge)
        # spaces horizontally above square
        if (mt1.y == mt2.y and mt1.y == self.y+2):
            if ((mt1.x == self.x and mt2.x == self.x+1)
                or (mt1.x == self.x+1 and mt2.x == self.x)):
                edge = self.make_edge(self.x, self.y+1, 'U')
                rv.append(edge)
        # spaces horizontally below square
        if (mt1.y == mt2.y and mt1.y == self.y-1):
            if ((mt1.x == self.x and mt2.x == self.x+1)
                or (mt1.x == self.x+1 and mt2.x == self.x)):
                edge = self.make_edge(self.x, self.y-1, 'D')
                rv.append(edge)

        return rv

    def populate_grid(self, board_grid):
        board_grid[self.y][self.x] = 'R'
        board_grid[self.y+1][self.x] = 'R'
        board_grid[self.y][self.x+1] = 'R'
        board_grid[self.y+1][self.x+1] = 'R'

def main():
    print("Initializing pieces")
    r = TxTPiece('R', 1, 3)

    x, y = r.get_pos()
    assert(x==1 and y==3)

    # test no move when both spots are not adjacent on the same side
    mt1 = MtSquare('mt1', 0, 0)
    mt2 = MtSquare('mt2', 0, 3)
    move_array = r.find_moves(mt1, mt2)
    assert (len(move_array) == 0)

    mt1.x = 0
    mt1.y = 3
    mt2.x = 3
    mt2.y = 3
    move_array = r.find_moves(mt1, mt2)
    assert (len(move_array) == 0)

    # test move direction when spots are adjacent
    # left
    mt1.x = 0
    mt1.y = 3
    mt2.x = 0
    mt2.y = 4
    move_array = r.find_moves(mt1, mt2)
    assert (len(move_array) == 1 and move_array[0].to_x == 0 
            and move_array[0].to_y == 3)

    # right
    mt1.x = 3
    mt1.y = 4
    mt2.x = 3
    mt2.y = 3
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 1)
    edge = edges[0]
    assert (edge.to_x == 2 and edge.to_y == 3)

    r = TxTPiece('R', 1, 2)

    # up
    mt1.x = 1
    mt1.y = 4
    mt2.x = 2
    mt2.y = 4
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 1)
    edge = edges[0]
    assert (edge.to_x == 1 and edge.to_y == 3 and edge.dir == 'U')

    # down
    mt1.x = 2
    mt1.y = 1
    mt2.x = 1
    mt2.y = 1
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 1)
    edge = edges[0]
    assert (edge.to_x == 1 and edge.to_y == 1 and edge.dir == 'D')

    cols, rows = (4, 5)
    b = [[0 for i in range(cols)] for j in range(rows)]
    r.populate_grid(b)
    print(b)

if __name__ == '__main__':
    main()