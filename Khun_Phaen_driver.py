#!/bin/env python

from GraphHandler import GraphHandler


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