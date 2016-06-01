#!/bin/python3
import logic
import logging
import io
import re
import string

LOG_FOLDER='/var/tmp/'

def askForInput(game_logic):
    print("\n")
    while(True):
        line = input("Choose figure:")
        position = convertPosition(line)
        if(position != None):
            figure = game_logic.getFigure(position[0],position[1])
            if(figure == None):
                print("No " + game_logic.getPlayer() + " figure at specified position!")
                continue
            moves = game_logic.getMoves(figure)
            if(not moves):
                print("No moves for figure!")
                continue
            print(moves)
            line = input("Choose move:")
            move = convertPosition(line)
            if(move == None or not checkMove(move,moves)):
                print("Move is invalid!")
                continue
            return (figure,move)

def convertPosition(input_text):
    """
    Convert position entered by player to coordinates in range 0-7.
    """
    position_regex = re.compile(r"([A-H]|[1-8])[1-8]",re.IGNORECASE)

    if(position_regex.match(input_text)):
        x_position = input_text[0]
        y_position = int(input_text[1])-1
        if(not (x_position.isdigit())):
            x_position = ord(x_position.lower())-96
        else:
            x_position = int(x_position)-1

        return (x_position,y_position)

    return None

def checkMove(move, moves):
    """
    Check if move exist in moves.
    """
    for m in moves:
        if(move == (m[0],m[1])):
            return True
    return False

if __name__ == "__main__":
    #Start logging
    logging.basicConfig(format='[%(asctime)s] ' +
            '{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            level=logging.DEBUG)
    game_logic = logic.ChessLogic()

    #game loop
    condition = logic.Conditions.play
    while(condition == logic.Conditions.play):
        print(game_logic.getState())
        print("Now playing player " + game_logic.getPlayer())
        figure,move = askForInput(game_logic)
        game_logic.moveFigure(figure,move[0],move[1])
        condition = game_logic.getCondition()

