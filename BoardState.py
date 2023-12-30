#!/bin/env python

from TxTPiece import TxTPiece
from OxOPiece import OxOPiece
from TxOPiece import TxOPiece
from OxTPiece import OxTPiece
from MtSquare import MtSquare
from Edge import Edge


class BoardState():
    def __init__(self, key, vertex_serial):
        self.key = key
        self.vertex_serial = vertex_serial
        self.edges = []

    def set_pieces_2_board_state(self, key, r, p, y1, y2, y3, y4, b1, b2, b3, b4):
        self.key = key
        x = int(key[0:1])
        y = int(key[1:2])
        r.set_pos(x, y)
        x = int(key[2:3])
        y = int(key[3:4])
        p.set_pos(x, y)
        x = int(key[4:5])
        y = int(key[5:6])
        y1.set_pos(x, y)
        x = int(key[6:7])
        y = int(key[7:8])
        y2.set_pos(x, y)
        x = int(key[8:9])
        y = int(key[9:10])
        y3.set_pos(x, y)
        x = int(key[10:11])
        y = int(key[11:12])
        y4.set_pos(x, y)
        x = int(key[12:13])
        y = int(key[13:14])
        b1.set_pos(x, y)
        x = int(key[14:15])
        y = int(key[15:16])
        b2.set_pos(x, y)
        x = int(key[16:17])
        y = int(key[17:18])
        b3.set_pos(x, y)
        x = int(key[18:19])
        y = int(key[19:20])
        b4.set_pos(x, y)

    def generate_key(self, r, p, y1, y2, y3, y4, b1, b2, b3, b4):
        key = str(r.x) + str(r.y) \
            + str(p.x) + str(p.y) \
            + str(y1.x) + str(y1.y) \
            + str(y2.x) + str(y2.y) \
            + str(y3.x) + str(y3.y) \
            + str(y4.x) + str(y4.y) \
            + str(b1.x) + str(b1.y) \
            + str(b2.x) + str(b2.y) \
            + str(b3.x) + str(b3.y) \
            + str(b4.x) + str(b4.y)
        # print ('generated key %s'%(key))
        return key

    # find empty spots
    def find_mts(self, r, p, y1, y2, y3, y4, b1, b2, b3, b4, print_flag=False):
        cols, rows = (4, 5)
        board_grid = [[' ' for i in range(cols)] for j in range(rows)]
        r.populate_grid(board_grid)
        p.populate_grid(board_grid)
        y1.populate_grid(board_grid)
        y2.populate_grid(board_grid)
        y3.populate_grid(board_grid)
        y4.populate_grid(board_grid)
        b1.populate_grid(board_grid)
        b2.populate_grid(board_grid)
        b3.populate_grid(board_grid)
        b4.populate_grid(board_grid)

        mt_count = 0
        mt_array = []
        for i in range(cols):
            for j in range(rows):
                if (board_grid[j][i] == ' '):
                    mt_count += 1
                    mt_array.append((i,j))
        assert (mt_count == 2)

        if (print_flag):
            print('Current board state for vertex %d'%(self.vertex_serial))
            self.print_board(board_grid)
            print('mt_array: ', mt_array)

        return mt_array

    # Generate to_bs boardState key for a given edge from the current boardstate
    # @return resulting bs key
    def gen_edge_to_bs(self, edge):
        new_key = self.key
        # print('edge bs %s'%(self.key))
        match edge.piece_name:
            case 'R':
                new_key = str(edge.to_x) + str(edge.to_y) + new_key[2:]
            case 'P':
                new_key = self.key[0:2] + str(edge.to_x) + str(edge.to_y) \
                    + self.key[4:]
            case 'y1':
                new_key = self.key[0:4] + str(edge.to_x) + str(edge.to_y) \
                    + self.key[6:]
            case 'y2':
                new_key = self.key[0:6] + str(edge.to_x) + str(edge.to_y) \
                    + self.key[8:]
            case 'y3':
                new_key = self.key[0:8] + str(edge.to_x) + str(edge.to_y) \
                    + self.key[10:]
            case 'y4':
                new_key = self.key[0:10] + str(edge.to_x) + str(edge.to_y) \
                    + self.key[12:]
            case 'b1':
                new_key = self.key[0:12] + str(edge.to_x) + str(edge.to_y) \
                    + self.key[14:]
            case 'b2':
                new_key = self.key[0:14] + str(edge.to_x) + str(edge.to_y) \
                    + self.key[16:]
            case 'b3':
                new_key = self.key[0:16] + str(edge.to_x) + str(edge.to_y) \
                    + self.key[18:]
            case 'b4':
                new_key = self.key[0:18] + str(edge.to_x) + str(edge.to_y)
            case _:
                print('Unhandled edge')
                assert(False)
        # print('lead to %s'%(new_key))
        return new_key

    # Swap y1-y4, b1-b4 to place each at a lower x, lower y than the next
    def swizzle_to_alias(self, key):
        y_key = self.swizzle4pieces(key[4:12])
        b_key = self.swizzle4pieces(key[12:20])
        rv = key[0:4] + y_key + b_key
        return rv

    def swizzle4pieces(self, partial_key):
        assert(len(partial_key) == 8)
        piece_array = []
        piece_array.append((int(partial_key[0:1]), int(partial_key[1:2])))
        piece_array.append((int(partial_key[2:3]), int(partial_key[3:4])))
        piece_array.append((int(partial_key[4:5]), int(partial_key[5:6])))
        piece_array.append((int(partial_key[6:7]), int(partial_key[7:8])))
        self.bubbleSort(piece_array)
        swizzled_key = str(piece_array[0][0]) + str(piece_array[0][1]) \
                     + str(piece_array[1][0]) + str(piece_array[1][1]) \
                     + str(piece_array[2][0]) + str(piece_array[2][1]) \
                     + str(piece_array[3][0]) + str(piece_array[3][1])
        return swizzled_key
        
    # sort an array of piece coordinates
    def bubbleSort(self, arr):
        n = len(arr)
        # optimize code, so if the array is already sorted, it doesn't need
        # to go through the entire process
        swapped = False
        # Traverse through all array elements
        for i in range(n-1):
            # range(n) also work but outer loop will
            # repeat one time more than needed.
            # Last i elements are already in place
            for j in range(0, n-i-1):

                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if self.is_lower_left(arr[j+1], arr[j]):
                    swapped = True
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            
            if not swapped:
                # if we haven't needed to make a single swap, we 
                # can just exit the main loop.
                return


    # test if piece1 is lower-left of piece2
    def  is_lower_left(self, piece1, piece2):
        if (piece1[1] < piece2[1]):     # Y is lower for piece1
            return True
        elif (piece1[1] > piece2[1]):   # Y is higher for piece1
            return False
        elif (piece1[0] < piece2[0]):   # Y is the same, X for piece 1 is lower
            return True
        else:                           # Y is the same, X for piece 2 is lower
            return False

    # calculate which piece to move given an input and resulting board state
    def calc_edge(self, from_bs, to_bs):

        if (from_bs[0:2] != to_bs[0:2]):
            move_piece = 'R'
            from_xy = from_bs[0:2]
            to_xy = to_bs[0:2]
            assert(from_bs[2:20] == to_bs[2:20])
        elif (from_bs[2:4] != to_bs[2:4]):
            move_piece = 'P'
            from_xy = from_bs[2:4]
            to_xy = to_bs[2:4]
            assert(from_bs[0:2] == to_bs[0:2] and from_bs[4:20] == to_bs[4:20])
        elif (from_bs[4:12] != to_bs[4:12]):
            move_piece = 'Y'
            from_xy, to_xy = self.calc_swizzled_edge(from_bs[4:12], to_bs[4:12])
            assert(from_bs[0:4] == to_bs[0:4] and from_bs[12:20] == to_bs[12:20])
        elif (from_bs[12:20] != to_bs[12:20]):
            move_piece = 'B'
            from_xy, to_xy = self.calc_swizzled_edge(from_bs[12:20], to_bs[12:20])
            assert(from_bs[0:12] == to_bs[0:12])

        self.print_move(move_piece, from_xy, to_xy)

    # find the one-piece move that gets from from_bs to to_bs, allowing for
    # aliasing causing multiple "apparent" moves.
    # Three of the blocks have to be in the same position, so find the one
    # that isn't, and its corresponding to_position
    def calc_swizzled_edge(self, from_bs, to_bs):
        from_positions = [from_bs[0:2], from_bs[2:4], from_bs[4:6], from_bs[6:8]]
        to_positions = [to_bs[0:2], to_bs[2:4], to_bs[4:6], to_bs[6:8]]
        matched_to_positions = []
        from_xy = ''
        to_xy = ''
        for fp in from_positions:
            if (fp in to_positions):
                matched_to_positions.append(fp)
            else:
                from_xy = fp
        for tp in to_positions:
            if (tp not in matched_to_positions):
                to_xy = tp
                break
        return from_xy, to_xy

    def print_move(self, move_piece, from_xy, to_xy):
        print('%s from (%s, %s) to (%s, %s)'%(move_piece,
                        from_xy[0], from_xy[1], to_xy[0], to_xy[1]))
        

    # check that an edge only has one transition
    def check_edge(self, from_bs, to_bs):

        if (from_bs[0:2] != to_bs[0:2]):
            assert(from_bs[2:20] == to_bs[2:20])
        elif (from_bs[2:4] != to_bs[2:4]):
            assert(from_bs[0:2] == to_bs[0:2] and from_bs[4:20] == to_bs[4:20])
        elif (from_bs[4:6] != to_bs[4:6]):
            assert(from_bs[0:4] == to_bs[0:4] and from_bs[6:20] == to_bs[6:20])
        elif (from_bs[6:8] != to_bs[6:8]):
            assert(from_bs[0:6] == to_bs[0:6] and from_bs[8:20] == to_bs[8:20])
        elif (from_bs[8:10] != to_bs[8:10]):
            assert(from_bs[0:8] == to_bs[0:8] and from_bs[10:20] == to_bs[10:20])
        elif (from_bs[10:12] != to_bs[10:12]):
            assert(from_bs[0:10] == to_bs[0:10] and from_bs[12:20] == to_bs[12:20])
        elif (from_bs[12:14] != to_bs[12:14]):
            assert(from_bs[0:12] == to_bs[0:12] and from_bs[14:20] == to_bs[14:20])
        elif (from_bs[14:16] != to_bs[14:16]):
            assert(from_bs[0:14] == to_bs[0:14] and from_bs[16:20] == to_bs[16:20])
        elif (from_bs[16:18] != to_bs[16:18]):
            assert(from_bs[0:16] == to_bs[0:16] and from_bs[18:20] == to_bs[18:20])
        elif (from_bs[18:20] != to_bs[18:20]):
            assert(from_bs[0:18] == to_bs[0:18])

    # Print board, input is a board_grid
    def print_board(self, bg):
        print(bg[4])
        print(bg[3])
        print(bg[2])
        print(bg[1])
        print(bg[0])

def main():
    print("testing BoardState")
    # set up initial pieces
    r = TxTPiece('R', 1, 3)
    p = TxOPiece('P', 1, 2)
    y1 = OxTPiece('y1', 0, 0)
    y2 = OxTPiece('y2', 3, 0)
    y3 = OxTPiece('y3', 0, 3)
    y4 = OxTPiece('y4', 3, 3)
    b1 = OxOPiece('b1', 1, 0)
    b2 = OxOPiece('b2', 2, 0)
    b3 = OxOPiece('b3', 1, 1)
    b4 = OxOPiece('b4', 2, 1)
    
    start_key = '13120030033310201121'   # key of start state
    vertex_serial = 99

    bs = BoardState(start_key, vertex_serial)

    print ('key: %s'%(bs.key))
    assert(bs.key == '13120030033310201121')

    # print board & find empty spots
    cols, rows = (4, 5)
    b = [[' ' for i in range(cols)] for j in range(rows)]
    r.populate_grid(b)
    p.populate_grid(b)
    y1.populate_grid(b)
    y2.populate_grid(b)
    y3.populate_grid(b)
    y4.populate_grid(b)
    b1.populate_grid(b)
    b2.populate_grid(b)
    b3.populate_grid(b)
    b4.populate_grid(b)

    bs.print_board(b)
    mt_array = bs.find_mts(r, p, y1, y2, y3, y4, b1, b2, b3, b4)
    print(mt_array)

    # test new key generation given edge
    edge = Edge('P', 1, 2, 'L', 0, 2)
    new_key = bs.gen_edge_to_bs(edge)
    print(new_key)
    assert (new_key == '13020030033310201121')

    # move p left & re-print board & empty spots
    p.set_pos(0, 2)
    mt_array = bs.find_mts(r, p, y1, y2, y3, y4, b1, b2, b3, b4, True)
    key = bs.generate_key(r, p, y1, y2, y3, y4, b1, b2, b3, b4)
    assert (key == '13020030033310201121')

    bs.set_pieces_2_board_state(key, r, p, y1, y2, y3, y4, b1, b2, b3, b4)
    x, y = r.get_pos()
    assert (x==1 and y==3)

    # Driver code to test swizzle logic
    p1 = (1, 1)
    p2 = (2, 1)
    p3 = (1, 2)
    p4 = (4, 2)
    p1_p4_key = '11211242'

    assert(bs.is_lower_left(p1, p2))
    assert(bs.is_lower_left(p1, p3))
    assert(bs.is_lower_left(p2, p1) == False)
    assert(bs.is_lower_left(p3, p1) == False)

    # test sort algorithm
    arr = [p4, p1, p3, p2]
    bs.bubbleSort(arr)
    print("Sorted array is:")
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()

    arr = [p3, p4, p2, p1]
    bs.bubbleSort(arr)
    print("Sorted array is:")
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()

    # test swizzle4pieces
    result_key = bs.swizzle4pieces('42211112')
    assert (result_key == p1_p4_key)
    result_key = bs.swizzle4pieces('12211142')
    assert (result_key == p1_p4_key)

    # test swizzle_to_alias
    input_key =  '13123000033320111021'
    result_key = '13120030033310201121'
    rv = bs.swizzle_to_alias(input_key)
    assert (rv == result_key)

    input_key =  '13120030033310201121'
    result_key = '13120030033310201121'
    rv = bs.swizzle_to_alias(input_key)
    assert (rv == result_key)

    # test calc_swizzled_edge
    from_bs = '10301121'
    to_bs =   '10203011'
    from_xy, to_xy = bs.calc_swizzled_edge(from_bs, to_bs)
    assert(from_xy == '21' and to_xy == '20')

    from_bs = '21301110'
    to_bs =   '10203011'
    from_xy, to_xy = bs.calc_swizzled_edge(from_bs, to_bs)
    assert(from_xy == '21' and to_xy == '20')

    # test calc_edge
    from_bs = '13020031033310301121'
    to_bs =   '13020031033310203011'
    from_xy, to_xy = bs.calc_edge(from_bs, to_bs)

if __name__ == '__main__':
    main()