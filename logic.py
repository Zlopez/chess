import logging
import figures
from enum import Enum

# Win conditions enum
class Conditions(Enum):
    check = 0
    checkMate = 1
    draw = 2
    play = 3

class ChessLogic:
    """
    Game logic for chess game.
    """

    def __init__(self, state):
        # init white figures
        self._figures = self._init_figures(state)
        self._current_state = self._create_state(self._figures)

    def _init_figures(self, state):
        """
        Generate figures array from state.
        """

        # generate new game state
        if not state:
            logging.debug("Generating new game.")
            return self._init_new_game()
        # generate game from existing state
        else:
            figures_arr = []
            for i in range(0,len(state)):
                figure_color = ''
                # If field is empty continue
                if not state[i]:
                    continue
                else:
                    logging.debug("Figure %s found on index %s",state[i],i)
                    # x coordination is get as modulo 8 (example: index 13 is in coordinates y = 6 and x = 5, 13%8=5) 
                    x = i%8
                    # y coordination is get as index divided by 8 cast to integer
                    y = int(i/8)
                    logging.debug("Coordinates transformed to %s:%s",x,y)
                # Black
                if state[i].startswith('b'):
                    figure_color = figures.black    
                # White
                elif state[i].startswith('w'):
                    figure_color = figures.white
                else:
                    logging.error("Undefined figure color %s",state[i])
                # King found
                if state[i].endswith('ki'):
                    logging.info("Generating %s with color %s on %s:%s", figures.king, figure_color, x, y)
                    figures_arr.append(figures.King(x,y,figures.king,figure_color))
                # Knight found
                elif state[i].endswith('kn'):
                    logging.info("Generating %s with color %s on %s:%s", figures.knight, figure_color, x, y)
                    figures_arr.append(figures.Knight(x,y,figures.knight,figure_color))
                # Rook found
                elif state[i].endswith('r'):
                    logging.info("Generating %s with color %s on %s:%s", figures.rook, figure_color, x, y)
                    figures_arr.append(figures.Rook(x,y,figures.rook,figure_color))
                # Bishop found
                elif state[i].endswith('b'):
                    logging.info("Generating %s with color %s on %s:%s", figures.bishop, figure_color, x, y)
                    figures_arr.append(figures.Bishop(x,y,figures.bishop,figure_color))
                # Queen found
                elif state[i].endswith('q'):
                    logging.info("Generating %s with color %s on %s:%s", figures.queen, figure_color, x, y)
                    figures_arr.append(figures.Queen(x,y,figures.queen,figure_color))
                # Pawn found
                elif state[i].endswith('p'):
                    logging.info("Generating %s with color %s on %s:%s", figures.pawn, figure_color, x, y)
                    figures_arr.append(figures.Pawn(x,y,figures.pawn,figure_color))

            return figures_arr

                
                


    def _init_new_game(self):
        """
        Generate figures array for new game.
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

    def moveFigure(self,start,target):
        """
        Move with figure from start to target position.
        """
        figure = self.getFigure(start[0],start[1])
        # Check if figure is on the start position
        if figure == None:
            logging.error("No figure on specified position %s:%s", start[0], start[1])
            return
        # Check if figure is owned by current player
        if figure.getOwner() != self._current_player:
            logging.error("Can't move with oponent figure")
            return

        figure.moveTo(target[0],target[1],self._current_state,8,8)
        # Delete captured figure
        for fig in self._figures:
            if ((target[0],target[1]) == fig.getPosition() and 
                    fig.getOwner() is not self._current_player):
                self._figures.remove(fig)
                break

        # Castling
        if figure.getType() == figures.king and figure.isCastling():
            pos = figure.getPosition()
            # Check if king moved left or right
            if pos[0] > 4:
                rook = self.getFigure(7,pos[1])
                rook.moveTo(target[0]-1, pos[1], self._current_state, 8, 8, False) 
                logging.info("Move rook figure on %s:%s after castling", 7, pos[1])
            else:
                rook = self.getFigure(0,pos[1])
                rook.moveTo(target[0]+1, pos[1], self._current_state, 8, 8, False) 
                logging.info("Move rook figure on %s:%s after castling", 0, pos[1])


    def getState(self):
        """
        Get current state of game.
        """
        state = []
        # Loop through whole game board
        # If figure is found in position, then print figure
        # else print empty space
        logging.info("Return chess game board state.")
        for y in range(0,8):
            for x in range(0,8):
                fig = self.getFigure(x,y)
                if fig:
                    logging.debug("Figure found on %s:%s with color %s", x, y, fig.getOwner())
                    state.append(self._getFigureMark(fig))
                else:
                    state.append('')

        return state
                
    def _getFigureMark(self,figure):
        """
        Return mark that will be print in application output.
        """
        mark = ''
        if figure.getOwner() == figures.black:
            mark += 'b'
        else:
            mark += 'w'
        
        figType = figure.getType()

        if figType == figures.pawn:
            mark += 'p'
        elif figType == figures.knight:
            mark += 'kn'
        elif figType == figures.rook:
            mark += 'r'
        elif figType == figures.bishop:
            mark += 'b'
        elif figType == figures.queen:
            mark += 'q'
        elif figType == figures.king:
            mark += 'ki'

        return mark

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
                        return Conditions.check
                    else:
                        return Conditions.checkMate
        return Conditions.play

    def setPlayer(self,player):
        """
        Return current player.
        """
        if player.lower() == 'black' or player.lower() == 'b':
            self._current_player = figures.black
        elif player.lower == 'white' or player.lower() == 'w':
            self._current_player = figures.white
        logging.debug("Player %s is on move",self._current_player)

# Test section
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
