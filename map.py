import random
from collections import deque
from room import Room
from typing import List, Tuple

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
MAIN_LENGTH = 10


class Map:
    def __init__(self, num=None) -> None:
        """
        Creates main branch, then t-room branch, and finally the pots branch of the Lost Halls map
        :param num: seed number to reproduce identical maps
        """
        if not num:
            random.seed()
        else:
            random.seed(num)
        self.matrix = [[Room() for _ in range(9)] for _ in range(9)]
        self.main_loop = False
        self.create_main_branch(x=4, y=4, depth=0, loop=False)
        self.create_split_branches()

    def create_split_branches(self) -> bool:
        candidates = deque()
        for y in range(9):
            for x in range(9):
                room = self.matrix[y][x]
                if not (room.empty or room.defender or room.colossus):
                    candidates.append((x, y))
        random.shuffle(candidates)

        # Place Troom
        rooms_tried = 0
        while rooms_tried < len(candidates):
            x, y = candidates.popleft()
            rooms_tried += 1
            split_length = random.randint(1, 3)
            if self.toggle_troom_branch(x, y, depth=0, length=split_length):
                break
            else:
                candidates.append((x, y))
        if rooms_tried == len(candidates):
            return False

        # Place pots
        pots_placed = 0
        while candidates and pots_placed < 5:
            x, y = candidates.popleft()
            split_length = random.randint(2, 4)
            if self.toggle_pot_branch(x, y, depth=0, length=split_length):
                pots_placed += 1
            else:
                self.toggle_pot_branch(x, y, depth=0, length=split_length)
        return pots_placed == 5

    def toggle_troom_branch(self, x: int, y: int, depth: int, length: int) -> bool:
        if depth == length:
            if y - 1 >= 0 and self.matrix[y - 1][x].empty:
                self.matrix[y][x].toggle_edge(direction=UP)
                self.matrix[y - 1][x].toggle_edge(direction=DOWN)
                self.matrix[y - 1][x].toggle_troom()
                return True
            else:
                return False

        choices = [(x, y - 1, UP, 0), (x + 1, y, RIGHT, 1), (x, y + 1, DOWN, 2), (x - 1, y, LEFT, 3)]
        weights = self.weight_adjacent_rooms(x, y)
        while any(weights):
            adj_x, adj_y, direction, index = random.choices(choices, weights)[0]
            self.matrix[y][x].toggle_edge(direction)
            adj_direction = self.opposite_direction(direction)
            self.matrix[adj_y][adj_x].toggle_edge(adj_direction)
            if self.toggle_troom_branch(adj_x, adj_y, depth + 1, length):
                return True
            else:
                weights[index] = 0
                self.matrix[y][x].toggle_edge(direction)
                self.matrix[adj_y][adj_x].toggle_edge(adj_direction)
        return False

    def toggle_pot_branch(self, x: int, y: int, depth: int, length: int) -> bool:
        if depth == length:
            self.matrix[y][x].toggle_pot()
            return True

        choices = [(x, y - 1, UP, 0), (x + 1, y, RIGHT, 1), (x, y + 1, DOWN, 2), (x - 1, y, LEFT, 3)]
        weights = self.weight_adjacent_rooms(x, y)
        while any(weights):
            adj_x, adj_y, direction, index = random.choices(choices, weights)[0]
            self.matrix[y][x].toggle_edge(direction)
            adj_direction = self.opposite_direction(direction)
            self.matrix[adj_y][adj_x].toggle_edge(adj_direction)
            if self.toggle_pot_branch(adj_x, adj_y, depth + 1, length):
                return True
            else:
                weights[index] = 0
                self.matrix[y][x].toggle_edge(direction)
                self.matrix[adj_y][adj_x].toggle_edge(adj_direction)
        return False

    @staticmethod
    def opposite_direction(direction: int) -> int:
        """
        Gives the opposite direction
        :param direction: UP, DOWN, LEFT, RIGHT
        :return: UP, DOWN, LEFT, RIGHT given DOWN, UP, RIGHT, LEFT respectively
        """
        return (direction + 2) % 4

    def create_main_branch(self, x: int, y: int, depth: int, loop: bool) -> bool:
        """
        Creates the rooms that are in the main branch of the map
        :param x: x coordinate of current room
        :param y: y coordinate of current room
        :param depth: current depth from the spawn room
        :param loop: whether in process of creating a loop
        :return: True if successful in creating a main-branch, False otherwise
        """
        if depth == MAIN_LENGTH:
            return self.create_colossus(x, y)

        if loop:
            choices = [(x, y, 0), (x + 1, y, 1), (x, y + 1, 2), (x + 1, y + 1, 3)]
            weights = self.weight_exit_rooms(x, y)
            while any(weights):
                exit_x, exit_y, index = random.choices(choices, weights)[0]
                if self.create_main_branch(exit_x, exit_y, depth, loop=False):
                    return True
                else:
                    weights[index] = 0
            return False

        if not self.main_loop and random.random() <= 0.2:
            self.main_loop = True
            loops = self.available_loops(x, y)
            random.shuffle(loops)
            for top_left_x, top_left_y, adj_x, adj_y, source_direction, adj_direction in loops:
                self.toggle_loop(top_left_x, top_left_y)
                self.matrix[y][x].toggle_edge(source_direction)
                self.matrix[adj_y][adj_x].toggle_edge(adj_direction)
                if self.create_main_branch(top_left_x, top_left_y, depth + 1, loop=True):
                    return True
                else:
                    self.toggle_loop(top_left_x, top_left_y)
                    self.matrix[y][x].toggle_edge(source_direction)
                    self.matrix[adj_y][adj_x].toggle_edge(adj_direction)
            self.main_loop = False

        choices = [(x, y - 1, UP, 0), (x + 1, y, RIGHT, 1), (x, y + 1, DOWN, 2), (x - 1, y, LEFT, 3)]
        weights = self.weight_adjacent_rooms(x, y)
        while any(weights):
            adj_x, adj_y, direction, index = random.choices(choices, weights)[0]
            self.matrix[y][x].toggle_edge(direction)
            adj_direction = self.opposite_direction(direction)
            self.matrix[adj_y][adj_x].toggle_edge(adj_direction)
            if self.create_main_branch(adj_x, adj_y, depth + 1, loop=False):
                return True
            else:
                weights[index] = 0
                self.matrix[y][x].toggle_edge(direction)
                self.matrix[adj_y][adj_x].toggle_edge(adj_direction)
        return False

    def weight_adjacent_rooms(self, x: int, y: int) -> List[int]:
        """
        Count number of empty rooms for the adjacent rooms to the current room
        :param x: x coordinate of current room
        :param y: y coordinate of current room
        :return: Counted empty rooms for the adjacent up, right, down, left rooms
        """
        return [self.count_empty(x, y - 1, direction=UP),
                self.count_empty(x + 1, y, direction=RIGHT),
                self.count_empty(x, y + 1, direction=DOWN),
                self.count_empty(x - 1, y, direction=LEFT)]

    def count_empty(self, x: int, y: int, direction: int) -> int:
        """
        Counts number of empty rooms from current room to a border in the given direction
        :param x: x coordinate of adjacent room
        :param y: y coordinate of adjacent room
        :param direction: direction from adjacent room to border
        :return: counted empty rooms
        """
        if y < 0 or y >= 9 or x < 0 or x >= 9 or not self.matrix[y][x].empty:
            return 0
        lower_x = lower_y = 0
        upper_x = upper_y = 9
        if direction == UP:
            upper_y = y + 1
        elif direction == RIGHT:
            lower_x = x
        elif direction == DOWN:
            lower_y = y
        else:
            upper_x = x + 1
        empty_rooms = 0
        for i in range(lower_y, upper_y):
            for j in range(lower_x, upper_x):
                if self.matrix[i][j].empty:
                    empty_rooms += 1
        return empty_rooms

    # TODO: CHANGE FROM LOCAL TO GLOBAL SCOPE
    def weight_exit_rooms(self, top_left_x: int, top_left_y: int) -> List[int]:
        """
        Counts number of adjacent empty rooms in all rooms of the loop
        :param top_left_x: x coordinate of top-left room in the loop
        :param top_left_y: y coordinate of top-left room in the loop
        :return: Counted empty rooms for top-left, top-right, bottom-left, and bottom-right rooms in the loop
        """

        def num_empty(x, y):
            n = 0
            if y > 0 and self.matrix[y - 1][y].empty:
                n += 1
            if x < 8 and self.matrix[y][x + 1].empty:
                n += 1
            if y < 8 and self.matrix[y + 1][x].empty:
                n += 1
            if x > 0 and self.matrix[y][x - 1].empty:
                n += 1
            return n

        return [num_empty(top_left_x, top_left_y), num_empty(top_left_x + 1, top_left_y),
                num_empty(top_left_x, top_left_y + 1), num_empty(top_left_x + 1, top_left_y + 1)]

    def available_loops(self, x: int, y: int) -> List[Tuple[int, int, int, int, int, int]]:
        """
        Returns all available loop coordinates which connects from room (x,y)
        :param x: x coordinate of current room
        :param y: y coordinate of current room
        :return: top-left loop coordinates, adjacent room to current room coordinates, and connecting directions
        """
        loops = []
        if (x > 0 and y > 1 and
                self.matrix[y - 1][x].empty and self.matrix[y - 2][x].empty and
                self.matrix[y - 1][x - 1].empty and self.matrix[y - 2][x - 1].empty):
            loops.append((x - 1, y - 2, x, y - 1, UP, DOWN))
        if (x < 8 and y > 1 and
                self.matrix[y - 1][x].empty and self.matrix[y - 2][x].empty and
                self.matrix[y - 1][x + 1].empty and self.matrix[y - 2][x + 1].empty):
            loops.append((x, y - 2, x, y - 1, UP, DOWN))
        if (x < 7 and y > 0 and
                self.matrix[y][x + 1].empty and self.matrix[y][x + 2].empty and
                self.matrix[y - 1][x + 1].empty and self.matrix[y - 1][x + 2].empty):
            loops.append((x + 1, y - 1, x + 1, y, RIGHT, LEFT))
        if (x < 7 and y < 8 and
                self.matrix[y][x + 1].empty and self.matrix[y][x + 2].empty and
                self.matrix[y + 1][x + 1].empty and self.matrix[y + 1][x + 2].empty):
            loops.append((x + 1, y, x + 1, y, RIGHT, LEFT))
        if (x < 8 and y < 7 and
                self.matrix[y + 1][x].empty and self.matrix[y + 2][x].empty and
                self.matrix[y + 1][x + 1].empty and self.matrix[y + 2][x + 1].empty):
            loops.append((x, y + 1, x, y + 1, DOWN, UP))
        if (x > 0 and y < 7 and
                self.matrix[y + 1][x].empty and self.matrix[y + 2][x].empty and
                self.matrix[y + 1][x - 1].empty and self.matrix[y + 2][x - 1].empty):
            loops.append((x - 1, y + 1, x, y + 1, DOWN, UP))
        if (x > 1 and y < 8 and
                self.matrix[y][x - 1].empty and self.matrix[y][x - 2].empty and
                self.matrix[y + 1][x - 1].empty and self.matrix[y + 1][x - 2].empty):
            loops.append((x - 2, y, x - 1, y, LEFT, RIGHT))
        if (x > 1 and y > 0 and
                self.matrix[y][x - 1].empty and self.matrix[y][x - 2].empty and
                self.matrix[y - 1][x - 1].empty and self.matrix[y - 1][x - 2].empty):
            loops.append((x - 2, y - 1, x - 1, y, LEFT, RIGHT))
        return loops

    def create_colossus(self, x: int, y: int) -> bool:
        """
        Creates the 3x3 colossus room, and connects the defender room to colossus
        :param x: x coordinate of defender room
        :param y: y coordinate of defender room
        :return: Successful or not
        """
        centre_x, centre_y, connecting_direction = self.find_colossus(x, y)
        self.matrix[y][x].toggle_defender()
        self.matrix[y][x].toggle_edge(connecting_direction)
        diff = [-1, 0, 1]
        for i in diff:
            for j in diff:
                if (centre_y + i < 0 or centre_y + i >= 9 or centre_x + j < 0 or centre_x + j >= 9 or
                        not self.matrix[centre_y + i][centre_x + j].empty):
                    self.matrix[y][x].toggle_defender()
                    self.matrix[y][x].toggle_edge(connecting_direction)
                    return False
        for i in diff:
            for j in diff:
                self.matrix[centre_y + i][centre_x + j].toggle_colossus()
        return True

    def find_colossus(self, x: int, y: int) -> Tuple[int, int, int]:
        """
        Finds the centre of colossus room, which is a 3x3 grid  and the connecting direction from defender to colossus
        :param x: x coordinate of defender room
        :param y: y coordinate of defender room
        :return: centre_x, centre_y, connecting_direction
        """
        centre_x, centre_y, connecting_direction = x, y, -1
        if self.matrix[y][x].up:
            centre_y += 2
            connecting_direction = self.opposite_direction(UP)
        elif self.matrix[y][x].right:
            centre_x -= 2
            connecting_direction = self.opposite_direction(RIGHT)
        elif self.matrix[y][x].down:
            centre_y -= 2
            connecting_direction = self.opposite_direction(DOWN)
        else:
            centre_x += 2
            connecting_direction = self.opposite_direction(LEFT)
        return centre_x, centre_y, connecting_direction

    def toggle_loop(self, top_left_x: int, top_left_y: int) -> None:
        """
        Toggles a loop consisting of 4 rooms
        :param top_left_x: x coordinate of top-left room in the loop
        :param top_left_y: y coordinate of top-left room in the loop
        """
        self.matrix[top_left_y][top_left_x].toggle_edge(direction=RIGHT)
        self.matrix[top_left_y][top_left_x].toggle_edge(direction=DOWN)
        self.matrix[top_left_y + 1][top_left_x].toggle_edge(direction=RIGHT)
        self.matrix[top_left_y + 1][top_left_x].toggle_edge(direction=UP)
        self.matrix[top_left_y][top_left_x + 1].toggle_edge(direction=LEFT)
        self.matrix[top_left_y][top_left_x + 1].toggle_edge(direction=DOWN)
        self.matrix[top_left_y + 1][top_left_x + 1].toggle_edge(direction=LEFT)
        self.matrix[top_left_y + 1][top_left_x + 1].toggle_edge(direction=UP)

    def __str__(self) -> str:
        """
        Gets edges of all rooms in map as a string, with rows separated by newline, and columns separated by space
        :return: str
        """
        lh_map = [["" for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                room = self.matrix[i][j]
                r = ["", "", "", ""]
                r[0] = "U" if room.up else "-"
                r[1] = "R" if room.right else "-"
                r[2] = "D" if room.down else "-"
                r[3] = "L" if room.left else "-"
                lh_map[i][j] = "".join(r)
        res = ""
        for i in range(9):
            for j in range(9):
                res = res + lh_map[i][j] + " "
            res = res + "\n"
        return res
