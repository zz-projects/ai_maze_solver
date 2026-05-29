from collections import deque
import heapq

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

# Maze with different move cost
maze4 = [
["S","M","~","#","."],
["#","#",".","#","."],
[".",".",".","M","M"],
[".","#","#","#","M"],
[".",".",".","G","~"]
]
# different move costs:
# "." = 1
# "~" = 3
# "M" = 7




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

def get_neighbors(position, maze):
    '''
    This function takes the position and the maze as input
    and returns neighbors' positions that are possible to go to as output.
    It tries to stay inside the grid and avoid walls.
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
    When using parent-pointer method for path, this functuion reconstructs path using 
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

def terrain_cost(symbol):
    costs = {".":1, "~":3, "M":7, "S":1, "G":1}
    return costs[symbol]

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
        
        # skipping the previously visited
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

def ucs_similar_cost(maze, start, goal):
    '''
    This functions uses a simple version of UCS algorithm for educational purposes.
    For now, every move costs 1.
    '''
    print("START UCS")
    step_counter = 0
    nodes_explored = 0
    max_frontier_size = 0
    total_cost = 0
    frontier = list()
    # Storing current position, total cost, and path.
    heapq.heappush(frontier, (total_cost, start, [start]))
    visited = set()


    # As long as frontier is not empty:
    while frontier:
        # Emergency Stop -- disable after tests
        step_counter+=1
        if step_counter> 100:
            print("Emergency Stop!")
            break

        max_frontier_size = max(max_frontier_size, len(frontier))
        # Least cost first
        total_cost, current, path = heapq.heappop(frontier)
        print("Total cost is:", total_cost, "And current is:", current)
        # As long as all moves' cost is positive this is okay, as each when each node is popped, ...
        # the cheapest way to it has been found
        if current in visited:
            continue
        nodes_explored+=1
        print("current is:", current)
        print("path now is:", path)
        print("frontier is :", frontier)

        visited.add(current)
        # Goal test in UCS is after selecting a node
        if current == goal:
            print("Goal achieved!")
            print("number of explored nodes:", nodes_explored)
            print("max frontier size = ", max_frontier_size)
            return path   
        
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                print("Neighbor is:", neighbor)
                heapq.heappush(frontier, (total_cost+1, neighbor, path+[neighbor]))

def ucs(maze, start, goal):
    '''
    This functions uses a standard version of UCS algorithm used for non-negative edge costs.
    In this version, moves have different cost:
    "." = 1
    "~" = 3
    "M" = 7
    '''
    print("START UCS")
    step_counter = 0
    nodes_explored = 0
    max_frontier_size = 0
    total_cost = 0
    frontier = list()
    # Storing current position, total cost, and path.
    heapq.heappush(frontier, (total_cost, start, [start]))
    visited = set()


    # As long as frontier is not empty:
    while frontier:
        # Emergency Stop -- disable after tests
        step_counter+=1
        if step_counter> 100:
            print("Emergency Stop!")
            break

        max_frontier_size = max(max_frontier_size, len(frontier))
        # Least cost first
        total_cost, current, path = heapq.heappop(frontier)
        current_node_cost = total_cost
        print("Total cost is:", total_cost, "And current is:", current)
        # With non-negative edge costs, the first valid pop of a node guarantees ...
        # the cheapest path to it has been found
        if current in visited:
            continue
        nodes_explored+=1
        print("current is:", current)
        print("path now is:", path)
        print("frontier is :", frontier)

        visited.add(current)
        # Goal test in UCS is after selecting a node
        if current == goal:
            print("Goal achieved!")
            print("number of explored nodes:", nodes_explored)
            print("max frontier size = ", max_frontier_size)
            return path   
        
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                print("Neighbor is:", neighbor)
                row, col = neighbor
                symbol = maze[row][col]
                move_cost = terrain_cost(symbol)
                new_node_cost = current_node_cost + move_cost
                print("Current node cost:", current_node_cost)
                print("Move Cost:", move_cost)
                print("New node cost:", new_node_cost)
                heapq.heappush(frontier, (new_node_cost, neighbor, path+[neighbor]))
                print("frontier is :", frontier)

def ucs_parent_pointer(maze, start, goal):
    '''
    This functions uses a standard version of UCS algorithm used for non-negative edge costs.
    In this version, moves have different cost:
    "." = 1
    "~" = 3
    "M" = 7
    in this version instead of keeping the path as a list of tuples,
    each node points to its parent, using a dictionary.
    '''
    print("START Parent-Pointer UCS")
    step_counter = 0
    nodes_explored = 0
    max_frontier_size = 0
    total_cost = 0
    frontier = list()
    parents = dict()
    # Storing current position, total cost, and parent.
    # In parent pointer version of UCS, parent should travel with the active node, otherwise...
    # finding the correct parent later will not be possible.
    heapq.heappush(frontier, (total_cost, start, None))
    parents[start] = None
    visited = set()

    # As long as frontier is not empty:
    while frontier:
        # Emergency Stop -- disable after tests
        step_counter+=1
        if step_counter> 100:
            print("Emergency Stop!")
            break

        max_frontier_size = max(max_frontier_size, len(frontier))
        # Least cost first
        total_cost, current, parent= heapq.heappop(frontier)
        current_node_cost = total_cost
        print("Total cost is:", total_cost, "And current is:", current, "And parent is:", parent)
        # With non-negative edge costs, the first valid pop of a node guarantees ...
        # the cheapest path to it has been found
        if current in visited:
            continue
        # Assigning parent after popping to make sure that it is the best path to that node
        parents[current] = parent
        nodes_explored+=1
        print("current is:", current)
        print("frontier is :", frontier)

        visited.add(current)
        # Goal test in UCS is after selecting a node
        if current == goal:
            path = reconstruct_path(parents, start, goal)
            print("Goal achieved!")
            print("number of explored nodes:", nodes_explored)
            print("max frontier size = ", max_frontier_size)
            return path   
        
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                print("Neighbor is:", neighbor)
                row, col = neighbor
                symbol = maze[row][col]
                move_cost = terrain_cost(symbol)
                new_node_cost = current_node_cost + move_cost
                print("Current node cost:", current_node_cost)
                print("Move Cost:", move_cost)
                print("New node cost:", new_node_cost)
                heapq.heappush(frontier, (new_node_cost, neighbor, current))
                print("frontier is :", frontier)

def dijkstra(maze, start, goal):
    '''
    This functions uses a dijkstra algorithm used for non-negative edge costs.
    In this version, moves have different cost:
    "." = 1
    "~" = 3
    "M" = 7
    in this version instead of keeping the path as a list of tuples,
    each node points to its parent, using a dictionary.
    In this algorithm, the best cost is saved for more efficient parent keeping.
    '''
    print("START Dijkstra")
    step_counter = 0
    nodes_explored = 0
    max_frontier_size = 0
    current_cost = 0
    frontier = list()
    parents = dict()
    # Storing current position, total cost, and parent.
    # In parent pointer version of UCS, parent should travel with the active node, otherwise...
    # finding the correct parent later will not be possible.
    heapq.heappush(frontier, (current_cost, start, None))
    parents[start] = None
    # Stores the cheapest discovered cost to each node so far.
    best_cost = dict()
    best_cost[start] = 0

    # As long as frontier is not empty:
    while frontier:
        # Emergency Stop -- disable after tests
        step_counter+=1
        if step_counter> 100:
            print("Emergency Stop!")
            break

        max_frontier_size = max(max_frontier_size, len(frontier))
        # Least cost first
        current_cost, current, parent= heapq.heappop(frontier)
        print("Total cost is:", current_cost, "And current is:", current, "And parent is:", parent)
        # With non-negative edge costs, the first valid pop of a node guarantees ...
        # the cheapest path to it has been found
        # frontier entery with worse cost than the best cost so far is ignored
        if current_cost > best_cost[current]:
            continue
        # Assigning parent after popping to make sure that it is the best path
        parents[current] = parent
        nodes_explored+=1
        print("current is:", current)
        print("frontier is :", frontier)

        # In Dijkstra, goal test is done after node selection
        if current == goal:
            path = reconstruct_path(parents, start, goal)
            print("Goal achieved!")
            print("number of explored nodes:", nodes_explored)
            print("max frontier size = ", max_frontier_size)
            return path   
        
        for neighbor in get_neighbors(current, maze):
            print("Neighbor is:", neighbor)
            row, col = neighbor
            symbol = maze[row][col]
            move_cost = terrain_cost(symbol)
            new_node_cost = current_cost + move_cost
            # Check if you have found a cheaper path to the state
            old_cost = best_cost.get(neighbor, float("inf"))
            if new_node_cost < old_cost:
                # Relaxing an edge
                best_cost[neighbor] = new_node_cost
                heapq.heappush(frontier, (new_node_cost, neighbor, current))
                print("frontier is :", frontier)

def dldfs(maze, start, goal, max_depth):
    '''
    Depth-Limited DFS is a variation of DFS that limit how deep the search can go.
    It helps prevent excessive exploration in very deep or infinite seach spaces.
    If the depth limit is too small, it may fail to find a solution even if one exists. 
    If the depth limit is too large, it behaves like normal DFS and may spend a long time 
    exploring deep non-optimal branches.   
    
    This function uses path-based DFS.
    No explored set is used, instead new nodes are checked with active path.
    The path is stored as a list of tuples.
    '''
    #step_counter = 0
    nodes_explored = 0
    max_stack_size = 0
    depth = 0
    print("START Path-Based DLDFS (Depth-Limited DFS)")
    stack = deque()
    stack.append((start,[start], depth))

    while stack:
        #Emergency Stop
        #step_counter+=1
        #if step_counter> 100:
            #print("Emergency Stop!")
            #break

        max_stack_size = max(max_stack_size, len(stack))
        #LIFO
        current, path, depth = stack.pop()
        nodes_explored += 1
        #print("current is:", current)
        #print("path now is:", path)
        #print("stack is :", stack)

        # Goal test (DLDFS's goal test is right after choosing the node)
        if current == goal:
            print("Goal achieved!")
            print("number of explored nodes:", nodes_explored)
            print("max stack size = ", max_stack_size)
            return path        
        
        # keep preference of choosing neighbors: up - right - down - left
        for neighbor in reversed(get_neighbors(current, maze)):
            if neighbor not in path:
                #print("neighbor is:", neighbor)
                if depth<max_depth:
                    stack.append((neighbor, path + [neighbor], depth+1))
                    print("Stack Now:", stack)

# display solution step-by-step
def copy_maze(maze):
    return [row[:] for row in maze]

def mark_path(maze, path):
    step = 0
    new_maze = copy_maze(maze)

    if path == None:
        print("Goal Not Found!")
    else:
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
#print("\nSolved Maze - Parent-Pointer Graph DFS:")
#print_maze(marked)
# UCS with similat move cost Test
#path7 = ucs(maze, start, goal)
#print("UCS path is: ", path7)
#marked = mark_path(maze,path7)
#print("\nSolved Maze - UCS:")
#print_maze(marked)
# DLDFS (Depth- Limited DFS) Test
#path8 = dldfs(maze, start, goal, max_depth = 9)
#print("DLDFS (Depth- Limited DFS) path is: ", path8)
#marked = mark_path(maze,path8)
#print("\nSolved Maze - DLDFS (Depth- Limited DFS) :")
#print_maze(marked)


#Test2 -- bigger maze:
#start = find_position(maze2, "S")
#goal = find_position(maze2, "G")
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
# UCS with similat move cost Test
#path7 = ucs_similar_cost(maze2, start, goal)
#print("UCS (similar move cost) path is: ", path7)
#marked = mark_path(maze2,path7)
#print("\nSolved Maze - UCS (similar move cost):")
#print_maze(marked)
# DLDFS (Depth- Limited DFS) Test
#path8 = dldfs(maze2, start, goal, max_depth = 11)
#print("DLDFS (Depth- Limited DFS) path is: ", path8)
#marked = mark_path(maze2,path8)
#print("\nSolved Maze - DLDFS (Depth- Limited DFS) :")
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
#path6 = dfs_graph_parent_pointer(maze3, start, goal)
#print("Parent-Pointer Graph DFS path is: ", path6)
#marked = mark_path(maze3,path6)
#print("\nSolved Maze - Parent-Pointer Graph DFS:")
#print_maze(marked)
# UCS with similat move cost Test
#path7 = ucs_similar_cost(maze3, start, goal)
#print("UCS (similar move cost) path is: ", path7)
#marked = mark_path(maze3,path7)
#print("\nSolved Maze - UCS (similar move cost):")
#print_maze(marked)
# DLDFS (Depth- Limited DFS) Test
path8 = dldfs(maze3, start, goal, max_depth = 7)
print("DLDFS (Depth- Limited DFS) path is: ", path8)
marked = mark_path(maze3,path8)
if path8 != None:
    print("\nSolved Maze - DLDFS (Depth- Limited DFS) :")
    print_maze(marked)

#Test 4 - Maze with different move cost
start = find_position(maze4, "S")
goal = find_position(maze4, "G")
# UCS (non-negative move cost) Test
#path8 = ucs(maze4, start, goal)
#print("UCS (different move cost) path is: ", path8)
#marked = mark_path(maze4,path8)
#print("\nSolved Maze - UCS(different move cost):")
#print_maze(marked)
# UCS Parent-Pointer Test
#path9 = ucs_parent_pointer(maze4, start, goal)
#print("UCS (different move cost)-Parent-Pointer path is: ", path9)
#marked = mark_path(maze4,path9)
#print("\nSolved Maze - UCS(different move cost)-Parent-Pointer:")
#print_maze(marked)
# Dijkstra Test:
#path10 = dijkstra(maze4, start, goal)
#print("Dijkstra path is: ", path10)
#marked = mark_path(maze4,path10)
#print("\nSolved Maze - Dijkstra:")
#print_maze(marked)
