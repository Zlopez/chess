"""
Board module for chess game. It contains information about every field on game board.
Every figure is asking this module for information about other figures.
"""
import logging
import itertools
from .. import figures
from .field import Field


class Board:
    """
    Class representing the board.
    """

    def __init__(self, state):
        self._fields = self._init_fields(state)
        self._size = [8, 8]

    def _init_fields(self, state):
        """
        Initialize all fields on chessboard from state.
        If no state is provided, then default board is generated.
        """

        # generate new game state
        if not state:
            logging.debug("Generating new game.")
            return self._init_new_game()
        else:
            # generate game from existing state
            fields = []
            row = []
            field_color = figures.figure.BLACK
            for y_index in range(0, 8):
                for x_index in range(0, 8):
                    figure_color = ''
                    # to get coordination from 1D array we need to convert 2D to 1D
                    # index in state is get as y_index*8+x_index
                    index = y_index * 8 + x_index
                    field_state = state[index]
                    # If field is empty continue
                    if not field_state:
                        row.append(Field(field_color))
                    else:
                        logging.debug(
                            "Figure %s found on index %s", state[index], index)
                        # Black
                        if state[index].startswith('b'):
                            figure_color = figures.figure.BLACK
                        # White
                        elif state[index].startswith('w'):
                            figure_color = figures.figure.WHITE
                        else:
                            logging.error(
                                "Undefined figure color %s", state[index])
                        # King found
                        if state[index].endswith('ki'):
                            figure_type = figures.figure.KING
                        # Knight found
                        elif state[index].endswith('kn'):
                            figure_type = figures.figure.KNIGHT
                        # Rook found
                        elif state[index].endswith('r'):
                            figure_type = figures.figure.ROOK
                        # Bishop found
                        elif state[index].endswith('b'):
                            figure_type = figures.figure.BISHOP
                        # Queen found
                        elif state[index].endswith('q'):
                            figure_type = figures.figure.QUEEN
                        # Pawn found
                        elif state[index].endswith('p'):
                            figure_type = figures.figure.PAWN

                        logging.info(
                            "Generating %s with color %s on %s:%s",
                            figure_type,
                            figure_color,
                            x_index,
                            y_index)

                        # generate figure
                        figure = self._generate_figure(
                            figure_type, figure_color, x_index, y_index)
                        row.append(Field(field_color, figure))

                    field_color = self._switch_color(field_color)

                # save current row
                fields.append(row)
                row = []

        return fields

    def _switch_color(self, color):
        """
        Switch current color to opposite color.
        """
        if color == figures.figure.BLACK:
            return figures.figure.WHITE
        else:
            return figures.figure.BLACK

    def _generate_figure(self, figure_type, color, x_index, y_index):
        """
        Generate figures by type and color.
        """

        if figure_type == figures.figure.PAWN:
            figure = figures.Pawn(
                x_index,
                y_index,
                figure_type,
                color,
                self)
        if figure_type == figures.figure.ROOK:
            figure = figures.Rook(
                x_index,
                y_index,
                figure_type,
                color,
                self)
        if figure_type == figures.figure.KNIGHT:
            figure = figures.Knight(
                x_index,
                y_index,
                figure_type,
                color,
                self)
        if figure_type == figures.figure.BISHOP:
            figure = figures.Bishop(
                x_index,
                y_index,
                figure_type,
                color,
                self)
        if figure_type == figures.figure.QUEEN:
            figure = figures.Queen(
                x_index,
                y_index,
                figure_type,
                color,
                self)
        if figure_type == figures.figure.KING:
            figure = figures.King(
                x_index,
                y_index,
                figure_type,
                color,
                self)

        return figure

    def _init_new_game(self):
        """
        Generate figures array for new game.
        """
        fields = []
        row = []
        field_color = figures.figure.BLACK
        for y_index in range(0, 8):
            for x_index in range(0, 8):
                figure_type = None
                # resolve figure color
                if y_index in [0, 1]:
                    figure_color = figures.figure.WHITE
                else:
                    figure_color = figures.figure.BLACK

                # resolve type of figure
                if y_index in [1, 6]:
                    figure_type = figures.figure.PAWN
                if y_index in [0, 7] and x_index in [0, 7]:
                    figure_type = figures.figure.ROOK
                if y_index in [0, 7] and x_index in [1, 6]:
                    figure_type = figures.figure.KNIGHT
                if y_index in [0, 7] and x_index in [2, 5]:
                    figure_type = figures.figure.BISHOP
                if y_index in [0, 7] and x_index in [3]:
                    figure_type = figures.figure.QUEEN
                if y_index in [0, 7] and x_index in [4]:
                    figure_type = figures.figure.KING

                logging.info(
                    "Generating %s with color %s on %s:%s",
                    figure_type,
                    figure_color,
                    x_index,
                    y_index)

                # generate figure
                if figure_type:
                    figure = self._generate_figure(
                        figure_type, figure_color, x_index, y_index)
                    row.append(Field(field_color, figure))
                else:
                    row.append(Field(field_color))

                field_color = self._switch_color(field_color)

            # save current row
            fields.append(row)
            row = []

        return fields

    def get_figure(self, x_index, y_index):
        """
        Return figure object on specified position.
        Returns None if no object is on specified positon.
        """
        return self._fields[y_index][x_index].get_figure()

    def get_king(self, figure_color):
        """
        Return king of specified color.
        This method can be used for checking a wining conditions.
        """

        for (position_x, position_y) in itertools.product(range(8), repeat=2):
            fig = self.get_figure(position_x, position_y)
            if (fig and fig.get_type() == figures.figure.KING and
                    fig.get_owner == figure_color):
                return fig

        return None

    def remove_figure(self, x_index, y_index):
        """
        Remove figure object on specified position.
        """
        self._fields[y_index][x_index].remove_figure()

    def move_figure(self, move_from, move_to):
        """
        Move figure from one field to other.
        """
        from_field = self._fields[move_from[1]][move_from[0]]
        to_field = self._fields[move_to[1]][move_to[0]]

        figure = from_field.get_figure()
        to_field.set_figure(figure)
        from_field.remove_figure()

    def get_size(self):
        """
        Return size of the board (x,y).
        """
        return self._size

    def _test_position(self, x_index, y_index):
        """
        Test if the figure on position is threaten by other figure.
        """
        test_figure = self.get_figure(x_index, y_index)

        for (position_x, position_y) in itertools.product(range(8), repeat=2):
            fig = self.get_figure(position_x, position_y)
            if fig:
                owner = fig.get_owner()
                logging.info(
                    "Testing figure on position %s:%s with color %s",
                    position_x,
                    position_y,
                    owner)
                # Don't test owner figures
                if owner != test_figure.get_owner():
                    # Oponent figure can be moved to destination
                    logging.info("Testing if %s can be moved to %s:%s",
                                 fig.get_type(), x_index, y_index)
                    if fig._test_move(x_index, y_index):
                        return False

        # Position is not threating figure
        return True
