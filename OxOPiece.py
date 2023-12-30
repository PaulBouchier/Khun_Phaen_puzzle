#!/bin/env python3

from Piece import Piece
from MtSquare import MtSquare

# One by One piece
class OxOPiece(Piece):
    def __init__(self, piece_name, start_x, start_y): 
        super().__init__(piece_name, 'OxO', start_x, start_y)
    
    # find array of possible moves given two empty space coordinates
    # @return empty array if no moves found or array of tuples of possible positions
    def find_moves(self, mt1, mt2):
        rv = []
        # either mt1 or mt2 left of piece
        if (mt1.y == self.y and mt1.x == self.x-1):
                edge = self.make_edge(self.x-1, self.y, 'L')
                rv.append(edge)
        if (mt2.y == self.y and mt2.x == self.x-1):
                edge = self.make_edge(self.x-1, self.y, 'L')
                rv.append(edge)
        # either mt1 or mt2 right of piece
        if (mt1.y == self.y and mt1.x == self.x+1):
                edge = self.make_edge(self.x+1, self.y, 'R')
                rv.append(edge)
        if (mt2.y == self.y and mt2.x == self.x+1):
                edge = self.make_edge(self.x+1, self.y, 'R')
                rv.append(edge)
        # either mt1 or mt2 above piece
        if (mt1.x == self.x and mt1.y == self.y+1):
                edge = self.make_edge(self.x, self.y+1, 'U')
                rv.append(edge)
        if (mt2.x == self.x and mt2.y == self.y+1):
                edge = self.make_edge(self.x, self.y+1, 'U')
                rv.append(edge)
        # either mt1 or mt2 below piece
        if (mt1.x == self.x and mt1.y == self.y-1):
                edge = self.make_edge(self.x, self.y-1, 'D')
                rv.append(edge)
        if (mt2.x == self.x and mt2.y == self.y-1):
                edge = self.make_edge(self.x, self.y-1, 'D')
                rv.append(edge)

        return rv

    def populate_grid(self, board_grid):
        board_grid[self.y][self.x] = 'B'

def main():
    print("Initializing pieces")
    r = OxOPiece('B', 1, 1)

    x, y = r.get_pos()
    assert(x==1 and y==1)

    # test no move when mt spots are not adjacent to piece
    mt1 = MtSquare('mt1', 2, 2)
    mt2 = MtSquare('mt2', 1, 3)
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 0)

    mt1.x = 3
    mt1.y = 1
    mt2.x = 0
    mt2.y = 0
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 0)

    # test move direction when a spot is adjacent
    # left
    mt1.x = 0
    mt1.y = 1
    mt2.x = 0
    mt2.y = 4
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 1)
    edge = edges[0]
    assert(edge.to_x == 0)
    assert(edge.to_y == 1)
    assert(edge.dir == 'L')

    # right
    mt1.x = 2
    mt1.y = 1
    mt2.x = 3
    mt2.y = 3
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 1)
    edge = edges[0]
    assert(edge.to_x == 2)
    assert(edge.to_y == 1)
    assert(edge.dir == 'R')

    # up
    mt1.x = 1
    mt1.y = 2
    mt2.x = 2
    mt2.y = 4
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 1)
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

    # test move array when two spots are adjacent
    # left & right
    mt1.x = 0
    mt1.y = 1
    mt2.x = 2
    mt2.y = 1
    edges = r.find_moves(mt1, mt2)
    assert (len(edges) == 2)
    edge = edges[0]
    assert(edge.to_x == 0)
    assert(edge.to_y == 1)
    assert(edge.dir == 'L')
    edge = edges[1]
    assert(edge.to_x == 2)
    assert(edge.to_y == 1)
    assert(edge.dir == 'R')

    # up & down
    mt1.x = 1
    mt1.y = 2
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
    b = [[' ' for i in range(cols)] for j in range(rows)]
    r.populate_grid(b)
    print(b)

if __name__ == '__main__':
    main()