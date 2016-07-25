import itertools
import logging

# Figures enum
pawn = "pawn"
knight = "knight"
rook = "rook"
bishop = "bishop"
queen = "queen"
king = "king"
# Players enum
black = "black"
white = "white"

class Figure:
    """
    Parent class for chess figures. Contains all common methods.
    """

    def __init__(self,x,y,figure,owner):
        self._x=x
        self._y=y
        self._figure=figure
        self._owner=owner

    def _changeState(self,x,y,state,figure):
        del state[(self._x,self._y)]
        state[(x,y)] = (figure,self._owner)

    def moveTo(self, x, y, state, max_x, max_y, check=True):
        """
        Move figure to next position. If check is false, then just change figure position (this is for special moves).
        """
        # First test if move is correct
        if (not check) or self._testMove(x, y, state, max_x, max_y):
            self._changeState(x,y,state,self._figure)
            self._x = x
            self._y = y

    def generateMoves(self, state, max_x, max_y):
        """
        Generate moves for figure.
        """
        moves = []
        list_x = range(0,max_x)
        list_y = range(0,max_y)
        logging.info("Generating moves for %s", self._figure)
        for x,y in itertools.product(list_x,list_y):
            if self._testMove(x,y,state,max_x,max_y):
                moves.append((x,y,self._figure))

        return moves

    def _testMove(self, x, y, state, max_x, max_y):
        """
        Test if figure can be moved to specified destination.
        """
        raise NotImplemented;

    def getPosition(self):
        """
        Return current position of figure.
        """

        return (self._x, self._y)

    def getType(self):
        """
        Return type of figure.
        """

        return self._figure

    def getOwner(self):
        """
        Return owner of figure (black, white).
        """

        return self._owner

    def _checkVector(self, state, x, y):
        """
        Test if movement vector is clear.
        """
        
        # Movement is done only in y axis
        if x == self._x:
            for move_y in self._generateRange(self._y,y):
                # Skip current figure
                if (x,move_y) == (self._x,self._y):
                    continue
                if (x,move_y) in state:
                    logging.info("Figure in path on position %s:%s", x, move_y)
                    return False

        # Movement is done only in x axis
        elif y == self._y:
            for move_x in self._generateRange(self._x,x):
                # Skip current figure
                if (move_x,y) == (self._x,self._y):
                    continue
                if (move_x,y) in state:
                    logging.info("Figure in path on position %s:%s", move_x, y)
                    return False

        # Movement is done in both axes
        else:
            list_x = self._generateRange(self._x,x)
            list_y = self._generateRange(self._y,y)
            for (move_x,move_y) in itertools.product(list_x,list_y):
                # Skip current figure
                if (move_x,move_y) == (self._x,self._y):
                    continue
                if (move_x,move_y) in state:
                    logging.info("Figure in path on position %s:%s", 
                            move_x, move_y)
                    return False

        return True

    def _generateRange(self,start,end):
        """
        Generate range from start to end. This method is needed for decreasing 
        ranges.
        """
        result = []
        if start > end:
            result=range(start,end,-1)
        else:
            result=range(start,end,1)

        logging.info("From %s to %s generated range %s",start, end ,str(result))
        return result
