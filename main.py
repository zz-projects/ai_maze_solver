from collections import deque

maze = [["S", ".", ".","#","."],
        ["#","#",".","#","."],
        [".",".",".",".","."],
        [".","#","#","#","."],
        [".",".",".","G","."]
]

maze2 = [["S", ".", ".",".","#","."],
        ["#","#",".",".","#","."],
        [".",".",".",".",".","."],
        [".","#","#","#","#","."],
        [".",".",".","G",".","."]
]
#"S" = Start
#"G" = Goal
#"." = free space
#"#" = wall 
#print(f"This is maze:\n{maze}")

def find_position(maze, symbol):
    '''
    This function takes the maze and S/G and
    returns the position of the S/G as output.
    '''

    for x_loc,each_row_list in enumerate(maze):
        for y_loc,item in enumerate(each_row_list):
            if item == symbol:
                position = (x_loc,y_loc)
                return position
#Test:
#print(find_position(maze, "G"))

def get_neighbors(position, maze):
    '''
    This function takes the position and the maze as input
    and returns neighbors' positions that are possible to go to as output.
    It trys to stay inside the grid and avoid walls.
    '''
    x,y = position
    moves = [(-1,0),(1,0),(0,1),(0,-1)]
    neighbors = []

    for dx,dy in moves:
        nx, ny = x+dx, y+dy

        if 0<=nx<len(maze) and 0<=ny<len(maze[0]):
            if maze[nx][ny] != "#":
                neighbors.append((nx,ny))   

    return neighbors
#Test:
#p1 = (4,4)
#print(get_neighbors(p1,maze))

def bfs(maze, start, goal):
    nodes_exploered = 0
    max_queue_size = 0
    print("START")
    queue = deque()
    # storing current position and path to reach it together
    queue.append((start, [start]))
    #print("queue now is:", queue)
    visited = set()

    # continue as long as there are positions to explore
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        current, path = queue.popleft()
        nodes_exploered += 1
        #print("current is:", current)
        #print("path now is:", path)

        # goal test [not ideal as in BFS we test for goal at the time of child node creation]
        if current == goal:
            print("Goal achieved!")
            print("number of explored nodes:", nodes_exploered)
            print("max queue size = ", max_queue_size)
            return path
        
        # skipping the previosuly visited
        if current in visited:
            #print(f"state {current} was already visited so skipped")
            continue
        
        # marking the already visited
        visited.add(current)
        #print(f"{current} was added to already visited set")
        #print("visited set=", visited)

        # expanding neighbors (excluding repeated neighbors)
        for neighbor in get_neighbors(current, maze):
            # goal test at the time of creating child nodes
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                #print("neighbor of current is:", neighbor)
                #print("new queue is:", queue)
        


def bfs_optimized(maze, start, goal):
    '''
    In this optimized version of BFS, 2 other options are added:
    1) goal test is done at the time of creation of child nodes
    2) With the aim of deleting nodes with repeated states, even more, child nodes are checked
    not only with explores set but also with frontier.
    '''
    nodes_exploered = 0
    max_queue_size = 0
    print("START")
    queue = deque()
    # storing current position and path to reach it together
    queue.append((start, [start]))
    #print("queue now is:", queue)
    visited = set()
    visited.add(start)

    # continue as long as there are positions to explore
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        current, path = queue.popleft()
        nodes_exploered += 1
        #print("current is:", current)
        #print("path now is:", path)
        #print("queue is :", queue)


        # expanding neighbors (+ excluding repeated neighbors)
        for neighbor in get_neighbors(current, maze):
            # goal test at the time of creating child nodes (BFS standard)
            if neighbor == goal:
                print("Goal achieved!")
                path = path + [neighbor]
                print("number of explored nodes:", nodes_exploered)
                print("max queue size = ", max_queue_size)
                return path
            # in BFS, for prevention of repeated nodes, the new child nodes should be checked with explored and 
            # in this code, we add neighbors to visited (which includes both explored and frontier), so we are...
            # checking both in one place (they are all in one set)
            if neighbor not in visited:
                #print("neighbor not in visited")
                    queue.append((neighbor, path + [neighbor]))
                    visited.add(neighbor)
                    #print("neighbor of current is:", neighbor)


# display solution step-by-step
def copy_maze(maze):
    return [row[:] for row in maze]

def mark_path(maze, path):
    step = 0
    new_maze = copy_maze(maze)
    print("\nStep 0 --- Initial Maze:")
    print_maze(new_maze)
    for (x,y) in path:
        if (x,y) != path[0] and (x,y) != path[-1]:
            new_maze[x][y] = "*"
            step+=1
            print(f"\nStep {step}:")
            print_maze(new_maze)
    return new_maze

def print_maze(maze):
    for row in maze:
        print("  ".join(row))

#Test1:
start = find_position(maze, "S")
goal = find_position(maze, "G")
path1 = bfs(maze, start, goal)
print("old path is: ", path1)
# Test display:
marked = mark_path(maze,path1)
print("\nSolved Maze:")
print_maze(marked)
#######
path2 = bfs_optimized(maze, start, goal)
print("new path is: ", path2)
# Test display:
marked = mark_path(maze,path2)
print("\nSolved Maze:")
print_maze(marked)


#Test2:
start = find_position(maze2, "S")
goal = find_position(maze2, "G")
path1 = bfs(maze2, start, goal)
print("old path is: ", path1)
# Test display:
marked = mark_path(maze2, path1)
print("\nSolved Maze:")
print_maze(marked)
#######
path2 = bfs_optimized(maze2, start, goal)
print("new path is: ", path2)
# Test display:
marked = mark_path(maze2,path2)
print("\nSolved Maze:")
print_maze(marked)
