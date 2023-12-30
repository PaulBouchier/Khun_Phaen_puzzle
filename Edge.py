#!/bin/env python

class Edge():
    def __init__(self, piece, from_x, from_y, dir, to_x, to_y):
        self.piece_name = piece
        self.from_x = from_x
        self.from_y = from_y
        self.dir = dir      # L, R, U, D direction to get to to_bs
        self.to_x = to_x
        self.to_y = to_y
        self.to_bs = ''  # board_state this edge leads to

    def print(self):
        print('edge from %s at %d %d in direction %s to %d %d next bs: %s'%(self.piece_name,
                self.from_x, self.from_y, self.dir, self.to_x, self.to_y, self.to_bs))

def main():
    edge = Edge('b1', 1, 1, 'U', 1, 2)
    edge.print()
    print('made edge from %s at %d %d in direction %s to %d %d'%(edge.piece_name,
                edge.from_x, edge.from_y, edge.dir, edge.to_x, edge.to_y))

if __name__ == '__main__':
    main()