#!/bin/env python3

from Piece import Piece

class MtSquare(Piece):
    def __init__(self, piece_name, start_x, start_y): 
        super().__init__(piece_name, 'Mt', start_x, start_y)
    
def main():
    print("Initializing pieces")
    mt1 = MtSquare('mt1', 0, 2)

    x, y = mt1.get_pos()
    assert(x==0 and y==2)
    print('r is at %d %d' % (x, y))

if __name__ == '__main__':
    main()