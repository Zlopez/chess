"""
Chess game logic module.
"""
import logging
from enum import Enum
import figures


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
        # init white figures
        self._figures = self._init_figures(state)
        self._current_state = self._create_state()
        self._current_player = figures.figure.WHITE

    def _init_figures(self, state):
        """
        Generate figures array from state.
        """

        # generate new game state
        if not state:
            logging.debug("Generating new game.")
            return self._init_new_game()
        # generate game from existing state
        else:
            figures_arr = []
            for i in range(0, len(state)):
                figure_color = ''
                # If field is empty continue
                if not state[i]:
                    continue
                else:
                    logging.debug("Figure %s found on index %s", state[i], i)
                    # x_index coordination is get as modulo 8 (example: index 13 is
                    # in coordinates y_index = 6 and x_index = 5, 13%8=5)
                    x_index = i % 8
                    # y_index coordination is get as index divided by 8 cast to
                    # integer
                    y_index = int(i / 8)
                    logging.debug(
                        "Coordinates transformed to %s:%s", x_index, y_index)
                # Black
                if state[i].startswith('b'):
                    figure_color = figures.figure.BLACK
                # White
                elif state[i].startswith('w'):
                    figure_color = figures.figure.WHITE
                else:
                    logging.error("Undefined figure color %s", state[i])
                # King found
                if state[i].endswith('ki'):
                    figure_type = figures.figure.KING
                    logging.info(
                        "Generating %s with color %s on %s:%s",
                        figure_type,
                        figure_color,
                        x_index,
                        y_index)
                    figures_arr.append(
                        figures.King(
                            x_index, y_index, figure_type, figure_color))
                # Knight found
                elif state[i].endswith('kn'):
                    figure_type = figures.figure.KNIGHT
                    logging.info(
                        "Generating %s with color %s on %s:%s",
                        figure_type,
                        figure_color,
                        x_index,
                        y_index)
                    figures_arr.append(
                        figures.Knight(
                            x_index, y_index, figure_type, figure_color))
                # Rook found
                elif state[i].endswith('r'):
                    figure_type = figures.figure.ROOK
                    logging.info(
                        "Generating %s with color %s on %s:%s",
                        figure_type,
                        figure_color,
                        x_index,
                        y_index)
                    figures_arr.append(
                        figures.Rook(
                            x_index, y_index, figure_type, figure_color))
                # Bishop found
                elif state[i].endswith('b'):
                    figure_type = figures.figure.BISHOP
                    logging.info(
                        "Generating %s with color %s on %s:%s",
                        figure_type,
                        figure_color,
                        x_index,
                        y_index)
                    figures_arr.append(
                        figures.Bishop(
                            x_index, y_index, figure_type, figure_color))
                # Queen found
                elif state[i].endswith('q'):
                    figure_type = figures.figure.QUEEN
                    logging.info(
                        "Generating %s with color %s on %s:%s",
                        figure_type,
                        figure_color,
                        x_index,
                        y_index)
                    figures_arr.append(
                        figures.Queen(
                            x_index, y_index, figure_type, figure_color))
                # Pawn found
                elif state[i].endswith('p'):
                    figure_type = figures.figure.PAWN
                    logging.info(
                        "Generating %s with color %s on %s:%s",
                        figure_type,
                        figure_color,
                        x_index,
                        y_index)
                    figures_arr.append(
                        figures.Pawn(
                            x_index, y_index, figure_type, figure_color))

            return figures_arr

    def _generate_figures(self, x_range, y_range, figures_arr, figure_type):
        """
        Append figures of one type to array.
        """
        for x_index in x_range:
            for y_index in y_range:
                logging.info(
                    "Generating %s on position %s:%s",
                    figure_type,
                    x_index,
                    y_index)
                if y_index in [6, 7]:
                    color = figures.figure.BLACK
                else:
                    color = figures.figure.WHITE

                # TODO: Use figures.FiguresFactory
                if figure_type == figures.figure.PAWN:
                    figures_arr.append(
                        figures.Pawn(
                            x_index,
                            y_index,
                            figure_type,
                            color))
                if figure_type == figures.figure.ROOK:
                    figures_arr.append(
                        figures.Rook(
                            x_index,
                            y_index,
                            figure_type,
                            color))
                if figure_type == figures.figure.KNIGHT:
                    figures_arr.append(
                        figures.Knight(
                            x_index,
                            y_index,
                            figure_type,
                            color))
                if figure_type == figures.figure.BISHOP:
                    figures_arr.append(
                        figures.Bishop(
                            x_index,
                            y_index,
                            figure_type,
                            color))
                if figure_type == figures.figure.QUEEN:
                    figures_arr.append(
                        figures.Queen(
                            x_index,
                            y_index,
                            figure_type,
                            color))
                if figure_type == figures.figure.KING:
                    figures_arr.append(
                        figures.King(
                            x_index,
                            y_index,
                            figure_type,
                            color))

    def _init_new_game(self):
        """
        Generate figures array for new game.
        """
        figures_arr = []

        # Generate pawns
        self._generate_figures(range(0, 8), [1, 6], figures_arr, figures.figure.PAWN)

        # Generate rooks
        self._generate_figures([0, 7], [0, 7], figures_arr, figures.figure.ROOK)

        # Generate knights
        self._generate_figures([1, 6], [0, 7], figures_arr, figures.figure.KNIGHT)

        # Generate bishops
        self._generate_figures([2, 5], [0, 7], figures_arr, figures.figure.BISHOP)

        # Generate queens
        self._generate_figures([3], [0, 7], figures_arr, figures.figure.QUEEN)

        # Generate kings
        self._generate_figures([4], [0, 7], figures_arr, figures.figure.KING)

        return figures_arr

    def _create_state(self):
        """
        Create state from array of figures.
        """

        state = {}

        for figure in self._figures:
            state[figure.get_position()] = (figure.get_type(), figure.get_owner())

        return state

    def get_moves(self, figure):
        """
        Returns all moves for selected figure.
        """

        logging.info("Generating moves for %s on %s:%s", figure.get_type(),
                     figure.get_position()[0], figure.get_position()[1])
        moves = figure.generate_moves(self._current_state, 8, 8)
        return moves

    def move_figure(self, start, target):
        """
        Move with figure from start to target position.
        """
        figure = self.get_figure(start[0], start[1])
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

        if figure.move_to(target[0], target[1], self._current_state, 8, 8):
            # Delete captured figure
            for fig in self._figures:
                if ((target[0], target[1]) == fig.get_position() and
                        fig.get_owner() is not self._current_player):
                    self._figures.remove(fig)
                    break

            # Castling
            if figure.get_type() == figures.king and figure.isCastling():
                pos = figure.get_position()
                # Check if king moved left or right
                if pos[0] > 4:
                    rook = self.get_figure(7, pos[1])
                    rook.move_to(
                        target[0] - 1,
                        pos[1],
                        self._current_state,
                        8,
                        8,
                        False)
                    logging.info(
                        "Move rook figure on %s:%s after castling", 7, pos[1])
                else:
                    rook = self.get_figure(0, pos[1])
                    rook.move_to(
                        target[0] + 1,
                        pos[1],
                        self._current_state,
                        8,
                        8,
                        False)
                    logging.info(
                        "Move rook figure on %s:%s after castling", 0, pos[1])

            # En passant
            if figure.get_type() == figures.pawn and figure.isEnPassant():
                pos = figure.get_position()
                if figure.get_owner() == figures.figure.BLACK:
                    pawn = self.get_figure(pos[0], pos[1] + 1)
                    self._figures.remove(pawn)
                    logging.info(
                        "Removed figure on %s:%s after en passant",
                        pos[0],
                        pos[1] + 1)
                if figure.get_owner() == figures.figure.WHITE:
                    pawn = self.get_figure(pos[0], pos[1] - 1)
                    self._figures.remove(pawn)
                    logging.info(
                        "Removed figure on %s:%s after en passant",
                        pos[0],
                        pos[1] - 1)

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
                fig = self.get_figure(x_index, y_index)
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

    def get_figure(self, x_index, y_index):
        """
        Return figure object on specified position.
        """
        for fig in self._figures:
            if (x_index, y_index) == fig.get_position():
                return fig

        return None

    def get_condition(self):
        """
        Check if current player is in check.
        """
        for fig in self._figures:
            if (fig.get_type() == figures.king and
                    fig.get_owner() == self._current_player):
                if fig.isCheck(self._current_state, 8, 8):
                    # Check mate
                    if self.get_moves(fig):
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
