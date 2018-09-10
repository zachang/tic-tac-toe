from flask import Flask, request, abort
import re

app = Flask(__name__)

'''
board: lowercase string of spaces, x's and o's of length nine.
player: represented by 'x' or 'o'
spaces: represent available fields to play in.
'''

def valid_board(data):
    return len(data) == 9 and re.match(r'^[o x]+?', data) and\
     (data.count('x') - data.count('o') in [0, 1])


def next_player(player):
    return {'o': 'x', 'x': 'o'}[player]


def won(data, player):
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


def draw(data):
    return bool(re.search(r'\s', data))


def play(data, index, player):
    """ Returns a new board, when player makes a move. """
    list_data = list(data)
    list_data[index] = player
    return "".join(list_data)


def board_outcomes(data, player):
    """ Returns all possible move from the board"""
    return [play(data, i, player) for i, char in enumerate(data) if char == " "]


def result(data, player):
    """ Returns -1, 1, 0 if player will lose, win or draw repectively"""
    opponent = next_player(player)

    if won(data, player):
        return 1
    if won(data, opponent):
        return -1 
    if draw(data):
        return 0

    return max(-1 * result(board_outcome, opponent) for board_outcome in board_outcomes(data, player))


@app.route('/')
def start():
    request_data = request.args.get('board')

    if not request_data or not valid_board(request_data) or not draw(request_data) or\
     won(request_data, 'x') or won(request_data, 'o'):
        abort(400, description='invalid request')

    outcomes = board_outcomes(request_data, 'o')
    if len(outcomes) == 1:
        return outcomes[0]
    return max(outcomes, key=lambda outcome: -1 * result(outcome, 'x'))


if __name__ == '__main__':
    app.run(debug=True)