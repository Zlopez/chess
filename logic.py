"""
Chess game logic module.
"""
import logging
from enum import Enum
from chess import figures
from chess.board import Board


class Conditions(Enum):
    """
    Enum for game conditions.
    """
    check = 0
    checkMate = 1
    draw = 2
    play = 3


class ChessLogic:
    """
    Game logic for chess game.
    """

    def __init__(self, state):
        self._board = Board(state)
        self._current_player = figures.figure.WHITE

    def get_moves(self, figure):
        """
        Returns all moves for selected figure.
        """

        logging.info("Generating moves for %s on %s:%s", figure.get_type(),
                     figure.get_position()[0], figure.get_position()[1])
        moves = figure.generate_moves(8, 8)
        return moves

    def move_figure(self, start, target):
        """
        Move with figure from start to target position.
        """
        figure = self._board.get_figure(start[0], start[1])
        # Check if figure is on the start position
        if figure is None:
            logging.error(
                "No figure on specified position %s:%s",
                start[0],
                start[1])
            return
        # Check if figure is owned by current player
        if figure.get_owner() != self._current_player:
            logging.error("Can't move with oponent figure")
            return

        if figure.move_to(target[0], target[1], 8, 8):
            # Castling
            if figure.get_type() == figures.figure.KING and figure.isCastling():
                pos = figure.get_position()
                # Check if king moved left or right
                if pos[0] > 4:
                    rook = self._board.get_figure(7, pos[1])
                    rook.move_to(
                        target[0] - 1,
                        pos[1],
                        8,
                        8,
                        False)
                    logging.info(
                        "Move rook figure on %s:%s after castling", 7, pos[1])
                else:
                    rook = self._board.get_figure(0, pos[1])
                    rook.move_to(
                        target[0] + 1,
                        pos[1],
                        8,
                        8,
                        False)
                    logging.info(
                        "Move rook figure on %s:%s after castling", 0, pos[1])

    def get_state(self):
        """
        Get current state of game.
        """
        state = []
        # Loop through whole game board
        # If figure is found in position, then print figure
        # else print empty space
        logging.info("Return chess game board state.")
        for y_index in range(0, 8):
            for x_index in range(0, 8):
                fig = self._board.get_figure(x_index, y_index)
                if fig:
                    logging.debug(
                        "Figure found on %s:%s with color %s",
                        x_index,
                        y_index,
                        fig.get_owner())
                    state.append(self._get_figure_mark(fig))
                else:
                    state.append('')

        return state

    def _get_figure_mark(self, figure):
        """
        Return mark that will be print in application output.
        """
        mark = ''
        if figure.get_owner() == figures.figure.BLACK:
            mark += 'b'
        else:
            mark += 'w'

        fig_type = figure.get_type()

        if fig_type == figures.figure.PAWN:
            mark += 'p'
        elif fig_type == figures.figure.KNIGHT:
            mark += 'kn'
        elif fig_type == figures.figure.ROOK:
            mark += 'r'
        elif fig_type == figures.figure.BISHOP:
            mark += 'b'
        elif fig_type == figures.figure.QUEEN:
            mark += 'q'
        elif fig_type == figures.figure.KING:
            mark += 'ki'

        return mark

    def get_condition(self):
        """
        Check if current player is in check.
        """
        king = self._board.get_king(self._current_player)
        if king:
            if king.isCheck(8, 8):
                # Check mate
                if self.get_moves(king):
                    return Conditions.check
                else:
                    return Conditions.checkMate
        return Conditions.play

    def set_player(self, player):
        """
        Return current player.
        """
        if player.lower() == 'black' or player.lower() == 'b':
            self._current_player = figures.figure.BLACK
        elif player.lower == 'white' or player.lower() == 'w':
            self._current_player = figures.figure.WHITE
        logging.debug("Player %s is on move", self._current_player)

# Test section
# if __name__ == "__main__":
#    # Start logging
#    logging.basicConfig(
#        format='[%(asctime)s] ' +
#        '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#        level=logging.DEBUG)
#
#    # Test figures generation
#    print("Test figures generation:")
#    logic = ChessLogic()
#    figs = logic._figures
#    print("Figures generated " + str(figs))
#
#    # Test state
#    print("Test initial state generation:")
#    state = logic.get_state()
#    print("State generated " + str(state))
#
#    # Test moves generation
#    print("Test moves generation:")
#    for figure in logic._figures:
#        moves = logic.get_moves(figure)
#        print("Moves generated " + str(moves))
#
#    # Test turn
#    print("Test turn:")
#    figure = logic.get_figure(0, 1)
#    print("Current player: " + logic._current_player)
#    logic.move_figure(figure, 0, 2)
#    state = logic.get_state()
#    print("Current state: " + str(state))
#    print("Current player: " + logic._current_player)
#
#    # Test capture
#    print("Test capture:")
#    figure_arr = []
#    figure_arr.append(figures.Pawn(4, 4, figures.pawn, figures.black))
#    figure_arr.append(figures.Pawn(3, 3, figures.pawn, figures.white))
#    logic._figures = figure_arr
#    logic._current_state = logic._create_state(figure_arr)
#    logic._current_player = figures.white
#    figure = logic.get_figure(3, 3)
#    logic.move_figure(figure, 4, 4)
#    state = logic.get_state()
#    print("Current state: " + str(state))
#    print("Current figures: " + str(logic._figures))
#
#    # Test checkmate
#    print("Test checkmate:")
#    figure_arr = []
#    figure_arr.append(figures.King(0, 0, figures.king, figures.black))
#    figure_arr.append(figures.Bishop(3, 3, figures.bishop, figures.white))
#    figure_arr.append(figures.Rook(0, 7, figures.rook, figures.white))
#    figure_arr.append(figures.Rook(3, 3, figures.rook, figures.white))
#    logic._figures = figure_arr
#    logic._current_state = logic._create_state(figure_arr)
#    logic._current_player = figures.black
#    figure = logic.get_figure(0, 0)
#    condition = logic.get_condition()
#    print("Current condition: " + str(condition))
