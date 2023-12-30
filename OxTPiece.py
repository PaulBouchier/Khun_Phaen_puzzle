#!/bin/env python3

from Piece import Piece
from MtSquare import MtSquare

# One by Two (vertical) piece
class OxTPiece(Piece):
    def __init__(self, piece_name, start_x, start_y): 
        super().__init__(piece_name, 'OxT', start_x, start_y)
    
    # find array of possible moves given two empty space coordinates
    # @return empty array if no moves found or array of tuples of possible positions
    def find_moves(self, mt1, mt2):
        rv = []
        # either mt1 or mt2 above piece
        if (mt1.x == self.x and mt1.y == self.y+2):
                edge = self.make_edge(self.x, self.y+1, 'U')
                rv.append(edge)
        if (mt2.x == self.x and mt2.y == self.y+2):
                edge = self.make_edge(self.x, self.y+1, 'U')
                rv.append(edge)
        # either mt1 or mt2 below piece
        if (mt1.x == self.x and mt1.y == self.y-1):
                edge = self.make_edge(self.x, self.y-1, 'D')
                rv.append(edge)
        if (mt2.x == self.x and mt2.y == self.y-1):
                edge = self.make_edge(self.x, self.y-1, 'D')
                rv.append(edge)
        # spaces vertically left of square
        if (mt1.x == mt2.x and mt1.x == self.x-1):
            if ((mt1.y == self.y and mt2.y == self.y+1)
                or (mt1.y == self.y+1 and mt2.y == self.y)):
                edge = self.make_edge(self.x-1, self.y, 'L')
                rv.append(edge)
        # spaces vertically right of square
        if (mt1.x == mt2.x and mt1.x == self.x+1):
            if ((mt1.y == self.y and mt2.y == self.y+1)
                or (mt1.y == self.y+1 and mt2.y == self.y)):
                edge = self.make_edge(self.x+1, self.y, 'R')
                rv.append(edge)

        return rv


    def populate_grid(self, board_grid):
        board_grid[self.y][self.x] = 'Y'
        board_grid[self.y+1][self.x] = 'Y'

def main():
    print("Initializing pieces")
    r = OxTPiece('B', 1, 1)

    x, y = r.get_pos()
    assert(x==1 and y==1)

    # test no move when mt spots are not adjacent to piece
    mt1 = MtSquare('mt1', 2, 2)
    mt2 = MtSquare('mt2', 0, 1)
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 0)

    mt1.x = 1
    mt1.y = 4
    mt2.x = 0
    mt2.y = 0
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 0)

    # test move direction when a spot is adjacent
    # up
    mt1.x = 1
    mt1.y = 3
    mt2.x = 2
    mt2.y = 4
    edges = r.find_moves(mt1, mt2)
    assert(len(edges) == 1)
    edge = edges[0]
    assert(edge.to_x == 1)
    assert(edge.to_y == 2)
    assert(edge.dir == 'U')

    # down
    mt1.x = 1
    mt1.y = 0
    mt2.x = 3
    mt2.y = 1
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 1)
    edge = edges[0]
    assert(edge.to_x == 1)
    assert(edge.to_y == 0)
    assert(edge.dir == 'D')

    # Two adjacent spots, one up & one down
    mt1.x = 1
    mt1.y = 3
    mt2.x = 1
    mt2.y = 0
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 2)
    edge = edges[0]
    assert(edge.to_x == 1)
    assert(edge.to_y == 2)
    assert(edge.dir == 'U')
    edge = edges[1]
    assert(edge.to_x == 1)
    assert(edge.to_y == 0)
    assert(edge.dir == 'D')

    cols, rows = (4, 5)
    b = [[0 for i in range(cols)] for j in range(rows)]
    r.populate_grid(b)
    print(b)


if __name__ == '__main__':
    main()