"""
  DEAD_CELLS = 0 [x as representation]
  ALIVE_CELLS = 1 [* as representation]

  RULES of LIFE:
  Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
  Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right
  Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
  Any dead cell with exactly 3 live neighbors becomes alive, by reproduction
"""

from pprint import pprint
import math, random
import copy
import time

def dead_state(width, height):
  return [[0 for _ in range(height)] for _ in range(width)]

def get_board_dimensions(board):
  width = len(board)
  height = len(board[0])
  return width, height

def random_state(width, height):
  board_state = dead_state(width, height)

  for row in range(len(board_state)):
    for col in range(len(board_state[row])):
      random_no = random.random()
      if random_no >= 0.85:
        board_state[row][col] = 1
      else:
        board_state[row][col] = 0


  return board_state


def render(initial_board_state):
  lines = []
  char_map = {
    0 : " ",
    1 :  u"\u2588"
  }
  board_state = copy.deepcopy(initial_board_state)
  for row in range(len(board_state)):
    line = ''
    for col in range(len(board_state[row])):
      line += char_map[initial_board_state[row][col]] * 2
    lines.append(line)
    
  print("\n".join(lines))

def get_new_cell_value(row, col, initial_state):
  cell_neighbour_population = 0
  range_start = {
    row: (row - 1),
    col: (col - 1)
  }
  range_end = {
    row: (row + 1),
    col: (col + 1)
  }

  board_width, board_height = get_board_dimensions(initial_state)
  return_val = 0
  for i in range(range_start[row], range_end[row] + 1):
    if i < 0 or i >= board_width:
      continue
    for j in range(range_start[col], range_end[col] + 1):
      if j < 0 or j >= board_height:
        continue
      if i == row and j == col:
        continue

      if initial_state[i][j] == 1:
        cell_neighbour_population += 1

  if initial_state[row][col] == 1:
    if cell_neighbour_population <= 1:
      return_val = 0
    elif cell_neighbour_population <= 3:
      return_val = 1
    else:
      return_val = 0
  else:
    if cell_neighbour_population == 3:
      return_val = 1
    else:
      return_val = 0

  return return_val


def next_board_state(initial_board_state):
  board_width, board_height = get_board_dimensions(initial_board_state)
  new_state = dead_state(board_width, board_height)
  for row in range(0,board_width):
    for col in range(0,board_height):
      new_val = get_new_cell_value(row, col, initial_board_state)
      new_state[row][col] = new_val
  return new_state


def main():
  board_state = random_state(20, 20)
  next_state = board_state
  i = 0
  while True:
    render(next_state)
    next_state = next_board_state(next_state)
    time.sleep(0.03)
    i+=1

if __name__ == "__main__":
  main()