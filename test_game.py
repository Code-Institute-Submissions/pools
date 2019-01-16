import json
import random
import unittest
from game import Player, Question, calc_winner, get_rand_match_week, create_fixtures, get_correct_result

player_1 = Player('Keane', 9)
player_2 = Player('Pirlo', 6)
player_3 = Player('Scholes', 8)
player_4 = Player('Silva', 6)

week_2 = [
        {
          "team1": {
            "name": "Aston Villa"
          },
          "team2": {
            "name": "Manchester United"
          },
          "score1": 0,
          "score2": 1,
          "result": 3
        },
        {
          "team1": {
            "name": "Southampton"
          },
          "team2": {
            "name": "Everton"
          },
          "score1": 0,
          "score2": 3,
          "result": 3
        },
        {
          "team1": {
            "name": "Sunderland"
          },
          "team2": {
            "name": "Norwich"
          },
          "score1": 1,
          "score2": 3,
          "result": 3
        },
        {
          "team1": {
            "name": "Swansea"
          },
          "team2": {
            "name": "Newcastle United"
          },
          "score1": 2,
          "score2": 0,
          "result": 1
        },
        {
          "team1": {
            "name": "Tottenham Hotspur"
          },
          "team2": {
            "name": "Stoke City"
          },
          "score1": 2,
          "score2": 2,
          "result": 2
        },
        {
          "team1": {
            "name": "Watford"
          },
          "team2": {
            "name": "West Bromwich Albion"
          },
          "score1": 0,
          "score2": 0,
          "result": 2
        },
        {
          "team1": {
            "name": "West Ham United"
          },
          "team2": {
            "name": "Leicester City"
          },
          "score1": 1,
          "score2": 2,
          "result": 3
        },
        {
          "team1": {
            "name": "Crystal Palace"
          },
          "team2": {
            "name": "Arsenal"
          },
          "score1": 1,
          "score2": 2,
          "result": 3
        },
        {
          "team1": {
            "name": "Manchester City"
          },
          "team2": {
            "name": "Chelsea"
          },
          "score1": 3,
          "score2": 0,
          "result": 1
        },
        {
          "team1": {
            "name": "Liverpool"
          },
          "team2": {
            "name": "Bournemouth"
          },
          "score1": 1,
          "score2": 0,
          "result": 1
        }
      ]
fixtures = [{'fixture': 'Aston Villa vs Manchester United', 'result': 3}, {'fixture': 'Southampton vs Everton', 'result': 3}, {'fixture': 'Sunderland vs Norwich', 'result': 3}, {'fixture': 'Swansea vs Newcastle United', 'result': 1}, {'fixture': 'Tottenham Hotspur vs Stoke City', 'result': 2}, {'fixture': 'Watford vs West Bromwich Albion', 'result': 2}, {'fixture': 'West Ham United vs Leicester City', 'result': 3}, {'fixture': 'Crystal Palace vs Arsenal', 'result': 3}, {'fixture': 'Manchester City vs Chelsea', 'result': 1}, {'fixture': 'Liverpool vs Bournemouth', 'result': 1}]




class TestGame(unittest.TestCase):

    def test_calc_winner(self):
        self.assertEqual(calc_winner(player_1, player_2), f'{player_1.name} is the winner!')
        self.assertEqual(calc_winner(player_2, player_3), f'{player_3.name} is the winner!')
        self.assertEqual(calc_winner(player_2, player_4), 'Game has finished in a draw!')


    def test_get_rand_match_week(self):
        self.assertEqual(get_rand_match_week(1), week_2)


    def test_create_fixtures(self):
        self.assertEqual(create_fixtures(week_2), fixtures)


    def test_get_correct_result(self):
        self.assertEqual(get_correct_result(1, fixtures), 3)
        self.assertEqual(get_correct_result(2, fixtures), 3)
        self.assertEqual(get_correct_result(4, fixtures), 1)
        self.assertEqual(get_correct_result(5, fixtures), 2)
        self.assertEqual(get_correct_result(10, fixtures), 1)












if __name__ == '__main__':
    unittest.main()
