"""
Representation of field on board. It contains information about color and figure.
"""


class Field:
    """
    Class representing field on board.
    """

    def __init__(self, color, figure=None):
        self._color = color
        self._figure = figure

    def get_figure(self):
        """
        Return figure on current field.
        Return None if no figure is on field.
        """
        return self._figure

    def set_figure(self, figure):
        """
        Add figure to current field.
        """
        self._figure = figure

    def remove_figure(self):
        """
        Remove figure from field.
        If no figure is on field nothing happens.
        """
        self._figure = None

    def get_color(self):
        """
        Return color of current field.
        """
        return self._color
