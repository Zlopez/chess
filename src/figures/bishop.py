import figure
import logging
import itertools
import math

class Bishop(figure.Figure):
    """
    Bishop figure for chess implementation.
    """

    def _testMove(self, x, y, state, max_x, max_y):
        # Return false if not move will be done
        if y == self._y and x == self._x:
            logging.info("Invalid move to %s:%s", x, y)
            return False
        # Check if the move is inside board
        if x >= max_x or y>= max_y or x < 0 or y < 0:
            logging.info("Invalid move to %s:%s", x, y)
            return False
        # Check if move is correct
            # Only diagonal move is permitted
        if (math.fabs(x - self._x) == math.fabs(y - self._y)):
            # check if path is free
            if(not self._checkVector(state,x,y)):
                return False
            # Check if king is in target position
            if ((x,y) in state and state[(x,y)][0] == figure.king and 
                    state[(x,y)] is not self._owner):
                logging.info("King on position %s:%s can't be attacked", 
                        x,y)
                return False
            # Attack
            if (x,y) in state and state[(x,y)][1] != self._owner:
                logging.info("Attacking %s on position %s:%s", 
                        state[(x,y)],x,y)
                return True
            # Check if another figure is on target destination
            if (x,y) in state and state[(x,y)][1] == self._owner:
                logging.info("There is already figure on position %s:%s",
                        x, y)
                return False
            # Move is legal
            else:
                logging.info("Bishop moved from %s:%s to %s:%s", 
                        self._x,self._y,x,y)
                return True

        # Move is illegal
        logging.info("Invalid move for bishop from %s:%s to %s:%s", self._x,
                self._y,x,y)
        return False



if __name__ == "__main__":
    #Start logging
    logging.basicConfig(format='[%(asctime)s] ' +
            '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            level=logging.DEBUG)

    #Test invalid move
    print("Test invalid move:")
    bishop = Bishop(0,0, figure.bishop, "black")
    state = {(0,0) : (figure.bishop,bishop._owner) }
    bishop.moveTo(-2,-2, state, 8, 8)
    print("New state " + str(state))

    #Test correct move
    print("Test correct move:")
    bishop = Bishop(0,0, figure.bishop, "black")
    state = {(0,0) : (figure.bishop, bishop._owner) }
    bishop.moveTo(2,2, state, 8, 8)
    print("New state " + str(state))

    #Test attack
    print("Test attack move:")
    bishop = Bishop(0,0, figure.bishop, "white")
    state = { (0,0) : (figure.bishop, bishop._owner),
            (2,2) : (figure.bishop,"black") }
    bishop.moveTo(2,2, state, 8, 8)
    print("New state " + str(state))

    #Test move on target destination
    print("Test move on target destination:")
    bishop = Bishop(0,0, figure.bishop, "white")
    state = { (0,0) : (figure.bishop, bishop._owner),
            (2,2) : (figure.bishop,"white") }
    bishop.moveTo(2,2, state, 8, 8)
    print("New state " + str(state))

    #Test generation
    print("Test moves generation:")
    bishop = Bishop(4,4, figure.bishop, "white")
    state = { (4,4) : (figure.bishop, bishop._owner)}
    states = bishop.generateMoves(state, 8, 8)
    print("Generated states " + str(states))

    #Test king capture
    print("Test king capture:")
    bishop = Bishop(0,0, figure.bishop, "white")
    state = { (0,0) : (figure.bishop, bishop._owner),
            (2,2) : (figure.king,figure.black) }
    bishop.moveTo(2,2, state, 8, 8)
    print("New state " + str(state))
