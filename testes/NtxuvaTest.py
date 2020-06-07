import unittest
from Ntxuva import Ntxuva
import numpy as np

ROWS = 4
COLUMNS = 8
SEEDS = 2

class MyTestCase(unittest.TestCase):

    def create_ntxuva(self ,seeds=2):
        return Ntxuva(rows=ROWS, columns=COLUMNS, seeds=seeds)

    def test_player_side(self):
        turn = 'x'
        ntxuva = Ntxuva(ROWS, COLUMNS, SEEDS)
        ntxuva.turn = turn

        ntxuva.player_side()
        player1_side = (0, 1)
        self.assertEquals(ntxuva.player_side(), player1_side)

        player2_side = (2, 3)
        ntxuva.turn = 'o'
        self.assertEquals(player2_side, ntxuva.player_side())

    def test_change_turn(self):
        ntxuva = self.create_ntxuva()
        ntxuva.turn = 'x'
        ntxuva.change_turn()
        current_turn = 'o'
        self.assertEqual(current_turn, ntxuva.turn)

    def test_move(self):
        ntxuva = self.create_ntxuva()
        ntxuva.turn = 'o'

        for column in range(COLUMNS):
            new_pos = ntxuva.move((3,column))
            if column == COLUMNS - 1:
                self.assertEqual(new_pos, (2, column))
            else:
                self.assertEqual(new_pos, (3, column + 1))

    def test_one_than_more_piece(self):
        ntxuva =  self.create_ntxuva(seeds=1)
        self.assertFalse(ntxuva.more_than_one_piece())
        ntxuva = self.create_ntxuva(seeds=2)
        self.assertTrue(ntxuva.more_than_one_piece())

    def test_is_atack_position(self):
        ntxuva = self.create_ntxuva()
        ntxuva.turn = 'x'
        for column in range(COLUMNS):
            position = (1,column)
            ntxuva.capture_stones(position)
            self.assertEquals(ntxuva.board[(2,column)],0)
            self.assertEquals(ntxuva.board[(3, column)],0)
        ntxuva.turn = 'o'
        for column in range(COLUMNS):
            position = (1, column)
            ntxuva.capture_stones(position)
            self.assertEquals(ntxuva.board[(2, column)], 0)
            self.assertEquals(ntxuva.board[(3, column)], 0)

    def test_is_terminal_state(self):
        ntxuva = self.create_ntxuva()
        ntxuva.board[2:] = np.full((2,COLUMNS), 0)
        val = ntxuva.is_terminal_state()
        self.assertTrue(val)
        ntxuva.board[2:] = np.ones((2,COLUMNS))
        val = ntxuva.is_terminal_state()
        self.assertFalse(val)

    def test_reset(self):

        ntxuva = self.create_ntxuva()
        is_over = ntxuva.is_over
        turn = ntxuva.turn
        player1_score = ntxuva.player1_score
        player2_score = ntxuva.player2_score
        ntxuva.board = np.random.random(size=(4,8))

        ntxuva.reset()
        flatten_board = np.reshape(ntxuva.board, [ROWS * COLUMNS])
        self.assertTrue(is_over == ntxuva.is_over)
        self.assertTrue(player1_score == ntxuva.player1_score)
        self.assertTrue(player2_score == ntxuva.player2_score)
        self.assertTrue(turn == ntxuva.turn)

        for data in flatten_board:
            self.assertTrue(data == 2)


    def test_step(self):
        ntxuva = self.create_ntxuva()






















if __name__ == '__main__':
    unittest.main()
