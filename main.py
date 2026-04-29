from collections import deque

maze = [["S", ".", ".","#","."],
        ["#","#",".","#","."],
        [".",".",".",".","."],
        [".","#","#","#","."],
        [".",".",".","G","."]
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
print(find_position(maze, "G"))

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
p1 = (4,4)
print(get_neighbors(p1,maze))

def bfs(maze, start, goal):
    queue = deque()
    queue.append((start, [start]))
