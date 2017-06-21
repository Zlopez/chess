"""
Factory for generating chess figures.
"""

from ..figures import *

class FigureFactory:
    """
    Factory for generating chess figures.
    """

    def generate_figure(fig_type, position, color, board):
        """
        Static method for generating figures.
        Params:
            fig_type - type of figure (see figures/figure.py)
            position - touple representing position on the board
            color - color of the figure (see figures/figure.py)
        Returns:
            Figure object of parent type Figure (see figures/figure.py)
        """

        if fig_type == figure.PAWN:
            return Pawn(position[0], position[1], figure.PAWN, color, board)
