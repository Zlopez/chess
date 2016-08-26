"""
Implementation of Rook figure in chess command line client.
"""
import logging
from . import figure
from ..board import Board


class Rook(figure.Figure):
    """
    Rook figure for chess implementation.
    """

    def _is_move_correct(self, x_index, y_index):
                #  Move only in x_index axis
        return (((x_index > self._x_index or x_index < self._x_index) and
                 y_index == self._y_index) or
                # Move only in y_index axis
                (x_index == self._x_index and (y_index > self._y_index or y_index < self._y_index)))

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
                target_figure = self._board.get_figure(x_index, y_index)
                # Attack
                if target_figure and target_figure.get_owner() != self._owner:
                    logging.info("Attacking %s on position %s:%s",
                                 target_figure.get_type(), x_index, y_index)
                    result = True
                # Move is legal
                else:
                    logging.info(
                        "Rook moved from %s:%s to %s:%s",
                        self._x_index,
                        self._y_index,
                        x_index,
                        y_index)
                    result = True
        else:
            # Move is illegal
            logging.info(
                "Invalid move for rook from %s:%s to %s:%s",
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
#    rook = Rook(0, 0, figure.rook, "black")
#    state = {(0, 0): (figure.rook, rook._owner)}
#    rook.moveTo(-2, 0, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test correct move
#    print("Test correct move:")
#    rook = Rook(0, 0, figure.rook, "black")
#    state = {(0, 0): (figure.rook, rook._owner)}
#    rook.moveTo(2, 0, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test attack
#    print("Test attack move:")
#    rook = Rook(0, 0, figure.rook, "white")
#    state = {(0, 0): (figure.rook, rook._owner),
#             (2, 0): (figure.rook, "black")}
#    rook.moveTo(2, 0, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test move on target destination
#    print("Test move on target destination:")
#    rook = Rook(0, 0, figure.rook, "white")
#    state = {(0, 0): (figure.rook, rook._owner),
#             (2, 0): (figure.rook, "white")}
#    rook.moveTo(2, 0, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test generation
#    print("Test moves generation:")
#    rook = Rook(4, 4, figure.rook, "white")
#    state = {(4, 4): (figure.rook, rook._owner)}
#    states = rook.generateMoves(state, 8, 8)
#    print("Generated states " + str(states))
#
#    # Test king capture
#    print("Test king capture:")
#    rook = Rook(0, 0, figure.rook, "white")
#    state = {(0, 0): (figure.rook, rook._owner),
#             (2, 0): (figure.king, "black")}
#    rook.moveTo(2, 0, state, 8, 8)
#    print("New state " + str(state))
