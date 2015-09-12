from mock import patch
import unittest
import game_objects

class TestGameObject(unittest.TestCase):

  def setUp(self):
    self.x_unit_patcher = patch('game_objects.x_unit')
    self.x_unit_mock = self.x_unit_patcher.start()
    def side_effect(direction):
      return direction * 2
    self.x_unit_mock.side_effect = side_effect
    self.ship = game_objects.Ship([0,0,0],0.5,30,90,2.0,3.0)

  def tearDown(self):
    self.x_unit_patcher.stop()

  def test_init_ship(self):
    self.assertEqual(self.ship.position, [0,0,0], "The ship position was not set correctly")
    self.assertEqual(self.ship.speed, 0.5, "The ship speed was not set correctly")
    self.assertEqual(self.ship.direction, 30, "The ship direction was not set correctly")
    self.assertEqual(self.ship.angular_rate, 90, "The ship angular rate was not set correctly")
    self.assertEqual(self.ship.d_vector, 60, "The ship d vector was not set corectly")
    self.assertEqual(self.ship.dim, [2.0, 3.0], "The ship dimensions were not set correctly")

if __name__ == '__main__':
  unittest.main()
