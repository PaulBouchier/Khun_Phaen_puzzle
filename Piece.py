#!/bin/env python3

from Edge import Edge

MAX_X = 3
MAX_Y = 4

class Piece:
    def __init__(self, piece_name, piece_type, start_x, start_y):
        self.name = piece_name
        self.type = piece_type
        self.x = start_x
        self.y = start_y
        # print('Initialized %s as %s at %d, %d'%(self.name, self.type, self.x, self.y))

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def make_edge(self, to_x, to_y, dir):
        edge = Edge(self.name, self.x, self.y, dir, to_x, to_y)
        return edge

def main():
    print("Initializing pieces")
    global r
    r = Piece('R', 'TxT', 1, 3)

    # test get_pos
    x, y = r.get_pos()
    assert(x==1 and y==3)

    # test set_pos
    r.set_pos(0, 2)
    x, y = r.get_pos()
    assert(x==0 and y==2)

    # test make_edge
    edge = r.make_edge(0, 3, 'U')
    edge.print()

if __name__ == '__main__':
    main()