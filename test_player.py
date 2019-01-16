import unittest
from game import Player

class TestPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setup')
        self.player_1 = Player('Keane')
        self.player_2 = Player('Pirlo')
        self.player_3 = Player('Xavi')

    def tearDown(self):
        print('teardown\n')

    def test_inc_score(self):
        print('test_inc_score')

        self.player_1.inc_score(1, 1)
        self.assertEqual(self.player_1.score, 1)

        self.player_2.inc_score(1, 3)
        self.assertEqual(self.player_2.score, 3)

        self.player_3.inc_score(2, 2)
        self.assertEqual(self.player_3.score, 1)






if __name__ == '__main__':
    unittest.main()
