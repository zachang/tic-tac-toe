from flask import Flask, request, abort
import re

app = Flask(__name__)

'''
board: lowercase string of spaces, x's and o's of length nine.
player: represented by 'x' or 'o'
spaces: represent available fields to play in.
'''

def valid_board(data):
    '''Checks if board supplied is valid'''
    return len(data) == 9 and re.match(r'^[o x]+?', data) and\
     (data.count('x') - data.count('o') in [0, 1])


def next_player(player):
    '''Returns the next player'''
    return {'o': 'x', 'x': 'o'}[player]


def won(data, player):
    '''Checks if game has been won already when a player tries to play'''
    list_to_compare = [player, player, player]

    possible_wins = [
        [data[0], data[1], data[2]] == list_to_compare,
        [data[3], data[4], data[5]] == list_to_compare,
        [data[6], data[7], data[8]] == list_to_compare,
        [data[0], data[3], data[6]] == list_to_compare,
        [data[1], data[4], data[7]] == list_to_compare,
        [data[2], data[5], data[8]] == list_to_compare,
        [data[0], data[4], data[8]] == list_to_compare,
        [data[2], data[4], data[6]] == list_to_compare
    ]

    return any(possible_wins)


def intended_win(data):
    '''Checks for possible winning moves'''
    x_combination1 = ['x', 'x', 'o'];
    x_combination2 = ['x', 'o', 'x'];
    x_combination3 = ['o', 'x', 'x'];

    intended_wins = [
        [data[0], data[1], data[2]],
        [data[3], data[4], data[5]],
        [data[6], data[7], data[8]],
        [data[0], data[3], data[6]],
        [data[1], data[4], data[7]],
        [data[2], data[5], data[8]],
        [data[0], data[4], data[8]],
        [data[2], data[4], data[6]]
    ]
    
    where_to = False
    for val in intended_wins:
        if val in [x_combination1, x_combination2, x_combination3]:
            where_to = True
            break
    return where_to


def draw(data):
    return bool(re.search(r'\s', data))


def play(data, index, player):
    '''Returns a new board, when player makes a move.'''
    list_data = list(data)
    list_data[index] = player
    return "".join(list_data)


def board_outcomes(data, player):
    '''Returns all possible move from the board'''
    return [play(data, i, player) for i, char in enumerate(data) if char == ' ']


def result(data, opponent):
    '''Returns -1, 1, 0 if player will lose, win or draw repectively'''
    player = next_player(opponent)

    if won(data, opponent):
        return 0
    if won(data, player):
        return 3 
    if not intended_win(data):
        return 1
    else:
        return 2


@app.route('/')
def start():
    '''Begins game'''
    request_data = request.args.get('board')

    if not request_data or not valid_board(request_data) or not draw(request_data) or\
     won(request_data, 'x') or won(request_data, 'o'):
        abort(400, description='invalid request')

    outcomes = board_outcomes(request_data, 'o')
    return max(outcomes, key=lambda outcome: 1 * result(outcome, 'x'))


if __name__ == '__main__':
    app.run()