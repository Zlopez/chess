#!/bin/python3
import logic
import logging
import io
import re
import string
import argparse
import sys

LOG_LEVEL=logging.ERROR
HUMAN_READABLE=False

#Convert figure marks to unicode character sequence
symbols = {
        'bki' : '\u2654',
        'bq'  : '\u2655',
        'br'  : '\u2656',
        'bb'  : '\u2657',
        'bkn' : '\u2658',
        'bp'  : '\u2659',
        'wki' : '\u265a',
        'wq'  : '\u265b',
        'wr'  : '\u265c',
        'wb'  : '\u265d',
        'wkn' : '\u265e',
        'wp'  : '\u265f'}


#Parse arguments
def parseArguments():
    global LOG_LEVEL
    global HUMAN_READABLE

    state = ''
    move = ''
    player = ''

    parser = argparse.ArgumentParser(description='Cheess command line client.')
    parser.add_argument('-s',metavar='state',help='State of game. If no state is provided start state is generated.')
    parser.add_argument('-m',metavar='move', help='Move player want to do. This must be provided in format FROM-TO (A1-B1). Ignored if State is not provided.')
    parser.add_argument('-p',metavar='player', choices=['WHITE','BLACK','W','B'], help='Player on turn. Possible values WHITE|BLACK|W|B. Ignored if State is not provided.')
    parser.add_argument('-H', action='store_true', help="Print output also in human readable format.")
    parser.add_argument('-ll',choices=['NOTSET','DEBUG','INFO','WARNING','ERROR','CRITICAL'],help='Change log level. Default is ERROR.')
    parser.add_argument('-lf',help='Log to file.')
    args = parser.parse_args()
    #Log file
    if args.lf:
        fileh = logging.FileHandler(args.lf, 'w')
        logging.getLogger().addHandler(fileh)
    #Log level
    if args.ll:
        if(args.ll == "NOTSET"):
            LOG_LEVEL = logging.NOTSET
        if(args.ll == "DEBUG"):
            LOG_LEVEL = logging.DEBUG
        if(args.ll == "INFO"):
            LOG_LEVEL = logging.INFO
        if(args.ll == "WARNING"):
            LOG_LEVEL = logging.WARNING
        if(args.ll == "ERROR"):
            LOG_LEVEL = logging.ERROR
        if(args.ll == "CRITICAL"):
            LOG_LEVEL = logging.CRITICAL
        logging.getLogger().setLevel(LOG_LEVEL)
        logging.info("Log level changed to %s", args.ll)
    #Human readable format
    if args.H:
        HUMAN_READABLE=True
        logging.info("Parameter -H detected. Output will be printed in human readable form.")
    #State
    if args.s:
        state = args.s.replace('\'','').replace(' ','')
        if (not re.match("^\[(((w|b)(ki|kn|r|b|q|p))?,){63}(w|b)(ki|kn|r|b|q|p)\]$",state)):
            logging.error("Invalid state format %s", args.s)
            parser.print_help()
            sys.exit(1)
        if args.m:
            move = args.m
            if (not re.match("^[a-hA-H][1-8]-[a-hA-H][1-8]$",move)):
                logging.error("Invalid move format %s", args.m)
                parser.print_help()
                sys.exit(1)
        else:
            logging.error("Move parameter not specified.")
            parser.print_help()
            sys.exit(1)
        if args.p:
            player = args.p
        else:
            logging.error("Player parameter not specified.")
            parser.print_help()
            sys.exit(1)

    return (state,move,player)

def getCoordinates(move):
    """
    Get coordinates from move.
    """
    x_position = ord(move[0].lower())-97
    y_position = int(move[1])-1

    return (x_position,y_position)


def convertPosition(input_text):
    """
    Convert move entered by player to coordinates in range 0-7.
    """
    moves = input_text.strip().lower().split('-')
    move_from = moves[0]
    move_to = moves[1]

    coordinates_from = getCoordinates(move_from)
    coordinates_to = getCoordinates(move_to)
    
    logging.debug("Converted move from %s to %s:%s-%s:%s", input_text, coordinates_from[0], coordinates_from[1], coordinates_to[0], coordinates_to[1])

    return (coordinates_from,coordinates_to)

def printNiceOutput(state):
    """
    Prints state in human readable form.
    """
    for row in range(7,-1,-1):
        print('   +---+---+---+---+---+---+---+---+')
        print(' '+ str(row+1) +' |',end='')
        for i in range(0,8):
            print(' '+symbols.get(state[row*8+i],' '),end=' ')
            print('|',end='')
        print('')
    
    print('   +---+---+---+---+---+---+---+---+')
    print('     A   B   C   D   E   F   G   H  ')


if __name__ == "__main__":
    #Start logging
    logging.basicConfig(format='[%(asctime)s] ' +
            '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            level=LOG_LEVEL)
    input_state,move_input,player = parseArguments()

    # generate starting state
    if not input_state:
        game_logic = logic.ChessLogic('')
        output_state = game_logic.getState()
    # process state
    else:
        #prepare current state
        state = re.sub(r"[\[\]\s]","",input_state).split(',')
        
        game_logic = logic.ChessLogic(state) 
        move = convertPosition(move_input)
        game_logic.setPlayer(player)
        game_logic.moveFigure(move[0],move[1])
        output_state = game_logic.getState()

    
    if HUMAN_READABLE:
        printNiceOutput(output_state)
        print('\nUse this state string for next move:')
    print(output_state)
