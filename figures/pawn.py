from figures import figure
import logging
import itertools

class Pawn(figure.Figure):
    """
    Pawn figure for chess implementation.
    """

    def __init__(self, x, y, figure, owner):
        super().__init__(x, y, figure, owner)
        self._promotion = False
        self._passant = False
        self._passant_danger = False

    def _testMove(self, x, y, state, max_x, max_y):
        # Return false if not move will be done
        if y == self._y and x == self._x:
            logging.info("Invalid move to %s:%s", x, y)
            return False
        # Check if peon is moving to right direction
        if y < self._y and self._owner==figure.white:
            logging.info("Invalid move to %s:%s", x, y)
            return False
        if y > self._y and self._owner==figure.black:
            logging.info("Invalid move to %s:%s", x, y)
            return False
        # Check if the move is inside board
        if x >= max_x or y>= max_y or x < 0 or y < 0:
            logging.info("Invalid move to %s:%s", x, y)
            return False
        # Check if king is in target position
        if ((x,y) in state and state[(x,y)][0] == figure.king and 
                state[(x,y)] is not self._owner):
            logging.info("King on position %s:%s can't be attacked", 
                    x,y)
            return False
        # Attack
        if ((x==self._x + 1 and (y==self._y + 1 or y==self._y - 1)) or
                (x==self._x - 1 and (y==self._y + 1 or y==self._y - 1))):
            if (x,y) in state and state[(x,y)][1] != self._owner:
                logging.info("Attacking %s on position %s:%s", state[(x,y)],x,y)
                return True
            # En passant
            if ((x,self._y) in state and state[(x,self._y)][1] != self._owner and
                    state[(x,self._y)][0] == figure.pawn):
                logging.info("En passant on position %s:%s", x, y)
                self._passant = True
                return True
        # Can't move in x axis except attack
        if x!=self._x:
            logging.info("Invalid move to %s:%s", x, y)
            return False
        # Check if another figure is on target destination
        if (x,y) in state and state[(x,y)][1] == self._owner:
            logging.info("There is already figure on position %s:%s", x, y)
            return False
        # First move can be two squares forward
        if x==self._x and (y==self._y+2 or y==self._y-2):
            if y > self._y:
                check_range = range(self._y+1,y+1)
            else:
                check_range = range(y,self._y)

            for i in check_range:
                if (x,i) in state:
                    logging.info("Move can't be done, figure on path %s:%s", x, i)
                    return False
            
            # Check if en passant can be done in next move
            if ((x+1,y) in state and state[x+1,y][0] == figure.pawn and
                    state[x+1,y][1] != self._owner):
                self._passant_danger = True
            if ((x-1,y) in state and state[x-1,y][0] == figure.pawn and 
                    state[x-1,y][1] != self._owner):
                self._passant_danger = True
            
            return True

        # Check if move is legal
        if (x==self._x and (y==self._y+1 or y==self._y-1) and ((x,y) not in state)):
            # Check transformation
            if (y==max_y - 1 or y==0) and ((x,y) not in state):
                logging.info("Pawn got promotion")
                self._promotion = True
                return True
            else:
                logging.info("Pawn moved from %s:%s to %s:%s", self._x,self._y,x,y)
                return True

        # Move is illegal
        logging.info("Invalid move for pawn from %s:%s to %s:%s", self._x,
                self._y,x,y)
        return False


    def isEnPassant(self):
        """
        Returns true, whether en passant was done in last move.
        """
        return self._passant

    def isEnPassantDanger(self):
        """
        Returns true, whether en passant is possible in next move.
        """
        return self._passant_danger

    def isPromoted(self):
        """
        Returns true, if promotion is possible.
        """
        return self._promotion

if __name__ == "__main__":
    #Start logging
    logging.basicConfig(format='[%(asctime)s] ' +
            '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            level=logging.DEBUG)

    #Test invalid move
    pawn = Pawn(0,0, figure.pawn, "black")
    state = {(0,0) : (figure.pawn,pawn._owner) }
    pawn.moveTo(-1,-1, state, 8, 8)
    print("New state " + str(state))

    #Test correct move
    pawn = Pawn(0,2, figure.pawn, "black")
    state = {(0,2) : (figure.pawn, pawn._owner) }
    pawn.moveTo(0,1, state, 8, 8)
    print("New state " + str(state))

    #Test attack
    pawn = Pawn(0,0, figure.pawn, "white")
    state = { (0,0) : (figure.pawn, pawn._owner),
            (1,1) : (figure.pawn,"black") }
    pawn.moveTo(1,1, state, 8, 8)
    print("New state " + str(state))

    #Test transformation
    pawn = Pawn(0,1, figure.pawn, "black")
    state = {(0,1) : (figure.pawn,pawn._owner) }
    pawn.moveTo(0,0, state , 8, 8)
    print("New state " + str(state))

    #Test move on target destination
    pawn = Pawn(0,0, figure.pawn, "white")
    state = { (0,0) : (figure.pawn, pawn._owner),
            (1,1) : (figure.pawn,"white") }
    pawn.moveTo(1,1, state, 8, 8)
    print("New state " + str(state))

    #Test generation
    pawn = Pawn(0,0, figure.pawn, "white")
    state = { (0,0) : (figure.pawn, pawn._owner)}
    states = pawn.generateMoves(state, 8, 8)
    print("Generated states " + str(states))

    #Test king capture
    pawn = Pawn(0,0, figure.pawn, "white")
    state = { (0,0) : (figure.pawn, pawn._owner),
            (1,1) : (figure.king,"black") }
    pawn.moveTo(1,1, state, 8, 8)
    print("New state " + str(state))
