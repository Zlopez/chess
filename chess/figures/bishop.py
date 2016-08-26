"""
Implementation of Bishop figure in chess command line client.
"""
import logging
import math
from . import figure

class Bishop(figure.Figure):
    """
    Bishop figure for chess implementation.
    """

    def _is_move_correct(self, x_index, y_index):
        return (math.fabs(x_index - self._x_index) ==
                math.fabs(y_index - self._y_index))

    def _test_move(self, x_index, y_index):
        result = None

        # First test if move is correct
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
                # Attack
                target_figure = self._board.get_figure(x_index, y_index)
                if target_figure and target_figure.get_owner != self._owner:
                    logging.info("Attacking %s on position %s:%s",
                                 target_figure.get_type(), x_index, y_index)
                    result = True
                else:
                    # Move is legal
                    logging.info(
                        "Bishop moved from %s:%s to %s:%s",
                        self._x_index,
                        self._y_index,
                        x_index,
                        y_index)
                    result = True
        else:
            # Move is illegal
            logging.info(
                "Invalid move for bishop from %s:%s to %s:%s",
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
#    bishop = Bishop(0, 0, figure.bishop, "black")
#    state = {(0, 0): (figure.bishop, bishop._owner)}
#    bishop.moveTo(-2, -2, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test correct move
#    print("Test correct move:")
#    bishop = Bishop(0, 0, figure.bishop, "black")
#    state = {(0, 0): (figure.bishop, bishop._owner)}
#    bishop.moveTo(2, 2, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test attack
#    print("Test attack move:")
#    bishop = Bishop(0, 0, figure.bishop, "white")
#    state = {(0, 0): (figure.bishop, bishop._owner),
#             (2, 2): (figure.bishop, "black")}
#    bishop.moveTo(2, 2, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test move on target destination
#    print("Test move on target destination:")
#    bishop = Bishop(0, 0, figure.bishop, "white")
#    state = {(0, 0): (figure.bishop, bishop._owner),
#             (2, 2): (figure.bishop, "white")}
#    bishop.moveTo(2, 2, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test generation
#    print("Test moves generation:")
#    bishop = Bishop(4, 4, figure.bishop, "white")
#    state = {(4, 4): (figure.bishop, bishop._owner)}
#    states = bishop.generateMoves(state, 8, 8)
#    print("Generated states " + str(states))
#
#    # Test king capture
#    print("Test king capture:")
#    bishop = Bishop(0, 0, figure.bishop, "white")
#    state = {(0, 0): (figure.bishop, bishop._owner),
#             (2, 2): (figure.king, figure.black)}
#    bishop.moveTo(2, 2, state, 8, 8)
#    print("New state " + str(state))
