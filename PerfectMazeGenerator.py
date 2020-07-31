import random
import numpy as np
from PIL import Image
import argparse


class Cell:
    def __init__(self):
        self.right_wall = True
        self.bottom_wall = True
        self.set_id = -1
        self.row_index = -1
        self.col_index = -1



class Maze:
    def __init__(self, row_count, col_count):
        self.row_count = row_count
        self.col_count = col_count
        self.set_id = 0
        self.cur_row = list()
        self.set_track = dict() # To keep track of the cells with same set id
        self.block_pixel = 6 # Pixels per cell
        self.maze_array = np.full(((self.row_count * self.block_pixel) ,
                                	(self.col_count * self.block_pixel) + 1, 3),
									255, dtype=np.uint8)
                                

    def get_new_set_id(self):
        self.set_id += 1
        return self.set_id


    def generate_first_row(self):
        for col in range(self.col_count):
            cur_cell = Cell()
            cur_cell.row_index = 0
            cur_cell.col_index = col
            cur_cell.set_id = self.get_new_set_id()
            self.cur_row.append(cur_cell)
            self.set_track[cur_cell.set_id] = [cur_cell]


    def generate_new_row(self, row):
        self.set_track.clear()
        for cell_index in range(self.col_count):
            cur_cell = self.cur_row[cell_index]
            cur_cell.row_index = row
            cur_cell.col_index = cell_index
            if cur_cell.bottom_wall:
                cur_cell.set_id = self.get_new_set_id()
                cur_cell.right_wall = True
            else:
                cur_cell.bottom_wall = True
                # If not the last cell
                if cell_index < self.col_count - 1:
                    next_cell = self.cur_row[cell_index + 1]
                    if next_cell.bottom_wall:
                        cur_cell.right_wall = True
                else:
                    cur_cell.right_wall = True
            if cur_cell.set_id in self.set_track:
                self.set_track[cur_cell.set_id].append(cur_cell)
            else:
                self.set_track[cur_cell.set_id] = [cur_cell]
        

    def update_right_wall(self):
        for col_index in range(self.col_count - 1):
            cur_cell = self.cur_row[col_index]
            next_cell = self.cur_row[col_index + 1]
            # randomly join adjacent cells, if they are not in the same set.
            if cur_cell.set_id != next_cell.set_id:
                if bool(random.getrandbits(1)):
                    cur_cell.right_wall = False
                    next_cell_set_id = next_cell.set_id
                    # union the sets to which the current cell and the cell to the right are members.
                    for cell in self.set_track[next_cell_set_id]:
                        cell.set_id = cur_cell.set_id
                    # all cells in both sets are now connected
                    self.set_track[cur_cell.set_id] += self.set_track[next_cell_set_id]
                    del self.set_track[next_cell_set_id]


    def update_bottom_wall(self):
        # For each set, randomly create vertical connections downward to the next row. 
        # Each remaining set must have at least one vertical connection.
        for set_id in self.set_track:
            same_set_cells = self.set_track[set_id].copy()
            random_cell = random.choice(same_set_cells)
            random_cell.bottom_wall = False
            same_set_cells.remove(random_cell)
            while(same_set_cells):
                random_cell = random.choice(same_set_cells)
                if bool(random.getrandbits(1)):
                    random_cell.bottom_wall = False
                same_set_cells.remove(random_cell)


    def update_final_row(self):
        for cell_index in range(self.col_count - 1):
            cur_cell = self.cur_row[cell_index]
            next_cell = self.cur_row[cell_index + 1]
            cur_cell.bottom_wall = True
            if cur_cell.set_id != next_cell.set_id:
                cur_cell.right_wall = False
                # Union the sets
                next_cell_set_id = next_cell.set_id
                for cell in self.set_track[next_cell_set_id]:
                    cell.set_id = cur_cell.set_id
                    # all cells in both sets are now connected
                self.set_track[cur_cell.set_id] += self.set_track[next_cell_set_id]
                del self.set_track[next_cell_set_id]
                

    # Displays current row in the terminal
    def display_cur_row(self, row_num):
        if row_num == 0:
            print(' ___' * self.col_count)
        print('|', end='')
        for col_index in range(self.col_count):
            cur_cell = self.cur_row[col_index]
            if cur_cell.right_wall:
                print('   |' , end = '')
            else:
                print('    ', end = '')
        print('\b|')

        for col_index in range(self.col_count):
            cur_cell = self.cur_row[col_index]
            if cur_cell.bottom_wall:
                print(' ___', end = '')
            else:
                print('    ', end = '')
        print("")

    
    def draw(self):
		# Draw the maze according to the self.current_row. 
        # Each cell has "self.block_pixel" pixels. 1 pixel denoting the wall on each side.
        for cell in self.cur_row:
        	if cell.right_wall:
        		for row in range(self.block_pixel):
        			self.maze_array[(cell.row_index * self.block_pixel) +
                                     row][(cell.col_index * self.block_pixel) +
                                         self.block_pixel] = [0, 0, 0] #Blackpixels
        	if cell.bottom_wall:
        		for col in range(self.block_pixel):
        			self.maze_array[(cell.row_index * self.block_pixel) + 
                                        self.block_pixel - 1][(cell.col_index * self.block_pixel) +
                                             col] = [0, 0, 0] #Blackpixels
    

    def generate_maze_image(self):
        # Drawing boundaries
        for col in range(self.col_count * self.block_pixel):
            self.maze_array[0][col] = [0, 0, 0]
        for row in range(self.row_count * self.block_pixel):
            self.maze_array[row][0] = [0, 0, 0]
        img = Image.fromarray(self.maze_array, 'RGB')
        img.save('Maze.png')
        self.display_maze_image(img)


    def display_maze_image(self, img):
    	img.show(img)

        
    def generate(self):
        for row_index in range(self.row_count):
            # print("Processing Row : ", row_index + 1)
            if row_index == 0:
                self.generate_first_row()
            else: 
                self.generate_new_row(row_index)
            if row_index == self.row_count - 1:
                self.update_final_row()
                self.display_cur_row(row_index)
                self.draw()
                break
            self.update_right_wall()
            self.update_bottom_wall()
            self.draw()
            self.display_cur_row(row_index)
        self.generate_maze_image()



#Parsing the argument passed while executinig the program file to get the maze dimension
def argument_parser():
    parser = argparse.ArgumentParser(description = "Perfect Maze Generator")
    parser.add_argument('--width',
                        metavar = 'maze width',
                        type = int,
                        help = 'Width of the maze (Number of columns)',
                        required = True
                        )
    parser.add_argument('--height',
                        metavar = 'maze height',
                        type = int,
                        help = 'Height of the maze (Number of rows)',
                        required = True
                        )
    args = parser.parse_args()
    width = args.width
    height = args.height
    return (width, height)
         


if __name__ == "__main__":
    maze_width, maze_height = argument_parser()
    Maze(maze_height, maze_width).generate()
    

    