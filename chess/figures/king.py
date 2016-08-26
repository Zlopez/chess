"""
Implementation of King figure in chess command line client.
"""
import logging
from . import figure
from ..board import board


class King(figure.Figure):
    """
    King figure for chess implementation.
    """

    def __init__(self, x_index, y_index, fig, owner, board):
        super().__init__(x_index, y_index, fig, owner, board)
        self._castling = False

    def _check_castling(self, x_index, y_index):
        """
        Check if castling can be done.
        """
        if (x_index == self._x_index + 2 or x_index ==
                self._x_index - 2) and y_index == self._y_index:
            if self.is_check():
                logging.info("Castling can't be done, king is in check")
                return False
            if x_index < self._x_index:
                check_range = range(x_index, self._x_index)
                # Check if ROOK is still on starting position
                target_figure = self._board.get_figure(0, y_index)
                if target_figure:
                    owner = target_figure.get_owner()
                    if not (target_figure.get_type() ==
                            figure.ROOK and owner == self._owner):
                        logging.info(
                            "Castling can't be done, figure on position %s:%s is not ROOK", 
                            0, 
                            y_index)
                        return False
                else:
                    logging.info(
                        "Castling can't be done, ROOK is not in starting position %s:%s", 
                        0, 
                        y_index)
                    return False
            else:
                check_range = range(self._x_index + 1, x_index + 1)
                # Check if ROOK is still on starting position
                target_figure = self._board.get_figure(7, y_index)
                if target_figure:
                    owner = target_figure.get_owner()
                    if not (target_figure.get_type() ==
                            figure.ROOK and owner == self._owner):
                        logging.info(
                            "Castling can't be done, figure on position %s:%s is not ROOK",
                            7,
                            y_index)
                        return False
                else:
                    logging.info(
                        "Castling can't be done, ROOK is not in starting position %s:%s",
                        7,
                        y_index)
                    return False

            for i in check_range:
                target_figure = self._board.get_figure(i, y_index)
                if target_figure:
                    logging.info(
                        "Castling can't be done, there is figure on position %s:%s", i, y_index)
                    return False

            self._castling = True

    def _is_move_correct(self, x_index, y_index):
        x_range = [self._x_index - 1, self._x_index + 1]
        y_range = [self._y_index - 1, self._y_index + 1]
        castling_range = [self._x_index - 2, self._x_index + 2]
        # x_index +/- 1 and y_index +/- 1
        return ((x_index in x_range and y_index in y_range) or
                # x_index +/- 1
                (x_index in x_range and y_index == self._y_index) or
                # y_index +/- 1
                (y_index in y_range and x_index == self._x_index) or
                # castling
                (x_index in castling_range and y_index == self._y_index))

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

            # Check if path is clear for castling
            if not self._check_castling(x_index, y_index):
                result = False

            # Check if king is in target position
            if self._is_king_on_position(x_index, y_index):
                result = False

            # Check if another figure is on target destination
            if self._is_figure_on_target_position(x_index, y_index):
                result = False

            # Check if no oponnent figure can be moved to king destination
            if not self._test_position(x_index, y_index):
                logging.info("Oponent figure can move to %s:%s",
                             x_index, y_index)
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
                        "King moved from %s:%s to %s:%s",
                        self._x_index,
                        self._y_index,
                        x_index,
                        y_index)
                    result = True
        else:
            # Move is illegal
            logging.info(
                "Invalid move for king from %s:%s to %s:%s",
                self._x_index,
                self._y_index,
                x_index,
                y_index)
            result = False

        return result

    def is_check(self):
        """
        Check if king is in check.
        """
        return not self._board.test_position(self._x_index, self._y_index)

    def is_castling(self):
        """
        Check if castling move was done.
        """
        return self._castling

# if __name__ == "__main__":
#    # Start logging
#    logging.basicConfig(
#        format='[%(asctime)s] ' +
#        '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#        level=logging.DEBUG)
#
#    # Test invalid move
#    print("Test invalid move:")
#    king = King(0, 0, figure.king, "black")
#    state = {(0, 0): (figure.king, king._owner)}
#    king.moveTo(-1, -1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test correct move
#    print("Test correct move:")
#    king = King(0, 0, figure.king, "black")
#    state = {(0, 0): (figure.king, king._owner)}
#    king.moveTo(1, 1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test attack
#    print("Test attack move:")
#    king = King(0, 0, figure.king, "white")
#    state = {(0, 0): (figure.king, king._owner),
#             (1, 1): (figure.pawn, "black")}
#    king.moveTo(1, 1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test move on target destination
#    print("Test move on target destination:")
#    king = King(0, 0, figure.king, "white")
#    state = {(0, 0): (figure.king, king._owner),
#             (1, 1): (figure.king, "white")}
#    king.moveTo(1, 1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test move on position, that is blocked by enemy move
#    print("Test move on position, that is blocked by enemy move:")
#    king = King(0, 0, figure.king, "white")
#    state = {(0, 0): (figure.king, king._owner),
#             (2, 2): (figure.bishop, "black")}
#    king.moveTo(1, 1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test generation
#    print("Test moves generation:")
#    king = King(4, 4, figure.king, "white")
#    state = {(4, 4): (figure.king, king._owner)}
#    states = king.generateMoves(state, 8, 8)
#    print("Generated moves " + str(states))
#
#    # Test king capture
#    print("Test attack move:")
#    king = King(0, 0, figure.king, "white")
#    state = {(0, 0): (figure.king, king._owner),
#             (1, 1): (figure.king, "black")}
#    king.moveTo(1, 1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test check
#    print("Test check:")
#    king = King(0, 0, figure.king, "white")
#    state = {(0, 0): (figure.king, king._owner),
#             (2, 2): (figure.bishop, "black")}
#    print("Check " + str(king.is_check(state, 8, 8)))
