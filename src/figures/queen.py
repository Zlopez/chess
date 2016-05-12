import figure
import logging
import itertools
import math

class Queen(figure.Figure):
    """
    Queen figure for chess implementation.
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
            # Move in x or y axis
        if (((x < self._x or x > self._x) and y == self._y or
            (y < self._y or y > self._y) and x == self._x) or
            # Move diagonally
            (math.fabs(x - self._x) == math.fabs(y - self._y))):
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
                    logging.info("Queen moved from %s:%s to %s:%s", 
                            self._x,self._y,x,y)
                    return True

        # Move is illegal
        logging.info("Invalid move for queen from %s:%s to %s:%s", self._x,
                self._y,x,y)
        return False



if __name__ == "__main__":
    #Start logging
    logging.basicConfig(format='[%(asctime)s] ' +
            '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            level=logging.DEBUG)

    #Test invalid move
    print("Test invalid move:")
    queen = Queen(0,0, figure.queen, "black")
    state = {(0,0) : (figure.queen,queen._owner) }
    queen.moveTo(-2,-32, state, 8, 8)
    print("New state " + str(state))

    #Test correct move in axis
    print("Test correct move in axis:")
    queen = Queen(0,0, figure.queen, "black")
    state = {(0,0) : (figure.queen, queen._owner) }
    queen.moveTo(2,0, state, 8, 8)
    print("New state " + str(state))

    #Test correct move diagonally
    print("Test correct move in axis:")
    queen = Queen(0,0, figure.queen, "black")
    state = {(0,0) : (figure.queen, queen._owner) }
    queen.moveTo(2,2, state, 8, 8)
    print("New state " + str(state))

    #Test attack
    print("Test attack move:")
    queen = Queen(0,0, figure.queen, "white")
    state = { (0,0) : (figure.queen, queen._owner),
            (2,2) : (figure.queen,"black") }
    queen.moveTo(2,2, state, 8, 8)
    print("New state " + str(state))

    #Test move on target destination
    print("Test move on target destination:")
    queen = Queen(0,0, figure.queen, "white")
    state = { (0,0) : (figure.queen, queen._owner),
            (2,2) : (figure.queen,"white") }
    queen.moveTo(2,2, state, 8, 8)
    print("New state " + str(state))

    #Test generation
    print("Test moves generation:")
    queen = Queen(4,4, figure.queen, "white")
    state = { (4,4) : (figure.queen, queen._owner)}
    states = queen.generateMoves(state, 8, 8)
    print("Generated states " + str(states))

    #Test king capture
    print("Test king capture:")
    queen = Queen(4,4, figure.queen, "white")
    state = { (4,4) : (figure.queen, queen._owner),
            (6,6) : (figure.king, figure.black)}
    queen.moveTo(6,6,state,8,8)
    print("New state " + str(state))
