import unittest

from map import Map, UP, RIGHT, DOWN, LEFT
from room import Room


class TestRoom(unittest.TestCase):

    def test_toggle_edge_up(self):
        room = Room()
        room.up = False
        room.empty = True

        room.toggle_edge(UP)
        self.assertTrue(room.up)
        self.assertFalse(room.empty)

        room.toggle_edge(UP)
        self.assertFalse(room.up)
        self.assertTrue(room.empty)

    def test_toggle_edge_down(self):
        room = Room()
        room.down = False
        room.empty = True

        room.toggle_edge(DOWN)
        self.assertTrue(room.down)
        self.assertFalse(room.empty)

        room.toggle_edge(DOWN)
        self.assertFalse(room.down)
        self.assertTrue(room.empty)

    def test_toggle_edge_left(self):
        room = Room()
        room.left = False
        room.empty = True

        room.toggle_edge(LEFT)
        self.assertTrue(room.left)
        self.assertFalse(room.empty)

        room.toggle_edge(LEFT)
        self.assertFalse(room.left)
        self.assertTrue(room.empty)

    def test_toggle_edge_right(self):
        room = Room()
        room.right = False
        room.empty = True

        room.toggle_edge(RIGHT)
        self.assertTrue(room.right)

        room.toggle_edge(RIGHT)
        self.assertFalse(room.right)

    def test_toggle_defender(self):
        room = Room()
        room.defender = False
        room.empty = True

        room.toggle_defender()
        self.assertTrue(room.defender)
        self.assertFalse(room.empty)

        room.toggle_defender()
        self.assertFalse(room.defender)
        self.assertTrue(room.empty)

    def test_toggle_colossus(self):
        room = Room()
        room.colossus = False
        room.empty = True

        room.toggle_colossus()
        self.assertTrue(room.colossus)
        self.assertFalse(room.empty)

        room.toggle_colossus()
        self.assertFalse(room.colossus)
        self.assertTrue(room.empty)

    def test_toggle_troom(self):
        room = Room()
        room.troom = False
        room.empty = True

        room.toggle_troom()
        self.assertTrue(room.troom)
        self.assertFalse(room.empty)

        room.toggle_troom()
        self.assertFalse(room.troom)
        self.assertTrue(room.empty)

    def test_toggle_pot(self):
        room = Room()
        room.pot = False
        room.empty = True

        room.toggle_pot()
        self.assertTrue(room.pot)
        self.assertFalse(room.empty)

        room.toggle_pot()
        self.assertFalse(room.pot)
        self.assertTrue(room.empty)


class TestMap(unittest.TestCase):

    def test_opposite_direction_up(self):
        self.assertEqual(Map.opposite_direction(UP), DOWN)

    def test_opposite_direction_down(self):
        self.assertEqual(Map.opposite_direction(DOWN), UP)

    def test_opposite_direction_left(self):
        self.assertEqual(Map.opposite_direction(RIGHT), LEFT)

    def test_opposite_direction_right(self):
        self.assertEqual(Map.opposite_direction(LEFT), RIGHT)
