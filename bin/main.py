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
import sys
import argparse

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
  board_width, board_height = get_board_dimensions(initial_board_state)
  for col in range(0,board_height):
    line = ''
    for row in range(0,board_width):
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


def load_state_from_file(file_path):
  with open(file_path, 'r') as infile:
    lines = [l.rstrip() for l in infile.readlines()]
  
  output = dead_state(len(lines), len(lines[0]))
  for i,line in enumerate(lines):
    for j,val in enumerate(line):
      output[i][j] = int(val)

  return output

def main():

  parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

  parser.add_argument('--grid-size', dest='N', required=False)
  parser.add_argument('--interval', dest='interval', required=False)
  parser.add_argument('--toad', action='store_true',required=False)
  parser.add_argument('--blinker', action='store_true',required=False)
  parser.add_argument('--beacon', action='store_true',required=False)
  parser.add_argument('--glider', action='store_true',required=False)
  ## TODO: Add gosper glider gun
  # parser.add_argument('--gosper', required=False)
  args = parser.parse_args()

  N = 100
  if args.N and float(args.N) > 8:
    N = int(args.N)

  update_interval = 0.05
  if args.interval:
    update_interval = float(args.interval)

  board_state = random_state(N, N)

  if args.toad:
    board_state = load_state_from_file('./toad.txt')
  elif args.blinker:
    board_state = load_state_from_file('./blinker.txt')
  elif args.beacon:
    board_state = load_state_from_file('./beacon.txt')
  elif args.glider:
    board_state = load_state_from_file('./glider.txt')
      
  next_state = board_state
  while True:
    render(next_state)
    next_state = next_board_state(next_state)
    time.sleep(update_interval)

if __name__ == "__main__":
    
  main()