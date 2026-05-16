# ai_maze_solver
Maze solver in Python using BFS pathfinding algorithm


This is a program that takes a maze, a start point, and a goal point as input.
Finds a path from start to goal.
Uses search algorithms
Outputs the solution clearly

------------------
Goal formulation: getting to the goal point position (goal state)

Problem formulation:
- What is state: the current position in maze (row, col)
- What is initial state: The start point's position (row, col)
- What are actions: up, down, right, left
--- What is action function?
- What is result function?
- What is goal test function? current state == goal state
- What is path cost? steps
- What is path? Sequence of steps

Search: Which algorithm to use?
BFS
DFS