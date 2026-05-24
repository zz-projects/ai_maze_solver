from collections import deque

maze = [
["S",".",".","#","."],
["#","#",".","#","."],
[".",".",".",".","."],
[".","#","#","#","."],
[".",".",".","G","."]
]

maze2 = [
["S",".",".",".","#","."],
["#","#",".",".","#","."],
[".",".",".",".",".","."],
[".","#","#","#","#","."],
[".",".",".","G",".","."]
]

maze3 = [
["S",".",".",".","."],
[".","#","#","#","."],
[".",".",".","#","."],
[".","#",".",".","#"],
[".",".",".",".","G"]
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
    # row, col = column
    for row,each_row_list in enumerate(maze):
        for col,item in enumerate(each_row_list):
            if item == symbol:
                position = (row,col)
                return position
#Test:
#print(find_position(maze, "G"))

def get_neighbors(position, maze):
    '''
    This function takes the position and the maze as input
    and returns neighbors' positions that are possible to go to as output.
    It trys to stay inside the grid and avoid walls.
    '''
    row,col = position
    # up - right - down - left
    moves = [(-1,0),(0,1),(1,0),(0,-1)]
    neighbors = []

    # dr=d_row | dc=d_column | nr=new row | nc=new column
    for dr,dc in moves:
        nr, nc = row+dr, col+dc

        if 0<=nr<len(maze) and 0<=nc<len(maze[0]):
            if maze[nr][nc] != "#":
                neighbors.append((nr,nc))   

    return neighbors
#Test:
#p1 = (4,4)
#print(get_neighbors(p1,maze))

def reconstruct_path(parents, start, goal):
    '''
    When using parent-pointer method for path, this functuion recunstructs path using 
    parents dictionaty, goal, and start.
    '''
    step_counter = 0
    path = list()
    current = goal

    while current is not None:
        # Emergency Stop -- disable after tests
        step_counter+=1
        if step_counter> 100:
            print("Emergency Stop!")
            break
        
        path.append(current)
        current = parents[current]
        if current == start:
            path.append(current)
            break
    path.reverse()
    return path   

def bfs(maze, start, goal):
    '''
    This is primary version of BFS.
    The path is saved as a list of tuples.
    '''
    nodes_explored = 0
    max_queue_size = 0
    print("START BFS")
    queue = deque()
    # storing current position and path to reach it together
    queue.append((start, [start]))
    #print("queue now is:", queue)
    visited = set()
    
    # continue as long as there are positions to explore
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        #FIFO
        current, path = queue.popleft()
        nodes_explored += 1
        #print("current is:", current)
        #print("path now is:", path)

        # goal test [not ideal as in BFS we test for goal at the time of child node creation]
        if current == goal:
            print("Goal achieved!")
            print("number of explored nodes:", nodes_explored)
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
    * The path is saved as a list of tuples.
    '''
    nodes_explored = 0
    max_queue_size = 0
    print("START Optimized BFS")
    queue = deque()
    # storing current position and path to reach it together
    queue.append((start, [start]))
    #print("queue now is:", queue)
    visited = set()
    visited.add(start)

    # continue as long as there are positions to explore
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        #FIFO
        current, path = queue.popleft()
        nodes_explored += 1
        #print("current is:", current)
        #print("path now is:", path)
        #print("queue is :", queue)


        # expanding neighbors (+ excluding repeated neighbors)
        for neighbor in get_neighbors(current, maze):
            # goal test at the time of creating child nodes (BFS standard)
            if neighbor == goal:
                print("Goal achieved!")
                path = path + [neighbor]
                print("number of explored nodes:", nodes_explored)
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

def dfs_graph(maze, start, goal):
    '''
    This function uses graph DFS.
    The path is saved as a list of tuples.
    '''
    #step_counter = 0
    nodes_explored = 0
    max_stack_size = 0
    print("START Graph DFS")
    stack = deque()
    stack.append((start,[start]))
    visited = set()

    while stack:
        #Emergency Stop -- disable after tests
        #step_counter+=1
        #if step_counter> 100:
            #print("Emergency Stop!")
            #break

        max_stack_size = max(max_stack_size, len(stack))
        #LIFO
        current, path = stack.pop()
        if current in visited:
            continue
        nodes_explored += 1
        #print("current is:", current)
        #print("path now is:", path)
        #print("stack is :", stack)

        visited.add(current)
        # Goal test (DFS's goal test is right after choosing the node)
        if current == goal:
            print("Goal achieved!")
            print("number of explored nodes:", nodes_explored)
            print("max stack size = ", max_stack_size)
            return path        
        
        # keep preference of choosing neighbors: up - right - down - left
        for neighbor in reversed(get_neighbors(current, maze)):
            if neighbor not in visited:
                #print("neighbor is:", neighbor)
                stack.append((neighbor, path + [neighbor]))
                #print("Stack Now:", stack)


def dfs_path_based(maze, start, goal):
    '''
    This function uses path-based DFS.
    No explored set, instead new nodes are checked with active path.
    The path is saved as a list of tuples.
    '''
    #step_counter = 0
    nodes_explored = 0
    max_stack_size = 0
    print("START Path-Based DFS")
    stack = deque()
    stack.append((start,[start]))

    while stack:
        #Emergency Stop
        #step_counter+=1
        #if step_counter> 100:
            #print("Emergency Stop!")
            #break

        max_stack_size = max(max_stack_size, len(stack))
        #LIFO
        current, path = stack.pop()
        nodes_explored += 1
        #print("current is:", current)
        #print("path now is:", path)
        #print("stack is :", stack)

        # Goal test (DFS's goal test is right after choosing the node)
        if current == goal:
            print("Goal achieved!")
            print("number of explored nodes:", nodes_explored)
            print("max stack size = ", max_stack_size)
            return path        
        
        # keep preference of choosing neighbors: up - right - down - left
        for neighbor in reversed(get_neighbors(current, maze)):
            if neighbor not in path:
                #print("neighbor is:", neighbor)
                stack.append((neighbor, path + [neighbor]))
                #print("Stack Now:", stack)

def bfs_parent_pointer(maze, start, goal):
    '''
    Optimized version of bfs, but in this version instead of keeping the path as a list of tuples,
    each node points to its parent, using a dictionary.
    '''
    nodes_explored = 0
    max_queue_size = 0
    #In this dictionary if you call a child(key), it will give you the parent(value)
    parents = dict()
    print("START Parent-Pointer BFS")
    queue = deque()
    # storing current position
    queue.append(start)
    parents[start] = None
    print("queue now is:", queue)
    visited = set()
    visited.add(start)

    # continue as long as there are positions to explore
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        #FIFO 
        current = queue.popleft()
        nodes_explored += 1
        print("current is:", current)
        print("queue is :", queue)


        # expanding neighbors (+ excluding repeated neighbors)
        for neighbor in get_neighbors(current, maze):
            # goal test at the time of creating child nodes (BFS standard)
            if neighbor == goal:
                print("Goal achieved!")
                parents[neighbor] = current
                path = reconstruct_path(parents, start, goal)
                print("This is path:", path)
                print("number of explored nodes:", nodes_explored)
                print("max queue size = ", max_queue_size)
                return path
            # in BFS, for prevention of repeated nodes, the new child nodes should be checked with explored and 
            # in this code, we add neighbors to visited (which includes both explored and frontier), so we are...
            # checking both in one place (they are all in one set)
            if neighbor not in visited:
                #print("neighbor not in visited")
                    queue.append(neighbor)
                    parents[neighbor] = current
                    visited.add(neighbor)
                    #print("neighbor of current is:", neighbor)


def dfs_graph_parent_pointer(maze, start, goal):
    '''
    In this version of Graph DFS, instead of keeping the path as a list of tuples,
    each node points to its parent, using a dictionary.
    '''
    step_counter = 0
    nodes_explored = 0
    max_stack_size = 0
    print("START Parent-Pointer Graph DFS")
    stack = deque()
    parents = dict()
    stack.append(start)
    parents[start] = None
    visited = set()

    while stack:
        # Emergency Stop -- disable after tests
        #step_counter+=1
        #if step_counter> 100:
            #print("Emergency Stop!")
            #break

        max_stack_size = max(max_stack_size, len(stack))
        #LIFO
        current = stack.pop()
        if current in visited:
            continue
        nodes_explored += 1
        print("current is:", current)
        print("stack is :", stack)

        visited.add(current)
        # Goal test (DFS's goal test is right after choosing the node)
        if current == goal:
            path = reconstruct_path(parents, start, goal)
            print("Goal achieved!")
            print("The path is:", path)
            print("number of explored nodes:", nodes_explored)
            print("max stack size = ", max_stack_size)
            return path        
        
        # keep preference of choosing neighbors: up - right - down - left
        for neighbor in reversed(get_neighbors(current, maze)):
            if neighbor not in visited:
                print("neighbor is:", neighbor)
                stack.append(neighbor)
                if neighbor not in parents:    
                    parents[neighbor] = current
                print("Stack Now:", stack)

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


#Test1 - smaller maze:
start = find_position(maze, "S")
goal = find_position(maze, "G")
# BFS Test
#path1 = bfs(maze, start, goal)
#print("BFS path is: ", path1)
#marked = mark_path(maze,path1)
#print("\nSolved Maze - BFS:")
#print_maze(marked)
# Optimized BFS Test
#path2 = bfs_optimized(maze, start, goal)
#print("Optimized BFS path is: ", path2)
#marked = mark_path(maze,path2)
#print("\nSolved Maze - BFS_Optimized:")
#print_maze(marked)
# Graph DFS Test
#path3 = dfs_graph(maze, start, goal)
#print("Graph DFS path is:", path3)
#marked = mark_path(maze,path3)
#print("\nSolved Maze - Graph DFS:")
#print_maze(marked)
# Path-Based DFS Test:
#path4 = dfs_path_based(maze, start, goal)
#print("Path-Based DFS is:", path4)
#marked = mark_path(maze,path4)
#print("\nSolved Maze - Path-Based DFS:")
#print_maze(marked)
# Parent-Pointer BFS Test
#path5 = bfs_parent_pointer(maze, start, goal)
#print("Parent-Pointer BFS path is: ", path5)
#marked = mark_path(maze,path5)
#print("\nSolved Maze - Parent-Pointer BFS:")
#print_maze(marked)
# Parent-Pointer Graph DFS Test
#path6 = dfs_graph_parent_pointer(maze, start, goal)
#print("Parent-Pointer Graph DFS path is: ", path6)
#marked = mark_path(maze,path6)
#rint("\nSolved Maze - Parent-Pointer Graph DFS:")
#print_maze(marked)


#Test2 -- bigger maze:
start = find_position(maze2, "S")
goal = find_position(maze2, "G")
# BFS Test:
#path1 = bfs(maze2, start, goal)
#print("BFS path is: ", path1)
#marked = mark_path(maze2, path1)
#print("\nSolved Maze - BFS:")
#print_maze(marked)
# Optimized BFS Test
#path2 = bfs_optimized(maze2, start, goal)
#print("Optimized BFS path is: ", path2)
#marked = mark_path(maze2,path2)
#print("\nSolved Maze - Optimized BFS:")
#print_maze(marked)
# Graph DFS Test
#path3 = dfs_graph(maze2, start, goal)
#print("Graph DFS path is:", path3)
#marked = mark_path(maze2,path3)
#print("\nSolved Maze - Graph DFS:")
#print_maze(marked)
# Path-Based DFS Test:
#path4 = dfs_path_based(maze2, start, goal)
#print("Path-Based DFS is:", path4)
#marked = mark_path(maze2,path4)
#print("\nSolved Maze - Path-Based DFS:")
#print_maze(marked)
# Parent-Pointer BFS Test
#path5 = bfs_parent_pointer(maze2, start, goal)
#print("Parent-Pointer BFS path is: ", path5)
#marked = mark_path(maze2,path5)
#print("\nSolved Maze - Parent-Pointer BFS:")
#print_maze(marked)
# Parent-Pointer Graph DFS Test
#path6 = dfs_graph_parent_pointer(maze2, start, goal)
#print("Parent-Pointer Graph DFS path is: ", path6)
#marked = mark_path(maze2,path6)
#print("\nSolved Maze - Parent-Pointer Graph DFS:")
#print_maze(marked)


#Test3 -- more complex maze (with more loops):
start = find_position(maze3, "S")
goal = find_position(maze3, "G")
# BFS Test:
#path1 = bfs(maze3, start, goal)
#print("BFS path is: ", path1)
#marked = mark_path(maze3, path1)
#print("\nSolved Maze - BFS:")
#print_maze(marked)
# Optimized BFS Test
#path2 = bfs_optimized(maze3, start, goal)
#print("Optimized BFS path is: ", path2)
#marked = mark_path(maze3,path2)
#print("\nSolved Maze - Optimized BFS:")
#print_maze(marked)
# Graph DFS Test
#path3 = dfs_graph(maze3, start, goal)
#print("Graph DFS path is:", path3)
#marked = mark_path(maze3,path3)
#print("\nSolved Maze - Graph DFS:")
#print_maze(marked)
# Path-Based DFS Test:
#path4 = dfs_path_based(maze3, start, goal)
#print("Path-Based DFS is:", path4)
#marked = mark_path(maze3,path4)
#print("\nSolved Maze - Path-Based DFS:")
#print_maze(marked)
# Parent-Pointer BFS Test
#path5 = bfs_parent_pointer(maze3, start, goal)
#print("Parent-Pointer BFS path is: ", path5)
#marked = mark_path(maze3,path5)
#print("\nSolved Maze - Parent-Pointer BFS:")
#print_maze(marked)
# Parent-Pointer Graph DFS Test
path6 = dfs_graph_parent_pointer(maze3, start, goal)
print("Parent-Pointer Graph DFS path is: ", path6)
marked = mark_path(maze3,path6)
print("\nSolved Maze - Parent-Pointer Graph DFS:")
print_maze(marked)