from model import SimpleCNN
from policy import *
import warnings
import argparse

parser = argparse.ArgumentParser()

warnings.filterwarnings("ignore")

parser.add_argument('-m', type=str, default='sigmago.pt', help='Path to save the trained models')
args = parser.parse_args()

class SimpleGTP:

    def __init__(self):
        self.board_size = 9  # Default board size
        self.game_over = False
        self.player_move = ''
        self.model_path = args.m
        self.commands = {
            'name': self.get_name,
            'version': self.get_version,
            'protocol_version': self.get_protocol_version,
            'list_commands': self.list_commands,
            'boardsize': self.set_board_size,
            'komi':self.set_komi,
            'clear_board': self.clear_board,
            'play': self.play_move,
            'genmove': self.generate_move,
            'quit': self.quit
            # Add other command handlers here
        }

    def start(self):
        while not self.game_over:
            line = input().strip()
            response = self.handle_command(line)
            print(response, end='')

    def handle_command(self, command):
        tokens = command.split()
        if not tokens:
            return '?\n\n'

        cmd = tokens[0]
        if cmd in self.commands:
            return self.commands[cmd](tokens[1:])
        else:
            return '? unknown command\n\n'

    def get_name(self, args):
        return '= Sigma Go\n\n'

    def get_version(self, args):
        #return '= 0.0.1\n\n'
        return f'{self.model_path}\n\n'

    def get_protocol_version(self, args):
        return '= 2\n\n'

    def list_commands(self, args):
        commands_list = '\n'.join(self.commands.keys())
        return f'= {commands_list}\n\n'

    def set_board_size(self, args):
        if len(args) != 1 or not args[0].isdigit():
            return '? syntax error\n\n'
        size = int(args[0])
        if size < 1 or size > 19:
            return '? unacceptable size\n\n'
        self.board_size = size
        return '=\n\n'
    def set_komi(self, args):
        if len(args) != 1:
            return '? syntax error\n\n'
        try:
            self.komi = float(args[0])
            return '=\n\n'
        except ValueError:
            return '? invalid komi value\n\n'

        return '=\n\n'

    def clear_board(self, args):
        # Reset the board state
        cmd_reset(komi=self.komi)
        self.player_move = ''
        return '=\n\n'

    def play_move(self, args):
        if len(args) != 2:
            return '? syntax error\n\n'
        color, move = args
        # Process the move for the given color
        self.player_move = move
        op_move(move)
        return '=\n\n'

    def generate_move(self, args):
        if len(args) != 1 or args[0] not in ['B', 'W']:
            return '? unknown player\n\n'
        # Generate a move for the given color
        # Placeholder implementation
        next_step = get_next_step(self.player_move,args[0])
        #now = self.player_move
        #print(self.player_move)
        return f'= {next_step}\n\n  '  # Example move

    def quit(self, args):
        self.game_over = True
        exit()
        return '=\n\n'

if __name__ == '__main__':
    gtp = SimpleGTP()
    gtp.start()
