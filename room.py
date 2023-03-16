UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Room:

    def __init__(self):
        """
        All non-empty rooms have at least one edge, and all empty rooms have no edges.
        A room can be at most one type (e.g. a room cannot be a pot room and defender room at the same time).
        At the same time, a room can have no type too.
        """

        # Edges
        self.up = False
        self.right = False
        self.down = False
        self.left = False

        # Branch
        self.main = False

        # Types
        self.troom = False
        self.pot = False
        self.defender = False
        self.colossus = False
        self.empty = True

    def toggle_edge(self, direction: int) -> None:
        """
        Toggles an edge for a room in the given direction
        :param direction: UP, RIGHT, DOWN, LEFT
        :return: Nothing
        """
        if direction == UP:
            self.up = not self.up
        elif direction == RIGHT:
            self.right = not self.right
        elif direction == DOWN:
            self.down = not self.down
        else:
            self.left = not self.left
        self.empty = not (self.left or self.right or self.down or self.right or
                          self.troom or self.pot or self.defender or self.colossus)

    def toggle_defender(self):
        """
        Toggles a room to be defender
        :return: Nothing
        """
        self.defender = not self.defender
        self.empty = not (self.left or self.right or self.down or self.right or
                          self.troom or self.pot or self.defender or self.colossus)

    def toggle_colossus(self):
        """
        Toggles a room to be the colossus room
        :return: Nothing
        """
        self.colossus = not self.colossus
        self.empty = not (self.left or self.right or self.down or self.right or
                          self.troom or self.pot or self.defender or self.colossus)

    def toggle_troom(self):
        """
        Toggles a room to be the treasure room
        :return: Nothing
        """
        self.troom = not self.troom
        self.empty = not (self.left or self.right or self.down or self.right or
                          self.troom or self.pot or self.defender or self.colossus)

    def toggle_pot(self):
        """
        Toggles a room to be the treasure room
        :return: Nothing
        """
        self.pot = not self.pot
        self.empty = not (self.left or self.right or self.down or self.right or
                          self.troom or self.pot or self.defender or self.colossus)
