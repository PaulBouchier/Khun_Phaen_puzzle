#!/bin/env python

from TxTPiece import TxTPiece
from OxOPiece import OxOPiece
from TxOPiece import TxOPiece
from OxTPiece import OxTPiece
from MtSquare import MtSquare
from BoardState import BoardState
from Edge import Edge
from collections import defaultdict

MAX_LOOPS = 100000

class GraphHandler():
    def __init__(self, start_key):
        print('Starting puzzle exploration with key %s'%(start_key))

        # set up initial pieces
        self.r = TxTPiece('R', 1, 3)
        self.p = TxOPiece('P', 1, 2)
        self.y1 = OxTPiece('y1', 0, 0)
        self.y2 = OxTPiece('y2', 3, 0)
        self.y3 = OxTPiece('y3', 0, 3)
        self.y4 = OxTPiece('y4', 3, 3)
        self.b1 = OxOPiece('b1', 1, 0)
        self.b2 = OxOPiece('b2', 2, 0)
        self.b3 = OxOPiece('b3', 1, 1)
        self.b4 = OxOPiece('b4', 2, 1)

        self.mt1 = MtSquare('mt1', 0, 2)
        self.mt2 = MtSquare('mt2', 4, 2)

        self.piece_list = [self.r, self.p,
                      self.y1, self.y2, self.y3, self.y4,
                      self.b1, self.b2, self.b3, self.b4]

        self.Q0 = []
        self.Q1 = []
        self.Q2 = []
        self.Q3 = []
        self.goal_states = []
        self.explored = set()
        self.graph = defaultdict(list)

        self.Q0_count = 0
        self.Q1_count = 0
        self.Q2_count = 0
        self.Q3_count = 0

        self.vertex_serial = 0
        self.cbs = BoardState(start_key, self.vertex_serial) 
        
        # push start key onto Q
        start_key = self.cbs.swizzle_to_alias(start_key)
        self.Q3.append(start_key)   # put start state into processing Q

        # print starting position
        print('Starting position:')
        self.cbs.set_pieces_2_board_state(start_key, self.r, self.p,
                                          self.y1, self.y2, self.y3, self.y4,
                                          self.b1, self.b2, self.b3, self.b4)
        self.cbs.find_mts(self.r, self.p, self.y1, self.y2, self.y3, self.y4,
                          self.b1, self.b2, self.b3, self.b4, True)

    # discover the moves possible from the current board state
    # and populate graph with the board states and their reacheable board states
    def create_graph(self):
        # limit how long it runs
        if (self.vertex_serial == MAX_LOOPS):
            self.report_run_stats()
            return -1     # max allowed # of vertices found

        if (len(self.Q0) != 0):
            key = self.Q0.pop(0)
            self.Q0_count += 1
        elif (len(self.Q1) != 0):
            key = self.Q1.pop(0)
            self.Q1_count += 1
        elif (len(self.Q2) != 0):
            key = self.Q2.pop(0)
            self.Q2_count += 1
        elif (len(self.Q3) != 0):
            key = self.Q3.pop(0)
            self.Q3_count += 1
        else:
            print('Q is empty - all vertices processed')
            self.report_run_stats()
            return 2     # no more vertices to explore

        # print('popped key %s off Q'%(key))
        assert (key not in self.select_Q(key))
        if (key in self.explored):
            print('Key in Q already in explored')
            return 0

        self.cbs.set_pieces_2_board_state(key, self.r, self.p,
                                          self.y1, self.y2, self.y3, self.y4,
                                          self.b1, self.b2, self.b3, self.b4)
        self.check_key_against_pieces(key)
        mts = self.cbs.find_mts(self.r, self.p, self.y1, self.y2, self.y3, self.y4,
                          self.b1, self.b2, self.b3, self.b4, False)
        self.mt1.set_pos(mts[0][0], mts[0][1])
        self.mt2.set_pos(mts[1][0], mts[1][1])

        moves = []
        for piece in self.piece_list:
            piece_moves = piece.find_moves(self.mt1, self.mt2)
            moves.extend(piece_moves)
        for move in moves:
            to_bs_key = self.cbs.gen_edge_to_bs(move)
            to_bs_key = self.cbs.swizzle_to_alias(to_bs_key)
            move.to_bs = to_bs_key
            if (to_bs_key in self.select_Q(to_bs_key)):
                #print('key %s already in Q'%(to_bs_key))
                continue
            if (to_bs_key in self.explored):
                #print('key %s already in explored'%(to_bs_key))
                continue
            self.select_Q(to_bs_key).append(to_bs_key)
            # self.cbs.edges.append(move)
            if (to_bs_key not in self.graph[key]):
                self.vertex_serial += 1
                self.graph[key].append(to_bs_key)
                self.graph[to_bs_key].append(key)
                # move.print()
        # print ('found %d edges from %s'%(len(self.cbs.edges), self.cbs.key))
        self.explored.add(key)

        # if we reached a goal-state, record current state
        if (self.is_goal_state()):
            self.goal_states.append(key)
            return 1

        return 0

    # return true to stop exploration
    def is_goal_state(self):
        if (self.r.x == 1 and self.r.y == 0):
            # self.report_run_stats()
            # print('Found a goal state: r is at exit')
            return True
        return False

    # Function to find the shortest path between two nodes of a graph
    # using dictionaries in a breadth-first search
    def bfs_sp(self, start, goal):
        explored = []
        
        # Queue for traversing the 
        # graph in the BFS
        queue = [[start]]
        
        # If the desired node is 
        # reached
        if start == goal:
            print("Same Node")
            return
        
        # Loop to traverse the graph 
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            # Condition to check if the
            # current node is not visited
            if node not in explored:
                neighbours = self.graph[node]
                
                # Loop to iterate over the 
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    
                    # Condition to check if the 
                    # neighbour node is the goal
                    if neighbour == goal:
                        # print("Shortest path = ", *new_path)
                        return new_path
                explored.append(node)

        # Condition when the nodes 
        # are not connected
        print("So sorry, but a connecting"\
                    "path doesn't exist :(")
        return []

    def print_path_moves(self, path):
        print('Sequence of board states')
        for bs in path:
            print(bs)

        print('Sequence of board moves to achieve aliased equivalent of board states')
        for i in range(len(path)-1):
            self.cbs.calc_edge(path[i], path[i+1])

    def report_run_stats(self):
        explored_sorted = []
        for v in self.explored:
            explored_sorted.append(v)
        explored_sorted.sort()
        # print(explored_sorted)
        for i in range(len(explored_sorted)-1):
            assert (explored_sorted[i] != explored_sorted[i+1])
        red_positions = set()
        for v in self.graph:
            if (v[0:2] not in red_positions):
                red_positions.add(v[0:2])
        # print('red_positions: ', red_positions)
        print('Found %d vertices, explored %d, %d %d %d %d in queue 0-3, %d in graph'%(
            self.vertex_serial, len(self.explored), 
            len(self.Q0), len(self.Q1), len(self.Q2), len(self.Q3),
            len(self.graph.keys())))
        print('Processed %d %d %d %d vertices from Q0-3'%(
            self.Q0_count, self.Q1_count, self.Q2_count, self.Q3_count))
        print('Found %d goal states'%len(self.goal_states))

    def select_Q(self, key):
        Q_id = key[1:2]
        if (Q_id == '0'):
            Q = self.Q0
        elif (Q_id == '1'):
            Q = self.Q1
        elif (Q_id == '2'):
            Q = self.Q2
        elif (Q_id == '3'):
            Q = self.Q3
        else:
            print('error: invalid Q - key is %s, id is %d'%(key[1:2], id(Q)))
            assert(False)
        return Q

    def check_key_against_pieces(self, key):
        x = int(key[0:1])
        y = int(key[1:2])
        assert (self.r.x == x and self.r.y == y)
        x = int(key[2:3])
        y = int(key[3:4])
        assert (self.p.x == x and self.p.y == y)
        x = int(key[4:5])
        y = int(key[5:6])
        assert (self.y1.x == x and self.y1.y == y)
        x = int(key[6:7])
        y = int(key[7:8])
        assert (self.y2.x == x and self.y2.y == y)
        x = int(key[8:9])
        y = int(key[9:10])
        assert (self.y3.x == x and self.y3.y == y)
        x = int(key[10:11])
        y = int(key[11:12])
        assert (self.y4.x == x and self.y4.y == y)
        x = int(key[12:13])
        y = int(key[13:14])
        assert (self.b1.x == x and self.b1.y == y)
        x = int(key[14:15])
        y = int(key[15:16])
        assert (self.b2.x == x and self.b2.y == y)
        x = int(key[16:17])
        y = int(key[17:18])
        assert (self.b3.x == x and self.b3.y == y)
        x = int(key[18:19])
        y = int(key[19:20])
        assert (self.b4.x == x and self.b4.y == y)


def main():
    real_start_key =  '13120030033310201121'   # key of start state
    test1_start_key = '11200313233300103132'   # key of test start state

    ###########################
    # Select the start position
    ###########################
    start_key = real_start_key
    #start_key = test1_start_key

    gh = GraphHandler(start_key)
    rv = 0
    count = 0
    while (rv == 0 or rv == 1):
        count += 1
        rv = gh.create_graph()

    print('Stopped exploration owing to', end=' ')
    match(rv):
        case -1:
            print('hitting max vertex count')
            return
        case 2:
            print('all vertices explored')
        case _:
            print('Error: unknown condition %d'%(rv))
            return
    
    print('Found %d goal states'%(len(gh.goal_states)))
    shortest_path = 1000000
    longest_path = 0
    for goal_state in gh.goal_states:
        # Do a bfs search to find shortest path to goal states
        path = gh.bfs_sp(start_key, goal_state)
        path_length = len(path)
        if (path_length < shortest_path):
            shortest_path = path_length
            print('found shorter path, %d moves'%(shortest_path))
        if (path_length > longest_path):
            longest_path = path_length

        # print moves for the 119-move sequence
        if (path_length == 119):
            gh.print_path_moves(path)
            break

    # print()
    # print('Shortest path to goal state: %d longest: %d moves: '%(shortest_path, longest_path))

if __name__ == '__main__':
    main()