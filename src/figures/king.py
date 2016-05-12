import figure
import logging
import pawn
import rook
import bishop
import queen
import knight

class King(figure.Figure):
    """
    King figure for chess implementation.
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
            # x +/- 1 and y +/- 1
        if (((x == self._x + 1 or x == self._x - 1) and 
            (y == self._y + 1 or y == self._y - 1)) or
            # x +/- 1
            ((x == self._x - 1 or x == self._x + 1) and y == self._y) or
            # y +/- 1
            ((y == self._y - 1 or y == self._y + 1) and x == self._x)):
                # Check if king is in target position
                if ((x,y) in state and state[(x,y)][0] == figure.king and 
                        state[(x,y)] is not self._owner):
                    logging.info("King on position %s:%s can't be attacked", 
                            x,y)
                    return False
                # Check if another figure is on target destination
                if (x,y) in state and state[(x,y)][1] == self._owner:
                    logging.info("There is already figure on position %s:%s",
                            x, y)
                    return False
                # Check if no oponnent figure can be moved to king destination
                if not self._testPosition(x,y,state,max_x,max_y):
                    logging.info("Oponent figure can move to %s:%s",
                            x, y)
                    return False
                # Attack
                if (x,y) in state and state[(x,y)][1] != self._owner:
                    logging.info("Attacking %s on position %s:%s", 
                            state[(x,y)],x,y)
                    return True
                # Move is legal
                else:
                    logging.info("King moved from %s:%s to %s:%s", 
                            self._x,self._y,x,y)
                    return True

        # Move is illegal
        logging.info("Invalid move for king from %s:%s to %s:%s", self._x,
                self._y,x,y)
        return False

    def _testPosition(self,x,y,state,max_x,max_y):
        """
        Test if the king can be moved to specified position. Check if no
        oponnent figure can be moved to specified posisiton.
        """

        for position in state.keys():
            logging.info("Testing figure on position %s:%s", position[0], 
                    position[1])
            (fig,owner) = state[position]
            # Don't test king's owner figures
            if owner != self._owner:
                test_figure = None
                if fig == figure.pawn:
                    test_figure = pawn.Pawn(position[0],position[1],fig,owner)
                elif fig == figure.knight:
                    test_figure = knight.Knight(position[0],position[1],fig,
                            owner)
                elif fig == figure.rook:
                    test_figure = rook.Rook(position[0],position[1],fig,
                            owner)
                elif fig == figure.bishop:
                    test_figure = bishop.Bishop(position[0],position[1],fig,
                            owner)
                elif fig == figure.queen:
                    test_figure = queen.Queen(position[0],position[1],fig,
                            owner)
                elif fig == figure.king:
                    test_figure = King(position[0],position[1],fig,owner)
                else:
                    raise ValueError(fig + " is not a valid value.")

                # Oponent figure can be moved to destination
                logging.info("Testing if %s can be moved to %s:%s", 
                        test_figure._figure, x, y)
                if test_figure._testMove(x,y,state,max_x,max_y):
                    return False

        # Move is valid
        return True

    def isCheck(self,state,max_x,max_y):
        """
        Check if king is in check.
        """
        return self._testPosition(self._x,self._y,state,max_x,max_y)


if __name__ == "__main__":
    #Start logging
    logging.basicConfig(format='[%(asctime)s] ' +
            '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            level=logging.DEBUG)

    #Test invalid move
    print("Test invalid move:")
    king = King(0,0, figure.king, "black")
    state = {(0,0) : (figure.king,king._owner) }
    king.moveTo(-1,-1, state, 8, 8)
    print("New state " + str(state))

    #Test correct move
    print("Test correct move:")
    king = King(0,0, figure.king, "black")
    state = {(0,0) : (figure.king, king._owner) }
    king.moveTo(1,1, state, 8, 8)
    print("New state " + str(state))

    #Test attack
    print("Test attack move:")
    king = King(0,0, figure.king, "white")
    state = { (0,0) : (figure.king, king._owner),
            (1,1) : (figure.pawn,"black") }
    king.moveTo(1,1, state, 8, 8)
    print("New state " + str(state))

    #Test move on target destination
    print("Test move on target destination:")
    king = King(0,0, figure.king, "white")
    state = { (0,0) : (figure.king, king._owner),
            (1,1) : (figure.king,"white") }
    king.moveTo(1,1, state, 8, 8)
    print("New state " + str(state))

    #Test move on position, that is blocked by enemy move
    print("Test move on position, that is blocked by enemy move:")
    king = King(0,0, figure.king, "white")
    state = { (0,0) : (figure.king, king._owner),
            (2,2) : (figure.bishop,"black") }
    king.moveTo(1,1, state, 8, 8)
    print("New state " + str(state))

    #Test generation
    print("Test moves generation:")
    king = King(4,4, figure.king, "white")
    state = { (4,4) : (figure.king, king._owner)}
    states = king.generateMoves(state, 8, 8)
    print("Generated moves " + str(states))

    #Test king capture
    print("Test attack move:")
    king = King(0,0, figure.king, "white")
    state = { (0,0) : (figure.king, king._owner),
            (1,1) : (figure.king,"black") }
    king.moveTo(1,1, state, 8, 8)
    print("New state " + str(state))
    
    #Test check
    print("Test check:")
    king = King(0,0, figure.king, "white")
    state = { (0,0) : (figure.king, king._owner),
            (2,2) : (figure.bishop,"black") }
    print("Check " + str(king.isCheck(state,8,8)))
