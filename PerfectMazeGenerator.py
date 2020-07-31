import random


class Cell:
    def __init__(self):
        self.right_wall = True
        self.bottom_wall = True
        self.set_id = -1



class Maze:
    def __init__(self, row_count, col_count):
        self.row_count = row_count
        self.col_count = col_count
        self.set_id = 0
        self.cur_row = list()
        self.set_track = dict() # To keep track of the cells with same set id
                                

    def get_new_set_id(self):
        self.set_id += 1
        return self.set_id


    def generate_first_row(self):
        for _ in range(self.col_count):
            cur_cell = Cell()
            cur_cell.set_id = self.get_new_set_id()
            self.cur_row.append(cur_cell)
            self.set_track[cur_cell.set_id] = [cur_cell]


    def generate_new_row(self):
        self.set_track.clear()
        for cell_index in range(self.col_count):
            cur_cell = self.cur_row[cell_index]
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
        

    def generate(self):
        for row_index in range(self.row_count):
            # print("Processing Row : ", row_index + 1)
            if row_index == 0:
                self.generate_first_row()
            else: 
                self.generate_new_row()
            if row_index == self.row_count - 1:
                self.update_final_row()
                self.display_cur_row(row_index)
                break
            self.update_right_wall()
            self.update_bottom_wall()
            self.display_cur_row(row_index)


         
if __name__ == "__main__":
    Maze(10, 10).generate()
        

    