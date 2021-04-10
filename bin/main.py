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
  return [ [0] * width ] * height


def random_state(width, height):
  board_state = dead_state(width, height)

  for row in range(len(board_state)):
    for col in range(len(board_state[row])):
      random_no = random.random()
      if random_no >= 0.85:
        board_state[row][col] = 1
      else:
        board_state[row][col] = 0

  # board_state = [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1], [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]
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


def next_board_state(initial_board_state):
  board_state = copy.deepcopy(initial_board_state)
  for row in range(len(board_state)):
    for col in range(len(board_state[row])):
      cell_neighbour_population = 0
      neighbours = [0] * 8
      if row != 0:
        if col != 0:
          neighbours[0] = initial_board_state[row - 1][col - 1]
          cell_neighbour_population += initial_board_state[row - 1][col - 1]
        
        neighbours[1] = initial_board_state[row - 1][col]
        cell_neighbour_population += initial_board_state[row - 1][col]

        if col != len(board_state[row])-1:
          neighbours[2] = initial_board_state[row - 1][col + 1]
          cell_neighbour_population += initial_board_state[row - 1][col + 1]
      
      if col != 0:
        neighbours[3] = initial_board_state[row][col - 1]
        cell_neighbour_population += initial_board_state[row][col - 1]

      if col != len(board_state[row])-1:
        neighbours[4] = initial_board_state[row][col + 1]
        cell_neighbour_population += initial_board_state[row][col - 1]

      if row != len(board_state)-1:
        neighbours[5] = initial_board_state[row + 1][col - 1]
        cell_neighbour_population += initial_board_state[row + 1][col - 1]
        
        neighbours[6] = initial_board_state[row + 1][col]
        cell_neighbour_population += initial_board_state[row + 1][col]


        if col != len(board_state[row])-1:
          neighbours[7] = initial_board_state[row + 1][col + 1]
          cell_neighbour_population += initial_board_state[row + 1][col + 1]

      cell_population = sum(neighbours)

      # print(row, col, board_state[row][col], cell_neighbour_population)
      if board_state[row][col] == 1:
        if cell_population <= 1 or cell_population > 3:
          board_state[row][col] = 0
      elif board_state[row][col] == 0 and cell_population == 3:
          board_state[row][col] = 1

  return board_state


def main():
  board_state = random_state(5, 5)
  next_state = board_state
  i = 0
  while True:
    render(next_state)
    # print(next_state)
    next_state = next_board_state(next_state)
    time.sleep(0.03)
    i+=1

if __name__ == "__main__":
  main()