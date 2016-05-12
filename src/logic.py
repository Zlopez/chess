import logging
import figures
from enum import Enum

# Win conditions enum
class Conditions(Enum):
    check = 0
    checkMate = 1
    draw = 2

class ChessLogic:
    """
    Game logic for chess game.
    """

    def __init__(self):
        # init white figures
        self._figures = self._init_figures()
        self._current_state = self._create_state(self._figures)
        self._current_player = figures.white

    def _init_figures(self):
        """
        Generate figures for game.
        """

        figures_arr = []

        # Generate pawns
        for x in range(0,8):
            for y in [1,6]:
                logging.info("Generating pawn on position %s:%s",x,y)
                if y in [6,7]:
                    figures_arr.append(figures.Pawn(x,y,figures.pawn,
                        figures.black))
                else:
                    figures_arr.append(figures.Pawn(x,y,figures.pawn,
                        figures.white))

        # Generate rooks
        for x in [0,7]:
            for y in [0,7]:
                logging.info("Generating rook on position %s:%s",x,y)
                if y in [6,7]:
                    figures_arr.append(figures.Rook(x,y,figures.rook,
                        figures.black))
                else:
                    figures_arr.append(figures.Rook(x,y,figures.rook,
                        figures.white))

        # Generate knights
        for x in [1,6]:
            for y in [0,7]:
                logging.info("Generating knight on position %s:%s",x,y)
                if y in [6,7]:
                    figures_arr.append(figures.Knight(x,y,figures.knight,
                        figures.black))
                else:
                    figures_arr.append(figures.Knight(x,y,figures.knight,
                        figures.white))

        # Generate bishops
        for x in [2,5]:
            for y in [0,7]:
                logging.info("Generating bishop on position %s:%s",x,y)
                if y in [6,7]:
                    figures_arr.append(figures.Bishop(x,y,figures.bishop,
                        figures.black))
                else:
                    figures_arr.append(figures.Bishop(x,y,figures.bishop,
                        figures.white))

        # Generate queens
        for x in [3]:
            for y in [0,7]:
                logging.info("Generating queen on position %s:%s",x,y)
                if y in [6,7]:
                    figures_arr.append(figures.Queen(x,y,figures.queen,
                        figures.black))
                else:
                    figures_arr.append(figures.Queen(x,y,figures.queen,
                        figures.white))

        # Generate kings
        for x in [4]:
            for y in [0,7]:
                logging.info("Generating king on position %s:%s",x,y)
                if y in [6,7]:
                    figures_arr.append(figures.King(x,y,figures.king,
                        figures.black))
                else:
                    figures_arr.append(figures.King(x,y,figures.king,
                        figures.white))

        return figures_arr

    def _create_state(self, figures_arr):
        """
        Create state from array of figures.
        """

        state = {}

        for figure in figures_arr:
            state[figure.getPosition()] = (figure.getType(), figure.getOwner())

        return state

    def getMoves(self,figure):
        """
        Returns all moves for selected figure.
        """

        logging.info("Generating moves for %s on %s:%s", figure.getType(), 
                figure.getPosition()[0], figure.getPosition()[1])
        moves = figure.generateMoves(self._current_state,8,8)
        return moves

    def moveFigure(self,figure,x,y):
        """
        Move with selected figure to specified position.
        """
        figure.moveTo(x,y,self._current_state,8,8)
        # Delete captured figure
        for fig in self._figures:
            if ((x,y) == fig.getPosition() and 
                    fig.getOwner() is not self._current_player):
                self._figures.remove(fig)
                break
        self._switchPlayer()

    def getState(self):
        """
        Get current state of game.
        """
        return self._current_state

    def _switchPlayer(self):
        """
        Switch current player.
        """
        if self._current_player == figures.white:
            self._current_player = figures.black
        else:
            self._current_player = figures.white

    def getFigure(self,x,y):
        """
        Return figure object on specified position.
        """
        for fig in self._figures:
            if (x,y) == fig.getPosition():
                return fig

        return None

    def getCondition(self):
        """
        Check if current player is in check.
        """
        for fig in self._figures:
            if (fig.getType() == figures.king and 
                    fig.getOwner() == self._current_player):
                if fig.isCheck(self._current_state, 8,8):
                    # Check mate
                    if self.getMoves(fig):
                        return Conditions.checkMate
                    else:
                        return Conditions.check


if __name__ == "__main__":
    #Start logging
    logging.basicConfig(format='[%(asctime)s] ' +
            '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            level=logging.DEBUG)

    #Test figures generation
    print("Test figures generation:")
    logic = ChessLogic()
    figs = logic._figures
    print("Figures generated " + str(figs))

    #Test state
    print("Test initial state generation:")
    state = logic.getState()
    print("State generated " + str(state))

    #Test moves generation
    print("Test moves generation:")
    for figure in logic._figures:
        moves = logic.getMoves(figure)
        print("Moves generated " + str(moves))

    #Test turn
    print("Test turn:")
    figure = logic.getFigure(0,1)
    print("Current player: " + logic._current_player)
    logic.moveFigure(figure,0,2)
    state = logic.getState()
    print("Current state: " + str(state))
    print("Current player: " + logic._current_player)
    
    #Test capture
    print("Test capture:")
    figure_arr = []
    figure_arr.append(figures.Pawn(4,4,figures.pawn,figures.black))
    figure_arr.append(figures.Pawn(3,3,figures.pawn,figures.white))
    logic._figures=figure_arr
    logic._current_state=logic._create_state(figure_arr)
    logic._current_player=figures.white
    figure = logic.getFigure(3,3)
    logic.moveFigure(figure,4,4)
    state = logic.getState()
    print("Current state: " + str(state))
    print("Current figures: " + str(logic._figures))

    #Test checkmate
    print("Test checkmate:")
    figure_arr = []
    figure_arr.append(figures.King(0,0,figures.king,figures.black))
    figure_arr.append(figures.Bishop(3,3,figures.bishop,figures.white))
    figure_arr.append(figures.Rook(0,7,figures.rook,figures.white))
    figure_arr.append(figures.Rook(3,3,figures.rook,figures.white))
    logic._figures=figure_arr
    logic._current_state=logic._create_state(figure_arr)
    logic._current_player=figures.black
    figure = logic.getFigure(0,0)
    condition = logic.getCondition()
    print("Current condition: " + str(condition))
