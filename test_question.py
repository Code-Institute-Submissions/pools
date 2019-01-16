import unittest
from game import Question

class TestQuestion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setup')
        self.game_1 = Question('Man Utd', 'Liverpool', 1)
        self.game_2 = Question('Spurs', 'Watford', 2)
        self.game_3 = Question('Newcastle', 'Chelsea', 3)

    def tearDown(self):
        print('teardown\n')

    def test_fixture(self):
        print('test_fixture')
        self.assertEqual(self.game_1.fixture(), 'Man Utd vs Liverpool')
        self.assertEqual(self.game_2.fixture(), 'Spurs vs Watford')
        self.assertEqual(self.game_3.fixture(), 'Newcastle vs Chelsea')

    def test_result(self):
        print('test_result')
        self.assertEqual(self.game_1.result, 1)
        self.assertEqual(self.game_2.result, 2)
        self.assertEqual(self.game_3.result, 3)


if __name__ == '__main__':
    unittest.main()
