"""
Implementation of Knight figure in chess command line client.
"""
import logging
from . import figure
from ..board import board


class Knight(figure.Figure):
    """
    Knight figure for chess implementation.
    """

    def _is_move_correct(self, x_index, y_index):
            # x_index +/- 2 and y_index +/- 3
        return ((x_index - self._x_index in [-1, 1] and y_index - self._y_index in [-2, 2]) or
                # x_index +/- 3 and y_index +/- 2
                (x_index - self._x_index in [-2, 2] and y_index - self._y_index in [-1, 1]))

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

            if result is None:
                # Attack
                target_figure = self._board.get_figure(x_index, y_index)
                if target_figure and target_figure.get_owner() != self._owner:
                    logging.info("Attacking %s on position %s:%s",
                                 target_figure.get_type(), x_index, y_index)
                    result = True
                # Move is legal
                else:
                    logging.info(
                        "Knight moved from %s:%s to %s:%s",
                        self._x_index,
                        self._y_index,
                        x_index,
                        y_index)
                    result = True
        else:
            # Move is illegal
            logging.info(
                "Invalid move for knight from %s:%s to %s:%s",
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
#    knight = Knight(0, 0, figure.knight, "black")
#    state = {(0, 0): (figure.knight, knight._owner)}
#    knight.moveTo(-2, -3, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test correct move
#    print("Test correct move:")
#    knight = Knight(0, 0, figure.knight, "black")
#    state = {(0, 0): (figure.knight, knight._owner)}
#    knight.moveTo(2, 3, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test attack
#    print("Test attack move:")
#    knight = Knight(0, 0, figure.knight, "white")
#    state = {(0, 0): (figure.knight, knight._owner),
#             (2, 3): (figure.knight, "black")}
#    knight.moveTo(2, 3, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test move on target destination
#    print("Test move on target destination:")
#    knight = Knight(0, 0, figure.knight, "white")
#    state = {(0, 0): (figure.knight, knight._owner),
#             (2, 3): (figure.knight, "white")}
#    knight.moveTo(2, 3, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test generation
#    print("Test moves generation:")
#    knight = Knight(4, 4, figure.knight, "white")
#    state = {(4, 4): (figure.knight, knight._owner)}
#    states = knight.generateMoves(state, 8, 8)
#    print("Generated states " + str(states))
#
#    # Test king capture
#    print("Test king capture:")
#    knight = Knight(0, 0, figure.knight, "white")
#    state = {(0, 0): (figure.knight, knight._owner),
#             (2, 3): (figure.king, "black")}
#    knight.moveTo(2, 3, state, 8, 8)
#    print("New state " + str(state))
