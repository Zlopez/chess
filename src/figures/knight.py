import figure
import logging
import itertools

class Knight(figure.Figure):
    """
    Knight figure for chess implementation.
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
            # x +/- 2 and y +/- 3
        if (((x == self._x + 2 or x == self._x - 2) and 
            (y == self._y + 3 or y == self._y - 3)) or
            # x +/- 3 and y +/- 2
            ((x == self._x - 3 or x == self._x + 3) and
            (y == self._y + 2 or y == self._y - 2))):    
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
                    logging.info("Knight moved from %s:%s to %s:%s", 
                            self._x,self._y,x,y)
                    return True

        # Move is illegal
        logging.info("Invalid move for knight from %s:%s to %s:%s", self._x,
                self._y,x,y)
        return False



if __name__ == "__main__":
    #Start logging
    logging.basicConfig(format='[%(asctime)s] ' +
            '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            level=logging.DEBUG)

    #Test invalid move
    print("Test invalid move:")
    knight = Knight(0,0, figure.knight, "black")
    state = {(0,0) : (figure.knight,knight._owner) }
    knight.moveTo(-2,-3, state, 8, 8)
    print("New state " + str(state))

    #Test correct move
    print("Test correct move:")
    knight = Knight(0,0, figure.knight, "black")
    state = {(0,0) : (figure.knight, knight._owner) }
    knight.moveTo(2,3, state, 8, 8)
    print("New state " + str(state))

    #Test attack
    print("Test attack move:")
    knight = Knight(0,0, figure.knight, "white")
    state = { (0,0) : (figure.knight, knight._owner),
            (2,3) : (figure.knight,"black") }
    knight.moveTo(2,3, state, 8, 8)
    print("New state " + str(state))

    #Test move on target destination
    print("Test move on target destination:")
    knight = Knight(0,0, figure.knight, "white")
    state = { (0,0) : (figure.knight, knight._owner),
            (2,3) : (figure.knight,"white") }
    knight.moveTo(2,3, state, 8, 8)
    print("New state " + str(state))

    #Test generation
    print("Test moves generation:")
    knight = Knight(4,4, figure.knight, "white")
    state = { (4,4) : (figure.knight, knight._owner)}
    states = knight.generateMoves(state, 8, 8)
    print("Generated states " + str(states))

    #Test king capture
    print("Test king capture:")
    knight = Knight(0,0, figure.knight, "white")
    state = { (0,0) : (figure.knight, knight._owner),
            (2,3) : (figure.king,"black") }
    knight.moveTo(2,3, state, 8, 8)
    print("New state " + str(state))
