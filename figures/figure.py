"""
Parent class for chess figures.
"""
import itertools
import logging

# Figures enum
PAWN = "pawn"
KNIGHT = "knight"
ROOK = "rook"
BISHOP = "bishop"
QUEEN = "queen"
KING = "king"
# Players enum
BLACK = "black"
WHITE = "white"


class Figure:
    """
    Parent class for chess figures. Contains all common methods.
    """

    def __init__(self, x_index, y_index, figure, owner):
        self._x_index = x_index
        self._y_index = y_index
        self._figure = figure
        self._owner = owner

    def _change_state(self, x_index, y_index, state, figure):
        del state[(self._x_index, self._y_index)]
        state[(x_index, y_index)] = (figure, self._owner)

    def _is_move_inside_board(self, x_index, y_index, max_x, max_y):
        """
        Check if move is inside game board.
        """
        if x_index >= max_x or y_index >= max_y or x_index < 0 or y_index < 0:
            logging.info("Invalid move to %s:%s", x_index, y_index)
            return False

        return True

    def _is_moving(self, x_index, y_index):
        """
        Check if figure is moving.
        """
        if y_index == self._y_index and x_index == self._x_index:
            logging.info("Invalid move to %s:%s", x_index, y_index)
            return False

        return True

    def _is_king_on_position(self, x_index, y_index, state):
        """
        Check if there is king on target position. King can't be attacked directly.
        """
        if ((x_index, y_index) in state and state[(x_index, y_index)][
                0] == KING and state[(x_index, y_index)] is not self._owner):
            logging.info("King on position %s:%s can't be attacked",
                         x_index, y_index)
            return True

        return False

    def _is_figure_on_target_position(self, x_index, y_index, state):
        """
        Check if there is another figure on target position.
        Player can't move figure on position where he already has another figure.
        """
        if (x_index, y_index) in state and state[
                (x_index, y_index)][1] == self._owner:
            logging.info(
                "There is already figure on position %s:%s",
                x_index,
                y_index)
            return True

        return False

    def _is_move_correct(self, x_index, y_index):
        """
        Check if move is legal for figure.
        """
        raise NotImplementedError

    def move_to(self, x_index, y_index, state, max_x, max_y, check=True):
        """
        Move figure to next position.
        If check is false, then just change figure position (this is for special moves).
        """
        # First test if move is correct
        if (not check) or self._test_move(x_index, y_index, state, max_x, max_y):
            self._change_state(x_index, y_index, state, self._figure)
            self._x_index = x_index
            self._y_index = y_index
            return True
        return False

    def generate_moves(self, state, max_x, max_y):
        """
        Generate moves for figure.
        """
        moves = []
        list_x = range(0, max_x)
        list_y = range(0, max_y)
        logging.info("Generating moves for %s", self._figure)
        for x_index, y_index in itertools.product(list_x, list_y):
            if self._test_move(x_index, y_index, state, max_x, max_y):
                moves.append((x_index, y_index, self._figure))

        return moves

    def _test_move(self, x_index, y_index, state, max_x, max_y):
        """
        Test if figure can be moved to specified destination.
        """
        raise NotImplementedError

    def get_position(self):
        """
        Return current position of figure.
        """

        return (self._x_index, self._y_index)

    def get_type(self):
        """
        Return type of figure.
        """

        return self._figure

    def get_owner(self):
        """
        Return owner of figure (black, white).
        """

        return self._owner

    def _check_vector(self, state, x_index, y_index):
        """
        Test if movement vector is clear.
        """

        # Movement is done only in y_index axis
        if x_index == self._x_index:
            for move_y in self._generate_range(self._y_index, y_index):
                # Skip current figure
                if (x_index, move_y) == (self._x_index, self._y_index):
                    continue
                if (x_index, move_y) in state:
                    logging.info("Figure in path on position %s:%s", x_index, move_y)
                    return False

        # Movement is done only in x_index axis
        elif y_index == self._y_index:
            for move_x in self._generate_range(self._x_index, x_index):
                # Skip current figure
                if (move_x, y_index) == (self._x_index, self._y_index):
                    continue
                if (move_x, y_index) in state:
                    logging.info("Figure in path on position %s:%s", move_x, y_index)
                    return False

        # Movement is done in both axes
        else:
            list_x = self._generate_range(self._x_index, x_index)
            list_y = self._generate_range(self._y_index, y_index)
            for (move_x, move_y) in itertools.product(list_x, list_y):
                # Skip current figure
                if (move_x, move_y) == (self._x_index, self._y_index):
                    continue
                if (move_x, move_y) in state:
                    logging.info("Figure in path on position %s:%s",
                                 move_x, move_y)
                    return False

        return True

    def _generate_range(self, start, end):
        """
        Generate range from start to end. This method is needed for decreasing
        ranges.
        """
        result = None
        if start > end:
            result = range(start, end, -1)
        else:
            result = range(start, end, 1)

        logging.info(
            "From %s to %s generated range %s",
            start,
            end,
            str(result))
        return result
