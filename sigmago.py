from model import SimpleCNN
from policy import *
import warnings
import argparse
import sys
import gym
from gym.envs.registration import register
import torch
from model import SimpleCNN
import warnings

parser = argparse.ArgumentParser()

warnings.filterwarnings("ignore")

parser.add_argument('-m', type=str, default='sigmago_v1.pt', help='Path to save the trained models')
args_main = parser.parse_args()

warnings.filterwarnings("ignore")
register(id='go_v0',  entry_point='gym_go.envs:GoEnv')

# 加載您的模型
from os.path import abspath, dirname
script_path = dirname(abspath(__file__))
model = SimpleCNN(num_classes=81)
model = torch.load(f'{script_path}/models/{args_main.m}', map_location=torch.device('cpu'))
model.eval()

global go_env
go_env = gym.make('go_v0', size=9, komi=0, reward_method='real')
state = go_env.reset()



def op_move(coord): #opponent move
    if coord == 'pass':
        player_step = 81
    else:
        player_step = go_coord_to_xy(coord) # 將圍棋座標轉成X, Y型式，從零開始
    state, reward, done, info = go_env.step(player_step)
    return 1


def get_next_step(player_move,color):

    if player_move == 'pass':
        result = 81
        state, reward, done, info = go_env.step(81)
        return 'pass'

    state = go_env.state()
    board = state[0]*-1 + state[1]
    #print(board)
    #print(player_move)
    if color == 'B':
        board *= -1
    board_d = board[None,...][None, ...]
    board_d = torch.from_numpy(board_d).to('cpu').float()
    logits = model(board_d)
    result0 = logits.cpu().detach().numpy()
    result = get_idx(result0, state[3].flatten())

    if result == 81:
        return 'pass'

    next_step_x = result // 9
    next_step_y = result % 9
    x = (next_step_x, next_step_y)
    state, reward, done, info = go_env.step(x)
    go_step = xy_to_go_coord(next_step_x, next_step_y)

    return go_step

def cmd_reset(komi):
    global go_env
    go_env = gym.make('go_v0', size=9, komi=komi, reward_method='real')
    go_env.reset()
    return 1

class SimpleGTP:

    def __init__(self):
        self.board_size = 9  # Default board size
        self.game_over = False
        self.player_move = ''
        self.model_path = args_main.m
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
        return f'= Sigma Go {args_main.m}\n\n'

    def get_version(self, args):
        return '= 0.0.1\n\n'
        #return f'{self.model_path}\n\n'

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
        print(self.player_move)
        return '=\n\n'

    def generate_move(self, args):
        if len(args) != 1 or args[0] not in ['B', 'W']:
            return '? unknown player\n\n'
        # Generate a move for the given color
        # Placeholder implementation
        next_step = get_next_step(self.player_move,args[0])
        #now = self.player_move
        #print(self.player_move)
        return f'= {next_step}\n\n'  # Example move

    def quit(self, args):
        self.game_over = True
        exit()
        return '=\n\n'

if __name__ == '__main__':
    gtp = SimpleGTP()
    gtp.start()
