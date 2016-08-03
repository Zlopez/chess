"""
Implementation of Pawn figure in chess command line client.
"""
import logging
from figures import figure


class Pawn(figure.Figure):
    """
    Pawn figure for chess implementation.
    """

    def __init__(self, x_index, y_index, fig, owner):
        super().__init__(x_index, y_index, fig, owner)
        self._promotion = False
        self._passant = False
        self._passant_danger = False

    def _check_direction(self, x_index, y_index):
        """
        Check if figure is moving in correct direction.
        """
        if y_index < self._y_index and self._owner == figure.WHITE:
            logging.info("Invalid move to %s:%s", x_index, y_index)
            return False
        if y_index > self._y_index and self._owner == figure.BLACK:
            logging.info("Invalid move to %s:%s", x_index, y_index)
            return False

        return True

    def _check_attack(self, x_index, y_index, state):
        """
        Check if attack can be done.
        """

        y_diff = y_index - self._y_index
        # Attack
        if ((x_index == self._x_index + 1 and y_diff in [-1, 1]) or
                (x_index == self._x_index - 1 and y_diff in [-1, 1])):
            if ((x_index, y_index) in state and state[
                    (x_index, y_index)][1] != self._owner):
                logging.info("Attacking %s on position %s:%s",
                             state[(x_index, y_index)],
                             x_index,
                             y_index)
                return True
            # En passant
            if ((x_index, self._y_index) in state and
                    state[(x_index, self._y_index)][1] != self._owner and
                    state[(x_index, self._y_index)][0] == figure.PAWN):
                logging.info("En passant on position %s:%s",
                             x_index,
                             y_index)
                self._passant = True
                return True

        return False

    def _is_first_move(self, x_index, y_index, state):
        """
        Check if this move is first move.
        In first move Pawn can be moved differently.
        """
        # First move can be two squares forward
        if x_index == self._x_index and (
                y_index == self._y_index + 2 or y_index == self._y_index - 2):
            if y_index > self._y_index:
                check_range = range(self._y_index + 1, y_index + 1)
            else:
                check_range = range(y_index, self._y_index)

            for i in check_range:
                if (x_index, i) in state:
                    logging.info(
                        "Move can't be done, figure on path %s:%s", x_index, i)
                    return False

            # Check if en passant can be done in next move
            if ((x_index + 1, y_index) in state
                    and state[x_index + 1, y_index][0] == figure.PAWN and
                    state[x_index + 1, y_index][1] != self._owner):
                self._passant_danger = True
            if ((x_index - 1, y_index) in state
                    and state[x_index - 1, y_index][0] == figure.PAWN and
                    state[x_index - 1, y_index][1] != self._owner):
                self._passant_danger = True

            return True

        return False

    def _is_move_correct(self, x_index, y_index):
        return (x_index == self._x_index and
                (y_index == self._y_index + 1 or y_index == self._y_index - 1))

    def _test_move(self, x_index, y_index, state, max_x, max_y):
        result = None

        # First test if move is correct or
        if (self._is_move_correct(x_index, y_index) or
                # Check if attack is correct or
                self._check_attack(x_index, y_index, state) or
                # Check if it is first move
                self._is_first_move(x_index, y_index, state)):

            # Check if figure is moving
            if not self._is_moving(x_index, y_index):
                result = False

            # Check if figure is moving in correct direction
            if not self._check_direction(x_index, y_index):
                result = False

            # Check if the move is inside board
            if not self._is_move_inside_board(
                    x_index, y_index, max_x, max_y):
                result = False

            # Check if king is in target position
            if self._is_king_on_position(x_index, y_index, state):
                result = False

            # Check if another figure is on target destination
            if self._is_figure_on_target_position(x_index, y_index, state):
                result = False

            if result is None:
                # Check transformation
                if (y_index == max_y - 1 or y_index ==
                        0) and ((x_index, y_index) not in state):
                    logging.info("Pawn got promotion")
                    self._promotion = True
                    result = True
                else:
                    logging.info(
                        "Pawn moved from %s:%s to %s:%s",
                        self._x_index,
                        self._y_index,
                        x_index,
                        y_index)
                    result = True

        else:
            # Move is illegal
            logging.info("Invalid move for pawn from %s:%s to %s:%s", self._x_index,
                         self._y_index, x_index, y_index)
            result = False

        return result

    def is_en_passant(self):
        """
        Returns true, whether en passant was done in last move.
        """
        return self._passant

    def is_en_passant_danger(self):
        """
        Returns true, whether en passant is possible in next move.
        """
        return self._passant_danger

    def is_promoted(self):
        """
        Returns true, if promotion is possible.
        """
        return self._promotion

# if __name__ == "__main__":
#    # Start logging
#    logging.basicConfig(
#        format='[%(asctime)s] ' +
#        '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#        level=logging.DEBUG)
#
#    # Test invalid move
#    pawn = Pawn(0, 0, figure.pawn, "black")
#    state = {(0, 0): (figure.pawn, pawn._owner)}
#    pawn.moveTo(-1, -1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test correct move
#    pawn = Pawn(0, 2, figure.pawn, "black")
#    state = {(0, 2): (figure.pawn, pawn._owner)}
#    pawn.moveTo(0, 1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test attack
#    pawn = Pawn(0, 0, figure.pawn, "white")
#    state = {(0, 0): (figure.pawn, pawn._owner),
#             (1, 1): (figure.pawn, "black")}
#    pawn.moveTo(1, 1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test transformation
#    pawn = Pawn(0, 1, figure.pawn, "black")
#    state = {(0, 1): (figure.pawn, pawn._owner)}
#    pawn.moveTo(0, 0, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test move on target destination
#    pawn = Pawn(0, 0, figure.pawn, "white")
#    state = {(0, 0): (figure.pawn, pawn._owner),
#             (1, 1): (figure.pawn, "white")}
#    pawn.moveTo(1, 1, state, 8, 8)
#    print("New state " + str(state))
#
#    # Test generation
#    pawn = Pawn(0, 0, figure.pawn, "white")
#    state = {(0, 0): (figure.pawn, pawn._owner)}
#    states = pawn.generateMoves(state, 8, 8)
#    print("Generated states " + str(states))
#
#    # Test king capture
#    pawn = Pawn(0, 0, figure.pawn, "white")
#    state = {(0, 0): (figure.pawn, pawn._owner),
#             (1, 1): (figure.king, "black")}
#    pawn.moveTo(1, 1, state, 8, 8)
#    print("New state " + str(state))
