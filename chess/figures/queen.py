"""
Implementation of Bishop figure in chess command line client.
"""
import logging
import math
from . import figure
from ..board import Board


class Queen(figure.Figure):
    """
    Queen figure for chess implementation.
    """

    def _is_move_correct(self, x_index, y_index):
                # Move x_index or y_index
        return (((x_index < self._x_index or x_index > self._x_index) and
                 y_index == self._y_index or
                 (y_index < self._y_index or y_index > self._y_index) and
                 x_index == self._x_index) or
                # Move diagonally
                (math.fabs(x_index - self._x_index) == math.fabs(y_index - self._y_index)))

    def _test_move(self, x_index, y_index):
        result = None

        # Check if move is correct
        if self._is_move_correct(x_index, y_index):
            # Check if figure is moving
            if not self._is_moving(x_index, y_index):
                result = False

            # Check if the move is inside board
            if not self._is_move_inside_board(
                    x_index, y_index):
                result = False

            # Check if king is in target position
            if self._is_king_on_position(x_index, y_index):
                result = False

            # Check if another figure is on target destination
            if self._is_figure_on_target_position(x_index, y_index):
                result = False

            # check if path is free
            if not self._check_vector(x_index, y_index):
                result = False

            if result is None:
                target_figure = self._board.get_figure(x_index, y_index)
                # Attack
                if target_figure and target_figure.get_owner() != self._owner:
                    logging.info("Attacking %s on position %s:%s",
                                 target_figure.get_type(), x_index, y_index)
                    result = True
                else:
                    logging.info(
                        "Queen moved from %s:%s to %s:%s",
                        self._x_index,
                        self._y_index,
                        x_index,
                        y_index)
                    result = True

        else:
            # Move is illegal
            logging.info(
                "Invalid move for queen from %s:%s to %s:%s",
                self._x_index,
                self._y_index,
                x_index,
                y_index)
            result = False

        return result

# if __name__ == "__main__":
#    # Start logging
#    logging.basicConfig(
#        format='[%(asctime)s] ' +
#        '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#        level=logging.DEBUG)
#
#    # Test invalid move
#    print("Test invalid move:")
#    queen = Queen(0, 0, figure.queen, "black")
#    state = {(0, 0): (figure.queen, queen._owner)}
#    queen.moveTo(-2, -32, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test correct move in axis
#    print("Test correct move in axis:")
#    queen = Queen(0, 0, figure.queen, "black")
#    state = {(0, 0): (figure.queen, queen._owner)}
#    queen.moveTo(2, 0, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test correct move diagonally
#    print("Test correct move in axis:")
#    queen = Queen(0, 0, figure.queen, "black")
#    state = {(0, 0): (figure.queen, queen._owner)}
#    queen.moveTo(2, 2, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test attack
#    print("Test attack move:")
#    queen = Queen(0, 0, figure.queen, "white")
#    state = {(0, 0): (figure.queen, queen._owner),
#             (2, 2): (figure.queen, "black")}
#    queen.moveTo(2, 2, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test move on target destination
#    print("Test move on target destination:")
#    queen = Queen(0, 0, figure.queen, "white")
#    state = {(0, 0): (figure.queen, queen._owner),
#             (2, 2): (figure.queen, "white")}
#    queen.moveTo(2, 2, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test generation
#    print("Test moves generation:")
#    queen = Queen(4, 4, figure.queen, "white")
#    state = {(4, 4): (figure.queen, queen._owner)}
#    states = queen.generateMoves(state, 8, 8)
#    print("Generated states " + str(states))
#
#    # Test king capture
#    print("Test king capture:")
#    queen = Queen(4, 4, figure.queen, "white")
#    state = {(4, 4): (figure.queen, queen._owner),
#             (6, 6): (figure.king, figure.black)}
#    queen.moveTo(6, 6, state, 8, 8)
#    print("New state " + str(state))
