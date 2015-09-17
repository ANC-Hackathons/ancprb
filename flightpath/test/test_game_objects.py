from mock import patch
import unittest
from flightpath import game_objects

class TestGameObject(unittest.TestCase):

  def setUp(self):
    self.x_unit_patcher = patch('flightpath.game_objects.x_unit')
    self.x_unit_mock = self.x_unit_patcher.start()
    def side_effect(direction):
      return direction * 2
    self.x_unit_mock.side_effect = side_effect

  def tearDown(self):
    self.x_unit_patcher.stop()

  def test_init_ship(self):
    ship = game_objects.Ship([0,0,0],0.5,30,90,2.0,3.0)
    self.assertEqual(ship.position, [0,0,0], "The ship position was not set correctly")
    self.assertEqual(ship.speed, 0.5, "The ship speed was not set correctly")
    self.assertEqual(ship.direction, 30, "The ship direction was not set correctly")
    self.assertEqual(ship.angular_rate, 90, "The ship angular rate was not set correctly")
    self.assertEqual(ship.d_vector, 60, "The ship d vector was not set corectly")
    self.assertEqual(ship.dim, [2.0, 3.0], "The ship dimensions were not set correctly")

  def test_turn_positive(self):
    ship = game_objects.Ship([0,0,0],0,10,5,0,0)
    self.assertEqual(ship.angular_rate, 5, "The ship angular rate was not initialized correctly")
    self.assertEqual(ship.direction, 10, "The ship direction was not initialized correctly")
    self.assertEqual(ship.d_vector, game_objects.x_unit(10), "The ship d vector was not initialized corectly")
    ship.turn(2)
    self.assertEqual(ship.direction, 20, "The ship direction was not updated correctly")
    self.assertEqual(ship.d_vector, game_objects.x_unit(20), "The ship d vector was not updated corectly")

  def test_turn_negative(self):
    ship = game_objects.Ship([0,0,0],0,10,5,0,0)
    self.assertEqual(ship.angular_rate, 5, "The ship angular rate was not initialized correctly")
    self.assertEqual(ship.direction, 10, "The ship direction was not initialized correctly")
    self.assertEqual(ship.d_vector, game_objects.x_unit(10), "The ship d vector was not initialized corectly")
    ship.turn(-1)
    self.assertEqual(ship.direction, 5, "The ship direction was not updated correctly")
    self.assertEqual(ship.d_vector, game_objects.x_unit(5), "The ship d vector was not updated corectly")

if __name__ == '__main__':
  unittest.main()

